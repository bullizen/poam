# Product Backlog

## Installation av miljön
Miljön installeras på en virtuell maskin med Linux som operativsystem.

## Integrerad SSH- och Container-Övervakning

SSH-baserad övervakning: Automatiserad anslutning via SSH för insamling av systemresurser som CPU, minne, nätverk och diskprestanda, tillsammans med logginsamling för att upptäcka säkerhetshot.
Container-övervakning: Djup integration med containerplattformar som Docker och Kubernetes, med fokus på både resursanvändning och säkerhetsövervakning, vilket inkluderar intrångsdetektion och konfigurationskontroller.

## Avancerad Säkerhetssårbarhetsanalys

Övervakning av öppna portar: Skanning och analys av öppna nätverksportar för att identifiera potentiella säkerhetshot.
Kontroll av filbehörigheter: Identifiering av filer och kataloger med osäkra behörigheter, såsom överdrivet generösa åtkomstinställningar.
Sårbarhetsanalys av programvarukomponenter: Automatiserad granskning av installerade programvaruversioner mot kända säkerhetsdatabaser för att identifiera potentiella risker.
Logggranskning: Insamling och analys av system- och applikationsloggar för att upptäcka misstänkta aktiviteter, inklusive felaktiga inloggningsförsök och oväntade systemändringar.

## Automatiserade Varningar och Incidenthantering

Realtidsvarningar: Implementering av varningar för kritiska säkerhets- och prestandaproblem via kanaler som e-post och samarbetsverktyg som Slack.
Tröskelbaserade varningar: Användning av konfigurerbara tröskelvärden för att utlösa varningar vid överanvändning av resurser eller upptäckt av säkerhetshot.
Incidentrapporter: Automatiserade sammanställningar av identifierade hot, inklusive rekommenderade åtgärder.

## Tydlig och Överskådlig Data Presentation

Interaktiva dashboards: En mix av grafer, listor och tabeller för att visualisera både prestanda- och säkerhetsdata på ett överskådligt sätt. Användaren kan enkelt filtrera och sortera data efter behov.
Detaljerad logggranskning: Möjligheten att gå djupt ner i loggar och händelser med kraftfulla sök- och filtreringsverktyg.
Sårbarhetsöversikter: Visar en sammanställning av alla identifierade säkerhetshot, kategoriserade efter allvarlighetsgrad och åtgärdsprioritet.

## Sömlös Integration med Externa System

CI/CD Integration: Integrering med befintliga CI/CD-verktyg för att säkerställa att säkerhets- och prestandatester körs automatiskt vid varje kodändring.
SIEM-koppling: Möjligheten att ansluta verktyget till Security Information and Event Management (SIEM)-system för att förbättra den övergripande säkerhetsövervakningen.
API: Tillhandahåller API-åtkomst för att möjliggöra integration med andra övervaknings- och managementverktyg.

## Användar- och Rollhantering

Rollbaserad åtkomstkontroll (RBAC): Finmaskig kontroll av användarbehörigheter för att säkerställa att endast auktoriserade personer har tillgång till känslig information.
Användarloggning: Registrering av användaraktiviteter inom verktyget för revisionsändamål.

## Automatiserade Åtgärder för Incidenthantering

Self-healing Scripts: Möjlighet att konfigurera automatiserade skript som triggas vid upptäckt av vanliga problem, t.ex. korrigering av osäkra behörigheter eller stängning av öppna portar.
Playbooks för incidenthantering: Fördefinierade handlingsplaner för att snabbt och effektivt hantera vanliga säkerhetsincidenter.

## Gränssnitt för användare

Göra ett gränssnitt för öka användar vänligheten.
