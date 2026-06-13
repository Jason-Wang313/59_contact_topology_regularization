# Hostile Reviewer Response

The strongest reviewer objection is that topology regularization can over-constrain dexterity. The v2 paper accepts this and measures it.

In the switch stress, a fixed-upper topology penalty has the same 0.333 success as smoothness-only and 0.000 switch-task success. Task-conditioned topology succeeds only after the topology weight reaches 1.25, and it drops to 0.800 under 20% topology-label noise.

This supports a narrow workshop claim: topology can be a useful training signal only when the task topology is declared and observed reliably.
