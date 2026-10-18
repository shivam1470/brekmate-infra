import json,sys
from decimal import Decimal
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'examples/cost-inputs.json'
d=json.loads(p.read_text());r=d['rates'];missing=[k for k,v in r.items() if v is None]
if missing:print(json.dumps({'complete':False,'missingRates':missing,'region':d['region'],'cashAfterCredits':'not-assessed'},indent=2));raise SystemExit(1)
D=lambda x:Decimal(str(x));million=D(1000000)
parts={'api':D(d['requests'])/million*D(r['apiPerMillion']),'lambdaRequests':D(d['requests'])/million*D(r['lambdaPerMillion']),'lambdaCompute':D(d['requests'])*D(d['averageDurationSeconds'])*D(d['memoryGB'])*D(r['lambdaPerGBSecond']),'ddbWrites':D(d['writeRequestUnits'])/million*D(r['writePerMillion']),'ddbReads':D(d['readRequestUnits'])/million*D(r['readPerMillion']),'storage':D(d['storageGB'])*D(r['storagePerGBMonth']),'pitr':D(d['pitrGB'])*D(r['pitrPerGBMonth']),'secrets':D(d['secretCount'])*D(r['secretPerMonth']),'logs':D(d['logIngestGB'])*D(r['logPerGB']),'alarms':D(d['alarmCount'])*D(r['alarmPerMonth']),'transfer':D(d['outboundGB'])*D(r['outboundPerGB'])}
print(json.dumps({'region':d['region'],'modelledChargesUSD':{k:str(v) for k,v in parts.items()},'subtotalUSD':str(sum(parts.values())),'complete':False,'note':'Partial model only: Cognito, CloudFront requests, S3 requests/state, provider communications, taxes/tiering and credits require explicit additional calculation.'},indent=2))
