import json

from factorypulse_contracts import validate_event

from factorypulse_ingestion.pipeline import emit_jsonl
from factorypulse_ingestion.simulator import PumpSimulator


def test_simulator_emits_valid_contract_event() -> None:
    event = PumpSimulator(seed=1).next_event()
    validate_event("telemetry.v1", event)
    assert event["asset_id"] == "PUMP-01"


def test_pipeline_writes_valid_jsonl_with_fault_episode(tmp_path) -> None:
    target = tmp_path / "telemetry.jsonl"
    summary = emit_jsonl(target, count=8, fault_after=5, seed=1)
    events = [json.loads(line) for line in target.read_text(encoding="utf-8").splitlines()]
    assert summary["normal_events"] == 5
    assert summary["degraded_events"] == 3
    assert len(events) == 8
    assert events[5]["measurements"]["vibration_mm_s"] > events[0]["measurements"]["vibration_mm_s"]
    for event in events:
        validate_event("telemetry.v1", event)
