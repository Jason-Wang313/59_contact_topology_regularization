# Novelty Boundary Map

## What is already well covered

- Smooth control for contact tasks
- Force limiting and collision avoidance
- Tactile graph encoders for state estimation
- Hybrid force-position control
- Contact-aware imitation/RL with reward shaping
- Deformable-object topology representations
- Contact mode planning in specific manipulatory domains

## What is not yet clearly covered

- Policy regularization that explicitly preserves contact topology under small input or latent perturbations
- A training objective that keeps the contact adjacency graph stable even when continuous outputs change
- An ablation showing that smoothing actions can destroy the contact mode sequence while topology regularization preserves task success
- A robotics-specific bridge between graph/topology representation and policy learning, rather than perception or planning only

## Hidden assumptions that may be false

1. Smooth actions imply stable contacts.
2. Force penalties preserve the right manipulation structure.
3. Contact-rich tasks can be treated as continuous control with occasional collisions.
4. Tactile graph encoders automatically preserve task-relevant topology.
5. A policy that is locally smooth is globally safe in contact.
6. Contact adjacency can be ignored if final success rate is high.
7. Contact mode transitions are nuisance variables rather than the core state.
8. The relevant structure is force magnitude rather than who touches whom.
9. One can regularize policy outputs without regularizing contact structure.
10. Action-space regularization transfers across objects and geometry.
11. Existing contact-safe methods also preserve topology.
12. Topological failure is rare enough to be ignored in benchmarks.
13. The number of contacts matters less than their arrangement.
14. Continuous latent smoothness is a proxy for discrete contact consistency.
15. Policy robustness and contact-topology robustness are equivalent.
16. Contact graphs need not be tracked through the entire rollout.
17. The object can be modeled as a point mass with contact costs.
18. Small action perturbations produce small changes in contact graph.
19. Safety constraints alone are enough for dexterous contact tasks.
20. The best representation for contact-rich control is still action-centric.

## Candidate directions that break assumptions

- Regularize the policy so the induced contact graph has bounded edit distance across neighboring states.
- Penalize changes in contact topology only when they alter the feasible task manifold.
- Learn a contact graph latent and match the topology of predicted and observed rollout graphs.
- Compare action-smoothness, force-bounded, and topology-preserving objectives on the same task family.

## Chosen direction
The strongest direction is a contact-topology consistency regularizer for manipulation policies, with an explicit demonstration that smoothness regularization can leave contact mode order and adjacency unstable.
