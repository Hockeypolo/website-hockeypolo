const SHEETS_URL = 'https://script.google.com/a/macros/hockeypolo.com/s/AKfycbx79RBnwaO4PGpxMCnwXYGl_Fhgw4YCrMDvqwgub3OD8mkovVZ3AzcpzFR_AaHfZIsP/exec';
const ANTHROPIC_HEADERS = (key) => ({
  'Content-Type': 'application/json',
  'x-api-key': key,
  'anthropic-version': '2023-06-01'
});

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

  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'API key not configured' });

  // ── PROSPECT SEARCH (POST with type=search) ──
  if (req.body?.type === 'search') {
    const { query } = req.body;
    const system = `Je bent een lead researcher voor Hockeypolo, een Rotterdams merchandisebedrijf (kleding, hoodies, banners, mokken, gepersonaliseerde merchandise voor teams en clubs). Zoek op het web naar potentiële klanten. Geef ALLEEN een JSON array terug, geen markdown of uitleg. Elk object bevat: naam, website, contactpersoon, email, telefoon, regio. Gebruik lege string "" als iets niet gevonden is.`;
    const userMsg = `Zoek 6 tot 8 concrete organisaties, clubs of bedrijven voor: "${query}". Gebruik web search om actuele contactinfo te vinden. Geef ALLEEN de JSON array terug.`;

    try {
      let messages = [{ role: 'user', content: userMsg }];
      let finalText = '';
      let iterations = 0;

      while (iterations < 6) {
        const resp = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: ANTHROPIC_HEADERS(apiKey),
          body: JSON.stringify({
            model: 'claude-sonnet-4-6',
            max_tokens: 4000,
            system,
            tools: [{ type: 'web_search_20250305', name: 'web_search' }],
            messages
          })
        });
        const data = await resp.json();

        if (data.stop_reason === 'end_turn') {
          finalText = data.content.filter(b => b.type === 'text').map(b => b.text).join('');
          break;
        }

        if (data.stop_reason === 'tool_use') {
          messages.push({ role: 'assistant', content: data.content });
          const toolResults = data.content
            .filter(b => b.type === 'tool_use')
            .map(b => ({ type: 'tool_result', tool_use_id: b.id, content: '' }));
          messages.push({ role: 'user', content: toolResults });
        } else {
          finalText = data.content?.filter(b => b.type === 'text').map(b => b.text).join('') || '[]';
          break;
        }
        iterations++;
      }

      const clean = finalText.replace(/```json|```/g, '').trim();
      const start = clean.indexOf('[');
      const end = clean.lastIndexOf(']');
      const jsonStr = start >= 0 && end > start ? clean.slice(start, end + 1) : '[]';
      res.status(200).json({ results: JSON.parse(jsonStr) });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
    return;
  }

  // ── AI MAIL/SCRIPT GENERATION (POST) ──
  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: ANTHROPIC_HEADERS(apiKey),
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.status(200).json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
