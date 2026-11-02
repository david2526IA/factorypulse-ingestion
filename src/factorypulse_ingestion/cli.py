from __future__ import annotations

import argparse

from .pipeline import emit_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(prog="factorypulse-ingestion")
    parser.add_argument("--output", default="artifacts/telemetry.jsonl")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--fault-after", type=int)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    print(emit_jsonl(args.output, args.count, args.fault_after, args.seed))


if __name__ == "__main__":
    main()
