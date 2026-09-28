# Rehearsal checklist

## Endpoint and evidence

- [ ] Health endpoint names the adapter mode without exposing credentials.
- [ ] Healthy proof starts inside the VM and returns one correlation ID.
- [ ] Response contains model identity, hardware identity, and validation state.
- [ ] Unavailable condition returns `ai_participated: false` and no advisory output.
- [ ] Evidence endpoint returns only redacted current-session records.
- [ ] Fixture responses display `REHEARSAL` or `OFFLINE` before interpretation.

## Presentation

- [ ] Presenter path completes in 5–7 minutes with seven or fewer scenes.
- [ ] Every internal architecture reveal is exercised.
- [ ] Healthy and unavailable proof conditions remain visible together.
- [ ] The payoff uses only current-session proof state or says proof was not run.
- [ ] `Close presentation` precedes the lab handoff.
- [ ] Fullscreen, presenter prompts, deep links, keyboard, touch, and reduced motion work.
- [ ] Every desktop state fits at 1920×1080 and 1440×900 without scrolling.
- [ ] Narrow rehearsal view remains usable.

## Lab

- [ ] All commands run from a clean checkout in a disposable namespace.
- [ ] The learner can resume after a browser or terminal restart.
- [ ] Secret values never appear in Showroom variables, logs, or evidence exports.
- [ ] Expected observations and failure states match the contracts.
- [ ] Evidence-map export is created and contains no secret or raw prompt data.
- [ ] Reclaim leaves zero candidate resources.

## Factory evidence

- [ ] Linux AMD64 workload and presentation images are digest-pinned.
- [ ] SBOM, signature, provenance, vulnerability, and exact-digest pull receipts exist.
- [ ] Per-seat CPU, memory, pods, storage, model requests/tokens, readiness, and cleanup are measured.
- [ ] Launchpad handoff retains `orderable: false`, `certified: false`, and `promotion_eligible: false`.
