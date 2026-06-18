# Novelty Boundary Map

## Core contribution

Contact topology regularization is framed as a task-conditioned penalty over induced contact graph sequences, with explicit separation from action smoothness, force penalties, and tactile graph representation.

## Final benchmark novelty

- Full deterministic factor grid over task family, topology class, policy family, topology weight, label noise, severity, observability, and extractor family.
- RAM-light streamed condition table with 430,080 rows.
- Required-switch stress that exposes fixed-topology over-regularization.
- Label-noise and extractor/observability stress that bound the topology claim.
- Reporting rule requiring topology accuracy, switch success, smoothness, graph edit gap, and label/extractor reliability to be reported separately.

## Boundary

The benchmark supports topology-aware evaluation and task-conditioned regularization claims. It does not establish real-robot safety, learned-policy deployment superiority, perfect graph extraction, or universal topology targets.

## Negative control preserved

The v2 switch stress remains useful: fixed-upper topology regularization reaches 0.333 success and 0.000 switch-task success in the toy setting, while task-conditioned topology only succeeds when the topology target is correct and sufficiently weighted.
