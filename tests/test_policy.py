import unittest,sys,json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from policy import inspect
class PlanPolicies(unittest.TestCase):
 def plan(self,kind,after,actions=None,before=None):return {'resource_changes':[{'mode':'managed','type':kind,'address':'fixture.resource','change':{'actions':actions or ['create'],'after':after,'before':before}}]}
 def test_unknown_plan_rejected(self):self.assertTrue(inspect({},'staging'))
 def test_valid_table_accepted(self):self.assertFalse(inspect(self.plan('aws_dynamodb_table',{'billing_mode':'PAY_PER_REQUEST','deletion_protection_enabled':True,'point_in_time_recovery':[{'enabled':True}],'server_side_encryption':[{'enabled':True}]}),'production'))
 def test_missing_encryption_rejected(self):self.assertTrue(inspect(self.plan('aws_dynamodb_table',{'billing_mode':'PAY_PER_REQUEST'}),'production'))
 def test_replacement_of_ledger_rejected(self):self.assertTrue(inspect(self.plan('aws_dynamodb_table',{},['delete','create']),'production'))
 def test_state_deletion_rejected(self):self.assertTrue(inspect(self.plan('aws_s3_bucket',{},['delete'],{'bucket':'brekmate-state-123-ap-south-1'}),'staging'))
 def test_public_bucket_setting_rejected(self):self.assertTrue(inspect(self.plan('aws_s3_bucket_public_access_block',{'block_public_acls':False}),'staging'))
 def test_secret_client_rejected(self):self.assertTrue(inspect(self.plan('aws_cognito_user_pool_client',{'generate_secret':True}),'production'))
 def test_unbounded_logs_rejected(self):self.assertTrue(inspect(self.plan('aws_cloudwatch_log_group',{'retention_in_days':0}),'staging'))
 def test_missing_boundary_rejected(self):self.assertTrue(inspect(self.plan('aws_iam_role',{'name':'brekmate-staging-api-runtime'}),'staging'))
 def test_unknown_artifact_rejected(self):self.assertTrue(inspect(self.plan('aws_lambda_function',{}),'staging'))
 def test_unapproved_nat_rejected(self):self.assertTrue(inspect(self.plan('aws_nat_gateway',{}),'staging'))
 def test_data_reads_not_treated_as_resource_creates(self):self.assertFalse(inspect({'resource_changes':[{'mode':'data','type':'aws_caller_identity','change':{'actions':['read']}}]},'staging'))
class SourcePolicies(unittest.TestCase):
 def source(self,module):return json.loads((ROOT/'modules'/module/'main.tf.json').read_text())
 def test_all_json_parses(self):
  for f in ROOT.rglob('*.json'):
   if '.terraform' not in f.parts:json.loads(f.read_text())
 def test_durable_resources_protected(self):
  d=self.source('storage')['resource'];t=d['aws_dynamodb_table']['data'];self.assertTrue(t['lifecycle']['prevent_destroy']);self.assertEqual(t['billing_mode'],'PAY_PER_REQUEST');self.assertTrue(t['point_in_time_recovery'][0]['enabled'].startswith('${'));self.assertTrue(t['server_side_encryption'][0]['enabled']);self.assertEqual(t['deletion_protection_enabled'],'${var.production}')
  self.assertTrue(d['aws_secretsmanager_secret']['provider']['lifecycle']['prevent_destroy'])
 def test_no_secret_values_in_iac(self):
  for f in ROOT.rglob('*.tf.json'):
   self.assertNotIn('aws_secretsmanager_secret_version',json.loads(f.read_text()).get('resource',{}))
 def test_staff_signup_and_mfa(self):
  d=self.source('identity')['resource'];staff=d['aws_cognito_user_pool']['staff'];self.assertTrue(staff['admin_create_user_config'][0]['allow_admin_create_user_only']);self.assertEqual(staff['mfa_configuration'],'ON')
  for c in d['aws_cognito_user_pool_client'].values():self.assertFalse(c['generate_secret'])
 def test_private_origin_and_tls(self):
  d=self.source('staff-web')['resource'];self.assertTrue(all(d['aws_s3_bucket_public_access_block']['site'][k] for k in ['block_public_acls','block_public_policy','ignore_public_acls','restrict_public_buckets']));self.assertEqual(d['aws_cloudfront_origin_access_control']['site']['signing_behavior'],'always');self.assertEqual(d['aws_cloudfront_distribution']['site']['default_cache_behavior'][0]['viewer_protocol_policy'],'redirect-to-https')
 def test_runtime_boundary_and_no_vpc_costs(self):
  d=self.source('runtime')['resource'];self.assertEqual(d['aws_iam_role']['function']['permissions_boundary'],'${var.boundary_arn}');self.assertNotIn('vpc_config',d['aws_lambda_function']['function']);self.assertNotIn('aws_nat_gateway',d)
 def test_environment_isolation_and_account_guard(self):
  for env in ['staging','production']:
   d=json.loads((ROOT/'environments'/env/'main.tf.json').read_text());self.assertEqual(d['provider']['aws']['allowed_account_ids'],['${var.aws_account_id}']);self.assertEqual(d['variable']['environment']['default'],env);self.assertFalse(d['variable']['backend_enabled']['default']);self.assertFalse(d['variable']['web_enabled']['default'])
 def test_ledger_has_no_update_or_delete_permission(self):
  d=self.source('runtime')['resource']['aws_iam_role_policy']['function']['policy'];ledger=d[d.index('var.table_arns.ledger')-160:d.index('var.table_arns.ledger')];self.assertNotIn('dynamodb:DeleteItem',ledger);self.assertNotIn('dynamodb:UpdateItem',ledger)
 def test_no_iam_admin_or_public_runtime_url(self):
  alltext='\n'.join(f.read_text() for f in ROOT.rglob('*.tf.json') if '.terraform' not in f.parts);self.assertNotIn('AdministratorAccess',alltext);self.assertNotIn('aws_lambda_function_url',alltext)
if __name__=='__main__':unittest.main()
