# Novelty Boundary Map

## In scope

- Toy demonstration that action smoothness does not identify contact topology.
- Task-conditioned contact topology regularization.
- Explicit regularization-weight and label-noise sensitivity.
- Mechanism-level argument for treating contact graph structure as a policy-learning signal.

## Out of scope

- Fixed topology preservation as a universal objective.
- Real robot or high-fidelity simulation validation.
- Learned contact graph extraction.
- Representative contact-rich benchmark performance.
- Proof that topology regularization is better than force, safety, or tactile graph baselines.

## V2 hostile boundary

The central failure mode is over-regularization. In the v2 switch stress, fixed-upper topology regularization reaches only 0.333 success and 0.000 switch-task success, matching smoothness-only. Task-conditioned topology only succeeds after `lambda_top=1.25`, and 20% label noise lowers success to 0.800.
