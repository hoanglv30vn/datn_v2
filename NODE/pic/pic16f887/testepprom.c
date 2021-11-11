#INCLUDE <16F887.H>
#DEVICE ADC=10
#INCLUDE <STRING.H>
#INCLUDE <STDLIB.H>
#INCLUDE <STDIO.H>
#INCLUDE <MATH.H>
#INCLUDE <xuatbyte74595.c>
#FUSES NOWDT, PUT, HS
#USE DELAY(CLOCK=20M)
#USE RS232(BAUD=9600,XMIT=PIN_C6,RCV=PIN_C7)
#DEFINE BT1_PIN PIN_B1
#DEFINE BT2_PIN PIN_B2
#DEFINE BT3_PIN PIN_B3
#DEFINE LCD_ENABLE_PIN  PIN_E0                                   
#DEFINE LCD_RS_PIN      PIN_E1                                
#DEFINE LCD_RW_PIN      PIN_E2  
#DEFINE LCD_DATA4       PIN_C0                               
#DEFINE LCD_DATA5       PIN_C1                                 
#DEFINE LCD_DATA6       PIN_C2                                   
#DEFINE LCD_DATA7       PIN_C3  
#INCLUDE <LCD.C>

//#INCLUDE <khaibaobien.c> // VARIABLE.

VOID MAIN(){
    SET_TRIS_D (0XF0);
    SET_TRIS_B (0XFF);
    SET_TRIS_E (0);
    SET_TRIS_C (0X80);
    SETUP_ADC (ADC_CLOCK_DIV_8);
    ENABLE_INTERRUPTS (INT_TIMER0);
    ENABLE_INTERRUPTS (INT_EXT); //CHO PHEP NGAT NGOAI
    ENABLE_INTERRUPTS (INT_EXT_H2L); //NGAT XAY RA KHI CO XUNG TU CAO XUONG THAP
    ENABLE_INTERRUPTS (INT_RDA);
    ENABLE_INTERRUPTS (GLOBAL);
    
    SETUP_TIMER_1 (T1_INTERNAL|T1_DIV_BY_8);
    //SET_TIMER1 (0);
    SET_TIMER1 (3036);
    unsigned int8 countUP = 0;
    unsigned int8 countDW = 0;
    LCD_INIT (); // KHOI TAO LCD
    TT_CONFIG = 0;
    TT_CONFIG_DONE = 0;
    TT_CONTROL = 1;
    OUTPUT_HIGH (PIN_D3) ;
    TTNHAN = 0;


   LCD_GOTOXY (1, 2) ;
   DELAY_MS (10);
   PRINTF (LCD_PUTC, "DW: ");
   LCD_GOTOXY (1, 1) ;


//#INCLUDE <CONFIG_NODE.C> // CÂU HINH NODE.
   countUP = 0;
   countDW = read_eeprom(2);
   countUP = read_eeprom(3);//doc gia tri luu tai dia chi 0x02
   LCD_GOTOXY (1, 1) ;
   PRINTF (LCD_PUTC, "UP: ");
   while(TRUE)
   {
      //TODO: User Code
      write_eeprom(3, countUP);//luu gia tri vao dia chi 0x02
      write_eeprom(2, countDW);
      lcd_gotoxy(6,1);
      DELAY_MS(20);
      ITOA(countUP,10,TEMP_CHAR);
      printf(lcd_putc, TEMP_CHAR);
      PRINTF (LCD_PUTC, "    ");      
      lcd_gotoxy(6,2);
      DELAY_MS(20);
      ITOA(countDW,10,TEMP_CHAR);
      printf(lcd_putc, TEMP_CHAR);
      PRINTF (LCD_PUTC, "    ");
      DELAY_MS(360);
      countUP = countUP+1;
      countDW = countDW - 1;
   }

}
