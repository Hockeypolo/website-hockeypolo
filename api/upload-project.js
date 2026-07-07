// ─────────────────────────────────────────────────────────────────────────
//  api/upload-project.js
//  Ontvangt de ingevulde projectaanvraag van /deel-je-idee als JSON
//  (tekstvelden + reeds-geüploade Blob-URLs) en relayt een nette samenvatting
//  naar FormSubmit, zodat de aanvraag per mail bij info@hockeypolo.com binnenkomt.
//
//  De bestanden zelf zijn al client-side naar Vercel Blob geüpload
//  (zie api/blob-upload.js); hier komen alleen de URLs binnen.
// ─────────────────────────────────────────────────────────────────────────

const FORMSUBMIT_ENDPOINT =
  process.env.FORMSUBMIT_ENDPOINT || 'https://formsubmit.co/ajax/info@hockeypolo.com';

export const config = { maxDuration: 60 };

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ success: false, error: 'Method not allowed' });

  try {
    const data = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});

    // ── Velden voor de FormSubmit-tabel opbouwen (plat, leesbaar) ──
    const fields = {
      _subject: `Nieuwe projectaanvraag — ${data.organisatie || data.naam || 'onbekend'}`,
      _template: 'table',
      _captcha: 'false'
    };

    const add = (label, value) => {
      if (value === undefined || value === null) return;
      const v = Array.isArray(value) ? value.filter(Boolean).join(', ') : String(value).trim();
      if (v) fields[label] = v;
    };

    // Stap 2 — Wie ben je
    add('Naam', data.naam);
    add('Organisatie', data.organisatie);
    add('Type organisatie', data.typeOrganisatie);
    add('Rol', data.rol);

    // Stap 3 — Wat wil je laten maken
    add('Gewenste producten', data.producten);
    add('Aantallen per product', data.aantallen);
    add('Anders, namelijk', data.productAnders);
    add('Omschrijving wensen', data.productOmschrijving);

    // Stap 4 — Logo's & bedrukking
    if (Array.isArray(data.logos)) {
      data.logos.forEach((logo, i) => {
        const parts = [];
        if (logo.naam) parts.push(`naam: ${logo.naam}`);
        if (logo.techniek) parts.push(`techniek: ${logo.techniek}`);
        if (logo.plaatsing) parts.push(`plaatsing: ${logo.plaatsing}`);
        if (logo.url) parts.push(`bestand: ${logo.url}`);
        if (parts.length) fields[`Logo ${i + 1}`] = parts.join(' · ');
      });
    }

    // Stap 5 — Kleuren & maten
    add('Kleuren', data.kleuren);
    add('Maatverdeling', data.maten);

    // Stap 6 — Inspiratie
    if (Array.isArray(data.inspiratie) && data.inspiratie.length) {
      data.inspiratie.forEach((url, i) => { if (url) fields[`Inspiratiefoto ${i + 1}`] = url; });
    }
    add('Inspiratie-URLs', data.inspiratieUrls);
    add('Briefing-document', data.briefingUrl);

    // Stap 7 — Budget
    add('Budget', data.budget);
    add('Budget-toelichting', data.budgetToelichting);

    // Stap 8 — Deadline
    add('Deadline', data.deadline);
    add('Type deadline', data.deadlineType);
    add('Deadline-toelichting', data.deadlineToelichting);

    // Stap 9 — Contact
    add('E-mail', data.email);
    add('Telefoon', data.telefoon);
    add('Voorkeur contact', data.voorkeurContact);

    // ── Versturen naar FormSubmit (AJAX → JSON-respons, geen redirect) ──
    // FormSubmit wijst server-naar-server requests af zonder Origin/Referer
    // (die headers zet een browser altijd automatisch, een serverless function niet).
    // Let op: FormSubmit's activatie is gekoppeld aan het EXACTE domein — het
    // canonieke domein van deze site is www.hockeypolo.com (hockeypolo.com
    // redirect ernaartoe), dus dat is de Origin/Referer die hier moet staan.
    const fsResp = await fetch(FORMSUBMIT_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'https://www.hockeypolo.com',
        'Referer': 'https://www.hockeypolo.com/deel-je-idee'
      },
      body: JSON.stringify(fields)
    });

    if (!fsResp.ok) {
      const text = await fsResp.text().catch(() => '');
      console.error('FormSubmit fout:', fsResp.status, text);
      return res.status(502).json({ success: false, error: 'Versturen naar mail mislukte' });
    }

    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('upload-project error:', err);
    return res.status(500).json({ success: false, error: err?.message || 'Onbekende fout' });
  }
}
