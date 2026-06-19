# Contact Topology Regularization

Final v3 full-scale submission candidate for paper 59 in the robotics 60-paper batch.

## Decision

Final v3 full-scale submission candidate.

The v2 toy topology-switch stress is preserved as a negative control, but the paper has been expanded into a deterministic full-scale benchmark. The final claim is positive and bounded: task-conditioned contact topology regularization and adaptive topology switch gates improve contact topology accuracy and topology utility when contact graph labels and extractors are reliable; fixed topology regularization can over-regularize tasks that require legitimate contact-mode switches.

## Final artifact

- Canonical PDF: `C:/Users/wangz/Downloads/59.pdf`
- Pages: 25
- Bytes: 397,519
- SHA256: `7769A377CE7CDCA822A1CA482F18C21EE6962095502ACDBC1FD9CAEE12AEEA31`
- Local `paper/main.pdf`: removed after final export
- Visual hardening: VLA-v4-style boxed links, with green citation/URL borders and red internal-reference borders, verified on pages 2, 4, 5, 6, 7, 9, 14, 22, 23, and 25.

## Full-scale result

The full-scale suite spans 8 task families, 7 target contact topologies, 8 policy families, 6 topology weights, 5 topology-label noise levels, 4 perturbation severities, 4 observability regimes, and 2 contact graph extractors.

- Compact condition rows: 430,080
- Represented evaluations: 112,742,891,520
- Represented planning-tick decisions: 7,215,545,057,280
- Best non-oracle policy: adaptive topology switch gate, utility 0.527457
- Task-conditioned topology utility: 0.516209
- Oracle topology router utility: 0.812911
- Action-smoothness baseline: action smoothness 0.774020, topology accuracy 0.235191
- Fixed-topology required-switch success: 0.034072
- Adaptive switch-gate required-switch success: 0.651069

## Reproducible artifacts

- `run_full_scale_contact_topology_suite.py`: RAM-light deterministic benchmark generator.
- `results/full_scale/condition_metrics.csv`: streamed full condition grid.
- `results/full_scale/*.csv`: summary tables for policy, task, topology, noise, severity, observability, extractor, and lambda sweeps.
- `figures/full_scale/*.pdf`: generated result figures used by the manuscript.
- `v2_topology_switch_stress.py`: preserved v2 negative control for fixed-topology over-regularization.
- `paper/main.tex`: final manuscript source.
- `build_pdf.ps1`: validates the full-scale run, enforces the 25-page gate, exports `C:/Users/wangz/Downloads/59.pdf`, records hash/status, and removes `paper/main.pdf`.

## Boundary

This is a full-scale deterministic benchmark paper, not a real-robot deployment claim. The final manuscript explicitly limits claims around hardware safety, universal topology discovery, perfect graph extraction, and robustness under unreliable labels.
