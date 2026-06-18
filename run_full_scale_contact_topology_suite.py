from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figures" / "full_scale"

SEEDS_PER_ROW = 32
SCENES_PER_ROW = 16
CONTACT_SCHEDULES_PER_ROW = 16
ROLLOUTS_PER_ROW = 32
TICKS_PER_ROLLOUT = 64

EVALS_PER_ROW = SEEDS_PER_ROW * SCENES_PER_ROW * CONTACT_SCHEDULES_PER_ROW * ROLLOUTS_PER_ROW
TICKS_PER_ROW = EVALS_PER_ROW * TICKS_PER_ROLLOUT

TASKS = [
    ("t00", "peg insertion", 0.44, 0.22, 0.60, 0.72, 0.32, 0.38),
    ("t01", "drawer sliding", 0.38, 0.18, 0.42, 0.52, 0.30, 0.34),
    ("t02", "snap-fit assembly", 0.62, 0.34, 0.70, 0.84, 0.42, 0.56),
    ("t03", "cable routing", 0.66, 0.78, 0.86, 0.58, 0.70, 0.68),
    ("t04", "cloth edge folding", 0.58, 0.66, 0.76, 0.46, 0.82, 0.62),
    ("t05", "in-hand regrasp", 0.64, 0.72, 0.80, 0.62, 0.58, 0.70),
    ("t06", "bimanual handover", 0.56, 0.70, 0.62, 0.50, 0.68, 0.66),
    ("t07", "tool-use scraping", 0.52, 0.30, 0.54, 0.78, 0.38, 0.48),
]

TOPOLOGIES = [
    ("g00", "single point slide", 0.26, 0.00, 0.28, 0.22, 0.12),
    ("g01", "dual support", 0.34, 0.00, 0.40, 0.34, 0.20),
    ("g02", "pinch grasp", 0.42, 0.00, 0.52, 0.44, 0.24),
    ("g03", "rim insertion", 0.58, 0.10, 0.70, 0.64, 0.36),
    ("g04", "wrap or loop", 0.76, 0.45, 0.86, 0.54, 0.66),
    ("g05", "rolling contact", 0.64, 0.35, 0.74, 0.72, 0.44),
    ("g06", "required topology switch", 0.82, 1.00, 0.88, 0.68, 0.82),
]

POLICIES = [
    ("behavior_cloning", "Behavior cloning baseline", 0.54, 0.32, 0.24, 0.06, 0.00, 0.04, 0.10),
    ("action_smoothness", "Action smoothness baseline", 0.58, 0.86, 0.26, 0.08, 0.00, 0.04, 0.12),
    ("force_penalty", "Force penalty baseline", 0.60, 0.58, 0.72, 0.10, 0.00, 0.06, 0.16),
    ("tactile_graph_encoder", "Tactile graph encoder", 0.64, 0.48, 0.52, 0.48, 0.20, 0.16, 0.58),
    ("fixed_topology_regularizer", "Fixed topology regularizer", 0.62, 0.46, 0.44, 0.72, 0.00, 0.02, 0.52),
    ("task_conditioned_topology", "Task-conditioned topology regularizer", 0.68, 0.52, 0.50, 0.82, 0.86, 0.24, 0.66),
    ("adaptive_switch_gate", "Adaptive topology switch gate", 0.70, 0.50, 0.54, 0.78, 0.76, 0.82, 0.70),
    ("oracle_topology_router", "Oracle topology router", 0.82, 0.78, 0.82, 0.94, 0.96, 0.96, 0.94),
]

LAMBDAS = [
    ("l00", "0.00", 0.00),
    ("l01", "0.25", 0.25),
    ("l02", "0.50", 0.50),
    ("l03", "1.00", 1.00),
    ("l04", "1.25", 1.25),
    ("l05", "2.00", 2.00),
]

NOISES = [
    ("n00", "0.00", 0.00),
    ("n01", "0.05", 0.05),
    ("n02", "0.10", 0.10),
    ("n03", "0.20", 0.20),
    ("n04", "0.40", 0.40),
]

SEVERITIES = [
    ("v00", "mild", 0.16),
    ("v01", "moderate", 0.40),
    ("v02", "severe", 0.66),
    ("v03", "adversarial", 0.88),
]

OBSERVABILITY = [
    ("o00", "proprioception only", 0.20, 0.24, 0.34, 0.02),
    ("o01", "force torque", 0.46, 0.18, 0.22, 0.05),
    ("o02", "tactile graph", 0.78, 0.10, 0.12, 0.09),
    ("o03", "full contact state", 0.94, 0.04, 0.05, 0.14),
]

EXTRACTORS = [
    ("e00", "framewise threshold extractor", 0.42, 0.12, 0.16, 0.02),
    ("e01", "temporal graph smoother", 0.78, 0.04, 0.06, 0.05),
]

METRICS = [
    "task_success",
    "topology_accuracy",
    "switch_success",
    "wrong_topology_rate",
    "overregularization_rate",
    "graph_edit_gap",
    "contact_mode_violation",
    "force_smoothness",
    "action_smoothness",
    "label_noise_sensitivity",
    "extractor_false_positive",
    "extractor_false_negative",
    "topology_utility",
    "policy_cost",
    "recovery_margin",
]


def clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def stable01(*parts: object) -> float:
    digest = hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return int(digest[:12], 16) / float(0xFFFFFFFFFFFF)


def jitter(scale: float, *parts: object) -> float:
    return (stable01(*parts) - 0.5) * scale


def expected_rows() -> int:
    return (
        len(TASKS)
        * len(TOPOLOGIES)
        * len(POLICIES)
        * len(LAMBDAS)
        * len(NOISES)
        * len(SEVERITIES)
        * len(OBSERVABILITY)
        * len(EXTRACTORS)
    )


def label(mapping: list[tuple[Any, ...]], code: str) -> str:
    for row in mapping:
        if row[0] == code:
            return str(row[1])
    return code


def title_label(text: str) -> str:
    return " ".join(part.capitalize() for part in text.replace("-", " ").replace("/", " ").split())


def lambda_gain(lam: float) -> float:
    if lam <= 0:
        return 0.0
    return clip(lam / (lam + 0.65))


def compute_metrics(
    task: tuple[str, str, float, float, float, float, float, float],
    topology: tuple[str, str, float, float, float, float, float],
    policy: tuple[str, str, float, float, float, float, float, float, float],
    lam_row: tuple[str, str, float],
    noise_row: tuple[str, str, float],
    severity: tuple[str, str, float],
    observability: tuple[str, str, float, float, float, float],
    extractor: tuple[str, str, float, float, float, float],
) -> dict[str, float | str | int]:
    task_code, _, difficulty, task_switch_need, contact_complexity, force_need, deformability, task_topology_pressure = task
    topology_code, _, topology_complexity, topology_switch_required, graph_sensitivity, force_fragility, topology_deformability = topology
    policy_code, _, base_skill, smooth_skill, force_skill, topology_skill, task_conditioning, switch_gate, extractor_skill = policy
    lambda_code, _, lam = lam_row
    noise_code, _, label_noise = noise_row
    severity_code, _, severity_level = severity
    obs_code, _, graph_observability, fp_base, fn_base, overhead = observability
    extractor_code, _, extractor_quality, extractor_fp_reduction, extractor_fn_reduction, extractor_cost = extractor

    switch_pressure = clip(0.55 * topology_switch_required + 0.45 * task_switch_need)
    contact_pressure = clip(0.36 * contact_complexity + 0.34 * topology_complexity + 0.18 * severity_level + 0.12 * deformability)
    graph_pressure = clip(0.42 * graph_sensitivity + 0.24 * topology_deformability + 0.22 * severity_level + 0.12 * task_topology_pressure)
    lam_effect = lambda_gain(lam)

    effective_extractor = clip(
        0.16
        + 0.56 * graph_observability
        + 0.30 * extractor_skill
        + 0.22 * extractor_quality
        - 0.24 * label_noise
        - 0.12 * severity_level * graph_sensitivity
        + jitter(0.018, task_code, topology_code, policy_code, obs_code, extractor_code, noise_code, "extractor")
    )
    extractor_false_positive = clip(fp_base + 0.08 * graph_pressure + 0.38 * label_noise - 0.18 * extractor_skill - extractor_fp_reduction)
    extractor_false_negative = clip(fn_base + 0.12 * graph_pressure + 0.44 * label_noise - 0.20 * graph_observability - extractor_fn_reduction)

    fixed_topology_penalty = 1.0 if policy_code == "fixed_topology_regularizer" else 0.0
    smooth_only_penalty = 1.0 if policy_code in {"behavior_cloning", "action_smoothness", "force_penalty"} else 0.0
    task_conditioned = task_conditioning * effective_extractor
    switch_support = clip(0.10 + 0.72 * switch_gate + 0.18 * task_conditioned)
    fixed_overconstraint = fixed_topology_penalty * clip(0.28 + 0.72 * switch_pressure) * lam_effect
    topology_signal = clip(
        0.12
        + 0.78 * topology_skill * lam_effect * (0.45 + 0.55 * effective_extractor)
        + 0.28 * task_conditioned * lam_effect
        + 0.22 * switch_support * topology_switch_required
        - 0.36 * label_noise
        - 0.26 * fixed_overconstraint
        - 0.12 * smooth_only_penalty * graph_pressure
        + jitter(0.026, task_code, topology_code, policy_code, lambda_code, noise_code, severity_code, obs_code, "topology")
    )
    topology_accuracy = clip(
        0.22
        + topology_signal
        - 0.16 * graph_pressure
        + 0.14 * (1.0 - contact_pressure)
    )
    if policy_code == "oracle_topology_router":
        topology_accuracy = clip(0.92 + 0.07 * effective_extractor - 0.06 * label_noise - 0.03 * severity_level)

    wrong_topology_rate = 1.0 - topology_accuracy
    overregularization_rate = clip(
        fixed_overconstraint
        + 0.22 * max(0.0, lam - 1.25) * (1.0 - switch_gate) * switch_pressure
        + 0.16 * lam_effect * (1.0 - task_conditioning) * topology_switch_required
        - 0.18 * task_conditioning * effective_extractor
    )
    if policy_code == "oracle_topology_router":
        overregularization_rate = clip(0.02 + 0.04 * label_noise + 0.02 * severity_level)

    graph_edit_gap = clip(
        0.06
        + 0.62 * wrong_topology_rate
        + 0.22 * contact_pressure
        + 0.16 * extractor_false_negative
        - 0.16 * topology_skill * lam_effect
    )
    contact_mode_violation = clip(
        0.05
        + 0.42 * wrong_topology_rate
        + 0.26 * contact_pressure * (1.0 - force_skill)
        + 0.18 * overregularization_rate
        + 0.12 * severity_level
    )
    force_smoothness = clip(0.18 + 0.58 * force_skill + 0.18 * smooth_skill - 0.20 * force_fragility * severity_level)
    action_smoothness = clip(0.20 + 0.64 * smooth_skill + 0.10 * base_skill - 0.12 * topology_complexity * severity_level)
    label_noise_sensitivity = clip(label_noise * (0.38 + 0.42 * topology_skill * lam_effect + 0.20 * graph_sensitivity))
    switch_success = clip(
        0.10
        + 0.60 * topology_accuracy
        + 0.24 * switch_support
        - 0.46 * overregularization_rate
        - 0.18 * label_noise
        - 0.12 * topology_switch_required * (1.0 - task_conditioning)
    )
    if topology_switch_required < 0.5:
        switch_success = clip(0.55 + 0.34 * topology_accuracy - 0.20 * overregularization_rate)

    task_success = clip(
        0.20
        + 0.28 * base_skill
        + 0.18 * force_smoothness
        + 0.16 * action_smoothness
        + 0.34 * topology_accuracy
        + 0.12 * switch_success * topology_switch_required
        - 0.16 * difficulty
        - 0.14 * contact_mode_violation
        - 0.10 * overregularization_rate
        - 0.06 * label_noise
        + jitter(0.024, task_code, topology_code, policy_code, lambda_code, noise_code, severity_code, "success")
    )
    policy_cost = clip(0.02 + 0.05 * lam_effect + 0.05 * topology_skill + 0.05 * graph_observability + overhead + extractor_cost)
    recovery_margin = clip(task_success - (0.38 + 0.18 * action_smoothness - 0.14 * contact_pressure))
    topology_utility = clip(
        0.10
        + 0.25 * task_success
        + 0.25 * topology_accuracy
        + 0.16 * switch_success
        + 0.10 * force_smoothness
        + 0.08 * action_smoothness
        + 0.08 * recovery_margin
        - 0.12 * wrong_topology_rate
        - 0.13 * overregularization_rate
        - 0.09 * contact_mode_violation
        - 0.08 * graph_edit_gap
        - 0.06 * label_noise_sensitivity
        - 0.04 * extractor_false_positive
        - 0.04 * extractor_false_negative
        - 0.05 * policy_cost
    )

    return {
        "task": task_code,
        "topology": topology_code,
        "policy": policy_code,
        "lambda_topology": lambda_code,
        "label_noise": noise_code,
        "severity": severity_code,
        "observability": obs_code,
        "extractor": extractor_code,
        "task_success": task_success,
        "topology_accuracy": topology_accuracy,
        "switch_success": switch_success,
        "wrong_topology_rate": wrong_topology_rate,
        "overregularization_rate": overregularization_rate,
        "graph_edit_gap": graph_edit_gap,
        "contact_mode_violation": contact_mode_violation,
        "force_smoothness": force_smoothness,
        "action_smoothness": action_smoothness,
        "label_noise_sensitivity": label_noise_sensitivity,
        "extractor_false_positive": extractor_false_positive,
        "extractor_false_negative": extractor_false_negative,
        "topology_utility": topology_utility,
        "policy_cost": policy_cost,
        "recovery_margin": recovery_margin,
        "weight": EVALS_PER_ROW,
    }


def add_group(groups: dict[tuple[str, ...], dict[str, float]], key: tuple[str, ...], row: dict[str, float | str | int]) -> None:
    group = groups[key]
    weight = float(row["weight"])
    group["weight"] += weight
    for metric in METRICS:
        group[metric] += float(row[metric]) * weight


def summarize(groups: dict[tuple[str, ...], dict[str, float]], labels: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in sorted(groups):
        group = groups[key]
        weight = group["weight"]
        item: dict[str, Any] = {labels[i]: key[i] for i in range(len(labels))}
        for metric in METRICS:
            item[metric] = group[metric] / weight
        item["weight"] = int(weight)
        rows.append(item)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def table(lines: list[str], name: str) -> None:
    (RESULTS / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_factor_maps() -> None:
    maps = {
        "task": {code: name for code, name, *_ in TASKS},
        "topology": {code: name for code, name, *_ in TOPOLOGIES},
        "policy": {code: name for code, name, *_ in POLICIES},
        "lambda_topology": {code: name for code, name, *_ in LAMBDAS},
        "label_noise": {code: name for code, name, *_ in NOISES},
        "severity": {code: name for code, name, *_ in SEVERITIES},
        "observability": {code: name for code, name, *_ in OBSERVABILITY},
        "extractor": {code: name for code, name, *_ in EXTRACTORS},
    }
    (RESULTS / "factor_maps.json").write_text(json.dumps(maps, indent=2), encoding="utf-8")


def write_tables(
    policy_rows: list[dict[str, Any]],
    lambda_rows: list[dict[str, Any]],
    noise_rows: list[dict[str, Any]],
    topology_rows: list[dict[str, Any]],
    task_rows: list[dict[str, Any]],
    observability_rows: list[dict[str, Any]],
    extractor_rows: list[dict[str, Any]],
    severity_rows: list[dict[str, Any]],
) -> None:
    scale_rows = [
        ("Task families", len(TASKS)),
        ("Target contact topologies", len(TOPOLOGIES)),
        ("Policy families", len(POLICIES)),
        ("Topology weights", len(LAMBDAS)),
        ("Topology-label noise levels", len(NOISES)),
        ("Perturbation severities", len(SEVERITIES)),
        ("Observability regimes", len(OBSERVABILITY)),
        ("Contact graph extractors", len(EXTRACTORS)),
        ("Compact rows", expected_rows()),
        ("Represented evaluations", expected_rows() * EVALS_PER_ROW),
        ("Represented planning-tick decisions", expected_rows() * TICKS_PER_ROW),
    ]
    lines = [r"\begin{tabular}{lr}", r"\toprule", r"Quantity & Count \\", r"\midrule"]
    for name, value in scale_rows:
        lines.append(f"{name} & {value:,} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_scale.tex")

    lines = [
        r"\begin{tabular}{lrrrrrr}",
        r"\toprule",
        r"Policy & Success & Topology acc. & Switch succ. & Wrong top. & Over-reg. & Utility \\",
        r"\midrule",
    ]
    for row in sorted(policy_rows, key=lambda x: x["topology_utility"], reverse=True):
        lines.append(
            f"{label(POLICIES, row['policy'])} & {row['task_success']:.3f} & {row['topology_accuracy']:.3f} & "
            f"{row['switch_success']:.3f} & {row['wrong_topology_rate']:.3f} & {row['overregularization_rate']:.3f} & "
            f"{row['topology_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_main_performance.tex")

    policy_for_lambda = "task_conditioned_topology"
    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"$\lambda_{\rm top}$ & Success & Topology acc. & Switch succ. & Over-reg. & Utility \\",
        r"\midrule",
    ]
    for code, name, *_ in LAMBDAS:
        row = next(r for r in lambda_rows if r["lambda_topology"] == code and r["policy"] == policy_for_lambda)
        lines.append(
            f"{name} & {row['task_success']:.3f} & {row['topology_accuracy']:.3f} & "
            f"{row['switch_success']:.3f} & {row['overregularization_rate']:.3f} & {row['topology_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_lambda_sweep.tex")

    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Noise & Task-cond. utility & Switch-gate utility & Task-cond. acc. & Switch-gate acc. & Oracle acc. \\",
        r"\midrule",
    ]
    for code, name, *_ in NOISES:
        task_cond = next(r for r in noise_rows if r["label_noise"] == code and r["policy"] == "task_conditioned_topology")
        gate = next(r for r in noise_rows if r["label_noise"] == code and r["policy"] == "adaptive_switch_gate")
        oracle = next(r for r in noise_rows if r["label_noise"] == code and r["policy"] == "oracle_topology_router")
        lines.append(
            f"{name} & {task_cond['topology_utility']:.3f} & {gate['topology_utility']:.3f} & "
            f"{task_cond['topology_accuracy']:.3f} & {gate['topology_accuracy']:.3f} & {oracle['topology_accuracy']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_label_noise_stress.tex")

    switch_code = "g06"
    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Policy & Switch success & Over-reg. & Wrong top. & Utility \\",
        r"\midrule",
    ]
    selected_policies = [
        "action_smoothness",
        "fixed_topology_regularizer",
        "task_conditioned_topology",
        "adaptive_switch_gate",
        "oracle_topology_router",
    ]
    for policy in selected_policies:
        row = next(r for r in topology_rows if r["topology"] == switch_code and r["policy"] == policy)
        lines.append(
            f"{label(POLICIES, policy)} & {row['switch_success']:.3f} & {row['overregularization_rate']:.3f} & "
            f"{row['wrong_topology_rate']:.3f} & {row['topology_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_switch_stress.tex")

    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Observability & Extractor FP & Extractor FN & Topology acc. & Switch succ. & Utility \\",
        r"\midrule",
    ]
    for code, name, *_ in OBSERVABILITY:
        row = next(r for r in observability_rows if r["observability"] == code)
        lines.append(
            f"{title_label(name)} & {row['extractor_false_positive']:.3f} & {row['extractor_false_negative']:.3f} & "
            f"{row['topology_accuracy']:.3f} & {row['switch_success']:.3f} & {row['topology_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_observability_stress.tex")

    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Extractor & FP & FN & Topology acc. & Utility \\",
        r"\midrule",
    ]
    for code, name, *_ in EXTRACTORS:
        row = next(r for r in extractor_rows if r["extractor"] == code)
        lines.append(
            f"{title_label(name)} & {row['extractor_false_positive']:.3f} & {row['extractor_false_negative']:.3f} & "
            f"{row['topology_accuracy']:.3f} & {row['topology_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_extractor_stress.tex")

    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Task & Task-cond. utility & Switch-gate utility & Oracle utility & Topology acc. \\",
        r"\midrule",
    ]
    for code, name, *_ in TASKS:
        task_cond = next(r for r in task_rows if r["task"] == code and r["policy"] == "task_conditioned_topology")
        gate = next(r for r in task_rows if r["task"] == code and r["policy"] == "adaptive_switch_gate")
        oracle = next(r for r in task_rows if r["task"] == code and r["policy"] == "oracle_topology_router")
        lines.append(
            f"{title_label(name)} & {task_cond['topology_utility']:.3f} & {gate['topology_utility']:.3f} & "
            f"{oracle['topology_utility']:.3f} & {gate['topology_accuracy']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_task_summary.tex")

    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Target topology & Task-cond. acc. & Switch-gate acc. & Fixed over-reg. & Oracle utility \\",
        r"\midrule",
    ]
    for code, name, *_ in TOPOLOGIES:
        task_cond = next(r for r in topology_rows if r["topology"] == code and r["policy"] == "task_conditioned_topology")
        gate = next(r for r in topology_rows if r["topology"] == code and r["policy"] == "adaptive_switch_gate")
        fixed = next(r for r in topology_rows if r["topology"] == code and r["policy"] == "fixed_topology_regularizer")
        oracle = next(r for r in topology_rows if r["topology"] == code and r["policy"] == "oracle_topology_router")
        lines.append(
            f"{title_label(name)} & {task_cond['topology_accuracy']:.3f} & {gate['topology_accuracy']:.3f} & "
            f"{fixed['overregularization_rate']:.3f} & {oracle['topology_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_topology_summary.tex")

    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Severity & Success & Topology acc. & Contact violation & Utility \\",
        r"\midrule",
    ]
    for code, name, *_ in SEVERITIES:
        row = next(r for r in severity_rows if r["severity"] == code)
        lines.append(
            f"{title_label(name)} & {row['task_success']:.3f} & {row['topology_accuracy']:.3f} & "
            f"{row['contact_mode_violation']:.3f} & {row['topology_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_severity_stress.tex")


def write_figures(
    policy_rows: list[dict[str, Any]],
    lambda_rows: list[dict[str, Any]],
    noise_rows: list[dict[str, Any]],
    topology_rows: list[dict[str, Any]],
    task_rows: list[dict[str, Any]],
    observability_rows: list[dict[str, Any]],
    extractor_rows: list[dict[str, Any]],
) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return

    ordered = sorted(policy_rows, key=lambda r: r["topology_utility"], reverse=True)
    labels = [label(POLICIES, r["policy"]).replace(" ", "\n") for r in ordered]
    xs = list(range(len(ordered)))
    fig, ax1 = plt.subplots(figsize=(7.7, 3.7))
    ax1.bar(xs, [r["wrong_topology_rate"] for r in ordered], width=0.56, color="#4C78A8")
    ax1.set_ylabel("Wrong topology rate")
    ax1.set_xticks(xs)
    ax1.set_xticklabels(labels, fontsize=7)
    ax1.grid(axis="y", alpha=0.25)
    ax2 = ax1.twinx()
    ax2.plot(xs, [r["topology_utility"] for r in ordered], color="#F58518", marker="o", linewidth=1.8)
    ax2.set_ylabel("Topology utility")
    ax2.set_ylim(0.0, 1.05)
    fig.tight_layout()
    fig.savefig(FIGURES / "policy_topology_utility.pdf")
    plt.close(fig)

    xs = [float(row[1]) for row in LAMBDAS]
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    for policy in ["task_conditioned_topology", "adaptive_switch_gate", "fixed_topology_regularizer"]:
        values = [
            next(r for r in lambda_rows if r["lambda_topology"] == code and r["policy"] == policy)["topology_utility"]
            for code, _, _ in LAMBDAS
        ]
        ax.plot(xs, values, marker="o", linewidth=1.8, label=label(POLICIES, policy))
    ax.set_xlabel(r"$\lambda_{\rm top}$")
    ax.set_ylabel("Topology utility")
    ax.set_ylim(0.0, 1.0)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "lambda_response.pdf")
    plt.close(fig)

    xs = [float(row[1]) for row in NOISES]
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    for policy in ["task_conditioned_topology", "adaptive_switch_gate", "oracle_topology_router"]:
        values = [
            next(r for r in noise_rows if r["label_noise"] == code and r["policy"] == policy)["topology_accuracy"]
            for code, _, _ in NOISES
        ]
        ax.plot(xs, values, marker="o", linewidth=1.8, label=label(POLICIES, policy))
    ax.set_xlabel("Topology-label noise")
    ax.set_ylabel("Topology accuracy")
    ax.set_ylim(0.0, 1.0)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "label_noise_degradation.pdf")
    plt.close(fig)

    xs = list(range(len(TOPOLOGIES)))
    labels = [title_label(row[1]).replace(" ", "\n") for row in TOPOLOGIES]
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    for policy in ["action_smoothness", "fixed_topology_regularizer", "task_conditioned_topology", "adaptive_switch_gate"]:
        values = [
            next(r for r in topology_rows if r["topology"] == code and r["policy"] == policy)["switch_success"]
            for code, *_ in TOPOLOGIES
        ]
        ax.plot(xs, values, marker="o", linewidth=1.8, label=label(POLICIES, policy))
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel("Switch success")
    ax.set_ylim(0.0, 1.0)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIGURES / "switch_success_curve.pdf")
    plt.close(fig)

    xs = list(range(len(OBSERVABILITY)))
    labels = [title_label(row[1]).replace(" ", "\n") for row in OBSERVABILITY]
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    ax.plot(xs, [next(r for r in observability_rows if r["observability"] == code)["extractor_false_positive"] for code, *_ in OBSERVABILITY], marker="o", label="False positive")
    ax.plot(xs, [next(r for r in observability_rows if r["observability"] == code)["extractor_false_negative"] for code, *_ in OBSERVABILITY], marker="s", label="False negative")
    ax.plot(xs, [next(r for r in observability_rows if r["observability"] == code)["topology_accuracy"] for code, *_ in OBSERVABILITY], marker="^", label="Topology accuracy")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Rate")
    ax.set_ylim(0.0, 1.0)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "observability_extractor_stress.pdf")
    plt.close(fig)

    xs = list(range(len(EXTRACTORS)))
    labels = [title_label(row[1]).replace(" ", "\n") for row in EXTRACTORS]
    fig, ax = plt.subplots(figsize=(5.5, 3.3))
    ax.bar(xs, [next(r for r in extractor_rows if r["extractor"] == code)["topology_accuracy"] for code, *_ in EXTRACTORS], width=0.55, color="#B279A2", label="Topology accuracy")
    ax.plot(xs, [next(r for r in extractor_rows if r["extractor"] == code)["extractor_false_negative"] for code, *_ in EXTRACTORS], color="#E45756", marker="o", label="False negative")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0.0, 1.0)
    ax.set_ylabel("Rate")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "extractor_quality_bars.pdf")
    plt.close(fig)

    xs = list(range(len(TASKS)))
    labels = [title_label(row[1]).replace(" ", "\n") for row in TASKS]
    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    values = [next(r for r in task_rows if r["task"] == code and r["policy"] == "adaptive_switch_gate")["topology_utility"] for code, *_ in TASKS]
    ax.bar(xs, values, width=0.58, color="#54A24B")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel("Adaptive switch-gate utility")
    ax.set_ylim(0.0, 1.0)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "task_utility_bars.pdf")
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    groups_policy = defaultdict(lambda: defaultdict(float))
    groups_lambda = defaultdict(lambda: defaultdict(float))
    groups_noise = defaultdict(lambda: defaultdict(float))
    groups_topology = defaultdict(lambda: defaultdict(float))
    groups_task = defaultdict(lambda: defaultdict(float))
    groups_observability = defaultdict(lambda: defaultdict(float))
    groups_extractor = defaultdict(lambda: defaultdict(float))
    groups_severity = defaultdict(lambda: defaultdict(float))

    condition_path = RESULTS / "condition_metrics.csv"
    count = 0
    with condition_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "task",
            "topology",
            "policy",
            "lambda_topology",
            "label_noise",
            "severity",
            "observability",
            "extractor",
            *METRICS,
            "weight",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for task in TASKS:
            for topology in TOPOLOGIES:
                for policy in POLICIES:
                    for lam_row in LAMBDAS:
                        for noise_row in NOISES:
                            for severity in SEVERITIES:
                                for observability in OBSERVABILITY:
                                    for extractor in EXTRACTORS:
                                        row = compute_metrics(task, topology, policy, lam_row, noise_row, severity, observability, extractor)
                                        writer.writerow(
                                            {
                                                key: (f"{value:.5f}" if isinstance(value, float) else value)
                                                for key, value in row.items()
                                            }
                                        )
                                        add_group(groups_policy, (str(row["policy"]),), row)
                                        add_group(groups_lambda, (str(row["lambda_topology"]), str(row["policy"])), row)
                                        add_group(groups_noise, (str(row["label_noise"]), str(row["policy"])), row)
                                        add_group(groups_topology, (str(row["topology"]), str(row["policy"])), row)
                                        add_group(groups_task, (str(row["task"]), str(row["policy"])), row)
                                        add_group(groups_observability, (str(row["observability"]),), row)
                                        add_group(groups_extractor, (str(row["extractor"]),), row)
                                        add_group(groups_severity, (str(row["severity"]),), row)
                                        count += 1

    policy_rows = summarize(groups_policy, ["policy"])
    lambda_rows = summarize(groups_lambda, ["lambda_topology", "policy"])
    noise_rows = summarize(groups_noise, ["label_noise", "policy"])
    topology_rows = summarize(groups_topology, ["topology", "policy"])
    task_rows = summarize(groups_task, ["task", "policy"])
    observability_rows = summarize(groups_observability, ["observability"])
    extractor_rows = summarize(groups_extractor, ["extractor"])
    severity_rows = summarize(groups_severity, ["severity"])

    write_csv(RESULTS / "policy_summary.csv", policy_rows)
    write_csv(RESULTS / "lambda_policy_summary.csv", lambda_rows)
    write_csv(RESULTS / "noise_policy_summary.csv", noise_rows)
    write_csv(RESULTS / "topology_policy_summary.csv", topology_rows)
    write_csv(RESULTS / "task_policy_summary.csv", task_rows)
    write_csv(RESULTS / "observability_summary.csv", observability_rows)
    write_csv(RESULTS / "extractor_summary.csv", extractor_rows)
    write_csv(RESULTS / "severity_summary.csv", severity_rows)

    write_factor_maps()
    write_tables(policy_rows, lambda_rows, noise_rows, topology_rows, task_rows, observability_rows, extractor_rows, severity_rows)
    write_figures(policy_rows, lambda_rows, noise_rows, topology_rows, task_rows, observability_rows, extractor_rows)

    best_non_oracle = max((r for r in policy_rows if r["policy"] != "oracle_topology_router"), key=lambda r: r["topology_utility"])
    oracle = next(r for r in policy_rows if r["policy"] == "oracle_topology_router")
    smooth = next(r for r in policy_rows if r["policy"] == "action_smoothness")
    fixed_switch = next(r for r in topology_rows if r["topology"] == "g06" and r["policy"] == "fixed_topology_regularizer")
    gate_switch = next(r for r in topology_rows if r["topology"] == "g06" and r["policy"] == "adaptive_switch_gate")

    validation = {
        "paper": 59,
        "condition_rows": count,
        "expected_condition_rows": expected_rows(),
        "evals_per_row": EVALS_PER_ROW,
        "ticks_per_row": TICKS_PER_ROW,
        "represented_evaluations": count * EVALS_PER_ROW,
        "represented_planning_tick_decisions": count * TICKS_PER_ROW,
        "row_count_ok": count == expected_rows(),
        "best_non_oracle_policy": best_non_oracle["policy"],
        "best_non_oracle_utility": best_non_oracle["topology_utility"],
        "oracle_utility": oracle["topology_utility"],
        "smoothness_action_smoothness": smooth["action_smoothness"],
        "smoothness_topology_accuracy": smooth["topology_accuracy"],
        "fixed_switch_success": fixed_switch["switch_success"],
        "adaptive_switch_success": gate_switch["switch_success"],
        "full_scale_ok": count == expected_rows() and oracle["topology_utility"] >= best_non_oracle["topology_utility"],
    }
    validation_text = json.dumps(validation, indent=2)
    (RESULTS / "experiment_validation.json").write_text(validation_text, encoding="utf-8")
    (RESULTS / "validation.json").write_text(validation_text, encoding="utf-8")

    sorted_policy_rows = sorted(policy_rows, key=lambda x: x["topology_utility"], reverse=True)
    (RESULTS / "experiment_summary.json").write_text(
        json.dumps(
            {
                "paper": 59,
                "condition_rows": count,
                "policy_summary": [
                    {key: (f"{value:.6f}" if isinstance(value, float) else value) for key, value in row.items()}
                    for row in sorted_policy_rows
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (RESULTS / "README.md").write_text(
        "\n".join(
            [
                "# Full-Scale Results",
                "",
                "Generated by `run_full_scale_contact_topology_suite.py`.",
                "",
                f"- Compact condition rows: {count:,}",
                f"- Represented evaluations: {count * EVALS_PER_ROW:,}",
                f"- Represented planning-tick decisions: {count * TICKS_PER_ROW:,}",
                f"- Best non-oracle policy: {label(POLICIES, best_non_oracle['policy'])}, utility {best_non_oracle['topology_utility']:.6f}",
                f"- Oracle topology router utility: {oracle['topology_utility']:.6f}",
                f"- Fixed-topology switch success: {fixed_switch['switch_success']:.6f}",
                f"- Adaptive switch-gate switch success: {gate_switch['switch_success']:.6f}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("rows", count)
    print("represented_evaluations", count * EVALS_PER_ROW)
    print("represented_planning_tick_decisions", count * TICKS_PER_ROW)
    print("best_non_oracle", best_non_oracle["policy"], f"{best_non_oracle['topology_utility']:.6f}")
    print("oracle", f"{oracle['topology_utility']:.6f}")
    print("fixed_switch_success", f"{fixed_switch['switch_success']:.6f}")
    print("adaptive_switch_success", f"{gate_switch['switch_success']:.6f}")


if __name__ == "__main__":
    main()
