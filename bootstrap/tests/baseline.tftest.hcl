mock_provider "aws" {}
variables { aws_account_id = "123456789012" }
run "baseline" {
  command = plan
  assert {
    condition     = aws_s3_bucket.state.force_destroy == false
    error_message = "State bucket must not be force-destroyed."
  }
  assert {
    condition     = aws_s3_bucket_versioning.state.versioning_configuration[0].status == "Enabled"
    error_message = "State history is mandatory."
  }
  assert {
    condition     = length(aws_iam_role.plan) == 0
    error_message = "CI roles must be opt-in with exact repositories."
  }
}
