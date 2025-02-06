#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <string.h>
#include <wiringPi.h>
#include "aes.h"

// GPIO 핀 번호 설정
#define TRIGGER_PIN 5

void aes()
{
    if (wiringPiSetupGpio() < 0)
    {
        fprintf(stderr, "wiring PI error");
        return;
    }
    pinMode(TRIGGER_PIN, OUTPUT);

    // 128bit key
    uint8_t plaintext[16] = { 0x00, };
    // 128bit key
    uint8_t key[16] = { 0x59, 0x6f, 0x75, 0x20, 0x52, 0x20, 0x53, 0x43, 0x41, 0x20, 0x4d, 0x61, 0x73, 0x74, 0x65, 0x72 };

    for (int byteindex = 0; byteindex < 16; byteindex++)
    {
        scanf("%2hhx", &plaintext[byteindex]);
    }
    struct AES_ctx ctx;
    AES_init_ctx(&ctx, key);
    
    // 트리거 신호 출력 (HIGH 상태)
    digitalWrite(TRIGGER_PIN, HIGH);

    AES_ECB_encrypt(&ctx, plaintext);

    // 트리거 신호 끄기 (LOW 상태)
    digitalWrite(TRIGGER_PIN, LOW);
    
    for (int byteindex = 0; byteindex < 15; byteindex++)
    {
        printf("%02x ", plaintext[byteindex]);
    }
    printf("%02x\n", plaintext[15]);
}

int main()
{
    aes();

    return 0;
}
