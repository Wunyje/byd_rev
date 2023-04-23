#include <stdio.h>

int main()
{
    int r2 = 0;
    long int r6 = 0;
    long int r5 = 0xFEBE55D4;
    long int r5_ptr[0x40]  = {0};
    long int r5_value[0x40] = {0};

    do {
        r6 = r2;
        r6 = (r6 * 0x4C) & 0xFFFFFFFF;
        r5 = r6 + 0xFEBE55D4;
        
        if(r2 > 0x3F || r2 == 0x3F)
            break;
        else
        {
            r2++;
            r6 = (r2 * 0x4C) & 0xFFFFFFFF;
            *(r5_ptr + r2 - 1) = 0xFEBE55D4 + r6;
            *(r5_value + r2 - 1) = r5;
        }
    } while (1);
    *(r5_ptr + 0x3F) = 0xFEBE55D4;
    r2 = 0;

    return 1;
}

