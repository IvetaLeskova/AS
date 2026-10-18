import json
from pathlib import Path

from analyze_configurations import analyze


def test_task_manager_experiment():
    model_path = Path(__file__).resolve().parents[1] / "feature-model" / "model.json"
    model = json.loads(model_path.read_text(encoding="utf-8"))
    summary, configurations = analyze(model)

    # Categories, Statistics, Export permit 000, 100, 110 and 111.
    # Priority and Deadlines independently multiply these four cases by four.
    assert summary == {
        "total_configurations": 32,
        "valid_configurations": 16,
        "invalid_configurations": 16,
        "rejected_percentage": 50.0,
        "rejection_reasons": {
            "Statistics requires Categories.": 8,
            "Export requires Statistics.": 8,
        },
    }
    assert len(configurations) == 32
    assert len({tuple(row["configuration"].items()) for row in configurations}) == 32
    assert all(row["configuration"]["Core"] is True for row in configurations)


def test_analysis_uses_model_features_and_handles_overlapping_reasons():
    model = {
        "mandatory": ["Base"],
        "optional": ["Reports", "Labels", "Storage"],
        "constraints": [
            {"type": "requires", "feature": "Reports", "requires": "Labels"},
            {"type": "requires", "feature": "Reports", "requires": "Storage"},
        ],
    }
    summary, configurations = analyze(model)
    assert summary["total_configurations"] == 8
    assert summary["valid_configurations"] == 5
    assert summary["invalid_configurations"] == 3
    assert summary["rejected_percentage"] == 37.5
    assert summary["rejection_reasons"] == {
        "Reports requires Labels.": 2,
        "Reports requires Storage.": 2,
    }
    assert any(len(row["reasons"]) == 2 for row in configurations)


def test_model_without_optional_features():
    summary, configurations = analyze({
        "mandatory": ["Base"], "optional": [], "constraints": [],
    })
    assert summary["total_configurations"] == 1
    assert summary["valid_configurations"] == 1
    assert summary["rejected_percentage"] == 0
    assert configurations == [
        {"configuration": {"Base": True}, "valid": True, "reasons": []}
    ]
