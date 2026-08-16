INSTALLATION AND RELEASE SECURITY GUIDELINES

This document describes a safe-by-default install policy and recommended release artifact workflow for maintainers and users.

Goals
- Make it easy for users to install pinned, auditable releases.
- Make it straightforward for maintainers to publish verifiable artifacts (tarballs, checksums, signatures).
- Avoid and discourage `curl | bash` patterns and other blind remote execution.

User install policy (safe-by-default)

1. Prefer pinned tags
   - Always install from a specific release tag (e.g. v1.2.3). Cloning a branch or using `main` is discouraged for production use.
   - Example:

     git clone --depth 1 --branch vX.Y.Z https://github.com/mrxsierra/omni-agent-skills.git
     cd omni-agent-skills

2. Verify release artifacts
   - Releases should publish a tarball and a checksum file (SHA256). Before extracting or running any installer, verify the checksum.

     # download tarball and checksum
     curl -fsSL -o ./omni-agent-skills-vX.Y.Z.tar.gz \
       https://github.com/mrxsierra/omni-agent-skills/archive/refs/tags/vX.Y.Z.tar.gz
     curl -fsSL -o ./sha256sums.txt \
       https://github.com/mrxsierra/omni-agent-skills/releases/download/vX.Y.Z/sha256sums.txt

     # verify
     sha256sum -c sha256sums.txt

   - If a single-checksum is known, you can verify directly:

     echo "<expected-sha256>  omni-agent-skills-vX.Y.Z.tar.gz" | sha256sum -c -

3. Prefer signature-based verification
   - SHA256 checksums are helpful but not sufficient on their own. Whenever possible verify a signature:
     - GPG: maintainers can sign the checksum file (sha256sums.txt.asc) and publish the public key (via a keyserver or GitHub key).
     - sigstore / cosign: artifacts can be signed via sigstore (recommended for cloud-native flows). Use cosign to verify signatures bound to a release.

   - Example (GPG):
     gpg --verify sha256sums.txt.asc sha256sums.txt

   - Example (cosign, using a local file):
     # verify that the artifact was signed (requires cosign installed)
     cosign verify-blob --key /path/to/pubkey.pem --signature omni-agent-skills-vX.Y.Z.tar.gz.sig \
       --blob omni-agent-skills-vX.Y.Z.tar.gz

Install script guidance (this repo)
- The included `install.sh` is intentionally conservative: it defaults to local installs and refuses to fetch remote artifacts without a pinned tag.
- Use `--local` to install from a checked-out copy. Use `--check --tag <tag> --sha256 <value>` to validate a downloaded tarball locally.
- Never run `curl | bash` without first downloading, inspecting, and verifying the artifact.

Maintainer workflow (outline)

1. Build release artifacts locally or in CI for the tagged commit.
2. Produce a compressed tarball: `omni-agent-skills-<tag>.tar.gz`.
3. Generate SHA256 checksum(s) and a checksum file `sha256sums.txt` containing exact filenames.
4. Sign the checksum file (GPG) or sign artifacts using sigstore/cosign. Store the public verification material in a well-known place (release notes, GitHub release attachments, or a key server).
5. Create a GitHub release for the tag and attach artifacts (`tar.gz`, `sha256sums.txt`, optional signatures).
6. Optionally rotate signing keys and document the signing key expiration/revocation plan.

Notes about secrets and automation
- CI/CD should use short-lived credentials (OIDC where possible) to push artifacts and sign with sigstore.
- Do not hardcode private keys or long-lived secrets in repository settings or workflows. Use GitHub Secrets or OIDC provider with restricted scopes.

Further reading
- sigstore / cosign: https://docs.sigstore.dev
- GPG signing basics: https://gnupg.org/documentation/

