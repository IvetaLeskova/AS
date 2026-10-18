import json
from pathlib import Path

import pytest

from validator.validator import validate


FEATURE_MODEL = Path(__file__).resolve().parents[1] / "feature-model"


@pytest.fixture
def model():
    return json.loads((FEATURE_MODEL / "model.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", ["basic", "student", "full"])
def test_valid_example(model, name):
    path = FEATURE_MODEL / "configurations" / f"{name}.json"
    configuration = json.loads(path.read_text(encoding="utf-8"))
    assert validate(model, configuration) == (True, [])


@pytest.mark.parametrize(
    ("configuration", "reasons"),
    [
        ({"Core": True, "Categories": True, "Statistics": True}, []),
        ({"Core": True, "Statistics": True}, ["Statistics requires Categories."]),
        ({"Core": True, "Categories": True, "Statistics": True, "Export": True}, []),
        ({"Core": True, "Categories": True, "Export": True},
         ["Export requires Statistics."]),
        ({}, ["Mandatory feature Core must be selected."]),
        ({"Core": False}, ["Mandatory feature Core must be selected."]),
        ({"Core": True, "Unknown": True}, ["Unknown feature: Unknown."]),
        ({"Core": True, "Priority": 1}, ["Feature Priority must have a boolean value."]),
    ],
)
def test_configuration_rules(model, configuration, reasons):
    assert validate(model, configuration) == (not reasons, reasons)


@pytest.mark.parametrize(
    ("name", "reason"),
    [
        ("statistics-without-categories", "Statistics requires Categories."),
        ("export-without-statistics", "Export requires Statistics."),
    ],
)
def test_invalid_example(model, name, reason):
    path = FEATURE_MODEL / "configurations" / "invalid" / f"{name}.json"
    configuration = json.loads(path.read_text(encoding="utf-8"))
    assert validate(model, configuration) == (False, [reason])


def test_feature_names_come_from_model():
    model = {
        "mandatory": ["Base"],
        "optional": ["Reports", "Labels"],
        "constraints": [
            {"type": "requires", "feature": "Reports", "requires": "Labels"}
        ],
    }
    assert validate(model, {"Base": True, "Reports": True}) == (
        False, ["Reports requires Labels."]
    )
