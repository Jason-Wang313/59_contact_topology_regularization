# Literature Map

## Field box
`Contact rich policy learning` covers policies for manipulation, assembly, locomotion-adjacent contact, tactile in-hand control, force-aware control, contact-rich sim-to-real transfer, and contact planning under partial observability.

## Initial hypothesis
The seed hypothesis is: regularize policies by preserving contact topology rather than output smoothness.

## Stronger framing
The literature suggests the more defensible thesis is:

> Contact-rich policies fail less often when the learned objective preserves the discrete structure of contact modes, contact adjacency, and loop/chain topology, not when it merely penalizes action variation.

This keeps the proposal in embodied robotics, but shifts the mechanism from generic smoothness or force penalties to topology-aware policy regularization.

## 1000-paper sweep
`docs/related_work_matrix.csv` contains 4374 unique records collected from Crossref and arXiv queries spanning:

- contact-rich manipulation
- tactile sensing and visuotactile policy learning
- contact-safe RL and force control
- contact sequence and state-transition models
- graph/topology representations in manipulation
- deformable object manipulation and grasp loops

## 300-paper serious skim
The serious skim shortlist should favor papers that explicitly involve one or more of:

- discrete contact states
- contact-mode switching
- tactile graph encodings
- force-position hybrid control
- contact-safe optimization
- topology-sensitive manipulation of deformables

Representative papers:

- [Learning Contact-Rich Manipulation Skills with Guided Policy Search](https://arxiv.org/abs/1501.05611)
- [Learning Force Control for Contact-Rich Manipulation Tasks With Rigid Position-Controlled Robots](https://arxiv.org/abs/2002.03371)
- [A Contact-Safe Reinforcement Learning Framework for Contact-Rich Robot Manipulation](https://arxiv.org/abs/2207.13438)
- [TacGNN: Learning Tactile-Based In-Hand Manipulation With a Blind Robot](https://arxiv.org/abs/2304.00736)
- [The Grasp Loop Signature: A Topological Representation for Manipulation Planning With Ropes and Cables](https://arxiv.org/abs/2403.01611)

## 200-250-paper deep read
Deep read targets should be limited to papers that either:

1. make contact mode a first-class state variable,
2. use graph structure for tactile/contact perception, or
3. regulate policy learning with a contact-safety or contact-consistency objective.

Candidate deep-read set:

- Guided Policy Search for contact-rich manipulation
- Dense reward learning for contact-rich manipulation
- Contact-safe RL
- Force control for contact-rich manipulation
- TacGNN
- 3D-ViTac
- NeuralFeels
- Glove-style / tactile graph approaches
- Grasp loop signature
- Changing-contact manipulation
- Contact sequence learning / state-transition graphs

## 100-paper hostile prior set
The hostile set should include papers that would make this idea look redundant if they already solved the core mechanism. It must therefore include:

- action-smoothness regularization papers
- contact-safe and force-bounded policy learning
- graph neural network tactile perception
- contact mode planning
- topological representations for deformable manipulation
- visuotactile world models and contact-aware imitation learning
- hybrid force-position control learning

The key question for each hostile paper is whether it preserves:

- discrete contact adjacency
- topology of the contact graph
- mode-transition structure
- loop closure / chain connectivity

If not, it is adjacent but not the same mechanism.

## Bottom line
The literature strongly suggests novelty, if any, must come from preserving discrete contact structure under policy perturbations, not from another smoothness term, another reward shaping trick, or another tactile encoder.
