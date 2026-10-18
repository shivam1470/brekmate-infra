# Cost model — Mumbai pilot, no zero-cost guarantee

Architecture minimises idle compute: no EC2, NAT, RDS, load balancer or provisioned Lambda/Dynamo capacity. On-demand database capacity still bills requests, data, backups and indexes. Three tables have PITR enabled. Two Secrets Manager containers per environment can add an ongoing baseline. Cognito tier/MAU, logs/alarms, static storage, transfer, S3 state, notifications and optional budgets can add charges. Staging retained data/auth/secret resources are NOT free just because runtime is disabled.

Use examples/cost-inputs.json and scripts/cost.py. Price values are deliberately unset unless grounded in the accompanying dated regional AWS price extract. The calculator refuses to call an estimate complete while rates are missing. Populate quotes from the official ap-south-1 price lists, including tiering, unit size and effective dates. Do not reuse US-region prices as Mumbai prices.

Pilot sizing assumption for discussion: 100 orders/day, 30 days, 20 customer/staff API calls per order = 60,000 requests/month before polling, browsing, retries, background jobs and monitoring. At 256 MiB and 250 ms average Lambda duration this is 3,750 GB-seconds, not a guaranteed observed workload. DynamoDB transactions consume more request units than simple operations; indexes and item sizes matter. Model data storage, PITR and logs separately. Multiply retained environment baselines appropriately.

A provisional budgeting allowance of US$5–20/month for a small pilot is an engineering allowance, NOT a current regional quote, cap or promise. It excludes SMS, payment processing, heavy media/traffic, domains, staff effort, native-store fees and paid CI/cloud builds. Actual use can exceed it.

Eligible credits reduce cash payable temporarily; underlying usage remains tracked. Verify account eligibility/expiry in Billing. Existing-customer eligibility is not established by creating another account. Budgets alert rather than enforce a spending cap. Activate cost tags and add an account-wide budget to catch untagged services.

Official sources:
https://aws.amazon.com/lambda/pricing/
https://aws.amazon.com/api-gateway/pricing/
https://aws.amazon.com/dynamodb/pricing/on-demand/
https://aws.amazon.com/secrets-manager/pricing/
https://aws.amazon.com/cloudwatch/pricing/
https://aws.amazon.com/cloudfront/pricing/
https://aws.amazon.com/cognito/pricing/
https://aws.amazon.com/free/free-tier-faqs/

## Retrieved regional price evidence
The accompanying regional-price-evidence.json records source URLs, publication dates, effective dates, SKUs, units and tiers. The first-tier Mumbai HTTP API rate retrieved was US$1.05/million; Lambda request US$0.20/million and ARM compute US$0.0000133334/GB-second; standard DynamoDB US$0.71/million WRU and US$0.1425/million RRU, paid-tier storage US$0.285/GB-month and PITR US$0.228/GB-month; Secrets Manager US$0.40/secret-month. These are service-specific rates, not an all-in quote. Examples populate only those rates, deliberately leaving unknown logs/alarms/transfer blank. Eligibility, free allowances, taxes and communications must be assessed separately. Re-fetch current price lists before purchasing.
