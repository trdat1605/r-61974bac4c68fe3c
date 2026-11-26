"""Losslessly archive exactly three offline backups; never touch active runtimes."""
import ctypes
from ctypes import wintypes
import gzip
import hashlib
import json
import msvcrt
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import winreg

ROOT=Path(__file__).resolve().parent
ARCHIVES=Path('C:/Users/MFLAT-ADS-010/.codex/private-backups/archives')
GIB=1024**3
ENTRIES={
 'ubuntu-20261126':('D:/Dev/Backups/STORAGE-001/ubuntu/ext4.vhdx',17763926016,'1cb22afc534287d6b78cd76057661e237e3f2bfd5f34fc4e03ed42001ebb09c3'),
 'docker-20261126':('C:/Users/MFLAT-ADS-010/.codex/private-backups/STORAGE-001/docker/docker_data.vhdx',34207694848,'ff7bf40edf0d5056c4017dc1e3d206392ad577fb3c829e8a2cde410229dfa462'),
 'ubuntu-20261111':('C:/Users/MFLAT-ADS-010/Documents/Codex/2026-11-11/xin-2/work/private-backup/ubuntu-before-mirrored.vhdx',17388535808,None),
}

def free():return {d:shutil.disk_usage(d+':/').free for d in ('C','D')}
def write(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_bytes((json.dumps(value,indent=2)+'\n').encode())

def no_links(path):
 for p in [path,*path.parents]:
  if p.exists() and (p.is_symlink() or p.is_junction()):raise RuntimeError('Reparse path forbidden')

def active_paths():
 result=[Path('D:/Dev/Runtime/Docker/DockerDesktopWSL/disk/docker_data.vhdx').resolve(),Path('D:/Dev/Runtime/Ubuntu/ext4.vhdx').resolve()]
 with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Lxss') as parent:
  for i in range(winreg.QueryInfoKey(parent)[0]):
   with winreg.OpenKey(parent,winreg.EnumKey(parent,i)) as item:
    base=winreg.QueryValueEx(item,'BasePath')[0]
    try:name=winreg.QueryValueEx(item,'VhdFileName')[0]
    except FileNotFoundError:name='ext4.vhdx'
    result.append((Path(base)/name).resolve())
 return result

def locked_read(path):
 kernel=ctypes.WinDLL('kernel32',use_last_error=True)
 fn=kernel.CreateFileW
 fn.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]
 fn.restype=wintypes.HANDLE
 handle=fn(str(path),0x80000000,1,None,3,0,None) # read only; deny concurrent writes/deletes
 if handle==ctypes.c_void_p(-1).value:raise ctypes.WinError(ctypes.get_last_error())
 try:fd=msvcrt.open_osfhandle(handle,os.O_RDONLY|os.O_BINARY)
 except Exception:
  kernel.CloseHandle(wintypes.HANDLE(handle));raise
 return os.fdopen(fd,'rb')

def setup():
 no_links(ARCHIVES)
 ARCHIVES.mkdir(parents=True,exist_ok=True)
 sid=subprocess.check_output(['whoami','/user','/fo','csv','/nh']).decode().strip().split(',')[-1].strip('"')
 subprocess.run(['icacls',str(ARCHIVES),'/inheritance:r','/grant:r',f'*{sid}:(OI)(CI)F','*S-1-5-18:(OI)(CI)F','*S-1-5-32-544:(OI)(CI)F'],check=True,stdout=subprocess.DEVNULL)

def compact(key):
 setup()
 source=Path(ENTRIES[key][0]);expected_size=ENTRIES[key][1];expected_sha=ENTRIES[key][2]
 # Docker archive goes to D only after verified Ubuntu archive freed its D source.
 folder=Path('D:/Dev/Backups/archives') if key=='docker-20261126' else ARCHIVES
 no_links(folder);folder.mkdir(parents=True,exist_ok=True)
 if folder!=ARCHIVES:
  sid=subprocess.check_output(['whoami','/user','/fo','csv','/nh']).decode().strip().split(',')[-1].strip('"')
  subprocess.run(['icacls',str(folder),'/inheritance:r','/grant:r',f'*{sid}:(OI)(CI)F','*S-1-5-18:(OI)(CI)F','*S-1-5-32-544:(OI)(CI)F'],check=True,stdout=subprocess.DEVNULL)
 target=folder/(key+'.vhdx.gz');partial=target.with_suffix(target.suffix+'.partial')
 no_links(source);no_links(target);no_links(partial)
 assert source.resolve()==Path(ENTRIES[key][0]).resolve() and source.resolve() not in active_paths()
 assert source.is_file() and not target.exists() and not partial.exists(),'Source missing or archive conflict'
 assert not (ROOT/'evidence'/(key+'.json')).exists(),'Receipt exists; do not rerun'
 before=free();stat=source.stat();assert stat.st_size==expected_size
 assert before[folder.drive[0]]>=12*GIB,'Insufficient archive reserve'
 start=time.monotonic();digest=hashlib.sha256();total=0;report=0
 with locked_read(source) as inp,partial.open('xb') as raw:
  with gzip.GzipFile(filename='',mode='wb',compresslevel=1,fileobj=raw,mtime=0) as compressed:
   while block:=inp.read(8*1024*1024):
    assert free()[folder.drive[0]]>=10*GIB,'Capacity guard; retain source and partial for inspection'
    digest.update(block);compressed.write(block);total+=len(block)
    if time.monotonic()-report>=30:
     print(json.dumps({'backup':key,'phase':'compress','read_gib':round(total/GIB,2),'elapsed_seconds':round(time.monotonic()-start)}),flush=True);report=time.monotonic()
  raw.flush();os.fsync(raw.fileno())
  assert total==expected_size
  sha=digest.hexdigest();assert expected_sha is None or sha==expected_sha,'Backup SHA differs from migration evidence'
 # Fully decompress without writing a second 16/32GiB VHD; CRC checked by gzip EOF.
 verified=hashlib.sha256();count=0;report=0
 with locked_read(source) as pinned,gzip.open(partial,'rb') as restored:
  pinned_stat=os.fstat(pinned.fileno())
  assert (pinned_stat.st_ino,pinned_stat.st_size,pinned_stat.st_mtime_ns)==(stat.st_ino,stat.st_size,stat.st_mtime_ns),'Source changed'
  while block:=restored.read(8*1024*1024):
   verified.update(block);count+=len(block)
   if time.monotonic()-report>=30:
    print(json.dumps({'backup':key,'phase':'verify','verified_gib':round(count/GIB,2),'elapsed_seconds':round(time.monotonic()-start)}),flush=True);report=time.monotonic()
  assert count==total and verified.hexdigest()==sha,'Decompressed data differ; retain source'
  assert partial.stat().st_size<total,'Archive did not reduce size; retain source'
  # Atomic publish only to new name (Windows rename refuses an existing target).
  partial.rename(target)
  record={'status':'PASS_VERIFIED_SOURCE_RETAINED','source_path':str(source),'archive_path':str(target),'original_bytes':total,'archive_bytes':target.stat().st_size,'uncompressed_sha256':sha,'gzip_crc_and_full_decompressed_sha256':'PASS','free_before_bytes':before,'elapsed_seconds':round(time.monotonic()-start),'source_unlinked':False,'runtime_modified':False}
  write(folder/(key+'.manifest.json'),record)
  write(ROOT/'evidence'/(key+'.json'),record)
 # Only this exact offline source is removed, after durable verified archive+manifest.
 current=source.stat()
 assert (current.st_ino,current.st_size,current.st_mtime_ns)==(stat.st_ino,stat.st_size,stat.st_mtime_ns)
 assert source.resolve() not in active_paths() and target.is_file()
 source.unlink()
 record.update(status='PASS',source_unlinked=True,free_after_bytes=free(),elapsed_seconds=round(time.monotonic()-start))
 write(folder/(key+'.manifest.json'),record)
 write(ROOT/'evidence'/(key+'.json'),record)
 print(json.dumps({'backup':key,'status':'PASS','original_gib':round(total/GIB,3),'archive_gib':round(target.stat().st_size/GIB,3),'saved_logical_gib':round((total-target.stat().st_size)/GIB,3),'free_bytes':free()}),flush=True)

if __name__=='__main__':
 assert len(sys.argv)==2 and sys.argv[1] in ENTRIES,'Select exact allowlisted backup'
 compact(sys.argv[1])
