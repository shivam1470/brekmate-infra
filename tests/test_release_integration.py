import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class BackendIntegration(unittest.TestCase):
 def source(self,path):return json.loads((ROOT/path).read_text())
 def test_runtime_configuration_and_reserved_bindings(self):
  r=self.source('modules/runtime/main.tf.json')
  self.assertIn('application_environment',r['variable'])
  self.assertIn('var.application_environment',r['resource']['aws_lambda_function']['function']['environment'][0]['variables'])
  self.assertIn('CORE_TABLE',r['variable']['application_environment']['validation'][0]['condition'])
 def test_delivery_secret_and_environment_wiring(self):
  s=self.source('modules/storage/main.tf.json')
  self.assertIn('delivery-otp',s['resource']['aws_secretsmanager_secret']['provider']['for_each'])
  for env in ['staging','production']:
   r=self.source(f'environments/{env}/main.tf.json')
   self.assertIn('OTP_SECRET_ARN',r['module']['runtime']['application_environment'])
 def test_route_inventory_matches_backend(self):
  backend=ROOT.parent/'brekmate-be/integration/api-routes.tfvars.json'
  if not backend.exists():self.skipTest('Coordinated route parity requires sibling brekmate-be; not release evidence')
  expected=json.loads(backend.read_text())
  actual=self.source('examples/api-routes.tfvars.json')
  self.assertEqual(actual,expected)
 def test_staff_csp_explicit_connection_origins(self):
  d=self.source('modules/staff-web/main.tf.json')
  self.assertIn('connect_origins',d['variable'])
  csp=d['resource']['aws_cloudfront_response_headers_policy']['site']['security_headers_config'][0]['content_security_policy'][0]
  self.assertTrue(csp['override'])
  self.assertIn('connect-src',csp['content_security_policy'])
  self.assertIn('var.connect_origins',csp['content_security_policy'])
  self.assertNotIn('connect-src *',csp['content_security_policy'])
