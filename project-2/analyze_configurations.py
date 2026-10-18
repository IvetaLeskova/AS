"""Enumerate optional-feature combinations and validate them against the model."""

import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path

from validator.validator import validate


def analyze(model: dict) -> tuple[dict, list[dict]]:
    """Keep mandatory features selected and check every optional combination."""
    configurations = []
    reason_counts = Counter()
    valid_count = 0

    for values in product((False, True), repeat=len(model["optional"])):
        configuration = dict.fromkeys(model["mandatory"], True)
        configuration.update(zip(model["optional"], values))
        valid, reasons = validate(model, configuration)
        valid_count += int(valid)
        reason_counts.update(reasons)
        configurations.append({
            "configuration": configuration,
            "valid": valid,
            "reasons": reasons,
        })

    total = len(configurations)
    invalid_count = total - valid_count
    summary = {
        "total_configurations": total,
        "valid_configurations": valid_count,
        "invalid_configurations": invalid_count,
        "rejected_percentage": 100 * invalid_count / total,
        "rejection_reasons": dict(reason_counts),
    }
    return summary, configurations


def main() -> int:
    project_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model", type=Path,
        default=project_dir / "feature-model" / "model.json",
    )
    parser.add_argument("--output-dir", type=Path, default=project_dir / "results")
    args = parser.parse_args()

    try:
        model = json.loads(args.model.read_text(encoding="utf-8"))
        summary, configurations = analyze(model)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for filename, data in (
            ("summary.json", summary),
            ("configurations.json", configurations),
        ):
            (args.output_dir / filename).write_text(
                json.dumps(data, indent=2) + "\n", encoding="utf-8"
            )
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Analysis error: {error}\n")

    print(json.dumps(summary, indent=2))
    print(f"Results saved to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
