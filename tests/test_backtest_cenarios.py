import numpy as np
import pandas as pd
import pytest

from src.live import backtest_cenarios as bt

T0 = pd.Timestamp("2024-05-01 00:00", tz="UTC")
IDX = pd.date_range(T0, periods=24, freq="h")


def _frame():
    f = pd.DataFrame(index=IDX)
    for u in bt.UNIDADES:
        # MERGE: 1 mm por hora, rotulado no fim da hora (t reflete [t-1, t)).
        f[f"chuva_{u}_1h"] = 1.0
    return f


def _postos():
    return pd.DataFrame({u: 2.0 for u in bt.UNIDADES}, index=IDX)


def test_chuva_futura_vem_da_previsao_e_latencia_dos_postos():
    prev = pd.concat([pd.DataFrame({"hora_utc": IDX, "mm": 3.0, "unidade": u})
                      for u in bt.UNIDADES])
    x = bt.entradas_chuva(_frame(), prev, 6, _postos())
    t = IDX[10]
    assert x.loc[t, "nova_passada_antas"] == 10.0     # 5h de postos a 2 mm
    assert x.loc[t, "nova_futura_antas"] == 18.0      # 6h de previsão a 3 mm
    # Sem horas suficientes de previsão no fim da janela: NaN, nunca zero.
    assert np.isnan(x.loc[IDX[-1], "nova_futura_antas"])


def test_cenarios_sem_chuva_e_chuva_perfeita():
    seco = bt.entradas_chuva(_frame(), None, 6, _postos())
    assert (seco.filter(like="futura") == 0).all(axis=None)
    perfeita = bt.entradas_chuva(_frame(), "perfeita", 6, _postos())
    assert perfeita.loc[IDX[10], "nova_futura_medio"] == 6.0


def _sim():
    linhas = []
    for cena, ridge, gbm in (("ECMWF D0", 100, 80), ("GFS D0", 120, 90),
                             ("ICON D0", 200, 95), ("GEM D0", 140, 85),
                             ("ECMWF D1", 0, 0)):
        for motor, v in (("ridge", ridge), ("gbm", gbm)):
            linhas.append({"evento": "ev", "alvo": "Muçum", "codigo": 86510000, "h": 12,
                           "t_ref_utc": T0, "nivel_em_t": 50.0, "observado_cm": 100.0,
                           "cenario": cena, "motor": motor, "barragens": "com",
                           "previsto_cm": float(v)})
    return pd.DataFrame(linhas)


def test_combinar_usa_so_a_versao_pedida():
    out = bt.combinar(_sim(), "D0")
    assert len(out) == 1
    # ridge: mediana(100,120,200,140)=130; gbm: mediana(80,90,95,85)=87,5
    assert out.previsto_cm.item() == pytest.approx((130 + 87.5) / 2)
    assert out.cenario.item() == "combinado D0"


def test_v2_cai_para_gbm_quando_falta_ridge():
    sim = _sim()
    sim.loc[sim.motor == "ridge", "previsto_cm"] = float("nan")
    assert bt.combinar(sim, "D0").previsto_cm.isna().all()        # regra publicada
    v2 = bt.combinar(sim, "D0", "combinado v2")
    assert v2.previsto_cm.item() == pytest.approx(87.5)           # mediana do GBM
    assert v2.cenario.item() == "combinado v2 D0"
    # Sem membros da Ridge com barragens no conjunto: não publica.
    assert bt.combinar(sim, "D0", "combinado v2 ridge+barragens").empty


def test_comparar_pareado_exige_todos_os_produtos():
    base = {"evento": "ev", "codigo": 1, "h": 12}
    res = pd.DataFrame([
        {**base, "t_ref_utc": T0, "produto": "a"},
        {**base, "t_ref_utc": T0, "produto": "b"},
        {**base, "t_ref_utc": IDX[1], "produto": "a"},
    ])
    out = bt.comparar_pareado(res, ["a", "b"])
    assert set(out.t_ref_utc) == {T0}


def test_chuva_propagada_estado_estacionario():
    from src.live.hidro import hid_features
    idx = pd.date_range("2024-01-01", periods=400, freq="h", tz="UTC")
    um = pd.Series(1.0, index=idx)
    # Chuva constante e prevista igual: armazenamento estável, aumento ~0.
    x = hid_features(um, um, um, 12, "antas")
    assert x["nova_hid_antas_6"].iloc[300] == pytest.approx(0.0, abs=1e-9)
    # Sem chuva futura: o armazenamento esvazia como a^h − 1.
    x = hid_features(um, um, pd.Series(0.0, index=idx), 12, "antas")
    assert x["nova_hid_antas_24"].iloc[300] == pytest.approx(np.exp(-12 / 24) - 1, rel=1e-6)
    # Lacuna no MERGE invalida o estado (nunca vira zero).
    buraco = um.copy()
    buraco.iloc[250] = np.nan
    x = hid_features(buraco, um, um, 12, "antas")
    assert np.isnan(x["nova_hid_antas_6"].iloc[262])
