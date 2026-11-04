import pandas as pd
import pytest

from src.live.combinado import combinar

T = pd.Timestamp("2026-09-29 12:00", tz="UTC")
MU, ES = 86510000, 86879300


def _op(codigo, alvo, motor, h, previsto):
    return {"alvo": alvo, "codigo": codigo, "motor": motor, "h": h, "t_ref_utc": T,
            "valido_para_utc": T + pd.Timedelta(hours=h), "nivel_em_t": 1000.0,
            "previsto_cm": previsto}


def _cen(codigo, alvo, h, cenario, motor, previsto):
    return {"alvo": alvo, "codigo": codigo, "h": h, "cenario": cenario, "motor": motor,
            "t_ref_utc": T, "valido_para_utc": T + pd.Timedelta(hours=h),
            "nivel_em_t": 1000.0, "previsto_cm": previsto}


def test_linear_no_curto_e_media_das_medianas_no_resto():
    op = pd.DataFrame([_op(ES, "Estrela", "linear", 3, 2010.0),
                       _op(ES, "Estrela", "linear", 6, 2020.0),
                       _op(MU, "Muçum", "gbm_delta", 6, 900.0)])
    linhas = []
    for codigo, alvo in ((ES, "Estrela"), (MU, "Muçum")):
        for h in (6, 12):
            for cena, ridge, gbm in (("ECMWF", 1100, 1000), ("GFS", 1200, 1040),
                                     ("ICON", 1300, 1060), ("GEM", 1500, 1080),
                                     ("sem mais chuva", 900, 950)):
                linhas += [_cen(codigo, alvo, h, cena, "ridge", ridge),
                           _cen(codigo, alvo, h, cena, "gbm", gbm)]
    out = combinar(op, pd.DataFrame(linhas)).set_index(["codigo", "h"])

    assert out.loc[(ES, 3), "previsto_cm"] == 2010.0
    assert out.loc[(ES, 6), "fonte"] == "linear operacional"
    # Muçum 6h: operacional é GBM, então vale o cenário.
    mu6 = out.loc[(MU, 6)]
    assert mu6["ridge_cm"] == 1250.0 and mu6["gbm_cm"] == 1050.0
    assert mu6["previsto_cm"] == pytest.approx(1150.0)
    assert mu6["envelope_inf_cm"] == 1000.0 and mu6["envelope_sup_cm"] == 1500.0
    assert mu6["sem_chuva_cm"] == pytest.approx(925.0)
    assert mu6["n_membros"] == 8
    assert out.loc[(ES, 12), "fonte"].startswith("cenários")


def test_sem_gbm_nao_publica_e_sem_ridge_usa_gbm():
    vazio = pd.DataFrame(columns=["motor", "h", "previsto_cm"])
    cen = pd.DataFrame([_cen(MU, "Muçum", 12, "ICON", "ridge", 1200.0),
                        _cen(MU, "Muçum", 12, "ICON", "gbm", float("nan"))])
    assert combinar(vazio, cen).empty
    cen = pd.DataFrame([_cen(MU, "Muçum", 12, "ICON", "ridge", float("nan")),
                        _cen(MU, "Muçum", 12, "GFS", "gbm", 1100.0),
                        _cen(MU, "Muçum", 12, "ICON", "gbm", 1140.0)])
    out = combinar(vazio, cen)
    assert out.previsto_cm.item() == 1120.0
    assert "ridge indisponível" in out.fonte.item()
