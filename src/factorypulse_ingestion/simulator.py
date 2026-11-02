"""Deterministic asset simulator for integration, not physical process modelling."""

from __future__ import annotations

import random
import uuid
from datetime import datetime, timedelta, timezone


class PumpSimulator:
    def __init__(self, asset_id: str = "PUMP-01", seed: int = 7, start: datetime | None = None) -> None:
        self.asset_id = asset_id
        self.random = random.Random(seed)
        self.current = start or datetime(2026, 1, 1, tzinfo=timezone.utc)

    def next_event(self, degraded: bool = False) -> dict[str, object]:
        """Generate one contract-shaped reading; degradation affects correlated signals."""
        load = 1.0 if degraded else 0.0
        event = {
            "event_id": str(uuid.UUID(int=self.random.getrandbits(128))),
            "event_type": "factorypulse.telemetry",
            "schema_version": "1.0",
            "occurred_at": self.current.isoformat().replace("+00:00", "Z"),
            "asset_id": self.asset_id,
            "measurements": {
                "temperature_c": round(62 + load * 27 + self.random.gauss(0, 0.8), 3),
                "vibration_mm_s": round(2.6 + load * 9.5 + self.random.gauss(0, 0.15), 3),
                "pressure_bar": round(7.4 - load * 2.0 + self.random.gauss(0, 0.08), 3),
                "power_kw": round(18 + load * 5.8 + self.random.gauss(0, 0.25), 3),
            },
            "source": "factorypulse-ingestion/simulator",
        }
        self.current += timedelta(seconds=15)
        return event
