#include <ESP8266WiFi.h>          //https://github.com/esp8266/Arduino

//các thư viện cần thiết
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include "WiFiManager.h"          //https://github.com/tzapu/WiFiManager


//serrial 

#include<SoftwareSerial.h>
SoftwareSerial s(3, 1);
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);


// khai baos bien
int count__ = 0;

void configModeCallback (WiFiManager *myWiFiManager)
{
  s.println("Entered config mode");
  s.println(WiFi.softAPIP());
  s.println(myWiFiManager->getConfigPortalSSID());
}
void connect_config_wifi(){
    
  //Khai báo wifiManager thuộc class WiFiManager, được quy định trong file WiFiManager.h
WiFiManager wifiManager;
  //có thểreset các cài đặt cũ bằng cách gọi hàm:
  //wifiManager.resetSettings();
//  if (0){
//    wifiManager.erase();
//  }
  
  //Cài đặt callback, khi kết nối với wifi cũ thất bại, thiết bị sẽ gọi hàm callback
  //và khởi động chế độ AP với SSID được cài tự động là "ESP+chipID"
//  wifiManager.autoConnect("NODE_ESP");
  wifiManager.setAPCallback(configModeCallback);
  if (!wifiManager.autoConnect("NODE_ESP","1234567890"))
  {
    s.println("failed to connect and hit timeout");
  //Nếu kết nối thất bại, thử kết nối lại bằng cách reset thiết bị
    ESP.reset();
    delay(1000);
  }
  //Nếu kết nối wifi thành công, in thông báo ra màn hình
  s.println("connected...yeey :)");
  }
  // Cài đặt thông số ban đầu
void setup()
{
  s.begin(9600);
  connect_config_wifi();
  pinMode(LED_BUILTIN, OUTPUT);  
  lcd.begin();
  lcd.backlight();
  lcd.print("Heyyy uu");
}

void loop()
{
  count__++;

  lcd.setCursor(14,0);  
  lcd.print(count__);   
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW); 
  delay(500);
}
