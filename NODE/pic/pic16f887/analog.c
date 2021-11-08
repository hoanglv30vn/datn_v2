
  INT ADC_READ (INT KENH)
 {
    UNSIGNED INT8 ANALOG_PORT[] = {1,2,4,8,16,32,64}; 
    SETUP_ADC_PORTS (ANALOG_PORT[KENH]);
    DELAY_MS(3);
    SET_ADC_CHANNEL (KENH);
    DELAY_MS(3);
    KQADC = 0;
    FOR (INT I = 0; I < 100; I++)
    {
       KQADC = KQADC + READ_ADC () ;
       DELAY_MS (1);
    }

    KQADC = KQADC / (100 * 2.046);
    RETURN KQADC;
 }


 VOID READ_ANALOG ( )
 {
   FOR(INT K = 0; K<SOLUONGCAMBIEN_CONFIG; K++){
      KET_QUA_ANALOG[K] = ADC_READ (K);  
   }
 }

 VOID SEND_ANALOG_UART()
 {
   OUTPUT_TOGGLE(PIN_C4);
   //CHAR *PACKAGE_SS[]={"*", "26","SS", "IDGW12" ,"NODE","ZZ","AA","VV","CC","SS"};
   CHAR *PACKAGE_SS[]={"IDGW12" ,"NODE","ZZ","AA","VV","CC","SS"};   
   PACKAGE_SS[0] = ID_GATEWAY_CHAR;
   PACKAGE_SS[1] = ID_NODE_CHAR;
   UNSIGNED INT8 DO_DAI =20;
   
   FOR(INT I = 0; I<SOLUONGCAMBIEN_CONFIG; I++)
   {
      ITOA(KET_QUA_ANALOG[I],10,PACKAGE_SS[2+I]);
      DO_DAI = DO_DAI + 3;
   }      
   ITOA(DO_DAI,10,TEMP_CHAR2);
   PRINTF ("*@");   
   PRINTF (TEMP_CHAR2);
   PRINTF ("@SS@");   
   FOR ( I = 0; I < 2 + SOLUONGCAMBIEN_CONFIG; I++)
   {
      PRINTF (PACKAGE_SS[I]);
      PRINTF ("@");
   }
   PRINTF ("#");
   OUTPUT_TOGGLE(PIN_C4);
   
 }
 
 
 
 
 /*
 INT ADC_READ (INT KENH)
 {
    UNSIGNED INT8 ANALOG_PORT[] = {1, 2, 4, 8, 16, 32, 64};
    SETUP_ADC_PORTS (ANALOG_PORT[KENH]);
    DELAY_MS (3) ;
    SET_ADC_CHANNEL (KENH);
    DELAY_MS (3) ;
    KQADC = 0;
    FOR (INT I = 0; I < 100; I++)
    {
       KQADC = KQADC + READ_ADC () ;
       DELAY_MS (1);
    }

    KQADC = KQADC / (100 * 2.046);
    RETURN KQADC;
 }

 VOID READ_ANALOG ()
 {
    FOR (INT K = 0; K < SOLUONGCAMBIEN_CONFIG; K++)
    {
       KET_QUA_ANALOG[K] = ADC_READ (K);
    }
 }

 VOID SEND_ANALOG_UART ()
 {
    OUTPUT_TOGGLE (PIN_C4) ;
    //CHAR * PACKAGE_SS[] ={" * ", "26", "SS", "IDGW12", "NODE", "ZZ", "AA", "VV", "CC", "SS"};
    CHAR * PACKAGE_SS[] ={"IDGW12", "NODE", "ZZ", "AA", "VV", "CC", "SS"};
    PACKAGE_SS[0] = ID_GATEWAY_CHAR;
    PACKAGE_SS[1] = ID_NODE_CHAR;
    UNSIGNED INT8 DO_DAI = 20;
    
    FOR (INT I = 0; I < SOLUONGCAMBIEN_CONFIG; I++)
    {
       ITOA (KET_QUA_ANALOG[I], 10, PACKAGE_SS[2 + I]) ;
       DO_DAI = DO_DAI + 3;
    }

    ITOA (DO_DAI, 10, TEMP_CHAR2) ;
    PRINTF (" * @");
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

*/


