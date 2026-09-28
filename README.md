# Virtualization + AI Foundations

An independent Red Hat × Intel level-101 candidate that teaches learners to
trace one request from an application inside an OpenShift Virtualization VM,
through an OpenShift Service and validation adapter, to governed Intel Xeon CPU
inference and back to a human decision owner.

This repository is a new catalog scope. It is not a migration or repackaging of
the 2026 virtualization roadshow, Triforce Virt, or `ai-virtual-agent`.

## What is included

- a seven-scene, evidence-led React presentation;
- a separate 60–75 minute Showroom lab;
- versioned request, response, evidence, and OpenAPI contracts;
- a standard-library Python adapter with `LIVE`, `REHEARSAL`, and `OFFLINE`
  source state;
- a Helm chart for the VM, Service, adapter, presentation, Route, and
  NetworkPolicies;
- healthy and controlled-unavailable proof paths;
- explicit human-only action authority; and
- factory tests, visual baselines, image receipts, and a draft Launchpad
  handoff proposal.
- a source-revision-bound GitHub Actions workflow for strict scanning, GHCR
  publication, keyless signing, SBOM/provenance attestations, and verification.

The default deployment is `rehearsal` and contains no secret. A live deployment
must provide an approved OpenAI-compatible model endpoint, model identity,
provider identity, the declared `Intel Xeon CPU` hardware class, and a
credential through a referenced Secret. Missing identity or invalid output
cannot produce a live AI claim.

## Verify the candidate

Requirements: Node.js 22+, Python 3.9+, Helm 3, and Playwright Chromium for the
browser gate.

```sh
npm ci
npm run check
npm run test:visual
```

`npm run check` validates the reviewed blueprint, runs the Python contract and
workload tests, lints and renders the Helm chart, runs the presentation tests,
builds the static site, and verifies offline fonts and logos.

## Run locally

Start the evidence adapter in one terminal:

```sh
ADAPTER_PORT=8088 ADAPTER_MODE=rehearsal python3 -m workload.app
```

Start the presentation in another:

```sh
npm run dev -- --host 127.0.0.1 --port 4179
```

The presentation proxy uses `http://127.0.0.1:8088` in development. If that
endpoint is absent or does not report `LIVE`, the UI uses checked-in,
conspicuously labeled rehearsal evidence.

## Deploy the chart

Development defaults use local tags for the two authored images. The
`values.candidate.yaml` overlay pins the built `linux/amd64` candidate digests.
Load its OCI archives into the target runtime or mirror the images into an
approved registry and change only the repository names.

```sh
helm upgrade --install virtualization-ai-101 \
  charts/virtualization-ai-foundations \
  --namespace virtualization-ai-101 \
  --create-namespace \
  -f charts/virtualization-ai-foundations/values.candidate.yaml \
  --set vm.sshAuthorizedKey='ssh-ed25519 REPLACE_AT_RUNTIME'
```

For live mode, create the runtime Secret outside source control and set the
model endpoint, identity, provider, and Secret reference. The VM never receives
the model credential.

## Earned level and next boundary

The source discovery supports 101: learners inspect, invoke, trace, explain,
exercise a controlled failure, and export a claim-to-evidence map. It does not
support 201 because none of the source experiences require the learner to
author and qualify the integration contract.

A separate future 201 must require learners to author or modify the versioned
contract, client configuration, Secret reference, Service, and NetworkPolicy;
prove allowed plus denied or unavailable behavior; and leave cleanup evidence.
This repository makes no performance, cost, capacity, autonomous-action,
migration-success, or certification claim.

## Evidence and authority

`demo-blueprint.yaml`, `story.brief.yaml`, and `tests/*.yaml` define the claim
and evidence boundary. The draft handoff keeps every authority flag false:
Launchpad must independently approve the source, render, artifacts, runtime,
capacity, reclaim behavior, certification, and promotion.

The immutable release workflow is documented in
`docs/immutable-release.md`. Local candidate digests and published GHCR digests
are recorded separately so a local build cannot be mistaken for publication
evidence.
