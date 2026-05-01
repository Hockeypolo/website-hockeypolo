const SHEETS_URL = 'https://script.google.com/a/macros/hockeypolo.com/s/AKfycbx79RBnwaO4PGpxMCnwXYGl_Fhgw4YCrMDvqwgub3OD8mkovVZ3AzcpzFR_AaHfZIsP/exec';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  // ── SHEETS PROXY (GET) ──
  if (req.method === 'GET') {
    try {
      const params = new URLSearchParams(req.query);
      const url = params.toString() ? `${SHEETS_URL}?${params}` : SHEETS_URL;
      const response = await fetch(url, { redirect: 'follow' });
      const data = await response.json();
      res.status(200).json(data);
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
    return;
  }

  // ── AI GENERATION (POST) ──
  if (req.method === 'POST') {
    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) return res.status(500).json({ error: 'API key not configured' });
    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify(req.body)
      });
      const data = await response.json();
      res.status(200).json(data);
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
}
