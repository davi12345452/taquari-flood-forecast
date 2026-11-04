"""Atualiza só as observações (ANA e ONS), sem emitir previsão.

Serve para conferir emissões antigas e para a checagem leve da automação.
Uso: ``uv run python -m src.core.execute src.live.atualizar``.
"""

from __future__ import annotations

from ..core import storage
from ..core.contracts import observations
from . import ingest
from .run import INTERIM


def main() -> None:
    ana, ons = ingest.ana_recente(), ingest.ons_recente()
    observations(ana, "codigo")
    observations(ons, "usina")
    storage.parquet(ana, INTERIM / "ana_hourly.parquet")
    storage.parquet(ons, INTERIM / "ons_hourly.parquet")
    print(f"[atualizar] ANA até {ana.ts_utc.max()}, ONS até {ons.ts_utc.max()}", flush=True)


if __name__ == "__main__":
    main()
