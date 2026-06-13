from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
PAPER = ROOT / "paper"

TOPOLOGIES = ["upper_arc", "lower_arc", "switching_arc"]
PATHS = [
    {"path": "lower", "topology": "lower_arc", "length": 4.8284},
    {"path": "upper", "topology": "upper_arc", "length": 4.8284},
    {"path": "switching", "topology": "switching_arc", "length": 6.0645},
]


def topology_distance(a: str, b: str) -> int:
    return 0 if a == b else 1


def noisy_target(target: str, trial: int, noise_rate: float, total_trials: int) -> str:
    if noise_rate <= 0:
        return target
    flips = int(round(noise_rate * total_trials))
    should_flip = ((trial * 37) % total_trials) < flips
    if not should_flip:
        return target
    idx = TOPOLOGIES.index(target)
    return TOPOLOGIES[(idx + 1) % len(TOPOLOGIES)]


def choose_path(selector: str, target: str, observed_target: str, lam: float) -> dict[str, object]:
    if selector == "smoothness_only":
        regularizer_target = None
    elif selector == "fixed_upper_topology":
        regularizer_target = "upper_arc"
    elif selector == "task_conditioned_topology":
        regularizer_target = observed_target
    else:
        raise ValueError(f"unknown selector: {selector}")

    scored = []
    for path in PATHS:
        penalty = 0 if regularizer_target is None else topology_distance(path["topology"], regularizer_target)
        scored.append((path["length"] + lam * penalty, path["length"], path["path"], path))
    _, _, _, best = min(scored)
    return {
        "target_topology": target,
        "observed_topology": observed_target,
        "chosen_path": best["path"],
        "chosen_topology": best["topology"],
        "length": best["length"],
        "success": int(best["topology"] == target),
        "switch_task": int(target == "switching_arc"),
    }


def evaluate(selector: str, lam: float, label_noise: float, trials_per_target: int = 100):
    total_trials = trials_per_target * len(TOPOLOGIES)
    rows = []
    trial = 0
    for target in TOPOLOGIES:
        for _ in range(trials_per_target):
            observed = noisy_target(target, trial, label_noise, total_trials)
            rows.append(choose_path(selector, target, observed, lam))
            trial += 1

    switch_rows = [row for row in rows if row["switch_task"]]
    return {
        "selector": selector,
        "lambda_topology": lam,
        "label_noise": label_noise,
        "trials": len(rows),
        "success_rate": sum(row["success"] for row in rows) / len(rows),
        "switch_success_rate": sum(row["success"] for row in switch_rows) / len(switch_rows),
        "mean_length": sum(float(row["length"]) for row in rows) / len(rows),
        "wrong_topology_rate": 1.0 - (sum(row["success"] for row in rows) / len(rows)),
    }


def write_outputs(summary_rows):
    csv_path = DOCS / "v2_topology_switch_stress.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "selector",
                "lambda_topology",
                "label_noise",
                "trials",
                "success_rate",
                "switch_success_rate",
                "mean_length",
                "wrong_topology_rate",
            ],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    payload = {
        "path_classes": PATHS,
        "task_topologies": TOPOLOGIES,
        "summary": summary_rows,
        "interpretation": (
            "Topology regularization helps only when it is task-conditioned and weighted strongly enough "
            "to pay the extra path length for necessary topology switches. A fixed-topology penalty "
            "over-regularizes and fails switching tasks."
        ),
    }
    (DOCS / "v2_topology_switch_stress.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    selected = [
        row
        for row in summary_rows
        if (
            (row["selector"] == "smoothness_only" and row["lambda_topology"] == 0.0)
            or (row["selector"] == "fixed_upper_topology" and row["lambda_topology"] == 1.25)
            or (row["selector"] == "task_conditioned_topology" and row["lambda_topology"] in {1.00, 1.25} and row["label_noise"] == 0.0)
            or (row["selector"] == "task_conditioned_topology" and row["lambda_topology"] == 1.25 and row["label_noise"] == 0.20)
        )
    ]
    labels = {
        "smoothness_only": "smoothness only",
        "fixed_upper_topology": "fixed upper",
        "task_conditioned_topology": "task-conditioned",
    }
    table_lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Selector & $\lambda_{\rm top}$ & Noise & Success & Switch succ. \\",
        r"\midrule",
    ]
    for row in selected:
        table_lines.append(
            f"{labels[row['selector']]} & {row['lambda_topology']:.2f} & "
            f"{row['label_noise']:.2f} & {row['success_rate']:.3f} & "
            f"{row['switch_success_rate']:.3f} \\\\"
        )
    table_lines.extend([r"\bottomrule", r"\end{tabular}"])
    (PAPER / "v2_topology_switch_table.tex").write_text("\n".join(table_lines) + "\n", encoding="utf-8")


def main() -> None:
    configs = [
        ("smoothness_only", 0.0, 0.0),
        ("fixed_upper_topology", 1.25, 0.0),
        ("task_conditioned_topology", 0.50, 0.0),
        ("task_conditioned_topology", 1.00, 0.0),
        ("task_conditioned_topology", 1.25, 0.0),
        ("task_conditioned_topology", 2.00, 0.0),
        ("task_conditioned_topology", 1.25, 0.10),
        ("task_conditioned_topology", 1.25, 0.20),
        ("task_conditioned_topology", 1.25, 0.40),
    ]
    summary_rows = [evaluate(*config) for config in configs]
    write_outputs(summary_rows)
    key = next(
        row
        for row in summary_rows
        if row["selector"] == "task_conditioned_topology"
        and row["lambda_topology"] == 1.25
        and row["label_noise"] == 0.0
    )
    noisy = next(
        row
        for row in summary_rows
        if row["selector"] == "task_conditioned_topology"
        and row["lambda_topology"] == 1.25
        and row["label_noise"] == 0.20
    )
    print(
        "task_conditioned_lambda_1.25_success="
        f"{key['success_rate']:.3f} "
        "label_noise_0.20_success="
        f"{noisy['success_rate']:.3f}"
    )


if __name__ == "__main__":
    main()
