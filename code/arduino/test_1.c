#include <M5StickC.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WiFi.h>

/* 初期設定 */
#define SRV 26
#define SRV_CH 0  //チャンネル
const double PWM_Hz = 50;   //PWM周波数
const uint8_t PWM_level = 16; //PWM 16bit(0～65535)
#define DEV_ID "m5stickc_1"              //観測デバイス名
#define ACCESS_POINT "hogahoga"         // WiFi アクセスポイント
#define PASSWORD "hugehuge"              // WiFi password
#define URL "http"  // http送信先アドレス
HTTPClient http;  // HTTPアクセスクライアント
int httpCode;
char url[64];
DynamicJsonDocument json_request(500);
DynamicJsonDocument json_receive(500);
char buffer[1024];                                // 送信文字列
char comment[64] = "none";  // comment送信用

void send_data(void){
  //データ送信
        // JSONデータに埋めていく
        json_request["id"] = DEV_ID;
        //json_request["send_date"] = now;
        //json_request["on_signal"] = 0;
        //json_request["off_signal"] = 0;
        json_request["comment"] = comment;
        // HTTP POST
        sprintf(url, "%s/add", URL);
        http.begin(url);
        http.addHeader("Content-Type", "application/json");
        // JSONを文字列に変換
        serializeJson(json_request, buffer, sizeof(buffer));
        Serial.println(buffer);
        // JSONを変換した文字列をPOSTで送信
        httpCode = http.POST((uint8_t *)buffer, strlen(buffer));
        Serial.printf("[HTTP] POST... code: %d\n", httpCode);
        http.end();
}

void setup() {
  m5.begin();
  Serial.begin(19200);
  Serial.print("...\n");
  pinMode(SRV, OUTPUT);
 
  //モータのPWMのチャンネル、周波数の設定
  ledcSetup(SRV_CH, PWM_Hz, PWM_level);
  //モータのピンとチャンネルの設定
  ledcAttachPin(SRV, SRV_CH);

  // WiFi接続
  WiFi.begin(ACCESS_POINT, PASSWORD);
  M5.Lcd.setCursor(0, 0);
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.print("\nConnecting\n Wifi...\n");
  while (WiFi.status() != WL_CONNECTED) {
      delay(1000);  //  接続確立まで待つ
  }
  // clear screen
  M5.Lcd.fillScreen(BLACK);
  delay(300); 
}

void loop() {
  M5.update();
  sprintf(comment, "none");  // default comment
  /*
  for (int i = 2295; i <= 7535; i=i+5) {   //700μsec -> 2300μsec
    ledcWrite(srv_CH0, i);
    delay(10);
  }
  for (int i = 7535; i > 2295; i=i-5) {   //2300μsec -> 700μsec
    ledcWrite(srv_CH0, i);
    delay(10);
  }
  */
  /*
  // webAPI側からの直接操作をデータベースに問い合わせ
  // HTTP GET
    sprintf(url, "%s/get", URL);
    http.begin(url);
  httpCode = http.GET();
  Serial.printf("[HTTP] GET... code: %d\n", httpCode);
    String payload = http.getString();
    Serial.println(payload);
    //文字列をJSONに変換
    deserializeJson(json_receive, payload);
    int on_signal = json_receive["on_signal"];
    int off_signal = json_receive["off_signal"];
    // String comment = json_receive["comment"];
    on_signal = 0;
    off_signal = 0;
    http.end();
    */
    int on_signal = 0, off_signal = 0;

  if (M5.BtnA.wasPressed() || on_signal ){
    ledcWrite(SRV_CH, 2300);
    sprintf(comment, "Door OPEN");
    //send_data();
    M5.Lcd.setCursor(0, 25);
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.println("Door OPEN");
    delay(100);
  }
  if (M5.BtnB.wasPressed() || off_signal ){
    ledcWrite(SRV_CH, 6000);
    sprintf(comment, "Door OPEN");
    //send_data();
    M5.Lcd.setCursor(0, 25);
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.println("Door CLOSE");
    delay(100);
  }
  //delay(1000);
}