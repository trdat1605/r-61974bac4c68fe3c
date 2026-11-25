"""Task-specific maintenance. Never prints private runtime data or removes resources."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
import ssl

GIB = 1024 ** 3
ROOT = Path(__file__).resolve().parent
PRIVATE = Path('D:/Dev/Backups/STORAGE-001')
C_PRIVATE = Path('C:/Users/MFLAT-ADS-010/.codex/private-backups/STORAGE-001')
DOCKER_SOURCE = Path('C:/Users/MFLAT-ADS-010/AppData/Local/Docker/wsl/disk/docker_data.vhdx')
DOCKER_TARGET_ROOT = Path('D:/Dev/Runtime/Docker')
UBUNTU_SOURCE = Path('C:/Users/MFLAT-ADS-010/AppData/Local/wsl/{423b648b-df64-4178-b913-db88d10b708e}/ext4.vhdx')
UBUNTU_TARGET_ROOT = Path('D:/Dev/Runtime/Ubuntu')

def run(args, data=None, timeout=120):
    p = subprocess.run(args, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if p.returncode:
        # Stderr can include connection strings or private arguments. Store privately only.
        if PRIVATE.exists():
            (PRIVATE / 'last-command-error.bin').write_bytes(p.stderr)
        raise RuntimeError(f'Command failed: {args[0]} {args[1] if len(args)>1 else ""}; exit {p.returncode}; details private')
    return p.stdout

def dock(*args, data=None):
    return run(['docker', *args], data=data)

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def read_private(name):
    return json.loads((PRIVATE / name).read_text(encoding='utf-8'))

def evidence(name, value):
    write_json(ROOT / 'evidence' / (name + '.json'), {'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()), **value})

def free():
    return {drive: shutil.disk_usage(drive + ':/').free for drive in ['C','D']}

def private_dirs():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    # Private ACLs: current Windows principal, SYSTEM, built-in administrators only.
    sid = run(['whoami','/user','/fo','csv','/nh']).decode(errors='replace').strip().split(',')[-1].strip('"')
    run(['icacls',str(PRIVATE),'/inheritance:r','/grant:r',f'*{sid}:(OI)(CI)F','*S-1-5-18:(OI)(CI)F','*S-1-5-32-544:(OI)(CI)F'])

def inventory():
    private_dirs()
    assert not (PRIVATE / 'inventory.json').exists(), 'Baseline exists; do not replace'
    ids = dock('ps','-aq').decode().split()
    items = json.loads(dock('inspect',*ids))
    # Raw metadata contains secrets; only restricted private folder, never Git/stdout.
    write_json(PRIVATE / 'inventory.json',items)
    volumes = json.loads(dock('volume','inspect',*dock('volume','ls','-q').decode().split()))
    write_json(PRIVATE / 'volumes.json',volumes)
    images = dock('image','ls','--no-trunc','--format','{{.ID}}').decode().split()
    write_json(PRIVATE / 'images.json',sorted(set(images)))
    settings = Path(os.environ['APPDATA']) / 'Docker/settings-store.json'
    shutil.copyfile(settings, PRIVATE / 'settings-before.private.json')
    http = http_checks()
    write_json(PRIVATE / 'http-before.json',http)
    evidence('inventory', {'status':'PASS','containers':len(items),'running':sum(x['State']['Running'] for x in items),'volumes':len(volumes),'images_unique':len(set(images)),'free_bytes':free(),'http':http,'sensitive_metadata':'restricted private folder only'})

def original():
    return read_private('inventory.json')

def category(item):
    name = item['Name']
    if '-proxy-' in name: return 0
    if '-postgres-' in name or '-db-' in name or '-redis-' in name: return 2
    return 1

def assert_inventory():
    before = original()
    now_ids = dock('ps','-aq','--no-trunc').decode().split()
    assert set(now_ids)=={x['Id'] for x in before}, 'Container identities changed'
    now = {x['Id']:x for x in json.loads(dock('inspect',*now_ids))}
    for item in before:
        other = now[item['Id']]
        assert item['Image']==other['Image'], 'Container image changed'
        assert item['HostConfig']['PortBindings']==other['HostConfig']['PortBindings'], 'Port binding changed'
        assert item['Mounts']==other['Mounts'], 'Mount metadata changed; inspect privately before accepting transient path'
    current_volumes = set(dock('volume','ls','-q').decode().split())
    assert current_volumes=={x['Name'] for x in read_private('volumes.json')}, 'Volume inventory changed'
    current_images = set(dock('image','ls','--no-trunc','--format','{{.ID}}').decode().split())
    assert current_images==set(read_private('images.json')), 'Image inventory changed'
    return now

def quiesce():
    assert_inventory()
    for group in [0,1]:
        targets = [x['Id'] for x in original() if x['State']['Running'] and category(x)==group]
        if targets: dock('stop','--time','60',*targets)
    evidence('writers-stopped',{'status':'PASS','free_bytes':free(),'maintenance_started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})

def pg(item, query, database='postgres'):
    # Role chosen inside container; no credential values cross into script output.
    return dock('exec','-i',item['Id'],'sh','-c','exec psql -X -v ON_ERROR_STOP=1 -U "${POSTGRES_USER:-postgres}" -d "$1" -At -F "|"','maintenance-psql',database,data=query.encode())

def datastore_snapshot(phase):
    snapshots=[]
    for item in original():
        if not item['State']['Running'] or category(item)!=2: continue
        if '-redis-' in item['Name']:
            # Only persistent keys to avoid TTL/process-heartbeat expiration false mismatches.
            lua="local k=redis.call('KEYS','*');table.sort(k);local a={};local exp=0;for _,v in ipairs(k) do if redis.call('PTTL',v)==-1 then local d=redis.call('DUMP',v);if d then table.insert(a,redis.sha1hex(v)..redis.sha1hex(d)) end else exp=exp+1 end end;return {#a,redis.sha1hex(table.concat(a)),exp}"
            value=dock('exec',item['Id'],'sh','-c','export REDISCLI_AUTH="$REDIS_PASSWORD"; exec redis-cli --raw EVAL "$1" 0','maintenance-redis',lua).decode().strip().splitlines()
            assert len(value)==3 and value[0].isdigit() and len(value[1])==40 and value[2].isdigit(), 'Redis snapshot failed; keep writers stopped'
            snapshots.append({'container':item['Id'],'kind':'redis','persistent_count':value[0],'persistent_digest':value[1],'expiring_keys_not_compared':value[2]})
            continue
        data_directory=pg(item,'SHOW data_directory;').decode().strip()
        databases=pg(item,"SELECT datname FROM pg_database WHERE NOT datistemplate ORDER BY datname;").decode().splitlines()
        for db in databases:
            tables=pg(item,"SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename;",db).decode().splitlines()
            queries=[]
            for table in tables:
                quoted='"'+table.replace('"','""')+'"'
                label=table.replace("'","''")
                queries.append(f"SELECT '{label}',count(*),md5(COALESCE(string_agg(md5(row_to_json(t)::text),'' ORDER BY md5(row_to_json(t)::text)),'')) FROM public.{quoted} AS t;")
            queries.append("SELECT sequencename,last_value FROM pg_sequences WHERE schemaname='public' ORDER BY sequencename;")
            output=pg(item,'\n'.join(queries),db)
            snapshots.append({'container':item['Id'],'database':db,'kind':'postgres','data_directory':data_directory,'tables':len(tables),'digest':hashlib.sha256(output).hexdigest()})
    write_json(PRIVATE / (phase+'-datastores.json'),snapshots)
    if phase=='after':
        before=read_private('before-datastores.json')
        clean=lambda rows:[{k:v for k,v in x.items() if k!='expiring_keys_not_compared'} for x in rows]
        assert clean(before)==clean(snapshots), 'Datastore digest differs; keep writers stopped'
    evidence(phase+'-datastores',{'status':'PASS','datasets':len(snapshots),'postgres_tables':sum(x.get('tables',0) for x in snapshots),'redis_scope':'DB0 persistent keys; expiring keys NOT_COMPARED; full offline VHD retains all databases','private_detail':phase+'-datastores.json'})

def stop_data():
    for item in original():
        if item['State']['Running'] and category(item)==2:
            dock('stop','--time','90',item['Id'])
    assert not dock('ps','-q').strip(), 'Unexpected running containers'
    evidence('all-stopped',{'status':'PASS'})

def exclusive(path):
    import ctypes.wintypes as wt
    fn=ctypes.WinDLL('kernel32',use_last_error=True).CreateFileW
    fn.argtypes=[wt.LPCWSTR,wt.DWORD,wt.DWORD,ctypes.c_void_p,wt.DWORD,wt.DWORD,wt.HANDLE]
    fn.restype=wt.HANDLE
    handle=fn(str(path),0x80000000,0,None,3,0,None)
    if handle==ctypes.c_void_p(-1).value:
        raise RuntimeError('VHD is still in use or inaccessible; do not copy')
    ctypes.WinDLL('kernel32',use_last_error=True).CloseHandle(wt.HANDLE(handle))

def sha(path):
    value=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(16*1024*1024),b''): value.update(block)
    return value.hexdigest()

def copy_verified(source,target,reserve_gib):
    assert source.is_file() and not target.exists(), 'Source missing or target conflict'
    assert free()[target.drive[0]]-source.stat().st_size>=reserve_gib*GIB, 'Capacity guard failed'
    target.parent.mkdir(parents=True,exist_ok=True)
    count=0; value=hashlib.sha256(); started=time.monotonic()
    with source.open('rb') as inp,target.open('xb') as out:
        for block in iter(lambda:inp.read(16*1024*1024),b''):
            out.write(block);value.update(block);count+=len(block)
            if count%(2*GIB)==0: print(json.dumps({'copy_gib':count/GIB,'elapsed_seconds':round(time.monotonic()-started)}),flush=True)
        out.flush();os.fsync(out.fileno())
    digest=value.hexdigest()
    assert sha(target)==digest and target.stat().st_size==source.stat().st_size, 'Copied bytes/hash mismatch'
    return {'bytes':count,'sha256':digest,'elapsed_seconds':round(time.monotonic()-started),'free_bytes':free()}

def backup_docker():
    exclusive(DOCKER_SOURCE)
    assert free()['D']-2*DOCKER_SOURCE.stat().st_size>=8*GIB, 'Backup + move + reserve do not fit'
    value=copy_verified(DOCKER_SOURCE,PRIVATE/'docker/docker_data.vhdx',8)
    evidence('docker-offline-backup',{'status':'PASS',**value})

def move_backup():
    backup=PRIVATE/'docker/docker_data.vhdx'
    target=C_PRIVATE/'docker/docker_data.vhdx'
    expected=json.loads((ROOT/'evidence/docker-offline-backup.json').read_text())['sha256']
    assert sha(backup)==expected, 'Original backup hash changed'
    # This only relocates the newly-created backup; it never discards a backup.
    C_PRIVATE.mkdir(parents=True,exist_ok=True)
    sid=run(['whoami','/user','/fo','csv','/nh']).decode(errors='replace').strip().split(',')[-1].strip('"')
    run(['icacls',str(C_PRIVATE),'/inheritance:r','/grant:r',f'*{sid}:(OI)(CI)F','*S-1-5-18:(OI)(CI)F','*S-1-5-32-544:(OI)(CI)F'])
    value=copy_verified(backup,target,13)
    assert value['sha256']==expected and sha(backup)==expected
    assert backup.resolve()==Path('D:/Dev/Backups/STORAGE-001/docker/docker_data.vhdx').resolve()
    backup.unlink()
    evidence('docker-backup-relocated',{'status':'PASS','retained_at':str(target),**value,'free_after_move':free()})

def export_ubuntu():
    exclusive(UBUNTU_SOURCE)
    target=PRIVATE/'ubuntu/ext4.vhdx'
    assert not target.exists() and not UBUNTU_TARGET_ROOT.exists(), 'Ubuntu target conflict'
    assert free()['D']-2*UBUNTU_SOURCE.stat().st_size>=8*GIB, 'Ubuntu backup + move + reserve do not fit'
    target.parent.mkdir(parents=True,exist_ok=True)
    before=sha(UBUNTU_SOURCE)
    run(['wsl.exe','--export','Ubuntu-22.04',str(target),'--format','vhd'],timeout=1200)
    after=sha(target)
    assert after==before and sha(UBUNTU_SOURCE)==before, 'WSL exported VHD not byte-identical; stop for investigation'
    evidence('ubuntu-export',{'status':'PASS','bytes':target.stat().st_size,'sha256':after,'free_bytes':free()})

def move_ubuntu():
    backup=PRIVATE/'ubuntu/ext4.vhdx'
    rec=json.loads((ROOT/'evidence/ubuntu-export.json').read_text())
    assert sha(backup)==rec['sha256'], 'Ubuntu backup changed'
    exclusive(UBUNTU_SOURCE)
    assert free()['D']-UBUNTU_SOURCE.stat().st_size>=8*GIB, 'Ubuntu move capacity guard'
    assert not UBUNTU_TARGET_ROOT.exists(), 'Ubuntu target already exists'
    UBUNTU_TARGET_ROOT.parent.mkdir(parents=True,exist_ok=True)
    run(['wsl.exe','--manage','Ubuntu-22.04','--move',str(UBUNTU_TARGET_ROOT)],timeout=1200)
    target=UBUNTU_TARGET_ROOT/'ext4.vhdx'
    assert target.exists() and not UBUNTU_SOURCE.exists() and sha(target)==rec['sha256'], 'Ubuntu move verification failed'
    evidence('ubuntu-moved',{'status':'PASS','path':str(target),'sha256':rec['sha256'],'free_bytes':free()})

def inventory_after():
    current=assert_inventory()
    writers=[x['Name'] for x in current.values() if x['State']['Running'] and category(x)!=2]
    assert not writers, 'Unexpected writer auto-start; stop and re-baseline before continuing'
    evidence('inventory-after',{'status':'PASS','containers':len(current),'auto_running_datastores':sum(x['State']['Running'] for x in current.values()),'free_bytes':free()})

def start_data():
    assert_inventory()
    for item in original():
        if item['State']['Running'] and category(item)==2:
            dock('start',item['Id'])
    time.sleep(5)

def resume():
    # Datastore exact comparison must have succeeded before app writers resume.
    rec=json.loads((ROOT/'evidence/after-datastores.json').read_text())
    assert rec['status']=='PASS'
    for group in [1,0]:
        for item in original():
            if item['State']['Running'] and category(item)==group:
                dock('start',item['Id'])
    evidence('services-resumed',{'status':'PASS','free_bytes':free()})

def http_checks():
    urls=['http://127.0.0.1:44330/app/login','http://127.0.0.1:44331/vite-dev/@vite/client','http://127.0.0.1:44332/','http://127.0.0.1:44400/','https://127.0.0.1:44403/','http://127.0.0.1:44405/','https://127.0.0.1:44406/']
    result=[]
    # Local TLS verification bypass here is a read-only probe, not browser certificate settings.
    for url in urls:
        start=time.monotonic()
        try:
            with urllib.request.urlopen(url,timeout=40,context=ssl._create_unverified_context()) as response:
                response.read(1024);status=response.status
        except urllib.error.HTTPError as error: status=error.code
        except Exception: status='UNREACHABLE'
        result.append({'url':url,'status':status,'elapsed_seconds':round(time.monotonic()-start,3)})
    return result

def postcheck():
    current=assert_inventory()
    for item in original():
        assert current[item['Id']]['State']['Running']==item['State']['Running'], 'Running state differs'
    checks=http_checks()
    before=read_private('http-before.json')
    assert [(x['url'],x['status']) for x in checks]==[(x['url'],x['status']) for x in before], 'HTTP baseline differs'
    evidence('postcheck',{'status':'PASS','http':checks,'free_bytes':free(),'limits':['Read-only HTTP probes, not full UI/security acceptance','Redis expiring keys not compared','No isolated restore rehearsal','Private raw metadata/backups retained outside Git']})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['inventory','quiesce','before','stop-data','backup-docker','move-backup','export-ubuntu','move-ubuntu','inventory-after','start-data','after','resume','postcheck'])
    stage=parser.parse_args().stage
    actions={'inventory':inventory,'quiesce':quiesce,'before':lambda:datastore_snapshot('before'),'stop-data':stop_data,'backup-docker':backup_docker,'move-backup':move_backup,'export-ubuntu':export_ubuntu,'move-ubuntu':move_ubuntu,'inventory-after':inventory_after,'start-data':start_data,'after':lambda:datastore_snapshot('after'),'resume':resume,'postcheck':postcheck}
    actions[stage]();print(json.dumps({'stage':stage,'status':'PASS'}),flush=True)
