"""Produto combinado: operacional no curto prazo, cenários de chuva no resto.

Regra fixa (Fase 11, reports/17_produto_combinado.md):

- h ≤ 6 com motor operacional ``linear``: o linear operacional. É o melhor
  motor de curto prazo no placar (skill 0,76 em 3–6h) e no benchmark do SACE.
- demais horizontes: média de dois membros, Ridge e GBM dos cenários, cada um
  como mediana dos modelos meteorológicos (ECMWF, GFS, ICON, GEM). A Ridge
  acerta melhor o pico e o GBM a recessão; a média reduz o erro nas três fases
  sem precisar detectar a fase em tempo real.
- envelope: mínimo e máximo de todos os membros com chuva prevista, mais o
  cenário "sem mais chuva" como referência inferior. Não é intervalo de
  confiança.

A regra foi escolhida com os pares de set/2026 (seleção dentro da amostra).
Só um evento novo ou um backtest com previsões de chuva arquivadas confirma
o ganho. Não é sistema de alerta.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

from ..core import storage
from ..ingest.common import ROOT
from .operational import ALVOS

RUNS = ROOT / "data" / "processed" / "live_runs"
TZ_LOCAL = "Etc/GMT+3"
SECO = "sem mais chuva"
H_LINEAR = 6
COLUNAS = ["alvo", "codigo", "h", "fonte", "t_ref_utc", "valido_para_utc", "nivel_em_t",
           "previsto_cm", "ridge_cm", "gbm_cm", "envelope_inf_cm", "envelope_sup_cm",
           "sem_chuva_cm", "n_membros"]


def combinar(operacional: pd.DataFrame, cenarios: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    op = operacional.dropna(subset=["previsto_cm"])
    curtos = set()
    for p in op[(op["motor"] == "linear") & (op["h"] <= H_LINEAR)].itertuples(index=False):
        curtos.add((p.codigo, p.h))
        linhas.append({"alvo": ALVOS[p.codigo][0], "codigo": p.codigo, "h": p.h,
                       "fonte": "linear operacional",
                       "t_ref_utc": p.t_ref_utc, "valido_para_utc": p.valido_para_utc,
                       "nivel_em_t": getattr(p, "nivel_em_t", float("nan")),
                       "previsto_cm": p.previsto_cm,
                       "n_membros": 1})
    cen = cenarios.dropna(subset=["previsto_cm"])
    for (codigo, h), g in cen.groupby(["codigo", "h"]):
        if (codigo, h) in curtos:
            continue
        chuva = g[g["cenario"] != SECO]
        med = chuva.groupby("motor")["previsto_cm"].median()
        if not {"ridge", "gbm"} <= set(med.index):
            continue
        seco = g.loc[g["cenario"] == SECO, "previsto_cm"]
        linhas.append({"alvo": ALVOS[codigo][0], "codigo": codigo, "h": h,
                       "fonte": "cenários (média ridge+gbm, mediana NWP)",
                       "t_ref_utc": g["t_ref_utc"].iloc[0],
                       "valido_para_utc": g["valido_para_utc"].iloc[0],
                       "nivel_em_t": g["nivel_em_t"].iloc[0],
                       "previsto_cm": (med["ridge"] + med["gbm"]) / 2,
                       "ridge_cm": med["ridge"], "gbm_cm": med["gbm"],
                       "envelope_inf_cm": chuva["previsto_cm"].min(),
                       "envelope_sup_cm": chuva["previsto_cm"].max(),
                       "sem_chuva_cm": seco.mean() if not seco.empty else float("nan"),
                       "n_membros": len(chuva)})
    out = pd.DataFrame(linhas, columns=COLUNAS)
    return out.sort_values(["codigo", "h"]).reset_index(drop=True)


def cenarios_da_execucao(run: Path) -> tuple[pd.DataFrame, pd.Timestamp] | None:
    """Primeiro arquivo de cenários gravado na execução e seu carimbo."""
    arquivos = sorted(run.glob("cenarios_2*.parquet"))
    if not arquivos:
        return None
    m = re.search(r"(\d{8}T\d{4})Z", arquivos[0].name)
    return pd.read_parquet(arquivos[0]), pd.Timestamp(m.group(1), tz="UTC")


def historico(pasta: Path = RUNS) -> pd.DataFrame:
    """Aplica a regra a cada emissão arquivada, só com o que ela já tinha gravado."""
    partes = []
    for run in sorted(pasta.glob("emissao_*")):
        achado = cenarios_da_execucao(run)
        if achado is None or not (run / "previsoes.parquet").exists():
            continue
        cen, carimbo = achado
        op = pd.read_parquet(run / "previsoes.parquet")
        if "modo" in op:
            op = op[op["modo"] == "emissao"]
        partes.append(combinar(op, cen).assign(execucao=run.name, emitido_em_utc=carimbo))
    return pd.concat(partes, ignore_index=True) if partes else pd.DataFrame()


def tabela_local(comb: pd.DataFrame) -> str:
    t = comb.copy()
    t["validade"] = t["valido_para_utc"].dt.tz_convert(TZ_LOCAL).dt.strftime("%d/%m %H:%M")
    cols = ["alvo", "h", "validade", "nivel_em_t", "previsto_cm", "envelope_inf_cm",
            "envelope_sup_cm", "sem_chuva_cm", "fonte"]
    t = t[cols]
    for c in ["nivel_em_t", "previsto_cm", "envelope_inf_cm", "envelope_sup_cm", "sem_chuva_cm"]:
        t[c] = t[c].map(lambda v: "—" if pd.isna(v) else f"{v:.0f}")
    return t.to_markdown(index=False)


def main() -> None:
    pastas = sorted(RUNS.glob("emissao_*"), key=lambda p: p.stat().st_mtime)
    run = pastas[-1]
    arquivos = sorted(run.glob("cenarios_2*.parquet"))
    if not arquivos:
        raise SystemExit(f"Sem cenários em {run.name}; rode python -m src.live.cenarios antes.")
    op = pd.read_parquet(run / "previsoes.parquet")
    op = op[op["modo"] == "emissao"] if "modo" in op else op
    comb = combinar(op, pd.read_parquet(arquivos[-1]))
    carimbo = re.search(r"(\d{8}T\d{4})Z", arquivos[-1].name).group(1)
    storage.parquet(comb, run / f"combinado_{carimbo}Z.parquet")
    print(tabela_local(comb))
    print(json.dumps({"pasta": str(run)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
