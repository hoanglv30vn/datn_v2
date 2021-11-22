VOID READ_BTN_STATE()
{
   
   INT TB = 0;
   INT ID_TB =52;
   FOR (TB = 0; TB < SOLUONGTHIETBI_CONFIG; TB++)
   {   IF (TB>3) ID_TB = 64;
       IF (!INPUT (ID_TB + TB))
      {  
         DELAY_MS(200);
         TT_THIETBI_TEMP[TB] = ~TT_THIETBI_TEMP[TB];         
      }
   }
/*
   FOR (TB = 0; TB < 4; TB++)
   {

      IF (!INPUT (68 + TB))
      {
          DELAY_MS(200);
          TT_THIETBI_TEMP[TB + 4] = ~TT_THIETBI_TEMP[TB + 4];           
      }
   }
*/
}
INT BIN_TO_DEC()
{
   INT8 DEC_VL = 0 ; 
   INT8 BASE = 1;
   INT8 I;
   FOR (I=0;I<8;I++)
   {
   DEC_VL = DEC_VL+ BASE*TT_THIETBI_TEMP[I];
   BASE = BASE*2;
   }
   RETURN DEC_VL;

}
 
 VOID XUAT_DIEU_KHIEN()
 {
   LENH_DIEU_KHIEN = BIN_TO_DEC();
   XUATTRANGTHAI (LENH_DIEU_KHIEN) ;  
   FOR (INT ST=0;ST<8;ST++){
      TEMP_CHAR = "0";
      ITOA(TT_THIETBI_TEMP[ST],10,TEMP_CHAR);      
   }
   //CHAR *PACKAGE_CONFIG[]={"*", "LENGHT","CF", "ID_GW1234" ,"ID_NODE","#"};
   IF(LENH_DIEU_KHIEN<10) TEMP_CHAR ="22";
   ELSE IF(LENH_DIEU_KHIEN>=10 && LENH_DIEU_KHIEN <100) TEMP_CHAR ="23";
   ELSE TEMP_CHAR ="24";    
   PRINTF ("*@");
   PRINTF (TEMP_CHAR);
   PRINTF ("@DK@");
   PRINTF (ID_GATEWAY_CHAR);
   PRINTF ("@");
   PRINTF (ID_NODE_CHAR);
   PRINTF ("@");
   ITOA(LENH_DIEU_KHIEN,10,TEMP_CHAR);
   PRINTF (TEMP_CHAR);
   PRINTF ("@#");
   
   
   LCD_GOTOXY (1, 2) ;
   DELAY_MS (10);
   PRINTF (LCD_PUTC, "SW: ");    
   FOR (ST=0;ST<8;ST++){
      TEMP_CHAR = "0";
      ITOA(TT_THIETBI_TEMP[ST],10,TEMP_CHAR);
      PRINTF (LCD_PUTC, TEMP_CHAR);
   }   
   
 }
 VOID DIEUKHIENTHIETBI ()
 {
    INT MA_DEC = 0;
    MA_DEC = ATOI (KYTUCHAR2);

   UNSIGNED INT8   SB;   
   #BIT BSERI  = MA_DEC.0
   
   FOR (SB=0;SB<8;SB++)
      {                                                    
         TT_THIETBI_TEMP[SB] = BSERI;
         MA_DEC=MA_DEC>>1; 
     }    
    XUAT_DIEU_KHIEN();
 }

