# Operator guide — commands below were NOT run against AWS

## Local verification
Install OpenTofu 1.12.6, Python 3, and provider dependencies, then:
```
python3 -m unittest discover -s tests -v
python3 scripts/check.py
```
The first validates source/plan policy logic. The second also initializes with backend disabled, validates AWS provider schemas, and runs mocked PLAN tests. Every supplied .tftest.hcl run uses command=plan and mock_provider; do not change these to live apply tests casually. Initializing downloads tools/providers but does not deploy AWS infrastructure. See STATUS.md for the observed environment limitations.

## Account prerequisites
Use an AWS account with MFA/short-lived operator credentials and billing access, not root access keys. Decide email/SRP versus phone OTP, verify the proposed DynamoDB access model, choose real environment/account IDs, confirm quotas and activate Project/Environment cost allocation tags. Configure alarm recipients explicitly. Staging and production can be in one account initially, but names/state keys/roles remain separate; separate accounts offer stronger isolation when affordable and operationally supported.

## Bootstrap: one-time, separately reviewed
1. Copy bootstrap/example.tfvars.json to a private local file and set the actual permitted account ID/region. Exact optional GitHub repositories only; leave empty if not using CI yet.
2. Authenticate through your approved operator role, verify `aws sts get-caller-identity` matches that account.
3. From bootstrap: `tofu init`; `tofu plan -var-file=/absolute/private/bootstrap.tfvars.json -out=/absolute/private/bootstrap.tfplan`.
4. Review the bootstrap plan for state bucket, boundary and optional read-only plan roles. Only after a separate authorised deployment, run `tofu apply /absolute/private/bootstrap.tfplan`.
5. Capture output state_bucket and runtime_boundary_arn. Keep a protected backup of the initial local state.
6. Copy bootstrap/remote-backend.tf.example to bootstrap/remote-backend.tf, fill a private backend JSON from backend.example.json with output bucket and exact account, then run `tofu init -migrate-state -backend-config=/absolute/private/bootstrap-backend.json`. Confirm state list and S3 object/version/locking. Never use -force-copy or -lock=false to silence a conflict.
7. Once remote migration and recovery copy are confirmed, remove unsecured transient state copies according to your retention procedure. Do not destroy bootstrap during staging cleanup.

## Environment plan
Copy the relevant example.tfvars.json and backend.example.json into a PRIVATE working directory. Configure actual account, exact environment state key, region and bootstrap bucket. Leave app enable flags false until actual ZIP artifacts and route contracts exist.
```
python3 scripts/plan.py staging --vars /absolute/private/staging.tfvars.json --backend /absolute/private/staging-backend.json
```
The script checks caller account, environment and backend safeguards, prepares a sensitive saved plan and applies partial plan policies. It NEVER applies. Inspect the plan, providers, IAM, cost and unresolved values; the policy scanner is not a full security audit. A separately authorised operator can use `tofu -chdir=environments/staging apply /absolute/path/review.tfplan` after rechecking the saved plan hash, account, state lock and freshness. Never apply JSON; apply the saved binary plan.

For production repeat using the production root/key/role. Real staging integration, rollback and restore rehearsal are prerequisites. Configuring `auto_deploy=true` on the HTTP stage controls route publication only after an authorised IaC apply; it is not permission to run unattended deployments.

## Application integration
Enable backend only after supplying actual ZIP, handler, boundary ARN, immutable deployment_label and real API route -> customer/staff/public mappings. The default route map is empty and no catch-all anonymous route is created. Native clients need backend issuer/client/token-use verification; staff browsers need exact HTTPS CORS origins, not wildcard CORS. Seed real secret values through approved secret tooling outside OpenTofu.

Code/alias changes are owned by OpenTofu through source_code_hash and published versions. Do not concurrently call update-function-code from another pipeline. Static staff assets are published separately to the output bucket after reviewing a real build; see scripts/publish_staff.py. Domain-free CloudFront HTTPS is provided; custom domain/ACM/DNS automation is out of scope until ownership is supplied. Native signing/store submission is separate.

## Cleanup and rollback
Do not run `tofu destroy` against bootstrap or durable environment roots. Stage retirement means preparing a normal staging plan with backend_enabled=false, worker_enabled=false and web_enabled=false; review resource deletions. Data, identities and secret containers remain. A versioned web bucket with objects cannot be deleted while force_destroy=false; retain it or separately review bounded object/version deletion. No automatic data purge is supplied.

For code rollback select a previously verified artifact, produce/review a new plan and update the live alias through IaC. For web rollbacks republish the prior approved bundle. Preserve API backwards compatibility and use expand/contract data migrations; no automatic destructive schema rollback.
