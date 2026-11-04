"""Experimento da Fase 11: atacar a subestimação das subidas.

O backtest (reports/18_backtest.md) mostrou viés de −95 cm na subida mesmo com
chuva perfeita: o gargalo é o modelo, não a chuva prevista. Três variantes,
definidas ANTES de rodar, comparadas com o mesmo arranjo do backtest (treino só
no passado, chuva de latência pelos postos, chuva futura arquivada D0):

- ``gbm_lt``: LightGBM com folhas lineares (``linear_tree``), que permite
  extrapolar além das subidas do treino;
- ``gbm_peso``: peso 5× nas subidas fortes (Δcota > 100 cm no horizonte) e 2×
  no regime alto (cota ≥ atenção) durante o treino;
- ``*_hid``: chuva propagada por reservatórios lineares (6h e 24h) por
  macro-unidade, como variável: ``nova_hid_{u}_{k}`` = aumento do armazenamento
  routed entre t e t+h, com a chuva conhecida até t e a prevista de t a t+h.
  Linear na chuva, então escala com eventos maiores que os do treino.

Protocolo: seleção nos eventos de 2024–2025; confirmação nos de 2026, que não
entram na escolha. Critério fixado antes: menor MAE em subida+pico de 12–24h,
sem piorar o MAE geral de 12–24h em mais de 5%.

Uso: ``uv run python -m src.live.experimento_subida`` (usa o cache de chuva
prevista do backtest). Grava ``data/processed/experimento_subida.parquet`` e
``reports/19_experimento_subida.md``.
"""

from __future__ import annotations

import sys

import lightgbm as lgb
import numpy as np
import pandas as pd

from ..core import storage
from ..ingest.common import ROOT, load_config
from ..models import baselines, gbm
from .backtest_cenarios import (
    EVENTOS,
    _md,
    _prever_ridges,
    _ridge_por_padrao,
    baixar_previsoes,
    comparar_pareado,
    entradas_chuva,
    operacional_replay,
    rotular,
    tabela,
)
from .cenarios import (
    HORIZONTES,
    chuva_postos,
    colunas_base,
    features_cenario,
    montar,
    prever,
    treinar,
)
from .hidro import hid_inferencia, hid_treino
from .operational import ALVOS, features_disponiveis, treino_antes

PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
SELECAO = [e for e in EVENTOS if e < "ev2026"]
CONFIRMACAO = [e for e in EVENTOS if e >= "ev2026"]
PESO_SUBIDA, PESO_ALTO, LIMIAR_SUBIDA_CM = 5.0, 2.0, 100.0


# --------------------------------------------------------------- GBM variantes

def treinar_gbm(train: pd.DataFrame, codigo: int, h: int, cols: list[str], *,
                linear: bool = False, peso: bool = False):
    propria = f"nivel_{baselines.PROPRIA[codigo]}"
    alvo = f"y_{h}h"
    train = train.dropna(subset=[alvo, propria, *[c for c in cols if c.startswith("nova_")]]).copy()
    train[alvo] = train[alvo] - train[propria]
    cfg = load_config("model")
    tr, ev = gbm._split_early_stopping(train, cfg["valid_frac_janelas"])
    params = cfg["lgbm"] | {"n_jobs": 4, "random_state": 42}
    if linear:
        params |= {"linear_tree": True, "linear_lambda": 1.0}
    pesos = None
    if peso:
        atencao = pd.read_csv(ROOT / "data/reference/cotas_referencia.csv").set_index(
            "codigo").loc[codigo, "atencao_cm"]
        pesos = (1 + (PESO_SUBIDA - 1) * (tr[alvo] > LIMIAR_SUBIDA_CM)
                 + (PESO_ALTO - 1) * (tr[propria] >= atencao)).to_numpy()
    modelo = lgb.LGBMRegressor(**params)
    modelo.fit(tr[cols], tr[alvo], sample_weight=pesos, eval_set=[(ev[cols], ev[alvo])],
               callbacks=[lgb.early_stopping(cfg["early_stopping_rounds"], verbose=False)])
    return modelo


# --------------------------------------------------------------- simulação

def simular_evento(frame: pd.DataFrame, evento: str, janela: pd.Series,
                   chuva_prev: pd.DataFrame) -> pd.DataFrame:
    disp = features_disponiveis(frame)
    postos = chuva_postos(frame)
    refs = frame.loc[janela.janela_inicio:janela.janela_fim].index
    d0 = chuva_prev[chuva_prev.versao == "D0"]
    linhas = []
    for codigo, (nome, ap) in ALVOS.items():
        ds = montar(frame, codigo)
        base = colunas_base(ds)
        nivel = frame[f"nivel_{ap}"]
        for h in HORIZONTES:
            nova = features_cenario(frame, h)
            hid = hid_treino(frame, h)
            treino = treino_antes(ds.join(nova).join(hid), janela.janela_inicio, h)
            nv, hd = list(nova.columns), list(hid.columns)
            gbms = {
                "gbm": treinar(treino, codigo, h, base + nv),
                "gbm_lt": treinar_gbm(treino, codigo, h, base + nv, linear=True),
                "gbm_peso": treinar_gbm(treino, codigo, h, base + nv, peso=True),
                "gbm_hid": treinar_gbm(treino, codigo, h, base + nv + hd),
                "gbm_hid_peso": treinar_gbm(treino, codigo, h, base + nv + hd, peso=True),
            }
            x_base = disp.loc[refs, base]
            ridges = {"ridge": _ridge_por_padrao(treino, x_base, codigo, h, base, nv, "ridge"),
                      "ridge_hid": _ridge_por_padrao(treino, x_base, codigo, h, base, nv + hd,
                                                     "ridge")}
            y = nivel.reindex(refs + pd.Timedelta(hours=h)).to_numpy()
            cenas = {"chuva perfeita": None}
            for modelo_met, g in d0.groupby("modelo"):
                cenas[f"{modelo_met} D0"] = g
            for cena, prev in cenas.items():
                if prev is None:
                    x = x_base.join(entradas_chuva(frame, "perfeita", h, postos).loc[refs])
                    x = x.join(hid.loc[refs])
                else:
                    x = x_base.join(entradas_chuva(frame, prev, h, postos).loc[refs])
                    x = x.join(hid_inferencia(frame, prev, postos, h).loc[refs])
                preds = {m: prever(mod, x, codigo) for m, mod in gbms.items()}
                preds |= {m: _prever_ridges(r, x, codigo) for m, r in ridges.items()}
                for motor, pred in preds.items():
                    linhas.append(pd.DataFrame({
                        "evento": evento, "alvo": nome, "codigo": codigo, "h": h,
                        "cenario": cena, "motor": motor, "barragens": "com",
                        "t_ref_utc": refs, "nivel_em_t": nivel.reindex(refs).to_numpy(),
                        "previsto_cm": pred, "observado_cm": y}))
    return pd.concat(linhas, ignore_index=True)


COMBINACOES = {
    "combinado v2": ("ridge", "gbm"),
    "comb lt": ("ridge", "gbm_lt"),
    "comb peso": ("ridge", "gbm_peso"),
    "comb hid": ("ridge_hid", "gbm_hid"),
    "comb hid+peso": ("ridge_hid", "gbm_hid_peso"),
    "comb ridge_hid": ("ridge_hid", "gbm"),
}


def combinar(sim: pd.DataFrame) -> pd.DataFrame:
    """Média das medianas D0 de cada par (ridge, gbm); sem Ridge, vale o GBM."""
    s = sim[sim.cenario.str.endswith(" D0")]
    chave = ["evento", "alvo", "codigo", "h", "t_ref_utc", "nivel_em_t", "observado_cm"]
    med = s.groupby(chave + ["motor"])["previsto_cm"].median().unstack("motor")
    partes = []
    for nome, (ridge, g) in COMBINACOES.items():
        v = ((med[ridge] + med[g]) / 2).fillna(med[g]).rename("previsto_cm").reset_index()
        partes.append(v.assign(cenario=nome, motor="combinado", barragens="com"))
    for g in ("gbm", "gbm_lt", "gbm_peso", "gbm_hid", "gbm_hid_peso", "ridge", "ridge_hid"):
        v = med[g].rename("previsto_cm").reset_index()
        partes.append(v.assign(cenario=f"{g} mediana D0", motor="combinado", barragens="com"))
    return pd.concat(partes, ignore_index=True)


# --------------------------------------------------------------- relatório

def avaliar(res: pd.DataFrame, eventos: list[str]) -> pd.DataFrame:
    """MAE por produto em 12–24h: geral e subida+pico, nos mesmos instantes."""
    alto = res[res.alto & res.evento.isin(eventos) & (res.h >= 12)]
    produtos = list(COMBINACOES) + [f"{g} mediana D0" for g in
                                    ("gbm", "gbm_lt", "gbm_peso", "gbm_hid", "gbm_hid_peso",
                                     "ridge", "ridge_hid")]
    p = comparar_pareado(alto, produtos)
    geral = tabela(p, ["produto"]).set_index("produto")
    sp = tabela(p[p.fase.isin(["subida", "pico"])], ["produto"]).set_index("produto")
    out = pd.DataFrame({"n": geral.n, "mae_geral_cm": geral.mae_cm, "vies_geral_cm": geral.vies_cm,
                        "mae_subida_pico_cm": sp.mae_cm, "vies_subida_pico_cm": sp.vies_cm})
    ref = out.loc["combinado v2"]
    out["delta_geral_pct"] = 100 * (out.mae_geral_cm / ref.mae_geral_cm - 1)
    out["delta_subida_pico_pct"] = 100 * (out.mae_subida_pico_cm / ref.mae_subida_pico_cm - 1)
    out["aprovado"] = (out.delta_geral_pct <= 5) & (out.delta_subida_pico_pct < 0)
    return out.sort_values("mae_subida_pico_cm").reset_index()


def escolher(sel: pd.DataFrame) -> str:
    aprovados = sel[sel.aprovado & (sel.produto != "combinado v2")]
    return aprovados.iloc[0]["produto"] if not aprovados.empty else "combinado v2"


def relatorio(res: pd.DataFrame) -> str:
    sel, conf = avaliar(res, SELECAO), avaliar(res, CONFIRMACAO)
    vencedor = escolher(sel)
    alto = res[res.alto]
    prods = ["combinado v2", vencedor] if vencedor != "combinado v2" else ["combinado v2"]
    final = comparar_pareado(alto[alto.h == 12], [*prods, "operacional"])
    longo = comparar_pareado(alto[alto.h >= 12], prods)
    return "\n".join([
        "# Experimento: subestimação das subidas",
        "",
        ("Gerado por `src/live/experimento_subida.py`. Mesmo arranjo do backtest "
         "(reports/18_backtest.md): treino só no passado, chuva de latência pelos postos, "
         "chuva futura arquivada D0. Regime alto, 12–24h, mesmos instantes para todos os "
         "produtos."),
        "",
        (f"Seleção: {', '.join(SELECAO)}. Confirmação (fora da escolha): "
         f"{', '.join(CONFIRMACAO)}. Critério fixado antes de rodar: menor MAE em "
         "subida+pico sem piorar o MAE geral em mais de 5% contra o combinado v2."),
        "",
        "## Seleção (2024–2025)",
        "",
        _md(sel),
        "",
        f"**Escolhido na seleção:** `{vencedor}`.",
        "",
        "## Confirmação (2026)",
        "",
        _md(conf),
        "",
        "## Escolhido × combinado v2 × operacional (todos os eventos, 12h)",
        "",
        _md(tabela(final, ["produto", "h"])),
        "",
        "## Escolhido × combinado v2 por evento (12–24h)",
        "",
        _md(tabela(longo, ["evento", "produto"])),
        "",
        "## Por fase (12–24h, todos os eventos)",
        "",
        _md(tabela(longo, ["produto", "fase"])),
        "",
    ])


def main() -> None:
    if "--relatorio" in sys.argv:
        res = pd.read_parquet(PROCESSED / "experimento_subida.parquet")
        storage.text(relatorio(res), REPORTS / "19_experimento_subida.md")
        return
    frame = pd.read_parquet(PROCESSED / "features_hourly.parquet").set_index("ts_utc")
    eventos = pd.read_parquet(PROCESSED / "eventos.parquet").set_index("evento_id")
    cotas = pd.read_csv(ROOT / "data/reference/cotas_referencia.csv").set_index("codigo")
    so = [a for a in sys.argv[1:] if a.startswith("ev")]
    partes = []
    for ev in so or EVENTOS:
        jan = eventos.loc[ev]
        chuva = baixar_previsoes(ev, jan.janela_inicio - pd.Timedelta(days=1),
                                 jan.janela_fim + pd.Timedelta(days=2))
        sim = simular_evento(frame, ev, jan, chuva)
        partes += [sim, combinar(sim)]
        print(f"[experimento] {ev}: {len(sim)} previsões", flush=True)
    res = pd.concat(partes, ignore_index=True)
    op = operacional_replay(cotas)
    op = op[op.t_ref_utc.isin(res.t_ref_utc.unique())].copy()
    op["nivel_em_t"] = [frame[f"nivel_{ALVOS[c][1]}"].get(t) for c, t in zip(op.codigo, op.t_ref_utc)]
    res = rotular(pd.concat([res, op], ignore_index=True), frame, cotas)
    res["erro_persistencia_cm"] = res.nivel_em_t - res.observado_cm
    res["produto"] = np.where(res.motor == "combinado", res.cenario,
                              np.where(res.cenario == "operacional", "operacional",
                                       res.cenario + " · " + res.motor))
    res = res.dropna(subset=["erro_persistencia_cm"])
    destino = "experimento_subida" + ("_parcial" if so else "")
    storage.parquet(res, PROCESSED / f"{destino}.parquet")
    if not so:
        storage.text(relatorio(res), REPORTS / "19_experimento_subida.md")
    print(f"[experimento] {len(res)} pares")


if __name__ == "__main__":
    main()
