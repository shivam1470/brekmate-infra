"""Download exact CLI release and verify official SHA256 before extracting. No root install."""
import urllib.request,hashlib,zipfile,platform,sys
from pathlib import Path
version='1.12.6';system=platform.system().lower();machine=platform.machine();arch={'x86_64':'amd64','AMD64':'amd64','arm64':'arm64','aarch64':'arm64'}.get(machine)
if system not in ['linux','darwin'] or not arch:raise SystemExit('Unsupported platform')
out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True);name=f'tofu_{version}_{system}_{arch}.zip';base=f'https://github.com/opentofu/opentofu/releases/download/v{version}/'
checks=urllib.request.urlopen(base+f'tofu_{version}_SHA256SUMS',timeout=60).read().decode();expected=[l.split()[0] for l in checks.splitlines() if l.split()[-1]==name]
if len(expected)!=1:raise SystemExit('Release checksum not found')
blob=urllib.request.urlopen(base+name,timeout=60).read()
if hashlib.sha256(blob).hexdigest()!=expected[0]:raise SystemExit('CLI checksum mismatch')
import io
with zipfile.ZipFile(io.BytesIO(blob)) as z:
 with z.open('tofu') as source:(out/'tofu').write_bytes(source.read())
(out/'tofu').chmod(0o755);print(out/'tofu')
