# Entry stub for the WPADProbe hook (gc.c built with MODE=2).  Runs in place of
# WPADProbe's first instruction with r3 = channel, r4 = where to store the
# device type (may be 0).  If gc_hook answers, return 0 ("connected") straight
# to WPADProbe's caller; otherwise run the displaced instruction and carry on.
    .globl stub
stub:
    stwu    1, -0x50(1)
    stw     0, 0x08(1)
    stw     3, 0x0C(1)
    stw     4, 0x10(1)
    stw     5, 0x14(1)
    stw     6, 0x18(1)
    stw     7, 0x1C(1)
    stw     8, 0x20(1)
    stw     9, 0x24(1)
    stw     10, 0x28(1)
    stw     11, 0x2C(1)
    stw     12, 0x30(1)
    mflr    0
    stw     0, 0x34(1)
    mfcr    0
    stw     0, 0x38(1)
    mfctr   0
    stw     0, 0x3C(1)
    bl      gc_hook
    mr      12, 3
    lwz     0, 0x3C(1)
    mtctr   0
    lwz     0, 0x38(1)
    mtcr    0
    lwz     0, 0x34(1)
    mtlr    0
    lwz     3, 0x0C(1)
    lwz     4, 0x10(1)
    lwz     5, 0x14(1)
    lwz     6, 0x18(1)
    lwz     7, 0x1C(1)
    lwz     8, 0x20(1)
    lwz     9, 0x24(1)
    lwz     10, 0x28(1)
    lwz     11, 0x2C(1)
    lwz     0, 0x08(1)
    cmpwi   12, 0
    lwz     12, 0x30(1)
    addi    1, 1, 0x50
    beq     1f
    li      3, 0
    blr
1:
    @DISPLACED@
