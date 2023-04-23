void sub_93704(unsigned char* input, unsigned char* output)
{
    unsigned char temp1, temp2;
    unsigned char *table = (unsigned char*)0x88050000;

    temp1 = input[0];
    temp2 = input[1];

    output[0] = table[(temp1 >> 2) & 0x3F];
    output[1] = table[((temp1 & 0x03) << 4) | ((temp2 >> 4) & 0x0F)];
    output[2] = table[((temp2 & 0x0F) << 2)];

    return;
}