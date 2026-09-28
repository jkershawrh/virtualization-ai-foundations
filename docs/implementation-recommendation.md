# Concrete implementation recommendation

## 101 candidate

Build one independent namespace-scoped journey:

1. A small KubeVirt `VirtualMachine` contains a checked-in client and synthetic
   operations notes.
2. The client sends `analysis-request/v1` to the `ai-analysis` Kubernetes
   `Service` using namespace-local DNS.
3. An `ai-analysis-adapter` `Deployment` validates the request, invokes one
   configured OpenAI-compatible Intel Xeon CPU inference endpoint, validates
   `analysis-response/v1`, and records redacted evidence.
4. The response exposes the correlation ID, source state, model identity,
   hardware identity, validation result, and human-authority boundary.
5. A controlled unavailable condition follows the same adapter path and
   returns a typed failure with `ai_participated: false`.
6. The presentation consumes only the typed evidence API; checked-in fixtures
   remain visibly `REHEARSAL` or `OFFLINE`.
7. Showroom guides the learner through verification, trace, healthy proof,
   safe failure, and evidence-map export.

Use a dedicated workload instead of deploying the complete AI Virtual Agent or
Triforce stacks. This reduces permissions, startup time, resource demand, and
narrative noise while preserving the relevant source patterns.

## Contract and authority rules

- Version request, response, error, and evidence schemas before implementation.
- Never place the model credential in the VM, browser, fixture, ConfigMap, or
  repository. Mount it into the adapter from a Secret.
- The model may classify and explain one synthetic note. It cannot call tools,
  mutate the VM or cluster, or approve an operational action.
- The adapter owns deterministic schema and category validation.
- Missing model or hardware identity prevents a `LIVE` AI claim.
- An unavailable or invalid response returns no advisory result.

## Future 201 build lab

The 201 learner authors or modifies the API contract, VM client configuration,
Service, NetworkPolicy, credential reference, and evidence mapping. The learner
must prove the allowed path, denied/unavailable paths, contract failure, and
cleanup. Keep it a separate catalog journey and repository milestone.
