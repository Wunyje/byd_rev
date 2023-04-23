void crypt_fun_1(char* replay_data) {
    char* decrypt_replay_data = NULL;
    int length = strlen(replay_data);

    if (length > MAX_LENGTH) {
        decrypt_replay_data = aDecryptReplayD;
        // sub_93366 is not provided, need to be implemented
        sub_93366(); // call sub_93366(decrypt_replay_data);
        return;
    }

    char arg_1, arg_2;
    arg_1 = replay_data[2];
    arg_2 = replay_data[1];

    int result1 = sub_C8D88(arg_2, 0xFEBD9C00);
    int result2 = sub_C8D88((replay_data[0] << 8) | replay_data[1], 0xFEBD9C00);

    int arg_12 = 0x12;
    int result3 = sub_C8D88(arg_1, arg_2);

    int i = 0;
    for (; i <= 0xE; i++) {
        int temp1 = result2 + i;
        int temp2 = sub_9D7B4(arg_1, temp1);
        result1 += temp2;
        result3 += (replay_data[arg_12++] + ((temp2 & 0xFF00) >> 8));
        result2 += (result3 & 0xFF);
        result2 = (result2 << 8) | ((result1 >> 8) & 0xFF);
        result1 &= 0xFF;
        int temp3 = (result2 & 0xFFF8) << 3;
        int temp4 = temp3 - result2;
        result1 += temp4;
    }

    int temp5 = ((result2 & 0xFFF8) << 3) - result2;
    for (; i <= temp5; i++) {
        result3 += ((arg_1 << 8) | arg_2) - result2;
        result2 = ((result3 & 0xFF) << 8) | ((result1 >> 8) & 0xFF);
        result1 &= 0xFF;

        int temp6 = (result2 & 0xFFF8) << 3;
        int temp7 = temp6 - result2;
        result1 += temp7;

        int temp8 = (temp6 & 0x7FFF8) - result2;
        result3 += replay_data[temp8];
    }
}
