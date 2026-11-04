"""Backtest fora da amostra dos cenários e do produto combinado (2024–2026).

Reproduz, hora a hora, o que o produto combinado teria publicado nas cheias de
2024 a 2026, com o que estaria disponível em cada referência:

- modelos treinados só com janelas encerradas antes do evento (``treino_antes``);
- latências do operacional (MERGE 5h, ONS 1h) via ``features_disponiveis``;
- chuva das 5h de latência pelos postos ANA, como ao vivo (o MERGE ainda não
  saiu);
- chuva futura pela previsão ARQUIVADA dos modelos meteorológicos (Open-Meteo
  previous runs API). Duas versões: ``D0`` usa a rodada mais recente
  disponível para cada hora (otimista, antecedência um pouco menor que a real)
  e ``D1`` a rodada de ~24h antes (conservadora). A verdade fica entre as duas.

Comparações nos mesmos instantes:

- ``chuva perfeita``: chuva MERGE observada no futuro, teto do método;
- ``sem mais chuva``: chuva futura zero;
- ``sem barragens``: os mesmos modelos sem as variáveis de defluência da CERAN;
- operacional selecionado (replay cronológico de ``src.live.evaluate``) e
  persistência.

Limitações: a chuva das previsões é média de pontos de grade de 0,3°, não a
mesma agregação por sub-bacia do MERGE; postos ANA cobrem mal o Antas; picos
de 2024 têm censura de sensor (Armadilha 0) e a 14 de Julho rompeu em
02/05/2024.

Uso: ``uv run python -m src.live.backtest_cenarios`` (baixa e guarda as
previsões arquivadas em ``data/raw/openmeteo_previous/``). Grava
``data/processed/backtest_cenarios.parquet`` e ``reports/18_backtest.md``.
"""

from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

from ..core import storage
from ..ingest.common import RAW, ROOT, get, is_cached, make_client, write_parquet
from ..models import baselines
from .cenarios import (
    HORIZONTES,
    MODELOS_MET,
    UNIDADES,
    RidgeChuva,
    chuva_nao_vista,
    chuva_por_hora,
    chuva_postos,
    colunas_base,
    features_cenario,
    montar,
    pontos_unidade,
    prever,
    treinar,
)
from .operational import ALVOS, features_disponiveis, treino_antes

PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
CACHE = RAW / "openmeteo_previous"
URL = "https://previous-runs-api.open-meteo.com/v1/forecast"
EVENTOS = ["ev20240430", "ev20240616", "ev20241012", "ev20250618", "ev20250922",
           "ev20251108", "ev20260629", "ev20260722"]
VERSOES = {"D0": "precipitation", "D1": "precipitation_previous_day1"}
PASSO_GRADE = 0.3
BARRAGENS = ("defluente_", "ddefluente_")


# --------------------------------------------------------------- chuva arquivada

def baixar_previsoes(evento: str, inicio: pd.Timestamp, fim: pd.Timestamp) -> pd.DataFrame:
    """Chuva prevista horária por unidade, modelo e versão (hora de início, UTC)."""
    dest = CACHE / f"{evento}.parquet"
    if is_cached(dest):
        return pd.read_parquet(dest)
    linhas = []
    params_base = {"hourly": ",".join(VERSOES.values()), "models": ",".join(MODELOS_MET),
                   "timezone": "GMT", "start_date": f"{inicio:%Y-%m-%d}",
                   "end_date": f"{fim:%Y-%m-%d}"}
    with make_client(timeout_s=120) as client:
        for u, pts in pontos_unidade(PASSO_GRADE).items():
            params = params_base | {"latitude": ",".join(str(p[0]) for p in pts),
                                    "longitude": ",".join(str(p[1]) for p in pts)}
            r = get(client, URL, params).json()
            r = r if isinstance(r, list) else [r]
            for m, rotulo in MODELOS_MET.items():
                for versao, var in VERSOES.items():
                    chave = f"{var}_{m}"
                    series = [pd.Series(p["hourly"].get(chave), dtype="float64",
                                        index=pd.to_datetime(p["hourly"]["time"], utc=True))
                              for p in r if chave in p["hourly"]]
                    if not series:
                        continue
                    # Média só com todos os pontos presentes; ausência fica NaN.
                    s = pd.concat(series, axis=1).mean(axis=1, skipna=False)
                    s.index = s.index - pd.Timedelta(hours=1)  # acumulado da hora anterior
                    linhas.append(s.rename("mm").to_frame().assign(
                        unidade=u, modelo=rotulo, versao=versao))
    df = pd.concat(linhas).rename_axis("hora_utc").reset_index()
    write_parquet(df, dest, url=URL, params=params_base | {"passo_grade": PASSO_GRADE})
    return df


# --------------------------------------------------------------- simulação

def entradas_chuva(frame: pd.DataFrame, previsao: pd.DataFrame | None, h: int,
                   postos: pd.DataFrame) -> pd.DataFrame:
    """nova_passada (postos) e nova_futura (previsão, MERGE ou zero) por hora."""
    out = {}
    for u in UNIDADES:
        out[f"nova_passada_{u}"] = chuva_nao_vista(postos[u], h).passada
        if previsao is None:
            out[f"nova_futura_{u}"] = 0.0
        elif isinstance(previsao, str):  # "perfeita"
            out[f"nova_futura_{u}"] = chuva_nao_vista(
                chuva_por_hora(frame[f"chuva_{u}_1h"]), h).futura
        else:
            r = previsao[previsao.unidade == u].set_index("hora_utc")["mm"]
            out[f"nova_futura_{u}"] = chuva_nao_vista(r, h).futura
    return pd.DataFrame(out).reindex(frame.index)


def _ridge_por_padrao(treino: pd.DataFrame, x_base: pd.DataFrame, codigo: int, h: int,
                      base: list[str], nova: list[str], motor: str) -> dict:
    """Uma Ridge por padrão de entradas presentes, como no live (``presentes``).

    Réguas que caem no evento (José Júlio em jun/2024) não derrubam a previsão:
    treina-se com as colunas disponíveis naquela hora. Devolve
    {padrão: (modelo, índice das referências)}.
    """
    extras = ("defluente_",) if motor == "ridge_barr" else ()
    relevantes = RidgeChuva(base, "", extras).feature_name_
    propria = f"nivel_{baselines.PROPRIA[codigo]}"
    presente = x_base[relevantes].notna()
    out = {}
    for padrao, idx in presente.groupby(list(presente.columns)).groups.items():
        cols = [c for c, ok in zip(relevantes, padrao) if ok]
        if propria not in cols:
            continue
        out[tuple(cols)] = (treinar(treino, codigo, h, cols + nova, motor), idx)
    return out


def simular_evento(frame: pd.DataFrame, evento: str, janela: pd.Series,
                   chuva_prev: pd.DataFrame) -> pd.DataFrame:
    disp = features_disponiveis(frame)
    postos = chuva_postos(frame)
    refs = frame.loc[janela.janela_inicio:janela.janela_fim].index
    linhas = []
    for codigo, (nome, ap) in ALVOS.items():
        ds = montar(frame, codigo)
        base = colunas_base(ds)
        sem_barr = [c for c in base if not c.startswith(BARRAGENS)]
        nivel = frame[f"nivel_{ap}"]
        for h in HORIZONTES:
            nova = features_cenario(frame, h)
            treino = treino_antes(ds.join(nova), janela.janela_inicio, h)
            x_base = disp.loc[refs, base]
            gbms = {b: treinar(treino, codigo, h, cols + list(nova.columns))
                    for b, cols in (("com", base), ("sem", sem_barr))}
            ridges = {m: _ridge_por_padrao(treino, x_base, codigo, h, base, list(nova.columns), m)
                      for m in ("ridge", "ridge_barr")}
            y = nivel.reindex(refs + pd.Timedelta(hours=h)).to_numpy()
            cenas = {"chuva perfeita": "perfeita", "sem mais chuva": None}
            for (modelo_met, versao), g in chuva_prev.groupby(["modelo", "versao"]):
                cenas[f"{modelo_met} {versao}"] = g
            for cena, prev in cenas.items():
                x = x_base.join(entradas_chuva(frame, prev, h, postos).loc[refs])
                ablacao = cena == "chuva perfeita" or cena.endswith("D0")
                preds = {("gbm", "com"): prever(gbms["com"], x, codigo),
                         ("ridge", "sem"): _prever_ridges(ridges["ridge"], x, codigo)}
                if ablacao:  # variantes de barragens só onde informam
                    preds[("gbm", "sem")] = prever(gbms["sem"], x, codigo)
                    preds[("ridge_barr", "com")] = _prever_ridges(ridges["ridge_barr"], x, codigo)
                for (motor, barr), pred in preds.items():
                    linhas.append(pd.DataFrame({
                        "evento": evento, "alvo": nome, "codigo": codigo, "h": h,
                        "cenario": cena, "motor": motor, "barragens": barr,
                        "t_ref_utc": refs, "nivel_em_t": nivel.reindex(refs).to_numpy(),
                        "previsto_cm": pred, "observado_cm": y}))
    return pd.concat(linhas, ignore_index=True)


def _prever_ridges(por_padrao: dict, x: pd.DataFrame, codigo: int) -> np.ndarray:
    pred = pd.Series(np.nan, index=x.index)
    for modelo, idx in por_padrao.values():
        pred.loc[idx] = prever(modelo, x.loc[idx], codigo)
    return pred.to_numpy()


# Variantes do produto combinado: (motor da Ridge, barragens no GBM, cai para GBM puro?)
VARIANTES = {
    "combinado": ("ridge", "com", False),               # regra publicada (v1)
    "combinado v2": ("ridge", "com", True),              # sem Ridge → GBM puro
    "combinado v2 ridge+barragens": ("ridge_barr", "com", True),
    "combinado v2 sem barragens": ("ridge", "sem", True),
}


def combinar(sim: pd.DataFrame, versao: str, variante: str = "combinado") -> pd.DataFrame:
    """Média das medianas NWP de Ridge e GBM (regra de ``combinado.combinar``, h ≥ 6)."""
    ridge, barr_gbm, cai = VARIANTES[variante]
    s = sim[sim.cenario.str.endswith(f" {versao}")]
    s = s[(s.motor == ridge) | ((s.motor == "gbm") & (s.barragens == barr_gbm))]
    if not {ridge, "gbm"} <= set(s.motor):
        return pd.DataFrame()
    chave = ["evento", "alvo", "codigo", "h", "t_ref_utc", "nivel_em_t", "observado_cm"]
    med = s.groupby(chave + ["motor"])["previsto_cm"].median().unstack("motor")
    out = (med[ridge] + med["gbm"]) / 2
    if cai:
        out = out.fillna(med["gbm"])
    out = out.rename("previsto_cm").reset_index()
    return out.assign(cenario=f"{variante} {versao}", motor="combinado", barragens=barr_gbm)


# --------------------------------------------------------------- métricas

def operacional_replay(cotas: pd.DataFrame) -> pd.DataFrame:
    """Motor operacional selecionado, do replay cronológico já validado."""
    manifesto = json.loads((REPORTS / "12_live_modelos.json").read_text())
    escolha = {(m["codigo"], m["h"]): m["motor"] for m in manifesto["modelos"]}
    v = pd.read_parquet(PROCESSED / "live_validacao_previsoes.parquet")
    v = v[v.evento.isin(EVENTOS)]
    v = v[[escolha.get((c, h)) == m for c, h, m in zip(v.codigo, v.h, v.motor)]]
    return v.assign(cenario="operacional", barragens="com")[
        ["evento", "alvo", "codigo", "h", "t_ref_utc", "cenario", "motor", "barragens",
         "previsto_cm", "observado_cm"]]


def rotular(df: pd.DataFrame, frame: pd.DataFrame, cotas: pd.DataFrame) -> pd.DataFrame:
    """Regime alto (≥ atenção na referência ou na validade) e fase pelo pico do evento."""
    df = df.dropna(subset=["previsto_cm", "observado_cm"]).copy()
    atencao = df.codigo.map(cotas["atencao_cm"])
    nivel_t = df.get("nivel_em_t", np.nan)
    df["alto"] = (df.observado_cm >= atencao) | (nivel_t >= atencao)
    df["valido_para_utc"] = df.t_ref_utc + pd.to_timedelta(df.h, unit="h")
    fase = pd.Series("recessao", index=df.index)
    for (ev, cod), g in df.groupby(["evento", "codigo"]):
        ap = ALVOS[cod][1]
        s = frame[f"nivel_{ap}"].loc[g.t_ref_utc.min():g.valido_para_utc.max()].dropna()
        if s.empty:
            continue
        t_pico = s.idxmax()
        v = g.valido_para_utc
        fase[g.index[v < t_pico - pd.Timedelta(hours=3)]] = "subida"
        fase[g.index[(v - t_pico).abs() <= pd.Timedelta(hours=3)]] = "pico"
    df["fase"] = fase
    df["erro_cm"] = df.previsto_cm - df.observado_cm
    return df


def tabela(df: pd.DataFrame, por: list[str]) -> pd.DataFrame:
    g = df.groupby(por)
    out = g["erro_cm"].agg(n="size", mae_cm=lambda e: e.abs().mean(), vies_cm="mean")
    out["mae_persistencia_cm"] = g["erro_persistencia_cm"].apply(lambda e: e.abs().mean())
    out["skill"] = 1 - out.mae_cm / out.mae_persistencia_cm
    return out.reset_index()


def comparar_pareado(res: pd.DataFrame, produtos: list[str]) -> pd.DataFrame:
    """Só instantes em que todos os produtos listados têm previsão e há observação."""
    chave = ["evento", "codigo", "h", "t_ref_utc"]
    sub = res[res.produto.isin(produtos)]
    n = sub.groupby(chave)["produto"].nunique()
    comuns = n[n == len(produtos)].index
    return sub.set_index(chave).loc[lambda d: d.index.isin(comuns)].reset_index()


def _md(df: pd.DataFrame) -> str:
    fmt = df.copy()
    for c in fmt.select_dtypes("number").columns:
        padrao = "{:.2f}" if c == "skill" else "{:.0f}"
        fmt[c] = fmt[c].map(padrao.format)
    return fmt.to_markdown(index=False)


def cobertura(alto: pd.DataFrame, produtos: list[str], h: int) -> pd.DataFrame:
    """Fração das horas de regime alto em que cada produto publicou algo."""
    chave = ["evento", "codigo", "h", "t_ref_utc"]
    sub = alto[alto.h == h]
    todas = sub[chave].drop_duplicates().groupby("evento").size()
    linhas = {prod: sub.loc[sub.produto == prod, chave].drop_duplicates()
              .groupby("evento").size() / todas for prod in produtos}
    return (pd.DataFrame(linhas).fillna(0) * 100).round(0).reset_index()


def relatorio(res: pd.DataFrame) -> str:
    alto = res[res.alto]
    v1, v2 = "combinado D0", "combinado v2 D0"
    barr = ["combinado v2 D0", "combinado v2 sem barragens D0", "combinado v2 ridge+barragens D0"]
    prin = [v1, v2, "combinado v2 D1", "operacional"]
    p = comparar_pareado(alto[alto.h.isin([6, 12])], [v2, "combinado v2 D1", "operacional"])
    p1 = comparar_pareado(alto[alto.h.isin([6, 12])], [v1, "operacional"])
    longos = [v2, "chuva perfeita · gbm", "chuva perfeita · ridge",
              "sem mais chuva · gbm", "sem mais chuva · ridge"]
    q = comparar_pareado(alto[alto.barragens.isin(["com", "sem"])], longos)
    b = comparar_pareado(alto[alto.h >= 12], barr)
    membros = alto[alto.cenario.str.contains(" D[01]$") & alto.motor.isin(["gbm", "ridge"])
                   & ~((alto.motor == "gbm") & (alto.barragens == "sem"))]
    return "\n".join([
        "# Backtest fora da amostra: cenários de chuva e produto combinado",
        "",
        (f"Eventos: {', '.join(EVENTOS)}. Regime alto: cota ≥ atenção na referência ou na "
         "validade. Treino só com janelas encerradas antes de cada evento; latências do "
         "operacional; chuva de latência pelos postos ANA; chuva futura pela previsão "
         "arquivada (Open-Meteo previous runs). Gerado por `src/live/backtest_cenarios.py`."),
        "",
        ("`D0`: rodada meteorológica mais recente (otimista); `D1`: rodada ~24h antes "
         "(conservadora). `skill` = 1 − MAE/MAE da persistência. `combinado` é a regra "
         "publicada em 04/11; `v2` cai para o GBM puro quando a Ridge não tem entradas."),
        "",
        "## Cobertura: % das horas de regime alto com previsão (12h)",
        "",
        _md(cobertura(alto, prin + barr[1:], 12)),
        "",
        "## Combinado v2 × operacional nos mesmos instantes",
        "",
        _md(tabela(p, ["produto", "h"])),
        "",
        "### Regra publicada (v1) × operacional, nos instantes em que a v1 existe",
        "",
        _md(tabela(p1, ["produto", "h"])),
        "",
        "### Por evento (12h, v2 D0 × operacional)",
        "",
        _md(tabela(p[(p.h == 12) & (p.produto != "combinado v2 D1")], ["evento", "produto"])),
        "",
        "### Por alvo (12h)",
        "",
        _md(tabela(p[(p.h == 12) & (p.produto != "combinado v2 D1")], ["alvo", "produto"])),
        "",
        "## Contra o teto (chuva perfeita) e o piso (sem mais chuva)",
        "",
        _md(tabela(q, ["produto", "h"])),
        "",
        "### Por fase da cheia",
        "",
        _md(tabela(q, ["produto", "fase"])),
        "",
        "## Barragens (defluência da CERAN), h ≥ 12",
        "",
        ("`sem barragens`: GBM sem defluência. `ridge+barragens`: a Ridge pode usar a "
         "defluência, o que cobre as horas sem régua de montante."),
        "",
        _md(tabela(b, ["produto", "h"])),
        "",
        "### Barragens por evento (12h)",
        "",
        _md(tabela(b[b.h == 12], ["evento", "produto"])),
        "",
        "## Membros meteorológicos: MAE (cm) por horizonte",
        "",
        _md(tabela(membros.assign(produto=membros.cenario + " · " + membros.motor),
                   ["produto", "h"]).pivot(index="produto", columns="h", values="mae_cm")
            .reset_index()),
        "",
    ])


def main() -> None:
    if "--relatorio" in sys.argv:  # só refaz o relatório a partir dos pares gravados
        escrever_relatorio(pd.read_parquet(PROCESSED / "backtest_cenarios.parquet"))
        return
    frame = pd.read_parquet(PROCESSED / "features_hourly.parquet").set_index("ts_utc")
    eventos = pd.read_parquet(PROCESSED / "eventos.parquet").set_index("evento_id")
    cotas = pd.read_csv(ROOT / "data/reference/cotas_referencia.csv").set_index("codigo")
    so = [a for a in sys.argv[1:] if a.startswith("ev")]
    sims = []
    for ev in so or EVENTOS:
        jan = eventos.loc[ev]
        chuva = baixar_previsoes(ev, jan.janela_inicio - pd.Timedelta(days=1),
                                 jan.janela_fim + pd.Timedelta(days=2))
        print(f"[backtest] {ev}: chuva prevista {chuva.groupby(['modelo', 'versao']).mm.count().min()}"
              f"–{chuva.groupby(['modelo', 'versao']).mm.count().max()} horas por membro", flush=True)
        sim = simular_evento(frame, ev, jan, chuva)
        sims += [sim] + [combinar(sim, v, var) for var in VARIANTES for v in ("D0", "D1")
                         if v == "D0" or var in ("combinado", "combinado v2")]
        print(f"[backtest] {ev}: {len(sim)} previsões", flush=True)
    res = pd.concat(sims, ignore_index=True)
    persist = [frame[f"nivel_{ALVOS[c][1]}"].get(t) for c, t in zip(res.codigo, res.t_ref_utc)]
    res["nivel_em_t"] = persist
    op = operacional_replay(cotas)
    op = op[op.t_ref_utc.isin(res.t_ref_utc.unique())].copy()
    op["nivel_em_t"] = [frame[f"nivel_{ALVOS[c][1]}"].get(t) for c, t in zip(op.codigo, op.t_ref_utc)]
    # Regra do combinado: até 6h, onde o operacional é linear, vale o linear.
    curto = op[(op.motor == "linear") & (op.h <= 6)]
    chave = ["evento", "codigo", "h", "t_ref_utc"]
    for nome in [c for c in res.cenario.unique() if c.startswith("combinado")]:
        alvo = res.cenario == nome
        sai = res[alvo].set_index(chave).index.isin(curto.set_index(chave).index)
        res = pd.concat([res.drop(res[alvo].index[sai]),
                         curto.assign(cenario=nome, motor="combinado")], ignore_index=True)
    res = rotular(pd.concat([res, op], ignore_index=True), frame, cotas)
    res["erro_persistencia_cm"] = res.nivel_em_t - res.observado_cm
    res["produto"] = np.where(res.motor.isin(["combinado"]) | (res.cenario == "operacional"),
                              res.cenario, res.cenario + " · " + res.motor)
    res = res.dropna(subset=["erro_persistencia_cm"])
    storage.parquet(res, PROCESSED / "backtest_cenarios.parquet")
    escrever_relatorio(res)


def escrever_relatorio(res: pd.DataFrame) -> None:
    storage.text(relatorio(res), REPORTS / "18_backtest.md")
    print(f"[backtest] {len(res)} pares; relatório em reports/18_backtest.md")


if __name__ == "__main__":
    main()
