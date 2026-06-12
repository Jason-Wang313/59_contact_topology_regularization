# Reviewer Attacks

## Attack 1: This is just smoothness regularization in disguise
Response: the regularizer is defined on contact adjacency graphs, not on action derivatives. The toy evidence shows equal-smoothness paths can still differ in topology.

## Attack 2: Graph neural networks already model contact structure
Response: perception encoders are not policy regularizers. A tactile GNN can represent contact features without constraining topology preservation across rollouts.

## Attack 3: Contact-safe RL already handles the hard part
Response: safety constraints bound force or collision risk, but they do not guarantee the order, adjacency, or loop structure of contacts needed by the task.

## Attack 4: Topology is too abstract for robotics control
Response: the relevant topology is not a generic topological invariant. It is a concrete contact graph abstraction tied to manipulation success.

## Attack 5: The toy experiment is too small
Response: agreed. It is only a runnable witness for the mechanism. A full paper would need a real contact-rich benchmark with contact graph labels or proxies.

## Attack 6: The method may over-regularize dexterity
Response: yes. This is the main failure mode. The loss must be scoped to task-relevant contact relations, not every contact edge.

## Attack 7: Existing topological manipulation papers already solve it
Response: papers like the grasp loop signature solve topology at the planning layer for deformables. That is close, but not the same as regularizing policy learning itself.

## Attack 8: There is no theorem
Response: correct. The current draft is mechanism-first and evidence-light, so the honest status is workshop/revise unless stronger experiments are added.
