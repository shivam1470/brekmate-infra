mock_provider "aws" {
  mock_data "aws_caller_identity" {
    defaults = { account_id = "123456789012" }
  }
}
variables {
  aws_account_id = "123456789012"
}
run "baseline" {
  command = plan
  assert {
    condition     = module.storage.table_names.core == "brekmate-production-core"
    error_message = "Core table must be environment isolated."
  }
  assert {
    condition     = output.environment == "production"
    error_message = "Wrong environment output."
  }
  assert {
    condition     = output.api_url == null && output.staff_url == null
    error_message = "No application can be deployed without supplied artifacts and explicit enable flags."
  }
}
run "reject_wildcard_cors" {
  command = plan
  variables { staff_origins = ["*"] }
  expect_failures = [var.staff_origins]
}
