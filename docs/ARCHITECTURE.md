# Architecture decision: low-idle-cost pilot

## Available evidence
Only the Figma Make prototype and the quality workspace were supplied. No actual backend, build ZIP, AWS account, domain, provider credentials or GitHub infra checkout is available here. Selection is a reviewable proposal, not a compatibility claim about unseen code.

## Selected proposal
- Region default ap-south-1 (Mumbai), configurable and account-guarded.
- One modular TypeScript backend as Lambda behind API Gateway HTTP API. No microservices or VPC/NAT baseline. Runtime proposes Node.js 24/arm64; bundle native dependencies for the actual target and verify backend compatibility.
- Three on-demand DynamoDB tables: core domain records; ledger; short-lived operations/idempotency. pk/sk plus gsi1 allow explicit access patterns. Core holds orders/menu/stock/customer/address/reservation/configuration, not a fixed final single-table schema.
- Separate customer and staff Cognito pools and public SRP clients; staff self-signup disabled, TOTP required, role groups. This email/password proposal is NOT the prototype phone-OTP experience. Decide authentication before creating pools because username settings can force replacement; protection deliberately blocks careless replacement.
- Private S3 origin + CloudFront OAC for ONE staff SPA bundle containing cafe/admin/rider routes. No customer ordering website. Actual build output is not supplied. Viewer routing rewrites extensionless paths; no fabricated build files are published.
- Optional SQS worker and DLQ, enabled only with an actual worker artifact. No queues or unused worker compute by default.
- Secret containers only, SNS alarm topic, bounded logs and optional budget/email subscriptions.

## Database comparison
DynamoDB trades cheap idle capacity and native conditional/transactional writes for access-pattern design and limited ad-hoc joins/reporting. PostgreSQL offers relational constraints/reporting but requires a reviewed managed hosting/proxy/backup/connection strategy and an underlying idle cost. The user's PostgreSQL familiarity is useful, but credits alone do not settle architecture. If actual backend code uses SQL, STOP integration and revise this decision; do not pretend DynamoDB is a drop-in replacement or provision two databases.

## Required application invariants
Use TransactWriteItems and conditional writes across order/stock/wallet/ledger/idempotency records; IAM uses underlying item operation permissions plus ConditionCheckItem. Never split a financial transaction into unrelated eventually consistent writes. Uniqueness is enforced by deterministic keys and conditions. Reservation exclusion needs an agreed duration/buffer and atomic lock/slot model; infrastructure cannot infer overlaps from arbitrary timestamps. TTL is asynchronous cleanup, never an expiry, stock release or reservation correctness guarantee. Use server-time checks and explicit business transitions.

The ledger role cannot UpdateItem/DeleteItem, but PutItem can still overwrite without a condition. Application code must use attribute_not_exists/conditional transaction rules. IAM is not an immutable ledger proof. Admin reporting needs explicit aggregate/index patterns; the runtime has no full-table Scan permission.

## Deliberately not provisioned
Kubernetes, NAT, always-on SQL, Redis, multi-region replication, API keys/WAF claims for HTTP API, photo galleries, WhatsApp automation, SMS sender infrastructure, custom domains/certificates or native store signing. These need specific requirements and cost decisions.
