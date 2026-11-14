"""Read the DEBUG_COUNTERS build's per-mode counters (calls, rejected pad reads, overlaid, kept) while a button is held."""
import os, sys, time, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dolphin import Dolphin
with Dolphin(os.environ['LAB_IMAGE'], gc=True, wiimote=os.environ.get('LAB_REMOTE', 'none') or None, region='RMKE01') as d:
    d.wait_boot(40)
    d.gc.press('A')
    for i in range(4):
        c = struct.unpack('>12I', d.peek(0x80002F00, 48))
        print('early', c[0:4], 'locked', c[4:8], 'probe', c[8:12], 'hold %04X dev %d' % (d.kpad()['hold'], d.kpad()['dev']), flush=True)
        time.sleep(2)

