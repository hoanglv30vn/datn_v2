#include "types.h"
#define DS1820_DATAPIN  PIN_A0
#include <ds18b20.h>



float KET_QUA_ANALOG[]={0,0,0,0,0};


//int16 temperature_raw; /*Du lieu nhiet do (resolution 1 / 256°C) */
float temperature_float; /* Gia tri nhiet do do duoc */
//char temperature[8];  /* Mang luu gia tri nhiet do*/
unsigned int8 sensor_count = 0;
float KET_QUA_ANALOG_TEMP=0;




 VOID READ_ANALOG ()
 {
   /*
   FOR (INT I =0; I<5; I++){
   KET_QUA_ANALOG[I]=0;
   }
   */
   float CHENH_LECH = 0;
   if ( DS1820_FindFirstDevice() ){
      do
      {               
         KET_QUA_ANALOG_TEMP = KET_QUA_ANALOG[sensor_count];
         //temperature_raw = DS1820_GetTempRaw();
         //DS1820_GetTempString(temperature_raw, temperature);
         temperature_float = DS1820_GetTempFloat();
         //fprintf(UART, "Sensor %d: %f°C \n\r", sensor_count, temperature_float);    
         
         KET_QUA_ANALOG[sensor_count] = temperature_float  ;
         
         CHENH_LECH = ABS( KET_QUA_ANALOG[sensor_count] -KET_QUA_ANALOG_TEMP );                  
         IF (CHENH_LECH>0.2){
            TT_SEND_ANALOG = 1;
         }
         //KET_QUA_ANALOG_TEMP[sensor_count] = KET_QUA_ANALOG[sensor_count];         
         
         sensor_count ++;
      }
      while ( DS1820_FindNextDevice() && SOLUONGCAMBIEN_CONFIG > sensor_count);
      sensor_count = 0;
   }     
 }


 VOID SEND_ANALOG_UART ()
 {
    TT_SEND_ANALOG = 0;
    OUTPUT_TOGGLE (PIN_C4) ;
    //CHAR * PACKAGE_SS[] ={" * ", "26", "SS", "IDGW12", "NODE", "ZZ", "AA", "VV", "CC", "SS"};
    CHAR * PACKAGE_SS[] ={"IDGW12", "NODE", "ZZZZZ", "AAAAA", "VVVVV", "CCCCC"};
    PACKAGE_SS[0] = ID_GATEWAY_CHAR;
    PACKAGE_SS[1] = ID_NODE_CHAR;
    UNSIGNED INT8 DO_DAI = 20;
    UNSIGNED INT8 I = 0;
    UNSIGNED INT8 K = 2;    
   WHILE (I < SOLUONGCAMBIEN_CONFIG){
      sprintf(PACKAGE_SS[K], "%g", KET_QUA_ANALOG[I]);
      //DO_DAI = DO_DAI + strlen(PACKAGE_SS[K])+1;    
      DO_DAI = DO_DAI + 5+1;    
      I++;
      K++;
   }
    ITOA (DO_DAI, 10, TEMP_CHAR2) ;
    PRINTF ("*@");
    PRINTF (TEMP_CHAR2);
    PRINTF ("@SS@");
    FOR (I = 0; I < 2 + SOLUONGCAMBIEN_CONFIG; I++)
    {
       PRINTF (PACKAGE_SS[I]);
       PRINTF ("@");
    }

    PRINTF ("#");
    OUTPUT_TOGGLE (PIN_C4) ;
    
 }


