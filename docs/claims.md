# Claims

## Supported

1. Equal-smoothness paths can have different contact topology in the toy witness.
2. A fixed topology penalty can over-regularize and fail tasks that require a contact-mode switch.
3. Task-conditioned topology reaches 1.000 success in the toy switch suite only when `lambda_top` reaches 1.25.
4. Topology-label noise matters: 20% label noise lowers task-conditioned success to 0.800.

## Removed or narrowed

1. No claim of real robot validation.
2. No claim that topology regularization is universally superior to smoothness.
3. No claim that topology graphs can be extracted reliably from perception.
4. No claim that the regularizer improves representative contact-rich policy-learning benchmarks.
