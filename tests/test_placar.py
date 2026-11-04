import pandas as pd
import pytest

from src.live import placar

MU = 86510000


def _obs():
    idx = pd.date_range("2026-09-28 00:00", periods=72, freq="h", tz="UTC")
    # Sobe 10 cm/h até 24h, depois desce 10 cm/h.
    nivel = [500 + 10 * min(i, 24) - 10 * max(i - 24, 0) for i in range(72)]
    return pd.DataFrame({MU: nivel}, index=idx).astype(float)


def _emissao(tmp_path, nome, t_ref, previsto, h=6, cenario=None):
    run = tmp_path / nome
    run.mkdir()
    linha = {"motor": "linear", "codigo": MU, "h": h, "t_ref_utc": t_ref,
             "valido_para_utc": t_ref + pd.Timedelta(hours=h), "previsto_cm": previsto}
    pd.DataFrame([{**linha, "modo": "emissao", "emitido_em_utc": pd.NaT}]).to_parquet(
        run / "previsoes.parquet")
    if cenario:
        carimbo = nome.split("_")[1][:13]
        pd.DataFrame([{**linha, "motor": "ridge", "cenario": cenario}]).to_parquet(
            run / f"cenarios_{carimbo}Z.parquet")
    return run


def test_persistencia_fase_e_deduplicacao(tmp_path):
    t = pd.Timestamp("2026-09-28 06:00", tz="UTC")
    _emissao(tmp_path, "emissao_20260928T064000000000Z", t, 620.0, cenario="ICON")
    # Reexecução com a mesma referência e outro número: deve ser ignorada.
    _emissao(tmp_path, "emissao_20260928T065000000000Z", t, 999.0)
    (tmp_path / "replay_20260928T070000000000Z").mkdir()

    prev = placar.carregar_emissoes(tmp_path)
    assert len(prev) == 2  # um operacional, um cenário
    assert prev.loc[prev.produto == "operacional", "previsto_cm"].item() == 620.0

    pares = placar.parear(prev, _obs(), pd.Timestamp("2026-10-01", tz="UTC"))
    p = pares.iloc[0]
    assert p.observado_cm == 620.0          # 500 + 10·12
    assert p.persistencia_cm == 560.0       # cota na referência
    assert p.erro_cm == 0.0
    assert p.erro_persistencia_cm == -60.0
    assert p.fase == "subida"


def test_pico_recessao_e_skill(tmp_path):
    _emissao(tmp_path, "emissao_20260928T190000000000Z",
             pd.Timestamp("2026-09-28 18:00", tz="UTC"), 740.0)   # validade 24h = pico
    _emissao(tmp_path, "emissao_20260929T020000000000Z",
             pd.Timestamp("2026-09-29 01:00", tz="UTC"), 700.0)   # validade 31h = recessão
    pares = placar.parear(placar.carregar_emissoes(tmp_path), _obs(),
                          pd.Timestamp("2026-10-01", tz="UTC"))
    assert sorted(pares.fase) == ["pico", "recessao"]
    m = placar.metricas(pares, ["fase"]).set_index("fase")
    assert m.loc["pico", "mae_cm"] == 0.0
    assert m.loc["pico", "skill"] == 1.0
    # Recessão: observado 670, persistência 730, previsto 700 → metade do erro.
    assert m.loc["recessao", "skill"] == pytest.approx(0.5)


def test_nao_confere_validade_futura(tmp_path):
    _emissao(tmp_path, "emissao_20260928T064000000000Z",
             pd.Timestamp("2026-09-28 06:00", tz="UTC"), 620.0)
    pares = placar.parear(placar.carregar_emissoes(tmp_path), _obs(),
                          pd.Timestamp("2026-09-28 10:00", tz="UTC"))
    assert pares.empty
