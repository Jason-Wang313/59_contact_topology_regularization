# Plan

Status: completed for Paper59 v3 full-scale.

1. Preserve the v2 topology-switch stress as a negative control: fixed topology regularization can over-constrain tasks that require legitimate contact-mode switches.
2. Add a RAM-light deterministic full-scale benchmark over task family, target topology, policy family, topology weight, label noise, perturbation severity, observability regime, and contact graph extractor family.
3. Stream compact condition rows and online aggregates to `results/full_scale/` without loading the full condition CSV into memory.
4. Generate full-scale tables, figures, validation JSON, and policy/task/topology/lambda/noise/observability summaries.
5. Rewrite the manuscript around the final positive claim: task-conditioned contact topology regularization improves topology accuracy and contact-task utility when topology labels are reliable, while fixed topology and noisy labels expose the method's limits.
6. Expand to at least 25 pages before final export.
7. Update `build_pdf.ps1` to enforce the page threshold, record size/hash/page count in ASCII JSON, copy only the final artifact to `C:/Users/wangz/Downloads/59.pdf`, and remove `paper/main.pdf`.
8. Render the Downloads PDF for visual QA, update all status docs, run stale scans and validation checks, then commit and push only after the repo is clean.

Final PDF: `C:/Users/wangz/Downloads/59.pdf`, 25 pages, SHA256 `E5186EFCE818FB00711EF4E367BCFE0AE0D00B6417B85D9BC42CFB7AC51E00A6`.
