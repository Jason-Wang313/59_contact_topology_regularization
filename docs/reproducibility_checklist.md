# Reproducibility Checklist

- [x] Run `python run_full_scale_contact_topology_suite.py` to regenerate `results/full_scale/` and `figures/full_scale/`.
- [x] Confirm `results/full_scale/experiment_validation.json` has `row_count_ok: true` and `full_scale_ok: true`.
- [x] Confirm `condition_rows == 430080`.
- [x] Confirm `represented_evaluations == 112742891520`.
- [x] Confirm `represented_planning_tick_decisions == 7215545057280`.
- [x] Confirm best non-oracle policy is `adaptive_switch_gate`.
- [x] Run `./build_pdf.ps1`.
- [x] Confirm `data/build_status.json` records 25 pages, 397,519 bytes, and SHA256 `E5186EFCE818FB00711EF4E367BCFE0AE0D00B6417B85D9BC42CFB7AC51E00A6`.
- [x] Confirm `C:/Users/wangz/Downloads/59.pdf` exists.
- [x] Confirm `paper/main.pdf` is absent after the build.
- [x] Render the Downloads PDF to PNG and visually inspect representative pages.

The v2 toy stress can still be regenerated with `python v2_topology_switch_stress.py`; it is preserved as a negative control, not the final evidence base.
