"""Prepare an environment-specific plan using short-lived operator credentials. No apply."""
import argparse,json,subprocess,os,hashlib
from pathlib import Path
from policy import inspect
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('environment',choices=['staging','production']);p.add_argument('--vars',required=True);p.add_argument('--backend',required=True);a=p.parse_args()
if os.environ.get('TF_WORKSPACE','default') != 'default':raise SystemExit('Use explicit environment roots, not OpenTofu workspaces')
variables=json.loads(Path(a.vars).read_text());backend=json.loads(Path(a.backend).read_text());account=variables.get('aws_account_id','')
if len(account)!=12 or not account.isdigit() or account=='000000000000':raise SystemExit('Actual account ID required')
if variables.get('environment')!=a.environment:raise SystemExit('Variable environment mismatch')
if backend.get('key')!=a.environment+'/terraform.tfstate':raise SystemExit('Wrong state key')
if backend.get('allowed_account_ids')!=[account] or backend.get('encrypt') is not True or backend.get('use_lockfile') is not True:raise SystemExit('Unsafe backend settings')
identity=json.loads(subprocess.check_output(['aws','sts','get-caller-identity'],text=True))
if identity['Account']!=account:raise SystemExit('Credential/account mismatch')
root=ROOT/'environments'/a.environment;tofu=os.environ.get('TOFU_BIN','tofu')
subprocess.run([tofu,'init','-input=false','-backend-config='+str(Path(a.backend).resolve())],cwd=root,check=True)
current=subprocess.check_output([tofu,'workspace','show'],cwd=root,text=True).strip()
if current!='default':raise SystemExit('Non-default workspace detected; stop and review environment isolation')
os.umask(0o077)
out=ROOT/'reports/private'/a.environment;out.mkdir(parents=True,exist_ok=True,mode=0o700);out.chmod(0o700)
plan=out/'review.tfplan';subprocess.run([tofu,'plan','-input=false','-var-file='+str(Path(a.vars).resolve()),'-out='+str(plan)],cwd=root,check=True)
raw=subprocess.check_output([tofu,'show','-json',str(plan)],cwd=root);(out/'review.tfplan.json').write_bytes(raw)
errors=inspect(json.loads(raw),a.environment)
if errors:raise SystemExit('Plan rejected: '+json.dumps(errors))
(out/'review-metadata.json').write_text(json.dumps({'environment':a.environment,'account':account,'sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'applied':False},indent=2))
print('Plan prepared and policy-checked. Contains sensitive data. Inspect locally; no apply was performed.')
