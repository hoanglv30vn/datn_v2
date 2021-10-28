
//--------------------------------------------------------------------//
VOID CHON_ID()
{
   // TT_CONFIG_DONE;
   TT_CONFIG_DONE = 0;
   TT_STT = 1;
   UNSIGNED INT8 NUM = 0;
   TEMP_CHAR = "0";
   LCD_GOTOXY (1, 2) ;
   DELAY_MS (10);
   PRINTF (LCD_PUTC, "NODE: ");
   PRINTF (LCD_PUTC, "0000          ");
   LCD_GOTOXY (1, 1) ;
   PRINTF (LCD_PUTC, "      _              ");//6 SPACE PHIA TRUOC "_"
   //ID_GW = "1234";    

   WHILE (TT_STT)
   {
      IF (!INPUT (BT2_PIN)) //NEU NUT BAM DUOC BAM
      {
         
         NUM++;
         NUM = NUM % 4;
         LCD_GOTOXY (3 + NUM, 1);
         PRINTF (LCD_PUTC, "    _    ");//4SPACE
         DELAY_MS (300); 
      }

      ELSE IF (!INPUT (BT3_PIN))
      {
         ID_NODE[NUM]++;
         ID_NODE[NUM] = ID_NODE[NUM] % 10;
         ITOA (ID_NODE[NUM], 10, TEMP_CHAR);
         LCD_GOTOXY (7 + NUM, 2);
         DELAY_MS (10);
         PRINTF (LCD_PUTC, TEMP_CHAR);
         DELAY_MS (300);
      }
   }
}

VOID NHAPID_GW()
{
   UNSIGNED INT8 NUM = 0;
   TEMP_CHAR = "0";
   TT_CONFIG_DONE = 0;
   TT_STT = 1;
   LCD_GOTOXY (1, 2) ;
   DELAY_MS (10);
   PRINTF (LCD_PUTC, "ID_GW:");
   PRINTF (LCD_PUTC, "000000        ");
   LCD_GOTOXY (1, 1) ;
   PRINTF (LCD_PUTC, "      _                ");//6 SPACE PHIA TRUOC "_"
   //ID_GW = "1234";    

   WHILE (TT_STT)
   {
      IF (!INPUT (BT2_PIN)) //NEU NUT BAM DUOC BAM
      {
         
         NUM++;
         NUM = NUM % 6;
         LCD_GOTOXY (3 + NUM, 1);
         PRINTF (LCD_PUTC, "    _        ");//4SPACE
         DELAY_MS (300); 
      }

      ELSE IF (!INPUT (BT3_PIN))
      {
         ID_GATEWAY[NUM]++;
         ID_GATEWAY[NUM] = ID_GATEWAY[NUM] % 10;
         ITOA (ID_GATEWAY[NUM], 10, TEMP_CHAR);
         LCD_GOTOXY (7 + NUM, 2);
         DELAY_MS (10);
         PRINTF (LCD_PUTC, TEMP_CHAR);
         DELAY_MS (300);
      }
   }
}

VOID BUTT_OKE()
{
   TT_CONFIG_DONE = 0;
   TT_FUN = 0;//BREAK WHILE BUTT_FUN
   TT_STT = 0;// BREAK WHILE CHONID/NHAPID_GW
}

VOID SELLECT_FUN()
{
   TT_CONFIG_DONE = 0;

   SWITCH (CONFIG_FUN)
   {
      CASE 0:
      CHON_ID ();
      BREAK;

      CASE 1:    
      NHAPID_GW ();
      BREAK;
   }
}

VOID BUTT_FUN()
{
   TT_FUN = 1;
   LCD_GOTOXY (1, 1) ;
   DELAY_MS (10);
   PRINTF (LCD_PUTC, "CONFIG:        ");

   // HIEN THI LCD
   LCD_GOTOXY (1, 2) ;
   DELAY_MS (10);
   PRINTF (LCD_PUTC, "CASE:          ") ;

   WHILE (TT_FUN)
   {
      IF (INPUT (BT2_PIN) == 0) //NEU NUT BAM DUOC BAM
      {
         CONFIG_FUN ++;
         CONFIG_FUN = CONFIG_FUN % 2;
         DELAY_MS (300);
         //HIEN THI
         LCD_GOTOXY (6, 2) ;
         ITOA (CONFIG_FUN, 10, TEMP_CHAR);
         DELAY_MS (10);
         PRINTF (LCD_PUTC, TEMP_CHAR);

         SWITCH (CONFIG_FUN)
         {
            CASE 0:
            PRINTF (LCD_PUTC, " - ID-NODE      ");
            BREAK;

            CASE 1:
            PRINTF (LCD_PUTC, " - ID-GW       ");
            BREAK;            
         }
      }
   }

   //////
   IF (!TT_CONFIG_DONE)
   {
      SELLECT_FUN ();
   }
}
VOID XULY_IDNODE_NHAP(){
   //*TEMP_CHAR3 = "\0";
   *ID_NODE_CHAR = "\0";
   FOR (int j = 0; j < 4; j++)
   {
      ITOA (ID_NODE[j], 10, TEMP_CHAR);
      DELAY_MS (1);
      STRCAT (ID_NODE_CHAR, TEMP_CHAR);
   }  
   //ID_NODE_CHAR = TEMP_CHAR3;   
   //STRCPY(ID_NODE_CHAR,TEMP_CHAR3);
   //strcpy
}
VOID XULY_IDGW_NHAP(){

   *ID_GATEWAY_CHAR = "\0";
   FOR (int j = 0; j < 6; j++)
   {
      ITOA (ID_GATEWAY[j], 10, TEMP_CHAR);
      DELAY_MS (1);
      STRCAT (ID_GATEWAY_CHAR, TEMP_CHAR);
   }  
}


VOID CONFIG_DONE()
{
   TT_FUN = 0;
   TT_STT = 0;
   CHAR *PACKAGE_CONFIG[]={"*", "LENGHT","C_F", "ID_GW1234" ,"ID_NODE","#"};
   XULY_IDGW_NHAP();
   PACKAGE_CONFIG[3] = ID_GATEWAY_CHAR;
   
   XULY_IDNODE_NHAP();
   PACKAGE_CONFIG[4] = ID_NODE_CHAR;         
   LEN_PACKAGES = 0;
   PACKAGE_CONFIG[1] = "12"; //DO DAI CUA LENGHT CO DO DAI = 2
   FOR (int J = 0; J < 6; J++)
   {
      LEN_PACKAGES += strlen(PACKAGE_CONFIG[J]);
   }   
   LEN_PACKAGES = LEN_PACKAGES+5; //5 @
   ITOA (LEN_PACKAGES, 10, TEMP_CHAR);
   PACKAGE_CONFIG[1] = TEMP_CHAR;
   
   FOR ( J = 0; J < 6; J++)
   {
      PRINTF (PACKAGE_CONFIG[J]);
      PRINTF ("@");
   }


   LCD_GOTOXY (1, 1) ;
   DELAY_MS (10);
   PRINTF (LCD_PUTC, "WAITING ....        ") ;
   LCD_GOTOXY (1, 1) ;
   DELAY_MS (10);
   PRINTF (LCD_PUTC, "WAITING ....        ") ;   
   TT_CONFIG_DONE = 0;
}

//--------------------------------------------------------------------//
