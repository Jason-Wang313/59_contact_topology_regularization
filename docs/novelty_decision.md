# Novelty Decision

## Decision
Proceed with `Contact Topology Regularization` as a robotics paper, but only if the contribution is framed around preserving discrete contact structure rather than generic smoothness.

## Why this is the strongest idea

- It attacks a real failure mode in contact-rich policies: continuous smoothness does not guarantee stable contact sequencing.
- It is more specific than adding force penalties or safety constraints.
- It connects existing graph/topology ideas to policy learning in a way that appears underexplored.

## Why weaker ideas were rejected

- Bigger model: forbidden and not mechanism-changing.
- Better data: not a new mechanism.
- New benchmark only: insufficient.
- Add uncertainty or active learning: orthogonal.
- Add verifier: does not change the central mechanism.
- Combine existing modules: too close to composition.
- LLM planner: off-topic.
- Plain RL: not distinctive enough.

## Main risk
The paper becomes non-novel if the method is just a contact-aware reward shaping term or a generic graph neural policy encoder. The regularizer must operate on contact topology itself.

## Working thesis
Policies for contact-rich manipulation should be regularized to preserve the topology of the contact graph and mode transitions, because output smoothness alone can hide catastrophic contact rearrangements.
