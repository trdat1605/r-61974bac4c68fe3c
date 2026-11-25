"""Read an offline backup and compare logical Redis data in an isolated fixture."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

spec=importlib.util.spec_from_file_location('maintenance',Path(__file__).with_name('maintain.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
FIXTURE='storage001-redis-verification'
FOLDER=m.PRIVATE/'redis-fixture'
RDB=FOLDER/'dump.rdb'
ENTRY='data/docker/volumes/cwlab-9200023e_redis/_data/dump.rdb'

LUA=r'''
local function frame(a)
  local b={}; for _,v in ipairs(a) do v=tostring(v); table.insert(b,tostring(#v)..':'..v) end
  return table.concat(b)
end
local keys=redis.call('KEYS','*'); table.sort(keys)
local rows={}; local types={}
for _,k in ipairs(keys) do
  if redis.call('PTTL',k)==-1 then
    local typ=redis.call('TYPE',k).ok; local a={}
    if typ=='string' then a={redis.call('GET',k)}
    elseif typ=='list' then a=redis.call('LRANGE',k,0,-1)
    elseif typ=='set' then a=redis.call('SMEMBERS',k); table.sort(a)
    elseif typ=='zset' then a=redis.call('ZRANGE',k,0,-1,'WITHSCORES')
    elseif typ=='hash' then
      local fields=redis.call('HKEYS',k); table.sort(fields)
      for _,f in ipairs(fields) do
        local ttl=redis.call('HPEXPIRETIME',k,'FIELDS',1,f)[1]
        if ttl~=-1 then return redis.error_reply('Hash field expiry requires separate comparison') end
        table.insert(a,f);table.insert(a,redis.call('HGET',k,f))
      end
    else return redis.error_reply('Unsupported Redis type; comparison aborted') end
    table.insert(rows,redis.sha1hex(frame({k,typ,frame(a)})))
    types[typ]=(types[typ] or 0)+1
  end
end
return cjson.encode({count=#rows,digest=redis.sha1hex(table.concat(rows)),types=types})
'''

def original_redis():
    rows=[x for x in m.original() if '-redis-' in x['Name'] and x['State']['Running']]
    assert len(rows)==1
    return rows[0]

def extract():
    assert not RDB.exists(),'Do not overwrite an extraction'
    FOLDER.mkdir(parents=True,exist_ok=True)
    backup=m.C_PRIVATE/'docker/docker_data.vhdx'
    p=subprocess.run(['C:/Program Files/7-Zip/7z.exe','x',str(backup),ENTRY.replace('/','\\'),'-so','-bd'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (m.PRIVATE/'redis-7zip-extraction.stderr').write_bytes(p.stderr)
    assert p.returncode==0 and p.stdout.startswith(b'REDIS') and len(p.stdout)==360525,'7zip extraction invalid; inspect privately'
    with RDB.open('xb') as out:out.write(p.stdout)
    # Independent parser opens only rb; no OS mount or journal replay.
    sys.path.insert(0,str(m.PRIVATE/'reader-libs'))
    from dissect.hypervisor.disk.vhdx import VHDX
    from dissect.extfs.extfs import ExtFS
    with backup.open('rb') as handle:
        fs=ExtFS(VHDX(handle))
        with fs.get('/'+ENTRY).open() as stream:
            independent=stream.read()
    assert independent==p.stdout,'Independent filesystem readers disagree'
    m.evidence('redis-backup-extracted',{'status':'PASS','bytes':len(p.stdout),'sha256':m.sha(RDB),'two_independent_readers_equal':True,'seven_zip_listing_warning':'Headers Error; cause unknown; specific file bytes validated by independent parser and later Redis checksum/load','source':'Immutable offline Docker backup','source_backup_sha256':json.loads((m.ROOT/'evidence/docker-offline-backup.json').read_text())['sha256']})

def launch():
    item=original_redis()
    assert RDB.exists() and m.sha(RDB)==json.loads((m.ROOT/'evidence/redis-backup-extracted.json').read_text())['sha256']
    assert FIXTURE not in m.dock('ps','-a','--format','{{.Names}}').decode().splitlines(),'Fixture name exists'
    args=['create','--name',FIXTURE,'--label','task=STORAGE-001','--network','none','--read-only','--memory','128m','--cpus','0.5','--cap-drop','ALL','--security-opt','no-new-privileges','--user','redis','--restart','no','--mount',f'type=bind,src={FOLDER.as_posix()},dst=/fixture,readonly','--tmpfs','/tmp:rw,nosuid,nodev,size=16m,mode=1777','--tmpfs','/data:rw,nosuid,nodev,size=1m,mode=1777','--entrypoint','redis-server',item['Image'],'--dir','/fixture','--dbfilename','dump.rdb','--appendonly','no','--save','','--port','0','--unixsocket','/tmp/storage-review.sock','--unixsocketperm','700']
    cid=m.dock(*args).decode().strip()
    m.write_json(m.PRIVATE/'redis-fixture.json',{'id':cid,'name':FIXTURE,'image':item['Image'],'original_redis_id':item['Id']})
    metadata=json.loads(m.dock('inspect',cid))[0]
    assert metadata['HostConfig']['NetworkMode']=='none' and not metadata['HostConfig']['PortBindings']
    binds=[x for x in metadata['Mounts'] if x['Type']=='bind']
    assert len(binds)==1 and binds[0]['Destination']=='/fixture' and not binds[0]['RW']
    assert not any(x['Type']=='volume' for x in metadata['Mounts']), 'Unexpected persistent fixture volume'
    m.dock('start',cid)
    for _ in range(20):
        p=subprocess.run(['docker','exec',cid,'redis-cli','-s','/tmp/storage-review.sock','PING'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if p.returncode==0 and p.stdout.strip()==b'PONG':break
        time.sleep(1)
    else: raise RuntimeError('Fixture not ready; original data remains untouched')
    check=m.dock('exec',cid,'redis-check-rdb','/fixture/dump.rdb')
    (m.PRIVATE/'redis-rdb-check.log').write_bytes(check)
    assert b'Checksum OK' in check and b'RDB looks OK' in check,'RDB validation incomplete'
    m.evidence('redis-fixture-created',{'status':'PASS','container_id':cid,'image_id':item['Image'],'network':'none','tcp_port':0,'original_volumes_mounted':False,'rdb_read_only':True,'rdb_checksum':'PASS','fixture_load':'PASS'})

def verify():
    fixture=m.read_private('redis-fixture.json'); item=original_redis()
    running=set(m.dock('ps','-q','--no-trunc').decode().split())
    allowed={x['Id'] for x in m.original() if x['State']['Running'] and m.category(x)==2}|{fixture['id']}
    assert running<=allowed,'Original app writers must stay stopped'
    old=json.loads(m.dock('exec',fixture['id'],'redis-cli','--raw','-s','/tmp/storage-review.sock','EVAL',LUA,'0'))
    now=json.loads(m.dock('exec',item['Id'],'sh','-c','export REDISCLI_AUTH="$REDIS_PASSWORD"; exec redis-cli --raw EVAL "$1" 0','storage-canonical',LUA))
    m.write_json(m.PRIVATE/'redis-canonical-comparison.json',{'backup_fixture':old,'current':now})
    assert old==now,'Canonical persistent Redis data differ; do not resume'
    before=[x for x in m.read_private('before-datastores.json') if x['kind']=='redis'][0]
    after=[x for x in m.read_private('after-datastores.json') if x['kind']=='redis'][0]
    assert old['count']==int(before['persistent_count'])==int(after['persistent_count'])
    m.dock('stop','--time','30',fixture['id'])
    m.evidence('redis-reconciled',{'status':'PASS','original_container_id':item['Id'],'fixture_container_id':fixture['id'],'image_id':item['Image'],'rdb_sha256':m.sha(RDB),'persistent_count':old['count'],'canonical_digest':old['digest'],'type_histogram':old['types'],'baseline_opaque_dump_digest':before['persistent_digest'],'current_opaque_dump_digest':after['persistent_digest'],'original_failed_digest_check':'RETAINED; DUMP binary serialization is not a canonical logical comparison','expiring_keys':'not compared; expected natural expiration during maintenance','fixture':'stopped and retained; no cleanup'})

if __name__=='__main__':
    {'extract':extract,'launch':launch,'verify':verify}[sys.argv[1]]()
    print(json.dumps({'redis_stage':sys.argv[1],'status':'PASS'}),flush=True)
