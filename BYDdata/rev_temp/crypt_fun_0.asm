crypt_fun_0:                            -- DATA XREF: sub_9DECE+10↓o

var_1F8         = -0x1F8
var_84          = -0x84
arg_0           =  0
arg_3           =  3
arg_FA          =  0xFA
arg_FB          =  0xFB
arg_FC          =  0xFC
arg_FD          =  0xFD
arg_FE          =  0xFE
arg_FF          =  0xFF
arg_100         =  0x100
arg_101         =  0x101
arg_102         =  0x102
arg_113         =  0x113
arg_114         =  0x114
arg_115         =  0x115
arg_116         =  0x116
arg_117         =  0x117
arg_118         =  0x118
arg_119         =  0x119
arg_11A         =  0x11A
arg_11B         =  0x11B
arg_11C         =  0x11C
arg_11D         =  0x11D
arg_174         =  0x174

prepare {r20, lp}, 0x1F
movea   0x84+var_1F8, sp, sp
ld.bu   1[r6], r2
shl     8, r2
ld.bu   [r6], r5
or      r5, r2
addi    -0xD4, r2, r0
mov     r6, r20
blt     loc_9DC6C
mov     aEncryptDataIsT, r6 -- "ENCRYPT DATA IS TOO LONG \r\n"
jarl    sub_93366, lp
movea   0x1F8+var_84, sp, sp
dispose 0x1F, {r20, lp}, [lp]
-- ---------------------------------------------------------------------------

loc_9DC6C:                              -- CODE XREF: crypt_fun_0+1A↑j
mov     2, r6
jarl    sub_A6C8C, lp
cmp     9, r10
bnz     loc_9DC7A
mov     0, r2
br      loc_9DC7E
-- ---------------------------------------------------------------------------

loc_9DC7A:                              -- CODE XREF: crypt_fun_0+36↑j
ld.bu   2[r20], r2

loc_9DC7E:                              -- CODE XREF: crypt_fun_0+3A↑j
st.b    r2, arg_FA[sp]
movea   -0x72, r0, r2
st.b    r2, arg_FC[sp]
mov     8, r2
st.b    r2, arg_FD[sp]
movea   0xD3, r0, r2
st.b    r2, arg_FE[sp]
st.b    r0, arg_FF[sp]
mov     -1, r2
st.b    r2, arg_100[sp]
st.b    r0, arg_101[sp]
movea   arg_102, sp, r6
jarl    sub_96646, lp
mov     0xB, r2
st.b    r2, arg_113[sp]
mov     3, r2
st.b    r2, arg_114[sp]
jarl    sub_9580A, lp
st.b    r10, arg_115[sp]
mov     r10, r2
shr     0x18, r2
st.b    r2, arg_118[sp]
mov     r10, r2
shr     0x10, r2
st.b    r2, arg_117[sp]
shr     8, r10
st.b    r10, arg_116[sp]
st.b    r0, arg_11C[sp]
st.b    r0, arg_11B[sp]
st.b    r0, arg_11A[sp]
st.b    r0, arg_119[sp]
ld.bu   1[r20], r8
ld.bu   [r20], r2
shl     8, r8
or      r2, r8
addi    3, r20, r7
movea   arg_11D, sp, r6
jarl    sub_C8D88, lp
ld.b    [r20], r2
st.b    r2, arg_FB[sp]
mov     sp, r9
movea   arg_3, sp, r8
mov     2, r7
movea   arg_FA, sp, r6
jarl    sub_9DFA2, lp
cmp     0, r10
bnz     loc_9DD2E
ld.bu   arg_0[sp], r8
movea   arg_3, sp, r7
mov     0x99000004, r6
jarl    sub_8FE0C, lp

loc_9DD2E:                              -- CODE XREF: crypt_fun_0+DC↑j
movea   arg_174, sp, sp
dispose 0x1F, {r20, lp}, [lp]