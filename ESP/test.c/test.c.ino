#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include "WiFiManager.h" 
int port = 8888;  
WiFiServer server(port);   
#include<SoftwareSerial.h>
#include <stdio.h> 
#include <stdlib.h>
SoftwareSerial s(3, 1);
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);

//----------------Biến--------------//
int button = 12; //GPIO12 -- D6  
int buttonState = 0;
int count = 0;
char *count_char ="";
char uart_data_rcv[50];
int tt_rcv_uart = 0;
int data = 0;
int len_data =0;
int count1=0;
 //Port number
//----------------Hàm--------------//

/***********RESET_ESP XOA_WIFI***********/
void reset_erase_wifi(){
  WiFiManager wifiManager;
  wifiManager.erase();
  ESP.reset();
  }
void checkbutt(){
  for( int i=0; i<20; i++){
      digitalWrite(LED_BUILTIN, LOW);
      delay(75);
      buttonState=digitalRead(button);       
      if (!buttonState){ return; }      
      digitalWrite(LED_BUILTIN, HIGH);
      delay(75);          
    }
    digitalWrite(LED_BUILTIN, HIGH);
    delay(750);
    digitalWrite(LED_BUILTIN, LOW);
    reset_erase_wifi();
  }
/***********WIFI MANAGER***********/
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
  // xóa config wifi wifiManager.erase()
  //  if (0){
  //    wifiManager.erase();
  //  }
  
  //Cài đặt callback, khi kết nối với wifi cũ thất bại, thiết bị sẽ gọi hàm callback
  //và khởi động chế độ AP với SSID được cài tự động là "ESP+chipID"
  wifiManager.setAPCallback(configModeCallback);
  if (!wifiManager.autoConnect("NODE_ESP","1234567890"))
  {
    s.println("failed to connect and hit timeout");
    //Nếu kết nối thất bại, thử kết nối lại bằng cách reset thiết bị
    ESP.reset();
    delay(1000);
  }
  //Nếu kết nối wifi thành công, in thông báo ra màn hình
  s.println("connected...hoanglv30vn");  
  server.begin();
  s.print("Open Telnet and connect to IP:");
  s.print(WiFi.localIP());
  s.print(" on port ");
  s.println(port);    
  }
/***********UART***********/
  int read_uart_int(){
    int index = 1;
    while(tt_rcv_uart){    
       data = s.read();
       if (data < 0)   {        
          tt_rcv_uart = 0;
        }
        else{
          uart_data_rcv[index]=data;
          index++; 
        }
      }    
      return  index;
    }
  int read_uart(){
      int index = 0;  
      tt_rcv_uart = 0;  
      data = s.read();   
      if (data >0)
      {       
        uart_data_rcv[0]=data;
        tt_rcv_uart = 1;
        index = read_uart_int();  
      }              
    return  index;
  }  
/***********TCP***********/  
void client_wifi(){
    WiFiClient client = server.available();  
     if (client) {
    if(client.connected())
    {
      s.println("Client Connected");
    }
    
    while(client.connected()){      
      while(client.available()>0){
        // read data from the connected client
        s.write(client.read()); 
      }
      //Send Data to connected client
      while(s.available()>0)
      {
        client.write(s.read());
      }
    }
    client.stop();
    s.println("Client disconnected");    
  }
}
void setup() {
  //Serial S Begin at 9600 Baud  
  s.begin(9600);
  connect_config_wifi();
  WiFiServer server(port);  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(button, INPUT);
  lcd.begin();
  lcd.backlight();
  lcd.print("Heyyy u");

}

void loop() {  
  client_wifi();
  digitalWrite(LED_BUILTIN, HIGH);
  len_data = read_uart();
  itoa(count, count_char, 10);
  /*butt reset wifi, reset esp*/
  buttonState=digitalRead(button);
  if (buttonState){
    checkbutt();
    }
    
  s.write(count_char);
  s.write("\n");
  lcd.setCursor(0,1);
  lcd.print(uart_data_rcv); 
  lcd.setCursor(14,0);
  lcd.print(len_data);        
  lcd.setCursor(8,0);
  lcd.print(count);    
  //s.write(data);
  count++;
  delay(500);
  delay(500);
}
