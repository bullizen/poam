**Vad har vi gjort sedan sist?**

**Hälsoindikatorn:** Vi har arbetat intensivt med att förbättra hälsoindikatorn för systemets prestandaövervakning. 
Nu fungerar koden korrekt så att när CPU-användningen överstiger en viss procentnivå, ändrar indikatorn färg till rött, vilket tydligt signalerar ett potentiellt problem. 
Om alla mätvärden håller sig inom normala gränser, lyser indikatorn grönt för att visa att systemet fungerar som det ska. Detta är en viktig funktion för att säkerställa att vi snabbt kan upptäcka och åtgärda problem innan de påverkar användarna.

**Installation och konfiguration av testmiljö:** 
Vi har också genomfört installationen och konfigurationen av vår testmiljö. 
Detta har varit ett viktigt steg för att säkerställa att vi kan testa våra funktioner i en kontrollerad miljö innan vi rullar ut dem i produktion. 
I samband med detta har vi även påbörjat implementeringen av ett varningssystem för kritiska problem. Detta system kommer att vara avgörande för att proaktivt identifiera och hantera allvarliga incidenter innan de eskalerar.

**Portövervakning:** 
Ett annat fokusområde har varit att utveckla och implementera portövervakning. 
Vi har nu ett fungerande skript som kan identifiera vilka portar som är öppna på systemet och övervaka trafiken som passerar genom dem. 
Detta inkluderar att logga IP-adresserna för inkommande trafik och att identifiera om det finns ovanligt hög trafikmängd, vilket då triggar en varning och genererar en loggfil. 
Denna varning skickas sedan automatiskt till en administratör för omedelbar uppföljning. 
Detta arbete är en central del av vårt säkerhetsarbete och hjälper till att skydda systemet mot potentiella hot.

**Vad ska vi göra till nästa gång?**

**Slutföra portövervakning och loggsystem:** 
Nästa steg är att färdigställa portövervakningen och loggsystemet. 
Vi planerar att integrera detta i ett övervakningsgränssnitt, vilket kommer att ge en översikt över systemets status i realtid och göra det enklare att snabbt identifiera och åtgärda eventuella problem. 
Denna integration är avgörande för att säkerställa att vårt övervakningssystem är både användarvänligt och effektivt.

**Hinder och utmaningar?**

**Utmaningar:** 
Projektet har verkligen ställt oss inför flera utmaningar, från att optimera hälsoindikatorn till att implementera ett pålitligt varningssystem. 
Varje steg har krävt noggrann planering och testning, och det har varit en del hinder på vägen, men genom att arbeta metodiskt och fokuserat har vi kunnat lösa de problem som uppstått. 
Detta har varit lärorikt och vi har stärkt våra kunskaper och färdigheter under processen.

![](26aug.png)
