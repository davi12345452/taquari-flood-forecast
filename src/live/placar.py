"""Placar das emissões reais: previsto × observado, contra persistência.

Reúne tudo o que foi gravado em ``data/processed/live_runs/emissao_*`` (produto
operacional e cenários de chuva) e confere contra a cota da ANA no interim.
Nada é recalculado: só entram números gravados antes da observação. Replays
não contam.

Cada par recebe:
- ``evento``: rodadas separadas por mais de 48h formam eventos distintos;
- ``fase``: subida, pico (±3h do máximo observado do evento) ou recessão,
  definida pela validade em relação ao pico do alvo no evento;
- persistência: a cota observada na referência, repetida até a validade.

Skill = 1 − MAE_modelo / MAE_persistência nos mesmos pares (1 é perfeito,
0 empata com persistência, negativo é pior que não prever).

Uso: ``uv run python -m src.live.placar``. Grava ``reports/16_placar.md``,
``reports/16_placar.csv`` e ``data/processed/placar_pares.parquet``.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from ..core import storage
from ..ingest.common import ROOT
from .operational import ALVOS

PROCESSED = ROOT / "data" / "processed"
INTERIM = ROOT / "data" / "interim"
REPORTS = ROOT / "reports"
TZ_LOCAL = "Etc/GMT+3"
GAP_EVENTO = pd.Timedelta(hours=48)
JANELA_PICO = pd.Timedelta(hours=3)

CHAVE = ["produto", "motor", "cenario", "codigo", "h", "t_ref_utc"]


def _carimbo(pasta: Path) -> pd.Timestamp:
    m = re.search(r"(\d{8}T\d{6})", pasta.name)
    return pd.Timestamp(m.group(1), tz="UTC")


def carregar_emissoes(pasta: Path = PROCESSED / "live_runs") -> pd.DataFrame:
    """Produto operacional e cenários de todas as emissões, numa tabela longa."""
    partes = []
    for run in sorted(pasta.glob("emissao_*")):
        emitido = _carimbo(run)
        prev = run / "previsoes.parquet"
        if prev.exists():
            p = pd.read_parquet(prev)
            if "modo" in p:
                p = p[p["modo"] == "emissao"]
            p = p.dropna(subset=["previsto_cm"])
            if "emitido_em_utc" in p:
                p["emitido_em_utc"] = p["emitido_em_utc"].fillna(emitido)
            else:
                p["emitido_em_utc"] = emitido
            p = p.assign(produto="operacional", cenario="—", execucao=run.name)
            partes.append(p[["execucao", "produto", "motor", "cenario", "codigo", "h",
                             "t_ref_utc", "valido_para_utc", "emitido_em_utc", "previsto_cm"]])
        for arq in sorted(run.glob("cenarios_2*.parquet")):
            c = pd.read_parquet(arq).dropna(subset=["previsto_cm"])
            m = re.search(r"(\d{8}T\d{4})Z", arq.name)
            c["emitido_em_utc"] = pd.Timestamp(m.group(1), tz="UTC") if m else emitido
            c = c.assign(produto="cenario", execucao=run.name)
            partes.append(c[["execucao", "produto", "motor", "cenario", "codigo", "h",
                             "t_ref_utc", "valido_para_utc", "emitido_em_utc", "previsto_cm"]])
    if not partes:
        return pd.DataFrame()
    todas = pd.concat(partes, ignore_index=True)
    todas = todas[todas["codigo"].isin(ALVOS)]
    # Reexecuções com a mesma referência: vale a primeira emitida.
    todas = todas.sort_values("emitido_em_utc").drop_duplicates(CHAVE, keep="first")
    return todas.reset_index(drop=True)


def observado() -> pd.DataFrame:
    """Cota horária por estação (colunas = código), índice UTC."""
    ana = pd.read_parquet(INTERIM / "ana_hourly.parquet", columns=["codigo", "ts_utc", "nivel_cm"])
    ana = ana[ana["codigo"].isin(ALVOS)]
    return ana.pivot_table(index="ts_utc", columns="codigo", values="nivel_cm").astype(float)


def _eventos(t_ref: pd.Series) -> pd.Series:
    ordem = t_ref.sort_values()
    novo = ordem.diff() > GAP_EVENTO
    rotulo = ordem.groupby(novo.cumsum()).transform("min").dt.tz_convert(TZ_LOCAL)
    return rotulo.dt.strftime("%Y-%m-%d").reindex(t_ref.index)


def parear(prev: pd.DataFrame, obs: pd.DataFrame, agora: pd.Timestamp) -> pd.DataFrame:
    out = prev[prev["valido_para_utc"] <= agora].copy()
    serie = lambda cod, t: obs[cod].get(t, float("nan")) if cod in obs else float("nan")
    out["observado_cm"] = [serie(c, t) for c, t in zip(out.codigo, out.valido_para_utc)]
    out["persistencia_cm"] = [serie(c, t) for c, t in zip(out.codigo, out.t_ref_utc)]
    out = out.dropna(subset=["observado_cm", "persistencia_cm"])
    out["erro_cm"] = out["previsto_cm"] - out["observado_cm"]
    out["erro_persistencia_cm"] = out["persistencia_cm"] - out["observado_cm"]
    out["alvo"] = out["codigo"].map(lambda c: ALVOS[c][0])
    out["evento"] = _eventos(out["t_ref_utc"])
    out["fase"] = _fases(out, obs)
    return out.reset_index(drop=True)


def _fases(pares: pd.DataFrame, obs: pd.DataFrame) -> pd.Series:
    fase = pd.Series("recessao", index=pares.index)
    for (ev, cod), g in pares.groupby(["evento", "codigo"]):
        ini = g["t_ref_utc"].min() - pd.Timedelta(hours=24)
        # O pico pode vir depois da última emissão: procura até 48h além.
        fim = g["valido_para_utc"].max() + GAP_EVENTO
        s = obs[cod].loc[ini:fim].dropna()
        if s.empty:
            continue
        t_pico = s.idxmax()
        v = g["valido_para_utc"]
        fase.loc[g.index[v < t_pico - JANELA_PICO]] = "subida"
        fase.loc[g.index[(v - t_pico).abs() <= JANELA_PICO]] = "pico"
    return fase


def metricas(pares: pd.DataFrame, por: list[str]) -> pd.DataFrame:
    def _m(g: pd.DataFrame) -> pd.Series:
        mae = g["erro_cm"].abs().mean()
        mae_p = g["erro_persistencia_cm"].abs().mean()
        return pd.Series({
            "n": len(g),
            "mae_cm": mae,
            "vies_cm": g["erro_cm"].mean(),
            "rmse_cm": (g["erro_cm"] ** 2).mean() ** 0.5,
            "p90_abs_cm": g["erro_cm"].abs().quantile(0.9),
            "mae_persistencia_cm": mae_p,
            "skill": 1 - mae / mae_p if mae_p > 0 else float("nan"),
        })
    return pares.groupby(por).apply(_m, include_groups=False).reset_index()


def pareado(pares: pd.DataFrame) -> pd.DataFrame:
    """Operacional × cenários nos MESMOS pares: mesma execução, alvo e validade.

    As tabelas gerais misturam amostras diferentes (o linear operacional de 12h
    é quase só Estrela, por exemplo); só esta comparação decide entre produtos.
    """
    k = ["execucao", "alvo", "valido_para_utc"]
    op = pares[pares["produto"] == "operacional"][k + ["motor", "erro_cm"]]
    ce = pares[pares["produto"] == "cenario"][k + ["motor", "cenario", "erro_cm"]]
    j = op.merge(ce, on=k, suffixes=("_op", "_cen"))
    if j.empty:
        return pd.DataFrame()
    j["cenario"] = j["motor_cen"] + " · " + j["cenario"]
    return (j.groupby(["alvo", "motor_op", "cenario"])
            .agg(n=("erro_cm_cen", "size"),
                 mae_operacional_cm=("erro_cm_op", lambda e: e.abs().mean()),
                 mae_cenario_cm=("erro_cm_cen", lambda e: e.abs().mean()))
            .reset_index())


def _md(df: pd.DataFrame) -> str:
    fmt = df.copy()
    for c in fmt.select_dtypes("number").columns:
        padrao = "{:.2f}" if c == "skill" else "{:.0f}"
        fmt[c] = fmt[c].map(padrao.format)
    return fmt.to_markdown(index=False)


def relatorio(pares: pd.DataFrame, agora: pd.Timestamp) -> str:
    principal = metricas(pares, ["produto", "motor", "cenario", "h"])
    fases = metricas(pares, ["produto", "motor", "cenario", "fase"])
    alvos = metricas(pares, ["alvo", "produto", "motor", "h"])
    eventos = metricas(pares, ["evento", "produto", "h"])
    linhas = [
        "# Placar das emissões reais",
        "",
        (f"Gerado em {agora.tz_convert(TZ_LOCAL):%d/%m/%Y %H:%M} (UTC−3) por `src/live/placar.py`. "
        f"{len(pares)} pares previsto × observado de "
        f"{pares['execucao'].nunique()} emissões, em {pares['evento'].nunique()} eventos. "
        "Só entram números gravados antes da observação; replays não contam. "
        "Reexecuções com a mesma referência contam uma vez (a primeira)."),
        "",
        ("`skill` = 1 − MAE/MAE da persistência nos mesmos pares: 1 é perfeito, 0 empata "
        "com repetir a cota atual, negativo é pior. `fase` é relativa ao máximo observado do "
        "alvo no evento (pico = ±3h)."),
        "",
        "## Por produto, motor e horizonte",
        "",
        _md(principal),
        "",
        "## Operacional × cenários nos mesmos pares",
        "",
        ("Mesma execução, alvo e validade. É a única comparação justa entre produtos; "
         "as tabelas gerais cobrem amostras diferentes."),
        "",
        _md(pareado(pares)),
        "",
        "## Por fase da cheia",
        "",
        _md(fases),
        "",
        "## Por alvo (produto operacional e cenários)",
        "",
        _md(alvos),
        "",
        "## Por evento",
        "",
        _md(eventos),
        "",
    ]
    return "\n".join(linhas)


def main() -> None:
    agora = pd.Timestamp.now(tz="UTC")
    obs = observado()
    pares = parear(carregar_emissoes(), obs, agora)
    if pares.empty:
        print("[placar] nenhum par conferível")
        return
    storage.parquet(pares, PROCESSED / "placar_pares.parquet")
    tabela = metricas(pares, ["produto", "motor", "cenario", "alvo", "fase", "h"])
    storage.text(tabela.to_csv(index=False), REPORTS / "16_placar.csv")
    storage.text(relatorio(pares, agora), REPORTS / "16_placar.md")
    print(f"[placar] {len(pares)} pares; observado até {obs.index.max()}")


if __name__ == "__main__":
    main()
