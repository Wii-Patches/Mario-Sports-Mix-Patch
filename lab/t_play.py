"""Drive the menus with the GC pad and take Dolphin screenshots (user/ScreenShots) along the way.

    python3 lab/t_play.py RMKE01 <remote|-> <disconnect 0/1> A A A Down A ...
"""
import os, sys, time, glob, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dolphin import Dolphin, GC_NAMES
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
region, remote, unplug = sys.argv[1], (None if sys.argv[2] == '-' else sys.argv[2]), sys.argv[3] == '1'
steps = sys.argv[4:]
out = os.path.join(ROOT, 'work', 'shots'); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
def shot(d, name):
    d.hk.tap('B', 0.2); time.sleep(1.0)
    fs = sorted(glob.glob(os.path.join(d.user, 'ScreenShots', '**', '*.png'), recursive=True), key=os.path.getmtime)
    if fs:
        shutil.move(fs[-1], os.path.join(out, name + '.png'))
with Dolphin(os.environ.get('LAB_IMAGE') or os.path.join(ROOT, 'work', 'test_%s.wbfs' % region), gc=True, wiimote=remote, region=region, video='Metal') as d:
    print('pid', d.proc.pid, flush=True)
    if unplug:
        time.sleep(1); d.hk.tap('A', 0.3)
    d.wait_boot(35)
    shot(d, '00_boot')
    for i, s in enumerate(steps, 1):
        if s == 'connect':
            d.hk.tap('A', 0.3); time.sleep(4)
        elif ':' in s:                      # MAIN:x,y or C:x,y  sets a GC stick (0.5,0.5 = centre)
            n, xy = s.split(':'); x, y = map(float, xy.split(',')); d.gc.axis(n, x, y); time.sleep(1.5)
        elif s.startswith('wait'):
            time.sleep(float(s[4:]))
        else:
            d.gc.tap(GC_NAMES.get(s, s), 0.2); time.sleep(2.5)
        shot(d, '%02d_%s' % (i, s.replace(':', '_').replace(',', '_')))
        print(i, s, d.kpad(), flush=True)
    print('alive', d.proc.poll() is None)
