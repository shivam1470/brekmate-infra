# Continue in local Codex

Open this directory as brekmate-infra next to the actual frontend/backend/quality repositories. Read README and docs/STATUS.md first. Preserve existing work.

1. Run source-policy tests, then run the pinned OpenTofu checks on the Mac. Resolve provider installation/handshake warnings without disabling integrity verification. Review lockfile provenance.
2. Inspect actual backend persistence/runtime/auth and review docs/ARCHITECTURE.md. This package proposes DynamoDB/email-SRP, not an implemented phone-OTP backend. Revise the IaC if actual application needs differ; do not create conflicting resources just because these templates exist.
3. Wire actual backend/worker artifacts and route contracts; no fake handler should reach production. Confirm arm64/nodejs24.x compatibility. Populate secret values outside state.
4. Connect local DynamoDB and BrekMate quality adapters. Demonstrate actual transactional invariants before enabling cloud deployment.
5. Prepare bootstrap/staging plans only after account/region/auth/cost choices are confirmed. No AWS resources were created here. Execute cloud commands only in a separately authorised deployment step, then complete cloud-checklist.json and record evidence.

GitHub writes were previously denied in this chat. These files are stored in Google Drive, not pushed or automatically synced to this Mac. No CI job or cloud workflow has run just because workflow files are supplied.
