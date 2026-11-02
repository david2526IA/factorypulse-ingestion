# FactoryPulse Ingestion

> A validated telemetry gateway simulator for the FactoryPulse multi-repository reference platform.

[![Ingestion CI](https://github.com/david2526IA/factorypulse-ingestion/actions/workflows/ci.yml/badge.svg)](https://github.com/david2526IA/factorypulse-ingestion/actions/workflows/ci.yml)
[![Contracts](https://img.shields.io/badge/uses-FactoryPulse%20Contracts-2563EB)](https://github.com/david2526IA/factorypulse-contracts)
[![JSONL](https://img.shields.io/badge/output-JSON%20Lines-0F766E)](https://jsonlines.org/)

FactoryPulse Ingestion is a deterministic simulator of an industrial telemetry gateway. It produces correlated pump measurements, can inject a controlled degradation episode and validates every event against the shared [`telemetry.v1`](https://github.com/david2526IA/factorypulse-contracts) contract before writing it to JSON Lines.

## Why it exists

An end-to-end platform needs a reliable source of events before it can demonstrate data quality, detection, storage and dashboards. A simulator makes integration repeatable without claiming to control real machinery or requiring inaccessible hardware.

## Flow

```text
Pump profile + seeded noise + optional degradation
                     │
                     ▼
        `telemetry.v1` contract validation
                     │
                     ▼
       JSON Lines event stream → lakehouse / broker adapter
```

## Quick start

```bash
git clone https://github.com/david2526IA/factorypulse-ingestion.git
cd factorypulse-ingestion
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -e ".[dev]"
factorypulse-ingestion --count 120 --fault-after 85 --output artifacts/telemetry.jsonl
pytest -q
```

The output is one valid JSON event per line. `--fault-after 85` begins a correlated episode: temperature, vibration and power rise while pressure falls. This is synthetic integration data, not a physical model or a safety system.

## Contract integration

The project depends directly on a pinned version of [FactoryPulse Contracts](https://github.com/david2526IA/factorypulse-contracts). Every event is validated before writing, so an incompatible event fails at the producer boundary rather than later in the platform. Pinning prevents an unreviewed future contract change from silently changing this producer's behaviour.

## Container run

```bash
docker build -t factorypulse-ingestion .
docker run --rm -v "${PWD}:/data" factorypulse-ingestion --count 20 --output /data/telemetry.jsonl
```

## Roadmap

- [ ] MQTT publisher adapter with delivery receipts
- [ ] OPC UA simulator adapter
- [ ] Multiple asset profiles and fault catalog
- [ ] Back-pressure and retry policy
- [ ] OpenTelemetry trace context

## License

MIT © 2026 David Falcon
