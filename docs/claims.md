# Claims

## Supported

1. Equal-smoothness paths can have different contact topology in the preserved v2 toy witness.
2. A fixed topology penalty can over-regularize and fail tasks that require a legitimate contact-mode switch.
3. The full-scale deterministic benchmark contains 430,080 compact rows representing 112,742,891,520 evaluations and 7,215,545,057,280 planning-tick decisions.
4. Action smoothness alone can be high while topology accuracy remains weak: the action-smoothness baseline has action smoothness 0.774020 but topology accuracy 0.235191.
5. Task-conditioned topology improves topology utility to 0.516209, and the adaptive topology switch gate is the best non-oracle policy with utility 0.527457.
6. The oracle topology router reaches utility 0.812911, leaving substantial headroom.
7. Fixed topology regularization fails required-switch cases: fixed-topology switch success is 0.034072, while the adaptive switch gate reaches 0.651069.
8. Topology-label noise degrades task-conditioned and adaptive topology methods, so the final claim is conditional on label and extractor reliability.

## Removed or narrowed

1. No claim of real robot validation.
2. No claim that topology regularization is universally superior to smoothness.
3. No claim that topology graphs can be extracted reliably from perception in all settings.
4. No claim that the oracle topology router is deployable.
5. No claim of robustness under arbitrary topology-label noise or adversarial extractor failure.
