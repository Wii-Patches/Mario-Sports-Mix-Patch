# Technical notes

## Layout

* `src/cc/<ID>.txt` - Vague Rant's Gecko codes, verbatim per region. `src/gen_cc.py` turns them into patch operations.
* `src/gc.c`, `src/gc_stub.s`, `src/gen_gc.py` - the GameCube pad hook, compiled with devkitPPC and turned into operations.
* `tools/prebuilt/{cc,gc}_<ID>.json` - the operations (hooks, in-place patches), one file per feature and region.
* `tools/ops.py` - one operation list, three outputs: a patched DOL (new text section), Gecko codes, Riivolution XML.
* `tools/sig.py` - masked-instruction signature search, used to carry each site from the USA DOL to Europe / Japan.
* `tools/patcher.py`, `disc.py`, `patch_disc.py`, `gui.py` - the disc patcher.
* `lab/` - the Dolphin test lab.

## How the GameCube pad works

The game links the Wii SDK's KPAD/WPAD but not PAD. KPAD keeps, per channel, a ring of 0x42-byte samples
(16 in the struct, plus a u32 count of extra ones at `+0x5A4` behind the pointer at `+0x5A0`). Three hooks:

1. **probe**, at the entry of `WPADProbe`: keeps SI auto-polling on (Wii SI registers are at `0xCD006400`; the
   `0xCC` alias used on GameCube is dropped on a console). If the channel has no Wii Remote (WPAD control block
   status -1 or device type 253) but a pad answers on the same SI port, it returns 0 ("connected") with device
   type 2 (Classic Controller). `KPADRead` probes every channel every frame before anything else and gives up on
   -1, which is why the pad did nothing without a remote before this hook existed. A real remote always wins;
2. **early** in `KPADRead`, before it gives up on an empty ring: queues a copy of the last sample if the remote
   sent none this frame (or there is no remote);
3. **locked**, right after `OSDisableInterrupts`: rewrites every queued sample as a Classic Controller sample
   (extension type 2, format 7), so a remote interrupt cannot slip a plain sample in.

Vague Rant's hooks downstream then see a normal Classic Controller. The hook code is position-independent and uses
no globals; it lives in `0x80001C00-0x80002C00` (Classic Controller: `0x80001820-0x80001C00`).

KPAD channel 0: USA `0x80548598`, Europe `0x80549518`, Japan `0x80549418`; stride `0x688`; sample ring at `+0x180`,
write index `+0x17A`, count `+0x17B`.

## Lab

Dolphin runs as a private, renamed copy (other tools `pkill Dolphin`), with a throwaway user folder per run.
Input is sent through Dolphin's Pipe device (needs `[Input] BackgroundInput = True`); state is read over the GDB stub.

```
python3 lab/mkimage.py RMKE01 cc gc     # needs games/ and dumps/<ID>.dol (retail main.dols, not committed)
python3 lab/t_cc.py RMKE01              # Classic Controller: every button and stick
python3 lab/t_gc.py RMKE01              # GameCube pad
```

`lab/t_play.py` drives the menus with the pad and saves Dolphin screenshots to `work/shots/`; `lab/t_hotplug.py`
boots with the Wii Remote disconnected and connects it mid-menu (Dolphin's connect hotkey on its own pipe).
`LAB_IMAGE=<extracted disc>/sys/main.dol` boots an extracted disc instead of a rebuilt `.wbfs`, and `LAB_REMOTE=`
(empty) runs `t_gc.py` / `t_gecko.py` with no Wii Remote at all.

Open item: with a Wii Remote connected next to the pad, a sampling test occasionally (about 1 read in 12) sees one
frame of the remote's own sample (device 0, no buttons). The debug counters (`-DDEBUG_COUNTERS`, `lab/t_counters.py`)
show every queued sample is rewritten and no pad read is rejected, and with the pad alone it never happens. It may be a
test-side artefact of halting the CPU over GDB, but that is not proven.

## Checks

`python3 tools/check.py` needs no game files (CI). `MSM_DOLS=<dir> python3 tools/verify.py` checks the retail DOLs.
