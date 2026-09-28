# Discovery review — Virtualization + AI foundations

Status: **reviewed for implementation at level 101**  
Review date: 2026-09-28  
Catalog scope: new, independent Virtualization + AI track

## Decision

The inspected sources earn a **101 foundation**, not 201 or 501. They separately
show VM management and service networking, an AI application architecture, and
a Triforce-style presentation cadence. They do not contain a tested,
source-bound VM-origin request to governed inference, and they do not ask the
learner to author that integration.

The 101 candidate therefore teaches the learner to trace and explain an
established path. A separate future 201 lab must require the learner to author
the versioned VM-to-AI contract, configure identity and networking, exercise
failure, and prove cleanup.

## Pinned discovery sources

| Source | Revision | Working state observed | Reusable evidence |
|---|---|---|---|
| `ai-virtual-agent` | `6c1ba5ca3478da438c91c684e19844c7bcf1b195` | clean | Managed AI request, model gateway, validation, and adapter patterns |
| `ocp-virt-roadshow-2026-showroom` | `5d296c9c9fbe773af09c16935c78b89baebd1f81` | clean | VM, Service, DNS, Route, and network-boundary learning patterns |
| `triforce` | `c6c17f47c0b9e4750053271514252580ec4ea3d2` | three pre-existing untracked files | Sparse business cadence, guided architecture, KubeVirt and AI concepts |

No source repository was modified during discovery.

## Verified findings

1. The roadshow is a seven-module virtualization curriculum. Only selected VM,
   Service/DNS, and network-boundary patterns are relevant; copying the complete
   roadshow would obscure the new learner decision.
2. `ai-virtual-agent` implements AI application and model integration, but its
   tracked source has no KubeVirt or VirtualMachine integration.
3. Triforce deploys VM and AI-shaped resources, but its claimed VM-to-AI proof
   is not executed from inside the guest by the automated tests.
4. Triforce's checked-in 501 content is mainly observation of a preconfigured
   deployment. This does not earn the factory roadmap's 501 outcome and does
   not yet earn 201.
5. Quantitative Triforce claims about resource use, cost, hardware, and
   utilization are often authored constants rather than current-session
   infrastructure evidence. They are excluded from this candidate.

## Independent learner outcome

After the 60–75 minute lab, the learner can:

- identify the VM/VMI, Service, adapter, model, and human-authority boundaries;
- originate a versioned request inside the VM and follow one correlation ID;
- distinguish connectivity proof from AI participation and output validation;
- compare the healthy path with a controlled unavailable-model condition;
- export a claim-to-evidence map that states what was and was not proven.

The learner does not create the API, Service, identity, or NetworkPolicy in
101. That construction work belongs to the future 201 lab.

## AI necessity

AI is required only for the bounded interpretation of an unstructured
operations note. Coexistence, DNS, Service selection, placement, health, and
failure detection are deterministic platform behavior. The model is advisory,
has no tools or action authority, receives only the synthetic note and task
instruction, and must return schema-valid output with observable model and
source identity. Invalid or unavailable output fails closed.

## Activation blockers

- Select the supported OpenShift and OpenShift Virtualization release pair.
- Select and pin the Linux AMD64 guest image and access method.
- Confirm a governed Intel Xeon CPU inference endpoint and observable hardware
  identity contract.
- Provide credentials only through a runtime Secret reference.
- Execute one complete development-cluster journey from inside the VM.
- Measure per-seat resources, readiness, requests, tokens, and cleanup.
- Build and verify immutable workload, presentation, and content artifacts.
- Complete independent Launchpad intake and certification after factory gates.

## Review boundary

This report approves implementation of a candidate. It does not certify a live
runtime, catalog item, image, capacity claim, or orderable lab.
