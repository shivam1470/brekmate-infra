# Local development and verification boundaries

Requires Docker Compose and AWS CLI for local DynamoDB. Neither was present in this execution environment, so container startup and transaction integration tests were NOT run.
```
docker compose -f local/compose.yaml up -d
python3 local/seed.py
```
The database binds only to 127.0.0.1. seed.py accepts only loopback endpoints and forces dummy credentials. It creates empty tables; it does not seed fake customer data or call actual AWS. DynamoDB Local 3.1.0 is pinned to the Docker registry OCI index digest sha256:7ef4a2c45b58c2901e70a4f28e0953a422c2c631baaaf5e2c15e0805740c7752. Registry metadata listed linux/arm64 and linux/amd64. This confirms image identity/platform metadata, not successful container execution. Storage is in a named Docker volume. Do not use `down -v` if you need its data.

Application adapters must use DYNAMODB_ENDPOINT explicitly. No local backend, Cognito emulator, gateway, SMS sender or fake production Lambda handler is shipped because actual application source/contracts are unavailable. Use the real backend's local entrypoint when supplied and stub only provider boundaries for deterministic tests. DynamoDB-local transactions must be tested against actual application code.

Source-policy tests cover protected data, encryption, public access, environment targeting, boundaries, client secrecy and unsafe-plan rejection. The policy parser is partial, not a comprehensive IAM/security scanner. Mocked-plan tests verify configuration relationships without AWS; they do not establish API validity in AWS, effective IAM, provider delivery, Cognito emails, locking, restore or end-to-end functionality.

Connect the existing brekmate-quality adapters to real code. Its 36,864 basket combinations and 432 quote examples are not replaced or counted as IaC coverage. Real cloud verification is listed in tests/cloud-checklist.json. Test logs must distinguish local static, mocked plan and actual deployed results.
