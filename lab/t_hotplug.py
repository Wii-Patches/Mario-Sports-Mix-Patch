"""Boot with only a GC pad (the remote is disconnected straight away), play, then connect a Wii Remote."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dolphin import Dolphin
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
region = sys.argv[1] if len(sys.argv) > 1 else 'RMKE01'
remote = sys.argv[2] if len(sys.argv) > 2 else 'none'
with Dolphin(os.environ.get('LAB_IMAGE') or os.path.join(ROOT, 'work', 'test_%s.wbfs' % region), gc=True, wiimote=remote, region=region) as d:
    print('pid', d.proc.pid, flush=True)
    time.sleep(1); d.hk.tap('A', 0.3)
    d.wait_boot(40)
    print('gc only  ', d.kpad(), flush=True)
    for _ in range(4):
        d.gc.tap('A', 0.2); time.sleep(1)
    print('after A  ', d.kpad(), flush=True)
    d.hk.tap('A', 0.3); time.sleep(5)
    print('connected', d.kpad(), flush=True)
    d.gc.press('B'); time.sleep(0.6); print('gc B     ', d.kpad(), flush=True); d.gc.release('B')
    time.sleep(5)
    print('alive', d.proc.poll() is None, flush=True)
