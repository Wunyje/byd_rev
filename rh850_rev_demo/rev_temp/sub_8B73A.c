void sub_8B73A(unsigned char *aSrc)
{
    unsigned char var_10;
    unsigned char r2, r7, r8, r9, r20, r21;
    
    r2 = *aSrc;
    if (r2 == 0) {
        if ((unsigned char)(*(int *)(0xFEBE0000 + 0x667C)) != 0)
        {
            r9 = 0x4D113;
            r8 = 0x78;
            char *r7 = "src\\app\\can\\Sources\\Upward\\can_mod.c";
            char *r6 = "assert! %s %d (%s)\n";
            sub_9344E(r7, r6);
        }
    }
    else {
        r2 = aSrc[3];
        r9 = aSrc[2];
        r8 = aSrc[1];
        r7 = aSrc[0];
        var_10 = r2;
        r9--;
        r9 = (unsigned char)r9;
        r7--;
        r7 = (unsigned char)r7;
        r20 = r6;
        r6 += 5;
        sub_93074(r7, r9, r8, var_10, r6);
        r10 = r6;
        debug_main_volume_set(0, r10);
        r10 = 0;
    }
}