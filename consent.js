/* ═══════════════════════════════════════════════════════════════
   Hockeypolo — cookiemelding + advertentiemeting
   ───────────────────────────────────────────────────────────────
   Wordt op elke publieke pagina synchroon in <head> geladen, vóór
   andere scripts, zodat de consent-standaard staat voordat gtag iets
   doet.

   1. Google-tag (AW-17893122065) met Consent Mode v2: standaard alles
      geweigerd, pas "granted" na Accepteren in de cookiemelding.
   2. Meta Pixel wordt pas geladen na Accepteren.
   3. Klik-ID's uit advertenties (gclid / gbraid / wbraid) blijven in de
      URL staan tijdens SPA-navigatie en bij links naar andere pagina's,
      zodat ze op de bedanktpagina nog aanwezig zijn. Na toestemming
      worden ze ook in sessionStorage bewaard (overleeft herladen).
   4. Conversie "Offerteaanvraag verzonden" gaat alleen af op een
      bedanktpagina als er vlak daarvoor écht een formulier is verzonden
      (eenmalige vlag via hpMarkeerAanvraag), dus niet bij herladen of
      direct openen.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var AW_ID          = 'AW-17893122065';
  var CONVERSIE      = 'AW-17893122065/SqcOCO6Rn58dEJHAjdRC';
  var META_PIXEL_ID  = '2193791588043355';

  var KEUZE_KEY      = 'hp_cookie_keuze';   // localStorage: { v, keuze: 'granted'|'denied', ts }
  var KEUZE_VERSIE   = 1;                   // ophogen als de cookietekst wezenlijk verandert
  var KLIK_KEY       = 'hp_klik_ids';       // sessionStorage, alleen na toestemming
  var AANVRAAG_KEY   = 'hp_aanvraag';       // sessionStorage, eenmalige conversievlag
  var AANVRAAG_MAX_MS = 30 * 60 * 1000;     // vlag ouder dan 30 min telt niet meer

  var KLIK_PARAMS    = ['gclid', 'gbraid', 'wbraid'];
  var BEDANKT_PADEN  = ['/bedankt', '/bedankt-deel-je-idee', '/bedankt-deel-je-idee.html'];

  // ── Opslag-helpers (kunnen falen in privévensters) ──────────────
  function lees(store, key) {
    try { var v = window[store].getItem(key); return v ? JSON.parse(v) : null; } catch (e) { return null; }
  }
  function schrijf(store, key, val) {
    try { window[store].setItem(key, JSON.stringify(val)); } catch (e) {}
  }
  function wis(store, key) {
    try { window[store].removeItem(key); } catch (e) {}
  }

  function huidigeKeuze() {
    var k = lees('localStorage', KEUZE_KEY);
    return (k && k.v === KEUZE_VERSIE) ? k.keuze : null;
  }

  // ── 1. Google-tag met Consent Mode v2 ───────────────────────────
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  gtag('consent', 'default', {
    ad_storage:         'denied',
    ad_user_data:       'denied',
    ad_personalization: 'denied',
    analytics_storage:  'denied',
    wait_for_update:    500
  });

  if (huidigeKeuze() === 'granted') {
    gtag('consent', 'update', toestemming('granted'));
  }

  gtag('js', new Date());
  gtag('config', AW_ID);

  var gs = document.createElement('script');
  gs.async = true;
  gs.src = 'https://www.googletagmanager.com/gtag/js?id=' + AW_ID;
  document.head.appendChild(gs);

  function toestemming(waarde) {
    return {
      ad_storage:         waarde,
      ad_user_data:       waarde,
      ad_personalization: waarde,
      analytics_storage:  waarde
    };
  }

  // ── 2. Meta Pixel (alleen na toestemming) ───────────────────────
  var metaGeladen = false;
  function laadMetaPixel() {
    if (metaGeladen) { if (window.fbq) window.fbq('consent', 'grant'); return; }
    metaGeladen = true;
    /* eslint-disable */
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window,document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    /* eslint-enable */
    window.fbq('init', META_PIXEL_ID);
    window.fbq('track', 'PageView');
  }

  if (huidigeKeuze() === 'granted') laadMetaPixel();

  // ── 3. Klik-ID's (gclid) vasthouden tot de bedanktpagina ────────
  function klikIdsUit(search) {
    var p = new URLSearchParams(search || '');
    var ids = {};
    KLIK_PARAMS.forEach(function (k) { if (p.get(k)) ids[k] = p.get(k); });
    return Object.keys(ids).length ? ids : null;
  }

  var klikIds = klikIdsUit(location.search) ||
                (huidigeKeuze() === 'granted' ? lees('sessionStorage', KLIK_KEY) : null);

  if (klikIds && huidigeKeuze() === 'granted') schrijf('sessionStorage', KLIK_KEY, klikIds);

  // Voegt de klik-ID's toe aan een interne URL (als ze er nog niet in staan).
  function metKlikIds(url) {
    if (!klikIds || url == null) return url;
    try {
      var u = new URL(String(url), location.href);
      if (u.origin !== location.origin) return url;
      var gewijzigd = false;
      Object.keys(klikIds).forEach(function (k) {
        if (!u.searchParams.has(k)) { u.searchParams.set(k, klikIds[k]); gewijzigd = true; }
      });
      return gewijzigd ? u.pathname + u.search + u.hash : url;
    } catch (e) { return url; }
  }
  window.hpUrl = metKlikIds;

  // De SPA (index.html) schrijft de URL via pushState/replaceState opnieuw
  // en zou de query-string daarbij weggooien. Houd de klik-ID's erin.
  ['pushState', 'replaceState'].forEach(function (fn) {
    var orig = history[fn];
    history[fn] = function (state, title, url) {
      return orig.call(history, state, title, url == null ? url : metKlikIds(url));
    };
  });

  // Gewone links naar andere pagina's op hockeypolo.com: klik-ID's meegeven.
  document.addEventListener('click', function (e) {
    if (!klikIds) return;
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#' || /^(mailto|tel|javascript):/i.test(href)) return;
    var nieuw = metKlikIds(href);
    if (nieuw !== href) a.setAttribute('href', nieuw);
  }, true);

  // ── 4. Conversie alleen na een echte verzending ─────────────────
  // Aanroepen door een formulier vlak vóór de redirect naar de bedanktpagina.
  window.hpMarkeerAanvraag = function () {
    var id = 'hp-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8);
    schrijf('sessionStorage', AANVRAAG_KEY, { id: id, ts: Date.now() });
  };

  var pad = location.pathname.replace(/\/+$/, '') || '/';
  if (BEDANKT_PADEN.indexOf(pad) !== -1) {
    var aanvraag = lees('sessionStorage', AANVRAAG_KEY);
    wis('sessionStorage', AANVRAAG_KEY);   // eenmalig: herladen telt niet opnieuw
    if (aanvraag && aanvraag.id && (Date.now() - aanvraag.ts) < AANVRAAG_MAX_MS) {
      gtag('event', 'conversion', { send_to: CONVERSIE, transaction_id: aanvraag.id });
      if (huidigeKeuze() === 'granted' && window.fbq) window.fbq('track', 'Contact');
    }
  }

  // ── Keuze verwerken ─────────────────────────────────────────────
  var MARKETING_COOKIES = ['_gcl_au', '_gcl_aw', '_gcl_gb', '_gcl_dc', '_fbp', '_fbc'];

  function verwijderMarketingCookies() {
    var host = location.hostname;
    var domeinen = ['', host, '.' + host, '.' + host.replace(/^www\./, '')];
    MARKETING_COOKIES.forEach(function (naam) {
      domeinen.forEach(function (d) {
        document.cookie = naam + '=; Max-Age=0; path=/' + (d ? '; domain=' + d : '');
      });
    });
  }

  function slaKeuzeOp(keuze) {
    schrijf('localStorage', KEUZE_KEY, { v: KEUZE_VERSIE, keuze: keuze, ts: Date.now() });
    gtag('consent', 'update', toestemming(keuze));
    if (keuze === 'granted') {
      if (klikIds) schrijf('sessionStorage', KLIK_KEY, klikIds);
      laadMetaPixel();
    } else {
      wis('sessionStorage', KLIK_KEY);
      if (window.fbq) window.fbq('consent', 'revoke');
      verwijderMarketingCookies();
    }
    verbergMelding();
    try { document.dispatchEvent(new CustomEvent('hp:cookiekeuze', { detail: keuze })); } catch (e) {}
  }

  // ── Cookiemelding (UI) ──────────────────────────────────────────
  var CSS = '' +
    '.hp-cookie{position:fixed;left:24px;bottom:24px;z-index:2147483000;max-width:420px;width:calc(100% - 48px);' +
      'background:#fff;color:#0a0a0a;border:1px solid #e5e5e5;border-radius:12px;' +
      'box-shadow:0 12px 40px rgba(0,0,0,.14);padding:22px 22px 20px;font-family:Inter,system-ui,-apple-system,sans-serif;' +
      'opacity:0;transform:translateY(12px);transition:opacity .3s ease,transform .3s ease}' +
    '.hp-cookie.zichtbaar{opacity:1;transform:none}' +
    '.hp-cookie h2{font-family:"Space Grotesk",Inter,sans-serif;font-size:18px;font-weight:700;letter-spacing:-.02em;margin:0 0 8px;line-height:1.2}' +
    '.hp-cookie p{font-size:14px;line-height:1.55;color:#555;margin:0 0 16px}' +
    '.hp-cookie p a{color:#00A652;text-decoration:underline;text-underline-offset:2px}' +
    '.hp-cookie-knoppen{display:grid;grid-template-columns:1fr 1fr;gap:10px}' +
    '.hp-cookie button{font-family:Inter,system-ui,sans-serif;font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;' +
      'padding:13px 16px;border-radius:8px;cursor:pointer;transition:background .2s ease,border-color .2s ease,color .2s ease}' +
    '.hp-cookie .hp-weiger{background:#fff;color:#0a0a0a;border:1.5px solid #0a0a0a}' +
    '.hp-cookie .hp-weiger:hover{background:#0a0a0a;color:#fff}' +
    '.hp-cookie .hp-accepteer{background:#00A652;color:#fff;border:1.5px solid #00A652}' +
    '.hp-cookie .hp-accepteer:hover{background:#008c45;border-color:#008c45}' +
    '.hp-cookie button:focus-visible{outline:2px solid #00A652;outline-offset:2px}' +
    '.hp-cookie-link{background:none;border:0;padding:0;font:inherit;color:inherit;cursor:pointer;text-decoration:underline;text-underline-offset:2px}' +
    '.hp-cookie-link:hover{color:#fff}' +
    '@media (max-width:640px){.hp-cookie{left:16px;right:16px;bottom:16px;width:auto;max-width:none;padding:18px}}';

  var melding = null;
  var cssGeplaatst = false;

  function plaatsCss() {
    if (cssGeplaatst) return;
    cssGeplaatst = true;
    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);
  }

  function bouwMelding() {
    if (melding) return melding;
    plaatsCss();

    melding = document.createElement('div');
    melding.className = 'hp-cookie';
    melding.setAttribute('role', 'dialog');
    melding.setAttribute('aria-live', 'polite');
    melding.setAttribute('aria-labelledby', 'hp-cookie-titel');
    melding.innerHTML =
      '<h2 id="hp-cookie-titel">Cookies</h2>' +
      '<p>We willen graag meten welke advertenties van Google en Meta leiden tot een offerteaanvraag, ' +
      'zodat we onze advertenties kunnen verbeteren. Daarvoor plaatsen we marketingcookies, alleen als jij dat goed vindt. ' +
      'Lees meer in onze <a href="/privacyverklaring">privacyverklaring</a>.</p>' +
      '<div class="hp-cookie-knoppen">' +
        '<button type="button" class="hp-weiger">Weigeren</button>' +
        '<button type="button" class="hp-accepteer">Accepteren</button>' +
      '</div>';
    melding.querySelector('.hp-weiger').addEventListener('click', function () { slaKeuzeOp('denied'); });
    melding.querySelector('.hp-accepteer').addEventListener('click', function () { slaKeuzeOp('granted'); });
    document.body.appendChild(melding);
    return melding;
  }

  function toonMelding() {
    var m = bouwMelding();
    m.style.display = '';
    void m.offsetWidth;   // reflow, zodat de fade-in ook start in een achtergrondtab
    m.classList.add('zichtbaar');
  }

  function verbergMelding() {
    if (!melding) return;
    melding.classList.remove('zichtbaar');
    setTimeout(function () { if (melding) melding.style.display = 'none'; }, 300);
  }

  // Openbare functie om de keuze te wijzigen (footer + privacyverklaring).
  window.hpCookieInstellingen = toonMelding;
  // Huidige keuze ('granted' | 'denied' | null) voor andere scripts (nieuwsbrief-popup).
  window.hpCookieKeuze = huidigeKeuze;

  // "Cookie-instellingen" in elke footer, zodat de keuze altijd te wijzigen is.
  function voegFooterLinksToe() {
    var spans = document.querySelectorAll('.footer-bottom > span:first-child');
    Array.prototype.forEach.call(spans, function (span) {
      if (span.querySelector('.hp-cookie-link')) return;
      var knop = document.createElement('button');
      knop.type = 'button';
      knop.className = 'hp-cookie-link';
      knop.textContent = 'Cookie-instellingen';
      knop.addEventListener('click', toonMelding);
      span.appendChild(document.createTextNode(' · '));
      span.appendChild(knop);
    });
  }

  function opDomKlaar() {
    plaatsCss();
    voegFooterLinksToe();
    if (!huidigeKeuze()) toonMelding();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', opDomKlaar);
  } else {
    opDomKlaar();
  }
})();
