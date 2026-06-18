# Hostile Reviewer Response

The strongest objection is that topology regularization can over-constrain dexterity. The paper accepts this and measures it. Fixed topology regularization has only 0.034072 switch success on required-switch cases, while the adaptive switch gate reaches 0.651069 and the oracle reaches 0.845909 on that topology slice.

The second objection is that smoothness already solves the problem. It does not in this benchmark: the action-smoothness baseline has action smoothness 0.774020 but topology accuracy 0.235191 and utility 0.250052.

The third objection is that the result may come from contact sensing rather than regularization. The tactile graph encoder baseline reaches utility 0.386031, below task-conditioned topology at 0.516209 and adaptive switch gating at 0.527457.

The fourth objection is label quality. The paper agrees: label noise degrades topology methods, so the final claim is conditional on reliable topology labels and graph extractors.

The fifth objection is hardware generality. The paper does not claim hardware validation. It claims a deterministic full-scale benchmark and reporting discipline.
