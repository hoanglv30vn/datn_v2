
#DEFINE      DS               PIN_D1
#DEFINE      SH_CP            PIN_D0  
#DEFINE      STCP             PIN_D2
VOID XUATTRANGTHAI(UNSIGNED INT8 BYTEXUAT)
{
   UNSIGNED INT8   SB;   
   #BIT BSERI  = BYTEXUAT.7
   
   FOR (SB=0;SB<8;SB++)
      {                                                 
         OUTPUT_BIT(DS,BSERI);    
         OUTPUT_LOW(SH_CP); OUTPUT_HIGH(SH_CP);
         BYTEXUAT=BYTEXUAT<<1; //10010010->00100100  
     }
      OUTPUT_LOW(STCP); OUTPUT_HIGH(STCP);
}

