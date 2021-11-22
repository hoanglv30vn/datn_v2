//#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include "WiFiManager.h" 
#include <stdio.h> 
#include <stdlib.h>
#include<SoftwareSerial.h>
SoftwareSerial s(3, 1);
#include <Wire.h>
WiFiClient client;
#include <EEPROM.h>


//----------------Biến--------------//
const int button = 12; //GPIO12 -- D6  
const int led_baohieu = 14; //GPIO12 -- D6  
int buttonState = 0;
//char *data_uart_char ="";
char *len_data_char;   
char uart_data_rcv[50];
int tt_rcv_uart = 0;
int data = 0;
int index_tcp =0;
int len_data =0;
bool tt_tcp= false;
bool tt_config_client = 0;
bool state_connect_tcp = false;

const uint16_t port = 8888;
String host = "192.168.0.000";

String name_esp = "";
String HEADER_NAME = "";
String HEADER_LENGHT = "";
char HEADER_SEND[60];
char data_send[60];
char data_read_tcp[60];
//----------------Hàm--------------//
/*get name esp*/
String getNameESP(){
  String hostString = String(WIFI_getChipId(),HEX);
  hostString.toUpperCase();
  // char hostString[16] = {0};
  // sprintf(hostString, "%06X", ESP.getChipId());  
  return  "ESP_" + hostString;
}

/***********RESET_ESP XOA_WIFI***********/
void reset_erase_wifi()
{
  WiFiManager wifiManager;
  wifiManager.erase();
  int i = 0;
  for( i=0;i<25;i++)
  {
    EEPROM.write(0x0F+i, '0'); //Write one by one with starting address of 0x0F
  }     
  EEPROM.write(0x0F+i, '0');
  EEPROM.commit();   
  
  ESP.reset();
}
void checkbutt(){
  for( int i=0; i<20; i++)
  {
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
  if (!wifiManager.autoConnect("","1234567890"))
  {
    s.println("failed to connect and hit timeout");
    //Nếu kết nối thất bại, thử kết nối lại bằng cách reset thiết bị
    ESP.reset();
    delay(1000);
  }
  //Nếu kết nối wifi thành công, in thông báo ra màn hình
  s.println("connected...hoanglv30vn");    
  }

  /***********UART***********/
  int read_uart_char(){
    int index = 0;
    tt_rcv_uart = 1;
    data = s.read();
    if (data > 0)   
    {                                 
      for (int i = 1; i<50; i++)
      {
        uart_data_rcv[i]='\0';
      } 
      uart_data_rcv[0]=data;  
      while(tt_rcv_uart)
      {    
        data = s.read();
        if (data < 0)
        {                            
          tt_rcv_uart = 0;
        }
        else 
        {
          index++;
          uart_data_rcv[index]=data;           
        }
      }                  
    }        
   delay(10);
  return  index;
  }

void config_client_host_port(){
  tt_config_client = 1;
  int cf_clt_tcp = 0;
  int host_bg, host_end;
  len_data = 0;
  host = "";
  digitalWrite(led_baohieu, LOW);
  int i=0;
  while(EEPROM.read(0x0F+i)!='$' && i<20 ){
    host = host + char(EEPROM.read(0x0F+i));
    i++;
  }  
//  if (!client.connect(host, port)){
//    tt_config_client = 1;
//  }
//  else tt_config_client = 0;
  while(!client.connect(host, port)){    
    delay(100);
    len_data = read_uart_char();
    if (len_data>0){
      String data_cf = uart_data_rcv ;            
      s.println("hihi");      
      s.println(data_cf);
      cf_clt_tcp = data_cf.indexOf("CF_CLIENT_TCP");
      if (cf_clt_tcp >= 0){
        host_bg =  data_cf.indexOf("_TCP%");
        host_end =  data_cf.indexOf("#TCP%");
        host = data_cf.substring(host_bg+5,host_end);
        for( i=0;i<host.length();i++)
        {
          EEPROM.write(0x0F+i, host[i]); //Write one by one with starting address of 0x0F
        }     
        EEPROM.write(0x0F+i, '$');
        EEPROM.commit();   
        tt_config_client = 0;
      }
    }    
  }
}

bool check_connect_serve_tcp(){
    client.flush();
    if (!client.connected()) {
      buttonState=digitalRead(button);  
      delay(250);
      if (buttonState){
        checkbutt();
        }         
      digitalWrite(led_baohieu, LOW);
      delay(200);
      digitalWrite(led_baohieu, HIGH);
      delay(200);
//      Serial.println();
//      Serial.println("disconnecting.");
      client.flush();
      client.stop();
      client.connect(host, port);
      client.write(HEADER_SEND);     
      return false;       
    }
    else return true;       
  
}

void read_data_tcp(){
      tt_tcp = false;      
    index_tcp = 0;  
    while (client.available() > 0 && index_tcp<60)
    {
        char c = client.read();
//        s.write(c); 
        data_read_tcp[index_tcp] = c;
        tt_tcp = true;
        index_tcp ++;
    }
    if (tt_tcp){
      client.flush();
      s.write(data_read_tcp); 
      delay(100);
      for (int i = 0; i<60; i++)
      {
        data_read_tcp[i]='\0';
      }            
    }
}
  
void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
    EEPROM.begin(512);
    s.begin(9600);    
    connect_config_wifi();
    for (int i = 0 ; i<10; i++){
       digitalWrite(LED_BUILTIN, LOW);
       delay(300);
       digitalWrite(LED_BUILTIN, HIGH);
       delay(300);
    }
    digitalWrite(LED_BUILTIN, LOW);
    config_client_host_port();
    pinMode(led_baohieu, OUTPUT);
    digitalWrite(led_baohieu, LOW);    
    digitalWrite(LED_BUILTIN, HIGH);
    
    name_esp = getNameESP();         
    int i= 0;    
    HEADER_LENGHT = "10";
    for (i=1; i<9; i++) {
      HEADER_LENGHT +=" ";
    }    
    HEADER_NAME = HEADER_LENGHT + name_esp;
    for( i =0; i<60; i++){
      HEADER_SEND[i] = HEADER_NAME[i];      
    }
    client.connect(host, port);
    client.write(HEADER_SEND);
//    client.connect(host, port);
    
}

void loop()
{    
    digitalWrite(led_baohieu, HIGH);
    //s.println("Connected to server successful!");
    //client.println("Hello From ESP8266");           
    read_data_tcp();
    state_connect_tcp = check_connect_serve_tcp();
    len_data = read_uart_char();
    delay(250);
    if (len_data>10 && len_data <100){
        int i= 0;                            
        len_data_char  = "10";
        itoa(len_data,len_data_char,10);            
        for (i=0; i<2; i++) {
          HEADER_LENGHT[i] = *len_data_char;
          data_send[i] = *len_data_char;
          *len_data_char ++;          
        } 
        for( i =2; i<11; i++){
          data_send[i] = ' ';      
        }
        for( i =10; i<len_data+10; i++){
          data_send[i] = uart_data_rcv[i-10];      
        }   
//        client.connect(host, port);
//           
        len_data = 0;
        for (int i = 0; i<50; i++)
        {
          uart_data_rcv[i]='\0';
        }
        if (state_connect_tcp)   {
           client.write(data_send);  
        }
        
        /*XOA DATA UART*/                 
    }
    else {
      int reset_esp=-1;
      String data_rset = uart_data_rcv ;       
      reset_esp = data_rset.indexOf("RST_ESP");
      if (reset_esp >= 0){
        client.connect(host, port);
        client.write(HEADER_SEND);        
//        ESP.reset();
      }
    }
    buttonState=digitalRead(button);  
    delay(250);
    if (buttonState){
      checkbutt();
      }    
    //s.print('\n');
//    client.stop();
//    delay(5000);
}
