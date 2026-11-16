# Website-aanvragen automatisch in de spreadsheet

Elke aanvraag via de website (contactformulier, ontwerptool, Start project en de
pagina's /bedrijven, /studenten en /evenementen) gaat naar info@hockeypolo.com via
FormSubmit, zoals altijd. Daarnaast stuurt de website een kopie (alleen tekst, geen
bestanden) naar de sheet **Hockeypolo – Website-aanvragen** in de gedeelde drive
(`02 Klanten & Projecten`).

Werkt de sheet een keer niet, dan komt de mail gewoon binnen.

## Stappen (± 5 minuten)

1. Open de sheet **Hockeypolo – Website-aanvragen**.
2. Menu **Extensies → Apps Script**.
3. Verwijder wat er staat en plak de code hieronder. Klik op **Opslaan** (schijfje).
4. Klik rechtsboven op **Implementeren → Nieuwe implementatie**.
   - Type (tandwiel): **Web-app**
   - Beschrijving: `Website-aanvragen`
   - Uitvoeren als: **Ik** (je eigen Hockeypolo-account)
   - Wie heeft toegang: **Iedereen**
5. Klik **Implementeren** en geef toestemming. Google waarschuwt dat de app niet
   geverifieerd is: kies **Geavanceerd → Ga naar … (onveilig)**. Dat is normaal voor
   een eigen script.
6. Kopieer de **web-app-URL**, die eindigt op `/exec`, en geef die aan Claude. Claude
   zet hem in `consent.js` (`SHEET_URL`), test op de testomgeving en zet het daarna live.

"Iedereen" betekent alleen dat de website een rij mag toevoegen. Lezen kan niemand
via deze URL, want het script heeft geen `doGet`.

## Code

```javascript
// Hockeypolo – website-aanvragen naar de sheet (kolommen A t/m R).
// Ontvangt een POST van de website (zie consent.js → hpStuurNaarSheet).
var TABBLAD = 'Aanvragen';

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(10000);
  try {
    var p = (e && e.parameter) || {};
    var v = function (k) { return (p[k] || '').toString().trim(); };
    var eerste = function () {
      for (var i = 0; i < arguments.length; i++) { if (v(arguments[i])) return v(arguments[i]); }
      return '';
    };

    var naam = eerste('Naam') || [v('Voornaam'), v('Achternaam')].filter(String).join(' ');
    var bericht = eerste('Bericht', 'Omschrijving wensen');
    if (bericht.length > 300) bericht = bericht.slice(0, 297) + '…';
    var telefoon = v('Telefoon');

    var rij = [
      new Date(),                                                       // A Ontvangen
      v('formulier') || 'Onbekend',                                     // B Formulier
      v('segment'),                                                     // C Segment
      naam,                                                             // D Naam
      v('Organisatie'),                                                 // E Organisatie
      v('E-mail'),                                                      // F E-mail
      telefoon ? "'" + telefoon : '',                                   // G Telefoon (als tekst)
      eerste('Producten', 'Product', 'Gewenste producten'),             // H Product(en)
      eerste('Aantal', 'Aantallen per product'),                        // I Aantal
      eerste('Gewenste leverdatum', 'Deadline'),                        // J Gewenste leverdatum
      bericht,                                                          // K Bericht
      v('hoe_gevonden'),                                                // L Hoe gevonden
      v('via_advertentie'),                                             // M Via advertentie
      'Website',                                                        // N Invoer
      'nee',                                                            // O Spam
      'Nieuw', '', ''                                                   // P Status, Q Orderwaarde, R Notities
    ];

    if (!naam && !v('E-mail')) return ContentService.createTextOutput('leeg');

    var blad = SpreadsheetApp.getActive().getSheetByName(TABBLAD);
    blad.appendRow(rij);
    blad.getRange(blad.getLastRow(), 1).setNumberFormat('dd-mm-yyyy hh:mm');
    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}
```

## Testen na het koppelen

1. Verstuur op de testomgeving een aanvraag via `/bedrijven`.
2. Binnen een paar seconden staat er een nieuwe rij onderaan het tabblad
   **Aanvragen**, met in kolom N `Website`.
3. Ook de mail komt zoals altijd binnen op info@hockeypolo.com.
