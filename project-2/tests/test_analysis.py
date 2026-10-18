import json
from copy import deepcopy
from pathlib import Path
import subprocess
import sys

from analyze_configurations import analyze, compare_scenarios


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


def test_scenario_comparison():
    model_path = Path(__file__).resolve().parents[1] / "feature-model" / "model.json"
    model = json.loads(model_path.read_text(encoding="utf-8"))
    original = deepcopy(model)
    scenarios = compare_scenarios(model)

    assert model == original
    assert [scenario["scenario"] for scenario in scenarios] == ["S0", "S1", "S2"]
    assert [scenario["active_constraints"] for scenario in scenarios] == [
        [], model["constraints"][:1], model["constraints"],
    ]
    assert [scenario["summary"]["valid_configurations"] for scenario in scenarios] == [32, 24, 16]
    assert [scenario["summary"]["invalid_configurations"] for scenario in scenarios] == [0, 8, 16]
    assert [scenario["summary"]["rejected_percentage"] for scenario in scenarios] == [0, 25, 50]
    assert [scenario["summary"]["rejection_reasons"] for scenario in scenarios] == [
        {}, {"Statistics requires Categories.": 8},
        {"Statistics requires Categories.": 8, "Export requires Statistics.": 8},
    ]

    candidates = [
        [row["configuration"] for row in scenario["configurations"]]
        for scenario in scenarios
    ]
    assert candidates[0] == candidates[1] == candidates[2]
    assert len(candidates[0]) == 32
    valid_sets = [
        {tuple(row["configuration"].items())
         for row in scenario["configurations"] if row["valid"]}
        for scenario in scenarios
    ]
    assert valid_sets[2] < valid_sets[1] < valid_sets[0]


def test_comparison_without_constraints():
    scenarios = compare_scenarios({
        "mandatory": ["Base"], "optional": ["Extra"], "constraints": [],
    })
    assert len(scenarios) == 1
    assert scenarios[0]["summary"]["valid_configurations"] == 2


def test_cli_writes_reproducible_results_without_changing_model(tmp_path):
    project_dir = Path(__file__).resolve().parents[1]
    model_path = project_dir / "feature-model" / "model.json"
    original_bytes = model_path.read_bytes()
    model = json.loads(original_bytes)
    command = [
        sys.executable, str(project_dir / "analyze_configurations.py"),
        "--model", str(model_path), "--output-dir", str(tmp_path / "results"),
    ]
    completed = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, check=True)
    assert "S2 | 32 | 16 | 16 | 50%" in completed.stdout
    output_dir = tmp_path / "results"
    expected_summary, expected_configurations = analyze(model)
    assert json.loads((output_dir / "summary.json").read_text()) == expected_summary
    assert json.loads((output_dir / "configurations.json").read_text()) == expected_configurations
    scenarios = compare_scenarios(model)
    for scenario in scenarios:
        path = output_dir / "scenarios" / f"{scenario['scenario']}.json"
        assert json.loads(path.read_text()) == scenario
    comparison = json.loads((output_dir / "comparison.json").read_text())
    assert comparison == [
        {key: value for key, value in scenario.items() if key != "configurations"}
        for scenario in scenarios
    ]
    first_run = {path.relative_to(output_dir): path.read_bytes()
                 for path in output_dir.rglob("*.json")}
    subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, check=True)
    assert {path.relative_to(output_dir): path.read_bytes()
            for path in output_dir.rglob("*.json")} == first_run
    assert model_path.read_bytes() == original_bytes
