# Reproducibility Checklist

- Run `python scripts/toy_contact_topology_demo.py` to regenerate the original toy witness.
- Run `python v2_topology_switch_stress.py` to regenerate the v2 CSV, JSON, and LaTeX table.
- Run `powershell -ExecutionPolicy Bypass -File build_pdf.ps1` to rebuild the canonical PDF.
- The canonical artifact is `C:/Users/wangz/Downloads/59.pdf`.
- `paper/main.pdf` is generated during compilation and removed after the canonical copy is made.
- `data/build_status.json` records local build status and is intentionally ignored.
