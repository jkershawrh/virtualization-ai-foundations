# Packaging evidence

## Published immutable candidates

Release source revision: `7d0d88d61dcfa1a1ab97f7d187249c7fc29f13da`

Workflow run:
[`36473568680`](https://github.com/jkershawrh/virtualization-ai-foundations/actions/runs/36473568680)
(`success`)

| Component | Exact GHCR Linux/AMD64 digest | Complete Grype 0.97.1 inventory | Hard gate |
| --- | --- | --- | --- |
| Adapter | `ghcr.io/jkershawrh/virtualization-ai-foundations-adapter@sha256:429d27ecd1eaaec98be8e8d252925fe8dd6b0f525d0c5f06f65d1a6adba6d9a9` | 6 MEDIUM; 0 HIGH; 0 CRITICAL | PASS |
| Presentation | `ghcr.io/jkershawrh/virtualization-ai-foundations-presentation@sha256:fb4869e465beb513636ad574d9ee1974d82431b226099e6d8933f24263b9d61c` | 4 MEDIUM; 0 HIGH; 0 CRITICAL | PASS |

The release gate includes every HIGH and CRITICAL finding, whether fixable or
not. Both images were pulled back from GHCR by exact digest and checked for
`linux/amd64` plus the expected source-revision label. GitHub OIDC signatures,
SPDX attestations, and custom source/build provenance attestations were created
and verified against the release workflow identity.

Complete scan inventories, SPDX SBOMs, digest records, provenance, and
verification output are retained as workflow artifacts for 90 days. Their
artifact names and SHA-256 values are recorded in
`handoff/evidence/published-adapter-release.json` and
`handoff/evidence/published-presentation-release.json`.

## Earlier local-only candidates

Source revision: `68e3980d0a1df4ff20d36e6e76f8518781345239`

| Component | Linux/AMD64 image digest | OCI archive SHA-256 | Trivy 0.74.0 |
| --- | --- | --- | --- |
| Adapter | `sha256:b55c096b006610e0c910ef133cbf0992bf24140ab872f233588a8420855e18ec` | `5f6b9b044a17cffcbf3d43a8cb75fa0f7fa17ea49e25594b9f4c2af793f57b5f` | 0 detected vulnerabilities |
| Presentation | `sha256:85bd11634e59e565ab882d21fc70274fa133712ca5afbc5ea2c29e20f82b2df5` | `bb37d872266d093d6ba3a0e4713ec62aeefd1c1b75ca7491facdf6a12be9434d` | 0 detected vulnerabilities |

CycloneDX SBOM SHA-256 values:

- adapter: `313925383925e5e2a10c4ad587a104b8a8b210bda1d652cc6ed627ceb31b3591`
- presentation: `2d3f09a354847e7ea7518011b226d2affe2d3b138f7a7f5f2ba1b99895990cfd`

The presentation and adapter passed a local container smoke test through the
presentation reverse proxy in `REHEARSAL` mode. The local smoke containers and
network were removed afterward.

The OCI archives, scan reports, and SBOM files remain untracked under
`artifacts/`; their hashes are recorded in the checked-in release receipts.
They are immutable local candidates, not published releases.

These receipts are historical local evidence. They do not describe the newer
GHCR images and cannot establish registry publication, signing, or attestation.

## Remaining qualification gates

- Approve GHCR as the Launchpad destination and approve evidence retention and
  rollback policy.
- Run the VM-origin journey on an approved OpenShift release and managed Intel
  Xeon CPU model endpoint.
- Measure one-, five-, and twenty-five-seat behavior and prove OpenShift
  reclaim leaves zero residue.
- Complete Launchpad trusted-render, artifact, certification, review, and
  promotion gates.

No published-image result is a certification claim or evidence that the live
OpenShift journey has run.
