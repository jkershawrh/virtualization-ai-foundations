# Packaging evidence

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

## Remaining release gates

- Mirror both images to an approved registry without changing their manifests.
- Verify an exact-digest pull from the destination.
- Sign the destination digests and attach provenance/SBOM attestations.
- Run the VM-origin journey on an approved OpenShift release and managed Intel
  Xeon CPU model endpoint.
- Measure one-, five-, and twenty-five-seat behavior and prove OpenShift
  reclaim leaves zero residue.
