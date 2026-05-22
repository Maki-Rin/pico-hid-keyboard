#include <Arduino.h>
#include <Keyboard.h>

// ===== カスタマイズ箇所 =====

// ボタンを接続した GPIO 番号（何個でも増減可能）
const uint8_t BUTTON_PINS[] = {3, 5, 7};

// 各ボタンを押したときに送信する文字列
// BUTTON_PINS と同じ順・同じ個数にすること
const char *MACROS[] = {
    "Hello, World!\n",
    "macro2\n",
    "macro3\n",
};

// ===========================

const uint8_t BUTTON_COUNT = sizeof(BUTTON_PINS) / sizeof(BUTTON_PINS[0]);
bool prevState[BUTTON_COUNT];

void setup()
{
    for (uint8_t i = 0; i < BUTTON_COUNT; i++)
    {
        pinMode(BUTTON_PINS[i], INPUT_PULLUP);
        prevState[i] = HIGH;
    }
    Keyboard.begin();
}

void loop()
{
    for (uint8_t i = 0; i < BUTTON_COUNT; i++)
    {
        bool cur = digitalRead(BUTTON_PINS[i]);
        if (cur == LOW && prevState[i] == HIGH)
        {
            Keyboard.print(MACROS[i]);
        }
        prevState[i] = cur;
    }
    delay(10);
}
