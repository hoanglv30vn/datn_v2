#INCLUDE <16F887.H>

#INCLUDE <STRING.H>
#INCLUDE <STDLIB.H>
#INCLUDE <STDIO.H>
#include <TIME.h>
#INCLUDE <MATH.H>
//#INCLUDE <TV_LCD.C>
#include <math.h>
/*
int atoi(CONST char *s) : sting --> s� nguy�n
long atol(CONST char *s) : string --> s� nguy�n d�i
float atof(CONST char *s) : string --> s� thuc
*/
#FUSES NOWDT, PUT, HS
#USE DELAY(CLOCK=20M)
#USE RS232(BAUD=9600,XMIT=PIN_C6,RCV=PIN_C7)
#define LCD_ENABLE_PIN  PIN_E0                                   
#define LCD_RS_PIN      PIN_E1                                
#define LCD_RW_PIN      PIN_E2                              
#define LCD_DATA4       PIN_D4                               
#define LCD_DATA5       PIN_D5                                 
#define LCD_DATA6       PIN_D6                                   
#define LCD_DATA7       PIN_D7  
#INCLUDE <LCD.C>


CHAR ENCODE_,CHUOIMAHOA[]="HIIHI";

int count_C(int16 m, int16 e, int16 n){
   int32 so_mu = pow(m, e);
   return so_mu % n;
}

VOID ENCODE(CHAR *P){
   LCD_GOTOXY (1, 2);
         DELAY_MS(500);
      PRINTF (LCD_PUTC, P);   
   FOR(int i=0; i < P[i]; i++){
      //int16 somahoaascii = (i+1)*m - i + 5;
      //if (somahoaascii > 9)
       //   somahoaascii = 10;
      CHUOIMAHOA[i]=P[i];
   
   }
}

VOID MAIN()
{
   SET_TRIS_D (0XF0);
   SET_TRIS_B (0xFF);
   SET_TRIS_E (0);
   SETUP_ADC (ADC_CLOCK_DIV_8);
   SETUP_ADC_PORTS (0x00011);
   OUTPUT_LOW (PIN_D0);
   LCD_INIT (); // KHOI TAO LCD
   //CHUOIMAHOA= "hello";
   LCD_GOTOXY (1, 1);
   DELAY_MS (10);
   PRINTF (LCD_PUTC, "Hoang");
   DELAY_MS (2000);
   ENCODE_ = "CHAOHIHI";
   ENCODE(ENCODE_);
   //LCD_GOTOXY (1, 2);
   DELAY_MS (10);
   //PRINTF (LCD_PUTC, CHUOIMAHOA);
   DELAY_MS (1000);
   WHILE (TRUE)
   {
      
   }
   
}



