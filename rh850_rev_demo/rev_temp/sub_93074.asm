sub_93074:                              -- CODE XREF: sub_8B73A+54↑p
                                        -- sub_8B79E+54↑p ...

arg_0           =  0

cmp     r9, r7
ld.w    arg_0[sp], r2
bnz     loc_93096
mov     7, r5
sub     r2, r5
movea   0xFF, r0, r10
shr     r5, r10
add     r6, r7
ld.bu   [r7], r2
and     r2, r10
shr     r8, r10
jmp     [lp]
-- ---------------------------------------------------------------------------

loc_93096:                              -- CODE XREF: sub_93074+6↑j
mov     8, r5
sub     r8, r5
mov     r7, r10
add     r6, r10
ld.bu   [r10], r10
shr     r8, r10
br      loc_930BE
-- ---------------------------------------------------------------------------

loc_930A8:                              -- CODE XREF: sub_93074+52↓j
andi    0xFF, r7, r8
add     r6, r8
ld.bu   [r8], r8
andi    0xFF, r5, r11
shl     r11, r8
or      r8, r10
add     8, r5

loc_930BE:                              -- CODE XREF: sub_93074+32↑j
add     1, r7
andi    0xFF, r7, r8
cmp     r9, r8
bl      loc_930A8
mov     7, r7
sub     r2, r7
movea   0xFF, r0, r2
shr     r7, r2
add     r9, r6
ld.bu   [r6], r6
and     r6, r2
zxb     r5
shl     r5, r2
or      r2, r10
jmp     [lp]
