"""Validate JSON configurations using a feature model's declarations."""

import argparse
import json
from pathlib import Path


def validate(model: dict, configuration: dict) -> tuple[bool, list[str]]:
    """Return validity and reasons; omitted features are treated as unselected.

    The model must declare mandatory and optional features and requires rules.
    Unsupported rule types raise ValueError instead of being silently ignored.
    """
    if not isinstance(configuration, dict):
        return False, ["Configuration must be a JSON object."]

    reasons = []
    known_features = set(model["mandatory"]) | set(model["optional"])

    for feature, selected in configuration.items():
        if feature not in known_features:
            reasons.append(f"Unknown feature: {feature}.")
        if not isinstance(selected, bool):
            reasons.append(f"Feature {feature} must have a boolean value.")

    for feature in model["mandatory"]:
        if configuration.get(feature) is not True:
            reasons.append(f"Mandatory feature {feature} must be selected.")

    for constraint in model["constraints"]:
        if constraint["type"] != "requires":
            raise ValueError(f"Unsupported constraint type: {constraint['type']}.")
        feature = constraint["feature"]
        required = constraint["requires"]
        if feature not in known_features or required not in known_features:
            raise ValueError("Constraint references an undeclared feature.")
        if (configuration.get(feature) is True
                and configuration.get(required) is not True):
            reasons.append(f"{feature} requires {required}.")

    return not reasons, reasons


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("configuration", type=Path, help="Configuration JSON file")
    parser.add_argument(
        "--model", type=Path,
        default=Path(__file__).resolve().parents[1] / "feature-model" / "model.json",
        help="Feature-model JSON file (defaults to the project's model)",
    )
    args = parser.parse_args()
    try:
        model = json.loads(args.model.read_text(encoding="utf-8"))
        configuration = json.loads(args.configuration.read_text(encoding="utf-8"))
        valid, reasons = validate(model, configuration)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Input error: {error}\n")

    print("VALID" if valid else "INVALID")
    for reason in reasons:
        print(reason)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
