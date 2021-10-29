
#INCLUDE <thuvien.c>

VOID QUET_PHIM()
{
   INT BDT = 0;

   WHILE (!INPUT (BT1_PIN)) //NEU NUT BAM DUOC BAM
   {
      IF (TMR1IF)
      {
         OUTPUT_TOGGLE (PIN_D2);
         TMR1IF = 0; SET_TIMER1 (3036); BDT++;
      }
   }

   IF (BDT > 20)
   {
      //CONFIG NODE
      TT_CONFIG = ~TT_CONFIG; // VAO TRANG THAI CONFIG
      TT_CONTROL = ~TT_CONTROL;
      //CONFIG_DONE ();
      TT_CONFIG_DONE = 1;
      TT_FUN = 0;
   }

   ELSE
   {
      BUTT_OKE (); //OKE
   }
}

#INT_EXT

 VOID NGAT_NGOAI ()
 {
    QUET_PHIM ();
 }

 #INT_RDA
 VOID NGAT ()
 {
    KYTUCHAR[VT] = GETCH ();

    IF (KYTUCHAR[VT] == '.')
    {
       KYTUCHAR[VT] = '\0';
       VT = 0;
       TTNHAN = 1;
    }

    ELSE
    VT++;
 }

 VOID XUATLCD ( CHAR CHUOI_PRINT[])
 {
    LCD_GOTOXY (1, 1) ;
    DELAY_MS (10);
    PRINTF (LCD_PUTC, CHUOI_PRINT);
    DELAY_MS (1);
 }
 VOID XACNHANCONFIG()
 {
   OUTPUT_D (0XFF);    
   DELAY_MS(500);
   LCD_GOTOXY (1, 1) ;
   DELAY_MS (10);
   PRINTF (LCD_PUTC,KYTUCHAR2);
   PRINTF (LCD_PUTC,"            ");
   DELAY_MS (1); 
   OUTPUT_D (0XFF);  
   LCD_GOTOXY (1, 2) ;
   DELAY_MS (10);
   PRINTF (LCD_PUTC,"                ");   
   OUTPUT_D (0X00);
   DELAY_MS(500);
   OUTPUT_D (0XFF);    
   DELAY_MS(500);
   OUTPUT_D (0X00);
   
 } 
 VOID DIEUKHIENTHIETBI()
 {
 
 }

 VOID XU_LY_UART()
 {
     //ID_NODE_NHAN = KYTU[1] - 48;
    //ID_DEVICE_NHAN = KYTU[2] - 48 + 64;
    //TT_DEVICE_NHAN = KYTU[3] - 48; // - 48 ASCII -- > S?. + 64 -- > PORT_D (D0 = 64)               

    /*TINH DO DAI*/
    CHAR CH = '*';
    CHAR *RET;
    *ID_NODE_NHAN = '\0';
    *ID_GW_NHAN = '\0';
    KYTUCHAR2 = "";
    UNSIGNED INT8 LEN_RET;    
    RET = STRCHR(KYTUCHAR,CH);
    LEN_RET = STRLEN(RET); 
    /* LAY TOKEN DAU TIEN */    
    KYTU = 0;
    TEMP_CHAR = "#";
    CHAR * TOKEN;
    TOKEN = STRTOK (KYTUCHAR, TEMP_CHAR);                
    /* DUYET QUA CAC TOKEN CON LAI */                
    WHILE (TOKEN != NULL)
    {                
       SWITCH(KYTU)
       {
         CASE 0:
         BREAK;
         CASE 1: 
         STRCAT (ID_GW_NHAN, TOKEN);
         BREAK;                     
         CASE 2:
         STRCAT (ID_NODE_NHAN, TOKEN);
         BREAK;      
         CASE 3:
         LENHDIEUKHIEN =  ATOI(TOKEN);                 
         BREAK;    
         CASE 4:
         DODAI_DATA_NHAN =  ATOI(TOKEN);                 
         BREAK;  
         CASE 5:  
         STRCAT (KYTUCHAR2, TOKEN);
         BREAK;         
       }         
      TOKEN = STRTOK(NULL, TEMP_CHAR);
      KYTU++;        
    }              
      /* SO SANH ID returns -1 if s1<s2, 0 if s1=s2, 1 if s1>s2 */
      SOSANH_IDGW = STRCMP(ID_GW_NHAN,ID_GATEWAY_CHAR);      
      SOSANH_IDNODE = STRCMP(ID_NODE_NHAN,ID_NODE_CHAR);    
    IF ( SOSANH_IDGW == 0 && SOSANH_IDNODE == 0 && LEN_RET == DODAI_DATA_NHAN)
    {                      
      SWITCH(LENHDIEUKHIEN)
       {
         CASE 0:
         BREAK;
         CASE 1:
         XACNHANCONFIG();
         BREAK;                     
         CASE 2:
         //DIEUKHIENTHIETBI();
         BREAK;              
       } 
    }
    ELSE{
      DELAY_MS (10);
      /*DATA RCV SAI ID NODE, ID GW HOAC LA SAI DO DAI*/
    }
    
 }

 INT ADC_READ (INT KENH)
 {
    SET_ADC_CHANNEL (KENH);
    KQADC = 0;
    FOR (INT I = 0; I < 100; I++)
    {
       KQADC = KQADC + READ_ADC () ;
       DELAY_MS (1);
    }

    KQADC = KQADC / (100 * 2.046);
    RETURN KQADC;
 }

 VOID CHUONG_TRINH_CON ()
 {
    FOR (INT I = 0; I <= 30; I++)
    {
       OUTPUT_TOGGLE (PIN_D1);
       DELAY_MS (100);
    }
 }

 VOID MAIN  ()
 {
    SET_TRIS_D (0X00);
    SET_TRIS_B (0XFF);
    SET_TRIS_E (0);
    SET_TRIS_C (0X80);
    SETUP_ADC (ADC_CLOCK_DIV_8);
    SETUP_ADC_PORTS (SAN0);
    ENABLE_INTERRUPTS (INT_TIMER0);
    ENABLE_INTERRUPTS (INT_EXT); //CHO PHEP NGAT NGOAI
    ENABLE_INTERRUPTS (INT_EXT_H2L); //NGAT XAY RA KHI CO XUNG TU CAO XUONG THAP
    ENABLE_INTERRUPTS (INT_RDA);
    ENABLE_INTERRUPTS (GLOBAL);
    
    SETUP_TIMER_1 (T1_INTERNAL|T1_DIV_BY_8);
    //SET_TIMER1 (0);
    SET_TIMER1 (3036);
    TMR1IF = 0;
    LCD_INIT (); // KHOI TAO LCD

    TT_CONFIG = 0;
    TT_CONFIG_DONE = 0;
    TT_CONTROL = 1;
    OUTPUT_D (0X00);
    TTNHAN = 0;
    
   
    WHILE (TRUE)
    {
       IF (TT_CONFIG)             {BUTT_FUN (); } // GOI HAM CHON LENH (SWITCH CASE)
       ELSE IF (TT_CONFIG_DONE)   { CONFIG_DONE ();}       
       ELSE
       {
          WHILE (!TT_CONFIG)
          {
             CHUONG_TRINH_CON ();             
             IF (TTNHAN == 1)
             {
                TTNHAN = 0;
                XU_LY_UART();
             }
          }
       }
    }
 }

