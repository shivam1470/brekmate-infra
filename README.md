# BrekMate OpenTofu foundation

Start with docs/OPERATIONS.md and docs/STATUS.md. Actual AWS resources have NOT been created. Configuration uses OpenTofu's supported JSON syntax (.tf.json). These are editable IaC source files, not deployed resource exports.

Proposal: Mumbai, Lambda + HTTP API, transactional DynamoDB, Cognito, private S3/CloudFront staff hosting, optional SQS worker. Persistent data/state is protected. Application hosting is disabled until real artifacts/routes and identity integration are supplied.

Run local policy tests: `python3 -m unittest discover -s tests -v`. With the pinned OpenTofu/provider available: `python3 scripts/check.py`. Read bootstrap, cost, identity and database decisions before an apply.

No credentials, customer data, real secret values or stub production handlers are supplied. Operator review and real staging verification remain necessary. Drive is a file copy, not an automatic Mac sync or CI runner.

## Coordinated review — 18 October 2026

Current findings, checks and release blockers: [release review](docs/release-2026-10-18/RELEASE_CHECKLIST.md). This review supersedes historical passing counts; no deployment or production approval is granted.
