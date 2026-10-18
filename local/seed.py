"""Create empty local tables only. Never points AWS CLI at AWS endpoints."""
import argparse,subprocess,json
p=argparse.ArgumentParser();p.add_argument('--endpoint',default='http://127.0.0.1:8000');a=p.parse_args()
if a.endpoint not in ['http://127.0.0.1:8000','http://localhost:8000']:raise SystemExit('Only loopback DynamoDB endpoint allowed')
import os
env={**os.environ,'AWS_ACCESS_KEY_ID':'localonly','AWS_SECRET_ACCESS_KEY':'localonly','AWS_DEFAULT_REGION':'ap-south-1','AWS_EC2_METADATA_DISABLED':'true'}
for name in ['core','ledger','operations']:
 table='brekmate-local-'+name
 args=['aws','--endpoint-url',a.endpoint,'dynamodb','describe-table','--table-name',table]
 r=subprocess.run(args,env=env,capture_output=True,text=True)
 if r.returncode==0:print('Exists',table);continue
 if 'ResourceNotFoundException' not in r.stderr:raise SystemExit(r.stderr)
 create=['aws','--endpoint-url',a.endpoint,'dynamodb','create-table','--table-name',table,'--billing-mode','PAY_PER_REQUEST','--attribute-definitions','AttributeName=pk,AttributeType=S','AttributeName=sk,AttributeType=S','AttributeName=gsi1pk,AttributeType=S','AttributeName=gsi1sk,AttributeType=S','--key-schema','AttributeName=pk,KeyType=HASH','AttributeName=sk,KeyType=RANGE','--global-secondary-indexes',json.dumps([{'IndexName':'gsi1','KeySchema':[{'AttributeName':'gsi1pk','KeyType':'HASH'},{'AttributeName':'gsi1sk','KeyType':'RANGE'}],'Projection':{'ProjectionType':'ALL'}}])]
 subprocess.run(create,env=env,check=True)
print('Empty local tables created. Auth/payments/notifications are application adapters, not emulated AWS guarantees.')
