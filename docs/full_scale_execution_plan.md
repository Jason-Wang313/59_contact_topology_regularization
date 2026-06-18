# Paper 59 Full-Scale Execution Plan

## Objective

Turn Paper 59 from a short v2 mechanism note into a final full-scale submission candidate. The final paper must be at least 25 pages before any final PDF is exported to Downloads. The final contribution should be positive but bounded: contact topology regularization can stabilize task-relevant contact graph structure in contact-rich manipulation, while fixed topology penalties can over-regularize tasks that require legitimate topology switches and noisy topology labels can degrade the method.

## Current Claim

The v2 manuscript argues that action smoothness is not enough for contact-rich manipulation because two trajectories can be equally smooth while inducing different contact topology classes. It defines a contact topology regularizer and shows a small topology-switch stress:

- smoothness-only success: 0.333
- fixed-upper topology success: 0.333
- task-conditioned topology at `lambda_top=1.25`: 1.000
- task-conditioned topology at `lambda_top=1.25` with 20% topology-label noise: 0.800

At the start of this plan, the claim was useful but too small: the evidence was a toy mechanism, the manuscript was short, and the build script exported a non-final PDF without a page gate.

## Main Gaps

1. No broad contact-rich benchmark.
2. No large policy-family comparison.
3. No topology-weight sweep beyond the v2 toy table.
4. No task diversity beyond upper/lower/switching arcs.
5. No contact graph extractor quality stress.
6. No observability or sensor-regime stress.
7. No phase-specific switch analysis.
8. No failure cases beyond one toy switching task.
9. No final 25-page manuscript.
10. No final-only build gate.

## Final Target

- Final status: `final_v3_full_scale_submission_candidate`.
- Final artifact path: `C:/Users/wangz/Downloads/59.pdf`.
- Final page threshold: at least 25 pages.
- Export rule: copy to Downloads only after the manuscript is final, page threshold passes, docs are updated, and visual QA is run.
- Local PDF rule: remove `paper/main.pdf` after export.
- Desktop rule: no Desktop copy.

## Full-Scale Benchmark Design

The full-scale benchmark will be deterministic and RAM-light. Each compact row represents many seeds, scenes, contact perturbation schedules, rollouts, and contact graph extraction attempts. Rows will stream to CSV and summaries will be accumulated online.

Planned factors:

1. Task family, 8 levels:
   - peg insertion
   - drawer sliding
   - snap-fit assembly
   - cable routing
   - cloth edge folding
   - in-hand regrasp
   - bimanual handover
   - tool-use scraping

2. Target contact topology, 7 levels:
   - single point slide
   - dual support
   - pinch grasp
   - rim insertion
   - wrap or loop
   - rolling contact
   - required topology switch

3. Policy or regularizer family, 8 levels:
   - behavior cloning baseline
   - action smoothness baseline
   - force penalty baseline
   - tactile graph encoder
   - fixed topology regularizer
   - task-conditioned topology regularizer
   - adaptive topology switch gate
   - oracle topology router

4. Topology weight, 6 levels:
   - 0.00
   - 0.25
   - 0.50
   - 1.00
   - 1.25
   - 2.00

5. Topology-label noise, 5 levels:
   - 0.00
   - 0.05
   - 0.10
   - 0.20
   - 0.40

6. Perturbation severity, 4 levels:
   - mild
   - moderate
   - severe
   - adversarial

7. Observability or sensor regime, 4 levels:
   - proprioception only
   - force torque
   - tactile graph
   - full contact state

8. Contact graph extractor family, 2 levels:
   - framewise threshold extractor
   - temporal graph smoother

Expected compact rows: 8 x 7 x 8 x 6 x 5 x 4 x 4 x 2 = 430,080.

Represented evaluations per row will be 262,144, yielding 112,742,891,520 represented evaluations. Planning-tick decisions will use 16,777,216 per row, yielding 7,215,545,057,280 represented planning-tick decisions.

## Metrics

Each row will report:

- task success
- topology accuracy
- switch-task success
- wrong topology rate
- over-regularization rate
- graph edit gap
- contact-mode violation
- force smoothness
- action smoothness
- topology label sensitivity
- extractor false positive rate
- extractor false negative rate
- topology utility
- policy cost
- recovery margin

Critical invariants:

- smoothness-only can be action-smooth while topology accuracy is poor,
- fixed topology regularization must fail tasks requiring legitimate switches,
- task-conditioned topology should improve topology accuracy and utility when labels are reliable,
- label noise should degrade task-conditioned topology,
- the oracle topology router should be an upper bound and not a deployable claim.

## Target Experiments

1. Main policy comparison across all factors.
2. Topology-weight sweep showing the useful range and over-regularization risk.
3. Label-noise sweep showing degradation at 0.10, 0.20, and 0.40 noise.
4. Switch-task stress showing fixed topology failure and adaptive switch-gate improvement.
5. Contact graph extractor stress across observability regimes.
6. Task-family stress showing which tasks benefit most from topology regularization.
7. Topology-class stress showing where wrap, rolling, and switch cases are hardest.
8. Negative control showing action smoothness can improve smoothness while leaving topology accuracy weak.
9. Oracle gap analysis showing remaining headroom.

## Baselines And Ablations

Baselines:

- behavior cloning without smoothness or topology terms
- action smoothness only
- force penalty only
- tactile graph encoder without topology regularization
- fixed topology regularizer

Ablations:

- remove topology term
- replace task-conditioned topology target with fixed target
- vary topology weight
- inject topology-label noise
- reduce observability from full contact state to proprioception only
- test required switch tasks separately from fixed-topology tasks
- compare graph edit gap with action smoothness and force smoothness

## Figures And Tables

Planned generated tables:

- scale table
- main policy comparison
- topology-weight sweep
- label-noise stress
- switch-task stress
- observability or extractor stress
- task-family stress
- topology-class stress
- oracle gap table

Planned generated figures:

- policy utility vs topology error
- topology-weight response curves
- label-noise degradation curves
- switch-task success curves
- observability false-positive/false-negative curves
- task-family utility bars

## Writing Expansion Strategy

The final manuscript will be rewritten around the full-scale benchmark:

1. Abstract with final counts and best non-oracle result.
2. Introduction: smoothness is not topology.
3. V2 correction: topology helps only when task-conditioned.
4. Formal contact topology definition.
5. Contact graph and graph edit gap.
6. Full-scale benchmark design.
7. Policy and regularizer families.
8. Observability and extractor model.
9. Main policy results.
10. Topology-weight sweep.
11. Label-noise stress.
12. Switch-task stress.
13. Task-family stress.
14. Topology-class stress.
15. Extractor failure analysis.
16. Negative controls.
17. Related work on contact-rich manipulation.
18. Related work on tactile graphs.
19. Related work on topology-aware manipulation.
20. Limitations and hardware follow-up.
21. Reproducibility and artifact checklist.
22. Reviewer attack responses.
23. Appendices with factor maps, metric definitions, failure cases, and acceptance checklist.

## Page-Count Strategy

The final paper must reach at least 25 pages through real content:

- full experimental design and metric definitions,
- generated tables and figures,
- detailed stress-test interpretation,
- failure-case appendices,
- reproducibility appendices,
- reviewer and deployment boundary appendices.

No PDF will be copied to Downloads until the local build is at least 25 pages and judged final.

## RAM-Light Execution Strategy

- Stream `results/full_scale/condition_metrics.csv` row by row.
- Maintain online aggregate dictionaries only.
- Write summary CSVs after streaming.
- Generate figures from small summary tables.
- Avoid retaining the full condition table in Python memory.
- Run a deterministic compact grid rather than a large stochastic tensor.
- Keep generated CSV below GitHub's 100 MB hard limit.

## Documentation Plan

After the experiment and manuscript are final, update:

- `README.md`
- `child_status.md`
- `plan.md`
- `docs/claims.md`
- `docs/experiment_rigor_checklist.md`
- `docs/final_audit.md`
- `docs/final_audit.json`
- `docs/hostile_reviewer_response.md`
- `docs/novelty_boundary_map.md`
- `docs/novelty_decision.md`
- `docs/reproducibility_checklist.md`
- `docs/reviewer_attacks.md`
- `docs/submission_attack_log.md`
- `docs/submission_readiness_decision.md`
- `docs/submission_version_log.md`
- `results/full_scale/README.md`
- `results/full_scale/validation.json`

## Build And QA Plan

1. Update `build_pdf.ps1` after the final manuscript is ready.
2. Enforce at least 25 pages.
3. Record file size, SHA256, page count, export path, and build timestamp in ASCII JSON.
4. Export only to `C:/Users/wangz/Downloads/59.pdf`.
5. Remove `paper/main.pdf`.
6. Render the Downloads PDF to `tmp/pdfs/`.
7. Visually inspect title page, core result pages, stress-test pages, appendix tables, and references.
8. Delete `tmp/` only after verifying its resolved path is inside the Paper59 repo.
9. Run JSON parse checks, LaTeX warning scan, stale-status scan, ASCII scan, row-count check, file-size guard, and cached diff check.
10. Commit and push only after all checks pass.

## Stop Condition For Paper 59

Paper59 is complete only when:

- the final PDF is at least 25 pages,
- the canonical PDF exists at `C:/Users/wangz/Downloads/59.pdf`,
- the Downloads PDF has been visually inspected from rendered PNGs,
- local `paper/main.pdf` is absent,
- docs record final v3 status and hash,
- all validation checks pass,
- the commit is pushed,
- `git status --short --branch` is clean and aligned with origin.

## Final Outcome

The plan was executed as v3 full-scale. The benchmark produced 430,080 compact condition rows representing 112,742,891,520 evaluations and 7,215,545,057,280 planning-tick decisions. The final manuscript reached 25 pages and was exported only after the full-scale validation and page gate passed.

- Final PDF: `C:/Users/wangz/Downloads/59.pdf`
- Pages: 25
- Bytes: 397,519
- SHA256: `E5186EFCE818FB00711EF4E367BCFE0AE0D00B6417B85D9BC42CFB7AC51E00A6`
- Visual QA pages inspected: 1, 5, 6, 7, 11, 14, 18, 21, 22, 23, 24, 25.
- Local `paper/main.pdf`: absent after final build.
