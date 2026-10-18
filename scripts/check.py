import subprocess,os,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];tofu=os.environ.get('TOFU_BIN','tofu')
subprocess.run(['python3','-m','unittest','discover','-s','tests','-v'],cwd=ROOT,check=True)
if not shutil.which(tofu):raise SystemExit('OpenTofu missing; source tests passed but provider validation is blocked')
subprocess.run([tofu,'fmt','-recursive','-check'],cwd=ROOT,check=True)
for d in ['bootstrap','environments/staging','environments/production']:
 subprocess.run([tofu,'init','-backend=false','-input=false'],cwd=ROOT/d,check=True)
 subprocess.run([tofu,'validate','-no-color'],cwd=ROOT/d,check=True)
 subprocess.run([tofu,'test','-no-color'],cwd=ROOT/d,check=True)
print('Source + provider schema + mocked-plan checks passed; no real AWS integration verified.')
