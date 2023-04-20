#include <stdio.h>
#include <stdint.h>

void crypt_fun_0(uint8_t* r6, uint8_t* aEncryptDataIsT) {
    int32_t var_1F8 = -0x1F8;
    int32_t var_84 = -0x84;

    uint8_t* sp = (uint8_t*)(&aEncryptDataIsT - var_1F8);

    uint8_t r2 = (r6[1] << 8) | r6[0];
    if (r2 < -0xD4) {
        sprintf((char*)aEncryptDataIsT, "ENCRYPT DATA IS TOO LONG \r\n");
        return;
    }

    uint8_t r10 = 0;
    if (sub_A6C8C(2, &r10)) {
        return;
    }

    if (r10 != 9) {
        r2 = r6[2];
    }
    sp[var_84 + 0xFA] = r2;
    sp[var_84 + 0xFC] = 0x72;
    sp[var_84 + 0xFD] = 8;
    sp[var_84 + 0xFE] = 0xD3;
    sp[var_84 + 0xFF] = 0;
    sp[var_84 + 0x100] = 0xFF;
    sp[var_84 + 0x101] = 0;
    sub_96646(sp + var_84 + 0x102);

    sp[var_84 + 0x113] = 0xB;
    sp[var_84 + 0x114] = 3;
    sub_9580A(sp + var_84 + 0x115);

    sp[var_84 + 0x115] = r10;
    sp[var_84 + 0x116] = r10 >> 8;
    sp[var_84 + 0x117] = r10 >> 16;
    sp[var_84 + 0x118] = r10 >> 24;

    sp[var_84 + 0x11C] = 0;
    sp[var_84 + 0x11B] = 0;
    sp[var_84 + 0x11A] = 0;
    sp[var_84 + 0x119] = 0;

    uint8_t r8 = (r6[1] << 8) | r6[0];
    r6 += 3;
    sub_C8D88(r8, r6, sp + var_84 + 0x11D);

    r6--;
    sp[var_84 + 0xFB] = *r6;
    sp[var_84 + 0xFD] = 2;
    sub_9DFA2(0, 0x03, sp + var_84 + 0xFA);
    if (r10 == 0) {
        uint8_t r8 = sp[var_84 + 0];
        // Do something with r8
    }
}