// ─────────────────────────────────────────────────────────────────────────
//  api/blob-upload.js
//  Token-handshake voor client-side uploads naar Vercel Blob.
//  De browser (@vercel/blob/client → upload()) vraagt hier een tijdelijk
//  upload-token aan en uploadt het bestand vervolgens DIRECT naar Blob.
//  Zo omzeilen we de 4,5 MB request-limiet van Vercel Functions.
//
//  Vereist env-var: BLOB_READ_WRITE_TOKEN  (automatisch toegevoegd zodra de
//  Blob-store aan het project is gekoppeld).
// ─────────────────────────────────────────────────────────────────────────

import { handleUpload } from '@vercel/blob/client';

const MAX_BYTES = 10 * 1024 * 1024; // 10 MB per bestand (harde server-cap)

const ALLOWED_TYPES = [
  'image/png',
  'image/jpeg',
  'image/jpg',
  'image/svg+xml',
  'image/webp',
  'application/pdf',
  'application/postscript',          // .ai / .eps
  'application/illustrator',         // .ai (alternatief)
  'application/msword',              // .doc
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // .docx
  'application/octet-stream'         // fallback voor o.a. .ai zonder mime-type
];

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  if (!process.env.BLOB_READ_WRITE_TOKEN) {
    console.error('blob-upload: BLOB_READ_WRITE_TOKEN ontbreekt in environment');
    return res.status(500).json({ error: 'Upload niet geconfigureerd' });
  }

  try {
    const jsonResponse = await handleUpload({
      request: req,
      body: req.body,
      onBeforeGenerateToken: async (pathname, clientPayload) => ({
        allowedContentTypes: ALLOWED_TYPES,
        maximumSizeInBytes: MAX_BYTES,
        addRandomSuffix: true,
        tokenPayload: clientPayload || null
      }),
      // Webhook na voltooide upload — wij hebben hier niets te doen,
      // de browser ontvangt de URL rechtstreeks van upload().
      onUploadCompleted: async () => {}
    });
    return res.status(200).json(jsonResponse);
  } catch (err) {
    console.error('blob-upload error:', err);
    return res.status(400).json({ error: err?.message || 'Upload mislukt' });
  }
}
