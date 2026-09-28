# Source-bound immutable release

`.github/workflows/release-images.yml` accepts only an exact 40-character commit
SHA. The workflow refuses dispatch/source drift, reruns the complete local gate,
and independently builds the presentation and adapter for `linux/amd64` without
cache.

For each image it:

1. retains a complete vulnerability inventory;
2. fails on every detected HIGH or CRITICAL vulnerability, including findings
   with no published fix;
3. generates an SPDX JSON SBOM;
4. publishes a commit-specific image to GHCR only after the gates pass;
5. removes the tag locally and proves an exact-digest pull has the expected
   architecture and source-revision label;
6. signs the digest with GitHub OIDC;
7. attaches SBOM and source/build provenance attestations;
8. verifies the expected workflow identity, signature, and both attestations;
9. retains scan, SBOM, digest, provenance, and verification files for 90 days.

Every external GitHub Action is pinned to a full commit SHA. `publish=false`
runs the validation, build, scan, and SBOM gates without changing GHCR.

The checked-in `values.candidate.yaml` and local artifact receipts describe the
local OCI candidates. They must not be treated as published evidence.
`values.published.yaml` and the `published-*-release.json` receipts separately
record the GHCR digest identities and successful workflow run that produced and
verified them.

The first strict run correctly stopped before publication after full scans
found HIGH vulnerabilities in the original runtime bases. Runtime hardening was
then committed without weakening the gate. Run
[`36473568680`](https://github.com/jkershawrh/virtualization-ai-foundations/actions/runs/36473568680)
built exact source revision `7d0d88d61dcfa1a1ab97f7d187249c7fc29f13da`,
published both hardened images, verified exact-digest pulls, and verified their
GitHub OIDC signatures plus SPDX and provenance attestations.

This release pipeline does not certify the lab. It does not replace live
OpenShift qualification, managed model/Intel Xeon placement evidence, capacity
tests, reclaim evidence, Launchpad review, or promotion authority.
