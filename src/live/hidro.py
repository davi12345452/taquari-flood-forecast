"""Chuva propagada por reservatórios lineares (Fase 11).

Variável ``nova_hid_{unidade}_{k}``: aumento, entre t e t+h, do armazenamento
de um reservatório linear de constante k horas alimentado pela chuva da
macro-unidade. O estado em t usa a chuva conhecida até t (MERGE até t−L−1 e a
chuva das L horas de latência); o aumento até t+h usa a chuva de t a t+h−1.
No treino tudo é MERGE (perfect prognosis); na inferência a latência vem dos
postos e o futuro da previsão. Linear na chuva: escala com eventos maiores que
os do treino. Validado em reports/19_experimento_subida.md.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .cenarios import LATENCIA, UNIDADES, chuva_por_hora

CONSTANTES_H = (6, 24)


def _ema(r: pd.Series, k: float) -> pd.Series:
    """E(t) = a·E(t−1) + (1−a)·r(t−1). NaN enquanto houver lacuna nas últimas 3k horas."""
    a = np.exp(-1 / k)
    e = r.fillna(0.0).ewm(alpha=1 - a, adjust=False).mean().shift(1)
    lacuna = r.isna().astype(float).rolling(int(3 * k), min_periods=1).max().shift(1)
    return e.where(lacuna == 0)


def _futuro(f: pd.Series, h: int, a: float) -> pd.Series:
    """Σ_{i=1..h} (1−a)·a^{h−i}·f(t+i−1): chuva de t a t+h−1 levada até t+h."""
    total = pd.Series(0.0, index=f.index)
    for i in range(1, h + 1):
        total = total + (1 - a) * a ** (h - i) * f.shift(-(i - 1))
    return total


def hid_features(merge_1h: pd.Series, passada: pd.Series, futura: pd.Series,
                 h: int, unidade: str) -> pd.DataFrame:
    """Séries indexadas pela hora de início da chuva; saída na grade horária comum."""
    # Grade regular cobrindo as três séries: deslocamentos por tempo, nunca por
    # posição, e a previsão pode passar do fim das observações.
    # Sem nenhum valor, a grade vem dos próprios índices e tudo sai NaN.
    series = [s.dropna() for s in (merge_1h, passada, futura)]
    if all(s.empty for s in series):
        series = [s for s in (merge_1h, passada, futura) if len(s)]
    inicio = min(s.index.min() for s in series if len(s))
    fim = max(s.index.max() for s in series if len(s))
    idx = pd.date_range(inicio, fim, freq="h")
    merge_1h, passada, futura = (x.reindex(idx) for x in (merge_1h, passada, futura))
    out = {}
    for k in CONSTANTES_H:
        a = np.exp(-1 / k)
        e_antes = _ema(merge_1h, k).shift(LATENCIA)  # E(t−L)
        latencia = sum((1 - a) * a ** (j - 1) * passada.shift(j) for j in range(1, LATENCIA + 1))
        e_t = a ** LATENCIA * e_antes + latencia
        out[f"nova_hid_{unidade}_{k}"] = (a ** h - 1) * e_t + _futuro(futura, h, a)
    return pd.DataFrame(out, index=idx)


def hid_treino(frame: pd.DataFrame, h: int) -> pd.DataFrame:
    partes = []
    for u in UNIDADES:
        r = chuva_por_hora(frame[f"chuva_{u}_1h"])
        partes.append(hid_features(r, r, r, h, u))
    return pd.concat(partes, axis=1).reindex(frame.index)


def hid_inferencia(frame: pd.DataFrame, previsao: pd.DataFrame, postos: pd.DataFrame,
                   h: int) -> pd.DataFrame:
    """Backtest: previsão arquivada como série contínua (hora_utc, mm, unidade)."""
    partes = []
    for u in UNIDADES:
        r = chuva_por_hora(frame[f"chuva_{u}_1h"])
        f = previsao[previsao.unidade == u].set_index("hora_utc")["mm"]
        partes.append(hid_features(r, postos[u], f, h, u))
    return pd.concat(partes, axis=1).reindex(frame.index)


def hid_no_instante(frame: pd.DataFrame, postos: pd.DataFrame,
                    futuras: dict[str, pd.Series], t: pd.Timestamp, h: int) -> dict[str, float]:
    """Ao vivo: MERGE completado pelos postos até t−1; ``futuras`` de t a t+h−1."""
    valores = {}
    for u in UNIDADES:
        r = chuva_por_hora(frame[f"chuva_{u}_1h"]).loc[:t - pd.Timedelta(hours=1)]
        conhecida = r.fillna(postos[u].reindex(r.index))
        x = hid_features(conhecida, conhecida, futuras[u], h, u)
        valores |= x.loc[t].to_dict() if t in x.index else {
            f"nova_hid_{u}_{k}": float("nan") for k in CONSTANTES_H}
    return valores
