"""Guarded staff bundle publisher. Default is S3 dry-run; --execute is explicit."""
import argparse,json,subprocess,os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('environment',choices=['staging','production']);p.add_argument('--dist',required=True);p.add_argument('--account',required=True);p.add_argument('--execute',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parents[1];dist=Path(a.dist).resolve()
if not(dist/'index.html').is_file():raise SystemExit('Actual built staff bundle required')
for f in dist.rglob('*'):
 if f.is_symlink():raise SystemExit('Symlink in build not permitted')
 if f.is_file() and (f.name.startswith('.env') or '.git' in f.parts):raise SystemExit('Private source file in bundle')
identity=json.loads(subprocess.check_output(['aws','sts','get-caller-identity'],text=True))
if identity['Account']!=a.account:raise SystemExit('Account mismatch')
tofu=os.environ.get('TOFU_BIN','tofu');outputs=json.loads(subprocess.check_output([tofu,'output','-json'],cwd=root/'environments'/a.environment,text=True))
if outputs['account_id']['value']!=a.account or outputs['environment']['value']!=a.environment:raise SystemExit('State/environment mismatch')
bucket=outputs['staff_bucket']['value'];distribution=outputs['staff_distribution']['value']
if not bucket or not bucket.startswith('brekmate-'+a.environment+'-'+a.account+'-'):raise SystemExit('Staff hosting not provisioned or wrong bucket')
cmd=['aws','s3','sync',str(dist),'s3://'+bucket,'--cache-control','public,max-age=300']
if not a.execute:cmd.append('--dryrun')
subprocess.run(cmd,check=True)
if a.execute:
 subprocess.run(['aws','s3','cp',str(dist/'index.html'),'s3://'+bucket+'/index.html','--cache-control','no-cache,no-store,must-revalidate','--content-type','text/html'],check=True)
 subprocess.run(['aws','cloudfront','create-invalidation','--distribution-id',distribution,'--paths','/index.html'],check=True)
print('Published' if a.execute else 'Dry-run only; no assets published')
