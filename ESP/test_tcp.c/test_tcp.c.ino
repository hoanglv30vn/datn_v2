#include <ESP8266WiFi.h>
int port = 8888;  //Port number
WiFiServer server(port);
char *ssid = "Wifi của Hoàngs";  //Enter your wifi SSID
char *password = "matkhauwifia";  //Enter your wifi Password
int count1=0;

#include<SoftwareSerial.h>
#include <stdio.h> 
#include <stdlib.h>
SoftwareSerial s(3, 1);
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);


int count = 0;
char *count_char ="";
char uart_data_rcv[50];
int tt_rcv_uart = 0;
int data = 0;
int len_data =0;
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
void setup_wifi(){
  int count_time_connect = 0;
  WiFi.mode(WIFI_STA);
WiFi.begin(ssid, password); //Connect to wifi
s.println("Connecting to Wifi");
while (WiFi.status() != WL_CONNECTED) {   
  delay(500);
  s.print(".");
  delay(500);
  count_time_connect++;
  if(count_time_connect > 20){
    s.println("khong the ket noi");
    return;
    }
  
  
}
  s.println("");
  s.print("Connected to ");
  s.println(ssid);
  s.print("IP address: ");
  s.println(WiFi.localIP());  
  server.begin();
  s.print("Open Telnet and connect to IP:");
  s.print(WiFi.localIP());
  s.print(" on port ");
  s.println(port);  
  }  
void setup() {
  //Serial S Begin at 9600 Baud
s.begin(9600);
setup_wifi();

pinMode(LED_BUILTIN, OUTPUT);
lcd.begin();
lcd.backlight();
lcd.print("Heyyy u");

}

void loop() {  
  client_wifi();
  len_data = read_uart();
  if(len_data>0){
    setup_wifi();
    
    }
  itoa(count, count_char, 10);
  //if (data >10)
  //s.write(count_char); 
  s.write(count_char);
  lcd.setCursor(0,1);
  lcd.print(uart_data_rcv); 
  lcd.setCursor(14,0);
  lcd.print(len_data);        
  lcd.setCursor(8,0);
  lcd.print(count);    
  //s.write(data);
  count++;
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW); 
  delay(500);
}
