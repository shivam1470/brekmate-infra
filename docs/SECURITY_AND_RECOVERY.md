# Security, IAM and recovery

## State
S3 backend uses encrypt=true, use_lockfile=true, versioning, TLS-only policy and public-access blocking. SSE-S3 avoids a separate paid KMS key for the pilot; customer-managed keys are an explicit later decision. Native S3 conditional locking is supported by the pinned OpenTofu version. Do not add a DynamoDB state-lock table just to copy an old example. Test actual concurrent lock contention in staging; never force-unlock an active process. Bootstrap and environment keys are isolated.

prevent_destroy is a configuration safeguard, not an account-wide guarantee: removing configuration can remove that protection. AWS deletion protection also protects production DynamoDB and Cognito, while state versioning/recovery and operator permissions matter independently. Existing bucket/version lifecycle must not automatically purge current state history. Treat saved plans, state and local provider trace logs as sensitive; exclude from Git/Drive bundles and restrict retention/access.

## Roles
Runtime roles have a bootstrap-managed boundary and narrower environment-specific inline permissions, exact table/secret/queue scopes and per-function log paths. No AWS credentials in mobile/web bundles. api sends messages; worker consumes only its queue. API Gateway invokes the live alias from its own account/execution ARN. Staff roles/groups and data ownership still require backend enforcement.

GitHub OIDC plan roles are optional, read-only toward application infrastructure, with exact repository/environment subjects and sts.amazonaws.com audience. They can read the environment state and create/delete ONLY its lock object. State contents remain sensitive even for a plan role. CloudFront and discovery metadata include documented account-global read scopes; no GetSecretValue or application item reads are granted to CI. Actual AWS refresh permissions still need staging verification.

No catch-all AdministratorAccess or unreviewed infrastructure apply policy is created. Cloud apply uses a separately approved short-lived operator role. Automated infra-write OIDC requires a reviewed environment-scoped apply policy and protected GitHub environments; it is deliberately not inferred from unseen account resources. This is an external deployment prerequisite, not a claim that all CI permissions are finished.

Require branch/reviewer protection on the GitHub environments named staging/production before enabling OIDC trust. An environment subject does not independently restrict branches; GitHub environment rules must do that. Do not run untrusted PR code with AWS write credentials. Verification workflows use read-only contents and no id-token. Manual cloud-plan workflow is disabled unless an explicit repository variable enables it.

## Identity/secrets
Staff TOTP enrollment is operational work. Email/SRP is proposed; phone-only signup and production SMS are NOT implemented. Default Cognito email service has quotas. Check token signature, issuer, audience/client ID, token_use, expiry and role/object permissions on the backend. Gateway JWT validation alone is not sufficient for all business authorisation or immediate session revocation. Account deletion/retention and refresh-token handling require actual application code.

Secret containers have recovery windows, but no secret values or credentials are generated/stored by IaC. Populate/rotate values outside OpenTofu. Avoid retrieving those values during planning. Payment webhook authenticity, idempotency and financial reconciliation belong in application code.

## Monitoring
Logs have bounded retention (7-day staging/30-day production proposals). Gateway logs omit request bodies, tokens and customer contacts. Backend must implement redaction; infrastructure cannot guarantee clean application logs. Alarm topic is restricted to matching CloudWatch alarm source/account and contains only non-sensitive operational metrics. It intentionally does not use alias/aws/sns encryption, which can require extra publisher key-policy work; customer-managed SNS encryption is a reviewed option. Configure/confirm email subscriptions and actually test delivery. No recipients are supplied now.

Budget notifications use activated cost-allocation tags and optional email. They can miss untagged/shared spend and are not hard caps; add an account-wide budget operationally. No budget or recipient is silently enabled without configuration.

## Recovery rehearsal
PITR is enabled for all data tables; its storage is billed. In isolated staging, restore a chosen timestamp into NEW table names, reconcile ledger totals/order invariants, verify permissions/indexes and repoint a test backend. Restores create new resources and are NOT run here. Keep application backups and provider/gateway reconciliation records according to an approved retention policy. Approve recovery targets before claiming an RPO/RTO.
