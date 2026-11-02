from __future__ import annotations

import json
from pathlib import Path

from factorypulse_contracts import validate_event

from .simulator import PumpSimulator


def emit_jsonl(output: str | Path, count: int = 100, fault_after: int | None = None, seed: int = 7) -> dict[str, object]:
    """Validate each generated event before it crosses the ingestion boundary."""
    if count <= 0:
        raise ValueError("count must be positive")
    if fault_after is not None and not 0 <= fault_after < count:
        raise ValueError("fault_after must be within the generated event range")
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    simulator = PumpSimulator(seed=seed)
    normal = degraded = 0
    with destination.open("w", encoding="utf-8") as stream:
        for index in range(count):
            event = simulator.next_event(degraded=fault_after is not None and index >= fault_after)
            validate_event("telemetry.v1", event)
            stream.write(json.dumps(event, separators=(",", ":")) + "\n")
            if fault_after is not None and index >= fault_after:
                degraded += 1
            else:
                normal += 1
    return {"events": count, "normal_events": normal, "degraded_events": degraded, "output": str(destination)}
