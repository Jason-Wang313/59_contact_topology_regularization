# Submission Version Log

## v1

Initial paper with literature sweep, toy equal-smoothness witness, and ICLR-style PDF.

## v2

- Added `v2_topology_switch_stress.py`.
- Added `docs/v2_topology_switch_stress.csv`.
- Added `docs/v2_topology_switch_stress.json`.
- Added `paper/v2_topology_switch_table.tex`.
- Reframed the paper around task-conditioned topology targets.
- Decision at that time: not final; needed a broader benchmark.

## v3 full-scale

- Added `run_full_scale_contact_topology_suite.py`.
- Generated 430,080 compact condition rows representing 112,742,891,520 evaluations.
- Generated full-scale tables and figures under `results/full_scale/` and `figures/full_scale/`.
- Rewrote the manuscript as a 25-page final submission candidate.
- Hardened `build_pdf.ps1` to validate the full-scale run, enforce the 25-page threshold, export only `C:/Users/wangz/Downloads/59.pdf`, record SHA256, and remove `paper/main.pdf`.
- Final canonical SHA256: `E5186EFCE818FB00711EF4E367BCFE0AE0D00B6417B85D9BC42CFB7AC51E00A6`.
