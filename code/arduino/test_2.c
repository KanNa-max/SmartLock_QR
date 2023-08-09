#include <M5StickC.h>

int led1 = 26;
// PWMの設定
const double PWM_Hz = 50;      // PWM周波数
const uint8_t PWM_level = 16;  // PWM 16bit(0～65535)
int lock_f = 0;

void setup() {
    Serial.begin(115200);
    m5.begin();
    pinMode(led1, OUTPUT);
    //モータのPWMのチャンネル、周波数の設定
    ledcSetup((uint8_t)1, PWM_Hz, PWM_level);

    //モータのピンとチャンネルの設定
    ledcAttachPin(led1, 1);

    // clear screen
    M5.Lcd.setCursor(0, 25);
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.println("Door\n auto system\n-------------\n");
    delay(300);
}

void loop() {
    M5.update();

    if (M5.BtnA.wasPressed()) {
        /*OPEN*/
        if (lock_f == 0) {
            M5.Lcd.setCursor(0, 25);
            M5.Lcd.fillScreen(BLACK);
            M5.Lcd.println("Door\n auto system\n-------------\n");
            M5.Lcd.println("Door OPEN");
            for (int i = 2300; i <= 9000; i = i + 100) {
                ledcWrite(1, i);
                delay(30);
            }
            delay(100);
            for (int i = 9000; i > 2300*2; i = i - 100) {
                ledcWrite(1, i);
                delay(30);
            }
            lock_f = 1;
        }
        /*CLOSE*/
        else if (lock_f == 1) {
            M5.Lcd.setCursor(0, 25);
            M5.Lcd.fillScreen(BLACK);
            M5.Lcd.println("Door\n auto system\n-------------\n");
            M5.Lcd.println("Door CLOSE");
            for (int i = 9000; i > 2300; i = i - 100) {
                ledcWrite(1, i);
                delay(30);
            }
            delay(100);
            for (int i = 2300; i <= 9000/2; i = i + 100) {
                ledcWrite(1, i);
                delay(30);
            }
            lock_f = 0;
        }
        /*clear screen*/
        M5.Lcd.setCursor(0, 25);
        M5.Lcd.fillScreen(BLACK);
        M5.Lcd.println("Door\n auto system\n-------------\n");
    }
}