crypt_fun_1:                            -- DATA XREF: sub_9DECE+1A↓o

var_110         = -0x110
var_94          = -0x94
arg_1           =  1
arg_2           =  2
arg_12          =  0x12
arg_7C          =  0x7C

prepare {r20-r24, lp}, 0x1F
movea   0x94+var_110, sp, sp
ld.b    0x24[r6], r2
movhi   0xFEBE, r0, r5
st.b    r2, -0x4C4F[r5]
ld.bu   1[r6], r2
shl     8, r2
ld.bu   [r6], r5
or      r5, r2
movea   0x10, r2, r2
mov     0x1FFF8, r5
and     r5, r2
add     8, r2
ori     1, r2, r2
movea   0x10, r2, r2
addi    -0xF8, r2, r0
mov     r6, r20
blt     loc_9DD86
mov     aDecryptReplayD, r6 -- "decrypt replay data is longer than MAX_"...
jarl    sub_93366, lp
movea   0x110+var_94, sp, sp
dispose 0x1F, {r20-r24, lp}, [lp]
-- ---------------------------------------------------------------------------

loc_9DD86:                              -- CODE XREF: crypt_fun_1+3C↑j
ld.b    2[r20], r2
st.b    r2, arg_1[sp]
movea   0x10, r0, r21
mov     0xFEBD9C00, r7
movea   arg_2, sp, r6
mov     r21, r8
jarl    sub_C8D88, lp
ld.bu   1[r20], r22
ld.bu   [r20], r2
shl     8, r22
or      r2, r22
addi    -2, r22, r23
zxh     r23
mov     r20, r7
add     3, r7
movea   arg_12, sp, r20
mov     r20, r6
mov     r23, r8
jarl    sub_C8D88, lp
movea   arg_1, sp, r24
add     r24, r23
movea   0x11, r23, r6
mov     0xFEBD9C10, r7
mov     r21, r8
jarl    sub_C8D88, lp
movea   0x10, r22, r21
addi    0xE, r22, r23
zxh     r23
mov     r20, r6
mov     r23, r7
jarl    sub_9D7B4, lp
add     r24, r23
mov     r10, r2
shr     8, r2
st.b    r2, 0x11[r23]
add     0xF, r22
zxh     r22
add     r24, r22
st.b    r10, 0x11[r22]
andi    0xFFFF, r21, r22
shr     3, r22
add     1, r22
mov     0, r2
br      loc_9DE28
-- ---------------------------------------------------------------------------

loc_9DE0C:                              -- CODE XREF: crypt_fun_1+10A↓j
andi    0xFFFF, r21, r5
mov     r22, r6
shl     3, r6
sub     r5, r6
andi    0xFF, r2, r7
add     r7, r5
movea   arg_1, sp, r7
add     r7, r5
st.b    r6, 0x11[r5]
add     1, r2

loc_9DE28:                              -- CODE XREF: crypt_fun_1+D4↑j
mov     r22, r5
shl     3, r5
mov     (loc_7FFF6+2), r6
and     r6, r5
andi    0xFFFF, r21, r6
sub     r6, r5
andi    0xFF, r2, r6
cmp     r5, r6
blt     loc_9DE0C
andi    0xFFFF, r22, r8
mov     0xFEBD9C00, r6
mov     r20, r7
jarl    sub_95D04, lp
shl     3, r22
movea   0x11, r22, r8
zxb     r8
movea   arg_1, sp, r7
mov     0x99000005, r6
jarl    sub_8FE0C, lp
movea   arg_7C, sp, sp
dispose 0x1F, {r20-r24, lp}, [lp]
