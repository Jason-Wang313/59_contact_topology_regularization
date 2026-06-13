# Final Audit

Paper: 59 contact_topology_regularization

Status: terminal

Decision: workshop-only

## Main reason

The paper has a crisp mechanism, but the evidence is still toy-only. V2 hardening shows the central limitation quantitatively: topology regularization helps only when the relevant topology is task-conditioned, weighted strongly enough, and observed reliably.

## V2 evidence

- Smoothness-only selector: 0.333 success and 0.000 switch-task success.
- Fixed-upper topology selector at `lambda_top=1.25`: 0.333 success and 0.000 switch-task success.
- Task-conditioned topology at `lambda_top=1.00`: 0.667 success and 0.000 switch-task success.
- Task-conditioned topology at `lambda_top=1.25`: 1.000 success and 1.000 switch-task success.
- Task-conditioned topology at `lambda_top=1.25` with 20% topology-label noise: 0.800 success and 0.800 switch-task success.

## Boundary

The paper may claim that action smoothness alone can miss contact topology and that task-conditioned topology can be a useful training signal in a toy witness. It may not claim real robot validation, representative benchmark performance, universal superiority, or robustness to noisy contact graph extraction.
