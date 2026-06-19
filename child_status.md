# Child Status 59

Status: complete
Decision: final_v3_full_scale_submission_candidate
Hardening version: v3 full-scale VLA highlights
Canonical PDF: `C:/Users/wangz/Downloads/59.pdf`
Canonical PDF pages: 25
Canonical PDF bytes: 397,519
Canonical PDF SHA256: `7769A377CE7CDCA822A1CA482F18C21EE6962095502ACDBC1FD9CAEE12AEEA31`
Canonical PDF built: 2026-06-19 21:01:22 +08:00
Local paper PDF: removed after canonical rebuild

## V3 changes

- Added `run_full_scale_contact_topology_suite.py`.
- Added a RAM-light deterministic full-scale benchmark with 430,080 compact condition rows.
- Represented 112,742,891,520 evaluations and 7,215,545,057,280 planning-tick decisions.
- Added full-scale policy, lambda, noise, switch, task, topology, severity, observability, and extractor summaries.
- Rewrote the manuscript into a 25-page final submission candidate.
- Preserved the v2 topology-switch toy stress as a negative control.
- Hardened `build_pdf.ps1` so Downloads export is gated by full-scale validation, page count, SHA256 recording, and local-PDF removal.
- Rendered the final Downloads PDF to PNG and visually inspected representative pages.
- Matched the VLA-v4 role-model boxed link style: 13 red internal-reference boxes, 16 green citation/URL boxes, and 29 total link annotations, all with `pdfborder={0 0 1}`.
- Rendered and visually QA'd pages 2, 4, 5, 6, 7, 9, 14, 22, 23, and 25 after rebuild.

## Final claim boundary

Supported: task-conditioned contact topology regularization and adaptive switch gates improve topology accuracy and topology utility in the deterministic benchmark, while fixed topology regularization fails required-switch cases.

Not supported: real-robot safety, universal superiority over smoothness, perfect contact graph extraction, or robustness to unreliable topology labels.
