"""Fail-closed checks for an actual `tofu show -json` saved plan. No AWS calls."""
import json
from pathlib import Path
RULES=json.loads((Path(__file__).resolve().parents[1]/'policies/release-rules.json').read_text())
def inspect(plan, environment):
    errors=[]
    if environment not in ['staging','production']: return ['Unknown environment']
    if not isinstance(plan,dict) or 'resource_changes' not in plan: return ['Missing resource_changes; not a saved plan JSON']
    for change in plan['resource_changes']:
        if change.get('mode','managed')!='managed':continue
        kind=change.get('type');name=change.get('address','unknown');ch=change.get('change',{});actions=ch.get('actions',[]);after=ch.get('after') or {}
        if kind in RULES['forbiddenTypes']:errors.append(name+': unapproved baseline cost architecture')
        if 'delete' in actions and kind in RULES['protectedTypes']:errors.append(name+': protected data replacement/deletion')
        if 'delete' in actions and kind=='aws_s3_bucket' and ('state' in str((ch.get('before')or{}).get('bucket',''))):errors.append(name+': state bucket deletion')
        if actions==['delete']:continue
        if kind=='aws_dynamodb_table':
            if after.get('billing_mode')!='PAY_PER_REQUEST':errors.append(name+': unapproved provisioned capacity')
            if environment=='production' and after.get('deletion_protection_enabled') is not True:errors.append(name+': missing production deletion protection')
            pitr=after.get('point_in_time_recovery') or []
            if not pitr or pitr[0].get('enabled') is not True:errors.append(name+': PITR absent/unknown')
            enc=after.get('server_side_encryption')or[]
            if not enc or enc[0].get('enabled') is not True:errors.append(name+': encryption absent/unknown')
        if kind=='aws_s3_bucket_public_access_block':
            for key in ['block_public_acls','block_public_policy','ignore_public_acls','restrict_public_buckets']:
                if after.get(key) is not True:errors.append(name+': '+key+' absent/unknown')
        if kind=='aws_cognito_user_pool' and environment=='production' and after.get('deletion_protection')!='ACTIVE':errors.append(name+': unprotected production user pool')
        if kind=='aws_cognito_user_pool_client' and after.get('generate_secret') is not False:errors.append(name+': public app client must not have secret')
        if kind=='aws_cloudwatch_log_group' and (not isinstance(after.get('retention_in_days'),int) or after['retention_in_days']>90 or after['retention_in_days']<=0):errors.append(name+': retention absent/unbounded/unapproved')
        if kind=='aws_iam_role' and str(after.get('name','')).endswith('-runtime') and not after.get('permissions_boundary'):errors.append(name+': missing runtime boundary')
        if kind=='aws_lambda_function' and not after.get('source_code_hash'):errors.append(name+': missing immutable artifact hash')
        if kind=='aws_sqs_queue' and after.get('sqs_managed_sse_enabled') is not True:errors.append(name+': queue encryption missing')
    return errors
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('plan');parser.add_argument('--environment',required=True);args=parser.parse_args()
    errors=inspect(json.loads(Path(args.plan).read_text()),args.environment)
    print(json.dumps({'passed':not errors,'errors':errors},indent=2));raise SystemExit(bool(errors))
