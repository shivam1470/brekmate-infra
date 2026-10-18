# Official documentation consulted 18 October 2026
https://opentofu.org/docs/language/syntax/json/ — .tf.json is supported IaC syntax.
https://opentofu.org/docs/v1.10/language/settings/backends/s3/ — native use_lockfile and versioned state.
https://opentofu.org/docs/v1.12/cli/commands/test/ — mocked provider/plan testing.
https://github.com/opentofu/opentofu/releases/tag/v1.12.6 — pinned CLI and official checksums.
https://registry.terraform.io/providers/hashicorp/aws/6.69.1/docs — pinned provider source/schema.
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis-iam.html
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html
https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html
https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html
https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa-totp.html

Versions are pinned, not claimed permanently latest. Revalidate current runtime/provider support before actual deployment. Provider installation signing warnings and local execution limitations are recorded in STATUS.md; do not disable verification or change checksums merely to silence a failure.
