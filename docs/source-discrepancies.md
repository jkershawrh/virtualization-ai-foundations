# Source discrepancy inventory

| ID | Evidence | Finding | Candidate treatment |
|---|---|---|---|
| D-001 | `triforce/content-501/modules/ROOT/pages/` | Content is labeled 501 but asks learners mainly to inspect a prebuilt environment. | Assign 101; exclude the old level label. |
| D-002 | `triforce/tests/test_virt_edge.py` | `test_scada_calls_bitnet_sidecar` calls the Service from the test harness, not inside the VM. | Require a guest-origin receipt and shared correlation ID. |
| D-003 | `triforce/tests/test_virt_edge.py` | `test_scada_sensors_configured` ends with unconditional `pass`. | Add an asserted VM client and evidence contract. |
| D-004 | `triforce/demo/engineer/triforce_virt_demo.py` | The presenter process calls the AI endpoint and then states that the VM can reach it. | Never infer VM reachability from an external call. |
| D-005 | Triforce presentation and 501 content | CPU, memory, utilization, cost, hardware-count, and migration claims are authored constants. | Exclude them; display only current-session adapter values. |
| D-006 | `triforce/tests/test_virt_edge.py` | The cost test is `assert True`. | Make no cost claim. |
| D-007 | Triforce Helm values/templates | Images use mutable tags; VM cloud-init contains default passwords. | Require digest pins and Secret/SSH-key access before release. |
| D-008 | `ai-virtual-agent` tracked source | No KubeVirt or VirtualMachine integration exists. | Reuse API and validation ideas only. |
| D-009 | `ai-virtual-agent/docs/virtual-agents-architecture.md` and implementation | Documentation describes older agent persistence and route names; implementation stores virtual agents locally under `/api/v1`. | Treat implementation and tests as authoritative. |
| D-010 | `ai-virtual-agent/docs/semantic-routing.md` | Semantic routing is optional, disabled by default, and the explored threshold is not independently validated. | Exclude routing and threshold claims from 101. |
| D-011 | Roadshow `README.adoc` and navigation | The source is a broad seven-module event rather than a focused VM-to-AI lab. | Reuse only VM/Service/DNS/network learning patterns. |
| D-012 | Cross-source inventory | No repository contains a qualifying integrated runtime receipt. | Implement a new contract-first workload and mark proof future-state until run. |
| D-013 | Cross-source packaging | No shared immutable image, SBOM, signature, provenance, scan, capacity, or zero-residue receipt exists for this new scope. | Produce new factory evidence; Launchpad re-verifies independently. |
