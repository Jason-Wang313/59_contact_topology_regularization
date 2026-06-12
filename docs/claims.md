# Claims

## Core claim
A topology-preserving regularizer on contact-rich robot policies can improve task stability because it constrains the discrete structure of contacts, not just the magnitude of output changes.

## Supporting claims

- Smooth action regularization is not enough to preserve contact mode order.
- The important structure in many contact-rich tasks is the contact adjacency graph.
- Graph- or topology-aware contact representations from perception are not the same as topology-aware policy regularization.
- A topology regularizer should reduce contact rearrangements that hurt task success.

## Claims that need evidence

- The regularizer improves success on representative contact-rich tasks.
- The regularizer reduces contact graph edit distance.
- The regularizer retains or improves force safety relative to smoothness baselines.
- The method remains useful across task types, not only one toy setup.

## Claims that must stay modest

- This is not a universal solution for all manipulation.
- This does not replace control-theoretic safety.
- This does not prove topology is the only useful inductive bias.
