#!/usr/bin/env python3
"""
Genereert de doelgroeppagina's bedrijven.html, studenten.html en evenementen.html
uit scripts/doelgroepteksten.py.

Navbar, footer, stijlen en zoekfunctie worden overgenomen van een gegenereerde
productpagina (producten-polos.html), zodat alles gelijk blijft met de rest van
de site. Draai dit dus NA genereer-productpaginas.py, voeg-uspbalk-toe.py,
voeg-zoekbalk-toe.py en voeg-doelgroepmenu-toe.py.

    python3 scripts/genereer-doelgroeppaginas.py
"""

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from doelgroepteksten import DOELGROEPEN, HOE_GEVONDEN, VERBORGEN_PRODUCTEN, WERKWIJZE  # noqa: E402

WORTEL = Path(__file__).resolve().parent.parent
BRON = WORTEL / "producten-polos.html"
DATA = WORTEL / "producten-data.js"
SITE = "https://hockeypolo.com"
FOTO = "/fotomateriaal/doelgroepen/"

e = html.escape
PIJL = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M3 8h10M8 3l5 5-5 5"/></svg>'
VINK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M3 8.5l3.2 3L13 4.5"/></svg>'


def producten():
    js = DATA.read_text(encoding="utf-8")
    lijst = json.loads(re.search(r"window\.HP_PRODUCTEN = (\[.*?\]);\n", js, re.S).group(1))
    return {p["slug"]: p for p in lijst}


def productkaart(slug, alle, namen):
    if slug in alle:
        p = alle[slug]
        k = p["kleuren"][0]
        foto = f"/productfotos/{p['fotomap']}/{k['slug']}/{k['fotos'][0]}-600.webp"
        naam, minimum = p["naam"], p["minQty"]
    else:
        naam, minimum, foto = VERBORGEN_PRODUCTEN[slug]
    naam = namen.get(slug, naam)
    return (f'<a class="dg-product" href="/producten/{slug}">'
            f'<span class="dg-product-foto"><img src="{foto}" alt="{e(naam)}" loading="lazy" width="600" height="600"></span>'
            f'<span class="dg-product-naam">{e(naam)}</span>'
            f'<span class="dg-product-min">Vanaf {minimum} stuks</span></a>'), naam


def fotopad(f):
    return f if f.startswith("/") else FOTO + f


def onderdelen():
    bron = BRON.read_text(encoding="utf-8")
    stijl = re.search(r"<style>(.*?)</style>", bron, re.S).group(1)
    kop = bron[bron.index('<div class="usp-bar">'):]
    mm = kop.index('<div class="mobile-menu" id="mobile-menu">')
    kop = kop[:kop.index("</div>", mm) + len("</div>")]
    staart = bron[bron.index("<!-- ═══ FOOTER ═══ -->"):bron.rindex("</body>")]
    # Kleurwissel-script van de productpagina eruit
    staart = re.sub(r'<script src="/producten-data\.js" defer></script>\s*<script>\s*// Kleurwissel.*?</script>\s*',
                    "", staart, flags=re.S)
    return stijl, kop, staart


CSS = """
    /* ═══ DOELGROEPPAGINA ═════════════════════════════════════════ */
    .dg-wrap { max-width: 1200px; margin: 0 auto; padding: 0 80px; }
    .dg-sectie { padding: 80px 0; }
    .dg-sectie.grijs { background: var(--gray-50); }
    .dg-kop { margin-bottom: 36px; max-width: 680px; }
    .dg-kop h2 { font-family: var(--font-head); font-size: clamp(28px, 3vw, 42px); font-weight: 700; letter-spacing: -.04em; line-height: 1.08; }
    .dg-kop h2 em { font-style: normal; color: var(--green); }
    .dg-kop p { margin-top: 12px; font-size: 16px; line-height: 1.65; color: var(--gray-600); }

    .dg-hero { background: var(--black); color: var(--white); position: relative; overflow: hidden; }
    .dg-hero::after { content: ''; position: absolute; top: -140px; left: 35%; width: 460px; height: 460px; border-radius: 50%; background: radial-gradient(circle, rgba(0,166,82,.16) 0%, transparent 70%); pointer-events: none; }
    .dg-hero-grid { display: grid; grid-template-columns: 1.05fr .95fr; gap: 56px; align-items: center; padding-top: 64px; padding-bottom: 72px; position: relative; z-index: 1; }
    .dg-hero h1 { font-family: var(--font-head); font-size: clamp(38px, 4.4vw, 64px); font-weight: 700; letter-spacing: -.045em; line-height: 1.02; margin-bottom: 20px; }
    .dg-hero h1 em { font-style: normal; color: var(--green); }
    .dg-hero-intro { font-size: 17px; line-height: 1.65; color: rgba(255,255,255,.72); max-width: 540px; margin-bottom: 28px; }
    .dg-hero-btns { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 28px; }
    .dg-feiten { display: flex; flex-wrap: wrap; gap: 10px 22px; list-style: none; }
    .dg-feiten li { display: flex; align-items: center; gap: 8px; font-size: 14px; color: rgba(255,255,255,.8); }
    .dg-feiten svg { width: 16px; height: 16px; color: var(--green); flex-shrink: 0; }
    .dg-hero-foto { border-radius: 18px; overflow: hidden; aspect-ratio: 4 / 4.2; background: #111; }
    .dg-hero-foto img { width: 100%; height: 100%; object-fit: cover; }
    .dg-hero .breadcrumb { margin-bottom: 20px; }

    .dg-tegels { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .dg-tegel { display: flex; flex-direction: column; gap: 6px; padding: 22px 22px 20px; border: 1.5px solid var(--gray-200); border-radius: 14px; background: var(--white); transition: border-color .2s, transform .2s var(--ease), box-shadow .2s; }
    .dg-tegel:hover { border-color: var(--green); transform: translateY(-2px); box-shadow: 0 10px 28px rgba(0,0,0,.07); }
    .dg-tegel strong { font-family: var(--font-head); font-size: 19px; letter-spacing: -.02em; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
    .dg-tegel strong svg { width: 16px; height: 16px; color: var(--green); flex-shrink: 0; transform: rotate(90deg); }
    .dg-tegel span { font-size: 14px; line-height: 1.55; color: var(--gray-600); }

    .dg-producten { display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; }
    .dg-product { display: flex; flex-direction: column; gap: 4px; }
    .dg-product-foto { display: block; aspect-ratio: 1; border-radius: 12px; overflow: hidden; background: var(--gray-100); margin-bottom: 8px; }
    .dg-product-foto img { width: 100%; height: 100%; object-fit: cover; transition: transform .35s var(--ease); }
    .dg-product:hover .dg-product-foto img { transform: scale(1.04); }
    .dg-product-naam { font-family: var(--font-head); font-size: 15px; font-weight: 700; letter-spacing: -.01em; }
    .dg-product-min { font-size: 12.5px; color: var(--gray-600); }
    .dg-meer { margin-top: 28px; }
    .dg-meer a { font-family: var(--font-head); font-size: 14px; font-weight: 600; color: var(--green); display: inline-flex; align-items: center; gap: 8px; }
    .dg-meer svg { width: 14px; height: 14px; }

    .dg-logos { display: flex; flex-wrap: wrap; align-items: center; gap: 28px 48px; padding: 28px 0 40px; border-bottom: 1px solid var(--gray-200); margin-bottom: 40px; }
    .dg-logos img { width: auto; filter: grayscale(1); opacity: .75; }
    .dg-cases { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; }
    .dg-case { border-radius: 14px; overflow: hidden; background: var(--white); border: 1px solid var(--gray-200); }
    .dg-case img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; }
    .dg-case div { padding: 16px 18px 20px; }
    .dg-case h3 { font-family: var(--font-head); font-size: 17px; letter-spacing: -.02em; margin-bottom: 6px; }
    .dg-case p { font-size: 14px; line-height: 1.6; color: var(--gray-600); }
    .dg-cases.enkel { grid-template-columns: 1fr; }
    .dg-cases.enkel .dg-case { display: grid; grid-template-columns: 1.1fr 1fr; align-items: center; }
    .dg-cases.enkel .dg-case img { height: 100%; max-height: 380px; aspect-ratio: auto; }
    .dg-cases.enkel .dg-case div { padding: 32px; }
    .dg-cases.enkel .dg-case h3 { font-size: 24px; }
    .dg-cases.enkel .dg-case p { font-size: 15.5px; }

    .dg-sub { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: center; padding: 48px 0; border-top: 1px solid var(--gray-200); }
    .dg-sub:first-of-type { border-top: 0; padding-top: 8px; }
    .dg-sub:nth-of-type(even) .dg-sub-foto { order: 2; }
    .dg-sub-foto { border-radius: 16px; overflow: hidden; aspect-ratio: 4 / 3; background: var(--gray-100); }
    .dg-sub-foto img { width: 100%; height: 100%; object-fit: cover; }
    .dg-sub h3 { font-family: var(--font-head); font-size: clamp(24px, 2.4vw, 32px); letter-spacing: -.035em; margin-bottom: 12px; }
    .dg-sub p { font-size: 15.5px; line-height: 1.7; color: var(--gray-600); margin-bottom: 16px; }
    .dg-punten { list-style: none; display: grid; gap: 8px; margin-bottom: 22px; }
    .dg-punten li { display: flex; gap: 10px; font-size: 15px; }
    .dg-punten svg { width: 17px; height: 17px; color: var(--green); flex-shrink: 0; margin-top: 2px; }
    .dg-sub-acties { display: flex; flex-wrap: wrap; gap: 12px 20px; align-items: center; }
    .dg-sub-link { font-family: var(--font-head); font-size: 14px; font-weight: 600; color: var(--green); text-decoration: underline; text-underline-offset: 3px; }

    .dg-stappen { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; counter-reset: stap; list-style: none; }
    .dg-stap { background: var(--white); border: 1px solid var(--gray-200); border-radius: 14px; padding: 22px 20px; }
    .dg-stap::before { counter-increment: stap; content: counter(stap); display: grid; place-items: center; width: 32px; height: 32px; border-radius: 50%; background: var(--green); color: #fff; font-family: var(--font-head); font-weight: 700; font-size: 14px; margin-bottom: 14px; }
    .dg-stap h3 { font-family: var(--font-head); font-size: 16px; letter-spacing: -.02em; margin-bottom: 6px; }
    .dg-stap p { font-size: 13.5px; line-height: 1.6; color: var(--gray-600); }
    .dg-noot { margin-top: 20px; font-size: 13px; color: var(--gray-600); }

    .dg-faq { max-width: 820px; }
    .dg-faq details { border-bottom: 1px solid var(--gray-200); }
    .dg-faq summary { list-style: none; cursor: pointer; display: flex; justify-content: space-between; gap: 16px; align-items: center; padding: 20px 0; font-family: var(--font-head); font-size: 17px; font-weight: 600; letter-spacing: -.01em; }
    .dg-faq summary::-webkit-details-marker { display: none; }
    .dg-faq summary::after { content: '+'; font-size: 24px; font-weight: 400; color: var(--green); flex-shrink: 0; transition: transform .2s; }
    .dg-faq details[open] summary::after { transform: rotate(45deg); }
    .dg-faq details p { padding: 0 0 20px; font-size: 15px; line-height: 1.7; color: var(--gray-600); max-width: 720px; }
    .dg-faq-meer { margin-top: 20px; font-size: 14px; color: var(--gray-600); }
    .dg-faq-meer a { color: var(--green); text-decoration: underline; }

    .dg-offerte { background: var(--black); color: var(--white); }
    .dg-offerte .dg-kop p { color: rgba(255,255,255,.65); }
    .dg-offerte-grid { display: grid; grid-template-columns: .8fr 1.2fr; gap: 56px; align-items: start; }
    .dg-offerte-info ul { list-style: none; display: grid; gap: 12px; margin-top: 8px; }
    .dg-offerte-info li { display: flex; gap: 10px; font-size: 15px; color: rgba(255,255,255,.8); }
    .dg-offerte-info svg { width: 17px; height: 17px; color: var(--green); flex-shrink: 0; margin-top: 2px; }
    .dg-offerte-info .dg-contact { margin-top: 28px; font-size: 14px; color: rgba(255,255,255,.6); line-height: 1.7; }
    .dg-offerte-info .dg-contact a { color: #fff; text-decoration: underline; text-underline-offset: 2px; }
    .dg-form { background: var(--white); color: var(--black); border-radius: 18px; padding: 32px; display: grid; grid-template-columns: 1fr 1fr; gap: 16px 18px; }
    .dg-veld { display: flex; flex-direction: column; gap: 6px; }
    .dg-veld.vol { grid-column: 1 / -1; }
    .dg-veld label, .dg-veld legend { font-family: var(--font-head); font-size: 12px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--gray-600); }
    .dg-veld label .opt, .dg-veld legend .opt { text-transform: none; letter-spacing: 0; font-weight: 400; color: var(--gray-400); }
    .dg-veld input, .dg-veld select, .dg-veld textarea { font-family: var(--font-body); font-size: 16px; color: var(--black); background: var(--gray-50); border: 1.5px solid var(--gray-200); border-radius: 10px; padding: 12px 14px; width: 100%; transition: border-color .2s, background .2s; }
    .dg-veld textarea { min-height: 110px; resize: vertical; }
    .dg-veld input:focus, .dg-veld select:focus, .dg-veld textarea:focus { outline: none; border-color: var(--green); background: #fff; }
    .dg-veld .ongeldig { border-color: #e53e3e; }
    fieldset.dg-veld { border: 0; padding: 0; margin: 0; min-width: 0; }
    .dg-veld .dg-chip { font-family: var(--font-body); font-size: 14px; font-weight: 400; letter-spacing: 0; text-transform: none; color: var(--black); }
    .dg-chips { display: flex; flex-wrap: wrap; gap: 8px; }
    .dg-chip { position: relative; }
    .dg-chip input { position: absolute; opacity: 0; width: 1px; height: 1px; }
    .dg-chip span { display: inline-block; padding: 8px 14px; border: 1.5px solid var(--gray-200); border-radius: 100px; font-size: 14px; cursor: pointer; transition: border-color .15s, background .15s, color .15s; }
    .dg-chip input:checked + span { border-color: var(--green); background: var(--green-dim); color: #006b35; font-weight: 600; }
    .dg-chip input:focus-visible + span { outline: 2px solid var(--green); outline-offset: 2px; }
    .dg-honing { position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden; }
    .dg-verstuur { grid-column: 1 / -1; display: flex; flex-direction: column; gap: 10px; margin-top: 4px; }
    .dg-verstuur .btn { width: 100%; padding: 16px; }
    .dg-melding { font-size: 14px; color: #e53e3e; min-height: 1em; }
    .dg-privacy { font-size: 12.5px; line-height: 1.6; color: var(--gray-600); }
    .dg-privacy a { color: var(--green); text-decoration: underline; }

    @media (max-width: 1024px) {
      .dg-wrap { padding: 0 40px; }
      .dg-producten { grid-template-columns: repeat(3, 1fr); }
      .dg-stappen { grid-template-columns: repeat(3, 1fr); }
      .dg-offerte-grid { grid-template-columns: 1fr; gap: 32px; }
    }
    @media (max-width: 768px) {
      .dg-wrap { padding: 0 16px; }
      .dg-sectie { padding: 52px 0; }
      .dg-kop { margin-bottom: 24px; }
      .dg-hero-grid { grid-template-columns: 1fr; gap: 0; padding-top: 0; padding-bottom: 32px; }
      .dg-hero-foto { order: -1; aspect-ratio: 16 / 9; border-radius: 0 0 16px 16px; margin: 0 -16px 24px; }
      .dg-hero .breadcrumb { display: none; }
      .dg-hero h1 { font-size: 36px; margin-bottom: 14px; }
      .dg-hero-intro { font-size: 15.5px; margin-bottom: 20px; }
      .dg-hero-btns { display: grid; grid-template-columns: 1fr; margin-bottom: 20px; }
      .dg-hero-btns .btn { justify-content: center; }
      .dg-feiten { flex-direction: column; gap: 8px; }
      .dg-tegels { grid-template-columns: 1fr; gap: 10px; }
      .dg-tegel { padding: 16px 18px; }
      .dg-producten { grid-template-columns: repeat(2, 1fr); gap: 12px; }
      .dg-logos { gap: 20px 32px; padding: 8px 0 28px; margin-bottom: 28px; }
      .dg-logos img { max-height: 32px; }
      .dg-cases.enkel .dg-case { grid-template-columns: 1fr; }
      .dg-cases.enkel .dg-case div { padding: 18px; }
      .dg-sub { grid-template-columns: 1fr; gap: 20px; padding: 36px 0; }
      .dg-sub:nth-of-type(even) .dg-sub-foto { order: 0; }
      .dg-stappen { grid-template-columns: 1fr; gap: 10px; }
      .dg-stap { display: grid; grid-template-columns: 32px 1fr; column-gap: 14px; padding: 16px; }
      .dg-stap::before { grid-row: span 2; margin-bottom: 0; }
      .dg-form { grid-template-columns: 1fr; padding: 22px 18px; }
    }
    @media (prefers-reduced-motion: reduce) {
      .dg-tegel, .dg-product-foto img { transition: none; }
    }
"""


def pagina(d, alle, stijl, kop, staart):
    slug = d["slug"]
    url = f"{SITE}/{slug}"
    hero_foto, hero_alt, hw, hh = d["hero"]

    kaarten, namen = [], []
    for s in d["producten"]:
        k, n = productkaart(s, alle, d.get("productnamen", {}))
        kaarten.append(k)
        namen.append(n)

    tegels = "".join(
        f'<a class="dg-tegel" href="#{s["id"]}" data-sub="{e(s["titel"])}"><strong>{e(s["titel"])} {PIJL}</strong>'
        f'<span>{e(s["kort"])}</span></a>' for s in d["sub"])

    subs = []
    for s in d["sub"]:
        punten = "".join(f"<li>{VINK}<span>{e(p)}</span></li>" for p in s["punten"])
        link = ""
        if s.get("link"):
            link = f'<a class="dg-sub-link" href="{s["link"][0]}">{e(s["link"][1])}</a>'
        subs.append(
            f'<article class="dg-sub" id="{s["id"]}">'
            f'<div class="dg-sub-foto"><img src="{fotopad(s["foto"])}" alt="{e(s["alt"])}" loading="lazy" width="800" height="600"></div>'
            f'<div><h3>{e(s["titel"])}</h3><p>{e(s["tekst"])}</p><ul class="dg-punten">{punten}</ul>'
            f'<div class="dg-sub-acties"><a class="btn btn-green" href="#offerte" data-sub="{e(s["titel"])}">Vraag een offerte aan {PIJL}</a>{link}</div></div>'
            f'</article>')

    logos = "".join(
        f'<img src="/fotomateriaal/partner-logos/{f}" alt="{e(a)}" style="height:{h}px" loading="lazy">'
        for f, a, h in d["logos"])
    cases = "".join(
        f'<article class="dg-case"><img src="{fotopad(f)}" alt="{e(t)}" loading="lazy" width="700" height="525">'
        f'<div><h3>{e(t)}</h3><p>{e(x)}</p></div></article>' for f, t, x in d["cases"])
    enkel = " enkel" if len(d["cases"]) == 1 else ""

    stappen = "".join(f'<li class="dg-stap"><h3>{e(t)}</h3><p>{e(x)}</p></li>' for t, x in WERKWIJZE)
    faq = "".join(f"<details><summary>{e(v)}</summary><p>{e(a)}</p></details>" for v, a in d["faq"])
    faq_ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": v, "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for v, a in d["faq"]],
    }, ensure_ascii=False)

    chips = "".join(
        f'<label class="dg-chip"><input type="checkbox" name="product" value="{e(n)}"><span>{e(n)}</span></label>'
        for n in namen + ["Iets anders"])
    sub_opties = "".join(f"<option>{e(s['titel'])}</option>" for s in d["sub"])
    hoe = "".join(f"<option>{e(o)}</option>" for o in HOE_GEVONDEN)
    feiten = "".join(f"<li>{VINK}<span>{e(f)}</span></li>" for f in d["feiten"])

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <!-- Cookiemelding + Google-tag (Consent Mode v2) + Meta Pixel na toestemming -->
  <script src="/consent.js"></script>
  <title>{e(d["titel"])}</title>
  <meta name="description" content="{e(d["omschrijving"])}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" type="image/png" href="/fotomateriaal/partner-logos/favicon.png" />
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{e(d["titel"])}">
  <meta property="og:description" content="{e(d["omschrijving"])}">
  <meta property="og:image" content="{SITE}{FOTO}{hero_foto}">
  <meta property="og:locale" content="nl_NL">
  <meta property="og:site_name" content="Hockeypolo">
  <link rel="preload" as="image" href="{FOTO}{hero_foto}" fetchpriority="high" />
  <link rel="preload" as="font" type="font/woff2" href="/fonts/space-grotesk-v22-latin-700.woff2" crossorigin />
  <link rel="preload" as="font" type="font/woff2" href="/fonts/inter-v20-latin-regular.woff2" crossorigin />
  <script type="application/ld+json">{faq_ld}</script>
  <style>{stijl}{CSS}  </style>
  <script defer src="/_vercel/insights/script.js"></script>
</head>
<body data-segment="{d["segment"]}">

{kop}

<div class="page">
<!-- AUTOMATISCH GEGENEREERD door scripts/genereer-doelgroeppaginas.py — pas de teksten aan in scripts/doelgroepteksten.py -->

<!-- 1. HERO -->
<header class="dg-hero">
  <div class="dg-wrap dg-hero-grid">
    <div>
      <div class="breadcrumb"><a href="/">Home</a> <i>/</i> <span>{e(d["menu"])}</span></div>
      <span class="lbl">{e(d["label"])}</span>
      <h1>{d["h1"]}</h1>
      <p class="dg-hero-intro">{e(d["intro"])}</p>
      <div class="dg-hero-btns">
        <a href="#offerte" class="btn btn-green">Vraag een offerte aan {PIJL}</a>
        <a href="#producten" class="btn btn-outline-white">Bekijk producten</a>
      </div>
      <ul class="dg-feiten">{feiten}</ul>
    </div>
    <div class="dg-hero-foto"><img src="{FOTO}{hero_foto}" alt="{e(hero_alt)}" width="{hw}" height="{hh}" fetchpriority="high"></div>
  </div>
</header>

<!-- 2. SUBDOELGROEPEN -->
<section class="dg-sectie" aria-labelledby="dg-sub-kop" style="padding-bottom:0">
  <div class="dg-wrap">
    <div class="dg-kop"><h2 id="dg-sub-kop">{e(d["sub_kop"])}</h2></div>
    <div class="dg-tegels">{tegels}</div>
  </div>
</section>

<!-- 3. PRODUCTEN -->
<section class="dg-sectie" id="producten" aria-labelledby="dg-prod-kop">
  <div class="dg-wrap">
    <div class="dg-kop"><h2 id="dg-prod-kop">Meest <em>gevraagd</em></h2><p>Alles met jullie logo, geborduurd of bedrukt. Klik voor kleuren en details.</p></div>
    <div class="dg-producten">{"".join(kaarten)}</div>
    <p class="dg-meer"><a href="/producten">Bekijk het hele assortiment {PIJL}</a></p>
  </div>
</section>

<!-- 4. LOGO'S EN CASES -->
<section class="dg-sectie grijs" aria-labelledby="dg-case-kop">
  <div class="dg-wrap">
    <div class="dg-kop"><h2 id="dg-case-kop">Zij gingen <em>je voor</em></h2></div>
    <div class="dg-logos">{logos}</div>
    <div class="dg-cases{enkel}">{cases}</div>
    <p class="dg-meer"><a href="/impressies">Meer projecten bekijken {PIJL}</a></p>
  </div>
</section>

<!-- SUBDOELGROEPEN UITGEWERKT -->
<section class="dg-sectie" aria-label="{e(d["sub_kop"])}">
  <div class="dg-wrap">{"".join(subs)}</div>
</section>

<!-- 5. WERKWIJZE -->
<section class="dg-sectie grijs" aria-labelledby="dg-werk-kop">
  <div class="dg-wrap">
    <div class="dg-kop"><h2 id="dg-werk-kop">Zo <em>werkt het</em></h2><p>Levertijd 2 tot 4 weken*. Minimale afname per product: zie de producten hierboven.</p></div>
    <ol class="dg-stappen">{stappen}</ol>
    <p class="dg-noot">* Na akkoord op de digitale proef. Afhankelijk van product, aantal en drukte; heb je een harde datum, zet die dan in je aanvraag.</p>
  </div>
</section>

<!-- 6. VEELGESTELDE VRAGEN -->
<section class="dg-sectie" aria-labelledby="dg-faq-kop">
  <div class="dg-wrap">
    <div class="dg-kop"><h2 id="dg-faq-kop">Veelgestelde <em>vragen</em></h2></div>
    <div class="dg-faq">{faq}</div>
    <p class="dg-faq-meer">Staat je vraag er niet bij? Bekijk <a href="/faq">alle veelgestelde vragen</a> of stel hem in het formulier hieronder.</p>
  </div>
</section>

<!-- 7. OFFERTEFORMULIER -->
<section class="dg-sectie dg-offerte" id="offerte" aria-labelledby="dg-off-kop">
  <div class="dg-wrap dg-offerte-grid">
    <div class="dg-offerte-info">
      <div class="dg-kop"><span class="lbl">Vrijblijvend</span><h2 id="dg-off-kop" style="color:#fff">Vraag een <em>offerte</em> aan</h2><p>Vertel kort wat je zoekt. Je hoort binnen één werkdag van ons.</p></div>
      <ul>
        <li>{VINK}<span>Gratis ontwerp en digitale proef</span></li>
        <li>{VINK}<span>Heldere offerte, geen verplichtingen</span></li>
        <li>{VINK}<span>Sinds 2005, 500+ projecten</span></li>
      </ul>
      <p class="dg-contact">Liever direct contact? Mail <a href="mailto:info@hockeypolo.com">info@hockeypolo.com</a> of bel <a href="tel:+31614200114">+31 6 14200114</a>.<br>Logo's en uitgebreide wensen kun je ook kwijt via <a href="/start-project?segment={d["segment"]}">Start project</a>.</p>
    </div>

    <form class="dg-form" id="dg-form" novalidate>
      <div class="dg-veld"><label for="dg-naam">Naam *</label><input id="dg-naam" name="Naam" autocomplete="name" required></div>
      <div class="dg-veld"><label for="dg-org">{e(d["organisatie_label"])} <span class="opt">(optioneel)</span></label><input id="dg-org" name="Organisatie" autocomplete="organization" placeholder="{e(d["organisatie_placeholder"])}"></div>
      <div class="dg-veld"><label for="dg-email">E-mailadres *</label><input id="dg-email" name="E-mail" type="email" autocomplete="email" required></div>
      <div class="dg-veld"><label for="dg-tel">Telefoon <span class="opt">(optioneel)</span></label><input id="dg-tel" name="Telefoon" type="tel" autocomplete="tel"></div>
      <div class="dg-veld vol"><label for="dg-type">Waarvoor?</label><select id="dg-type" name="Type aanvraag"><option value="">Maak een keuze</option>{sub_opties}<option>Iets anders</option></select></div>
      <fieldset class="dg-veld vol"><legend>Interesse in <span class="opt">(meerdere mogelijk)</span></legend><div class="dg-chips">{chips}</div></fieldset>
      <div class="dg-veld"><label for="dg-aantal">Aantal (ongeveer) <span class="opt">(optioneel)</span></label><input id="dg-aantal" name="Aantal" inputmode="numeric" placeholder="Bijv. 40"></div>
      <div class="dg-veld"><label for="dg-datum">Nodig op <span class="opt">(optioneel)</span></label><input id="dg-datum" name="Gewenste leverdatum" type="date"></div>
      <div class="dg-veld vol"><label for="dg-bericht">Je vraag of wensen *</label><textarea id="dg-bericht" name="Bericht" required placeholder="Bijv. kleuren, logo-plaatsing, maten of een idee dat je hebt."></textarea></div>
      <div class="dg-veld vol"><label for="dg-hoe">Hoe heb je ons gevonden? *</label><select id="dg-hoe" name="hoe_gevonden" required><option value="">Maak een keuze</option>{hoe}</select></div>
      <div class="dg-honing" aria-hidden="true"><label for="dg-honey">Laat dit veld leeg</label><input id="dg-honey" name="_honey" tabindex="-1" autocomplete="off"></div>
      <input type="hidden" name="segment" value="{d["segment"]}">
      <input type="hidden" name="via_advertentie" value="nee">
      <div class="dg-verstuur">
        <button type="submit" class="btn btn-green" id="dg-knop">Verstuur aanvraag {PIJL}</button>
        <p class="dg-melding" id="dg-melding" role="alert"></p>
        <p class="dg-privacy">We gebruiken je gegevens alleen om je aanvraag te behandelen. Zie onze <a href="/privacyverklaring">privacyverklaring</a>.</p>
      </div>
    </form>
  </div>
</section>
</div>

{staart}
<script>
// Doelgroeppagina: subdoelgroep onthouden in het formulier + versturen naar FormSubmit
(function () {{
  var form = document.getElementById('dg-form');
  var type = document.getElementById('dg-type');
  document.querySelectorAll('[data-sub]').forEach(function (a) {{
    a.addEventListener('click', function () {{ type.value = a.dataset.sub; }});
  }});
  // Bij binnenkomst via /{slug}#subdoelgroep ook het type voorinvullen
  var start = document.querySelector('.dg-tegel[href="' + location.hash + '"]');
  if (start) type.value = start.dataset.sub;

  form.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    var melding = document.getElementById('dg-melding');
    var knop = document.getElementById('dg-knop');
    var verplicht = ['dg-naam', 'dg-email', 'dg-bericht', 'dg-hoe'];
    var fout = null;
    verplicht.forEach(function (id) {{
      var el = document.getElementById(id);
      var ok = el.value.trim() && (el.type !== 'email' || /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(el.value.trim()));
      el.classList.toggle('ongeldig', !ok);
      if (!ok && !fout) fout = el;
    }});
    if (fout) {{
      melding.textContent = 'Vul je naam, e-mailadres, je vraag en hoe je ons gevonden hebt in.';
      fout.focus();
      return;
    }}
    melding.textContent = '';
    knop.disabled = true;
    knop.firstChild.textContent = 'Versturen… ';

    var fd = new FormData(form);
    var producten = fd.getAll('product');
    fd.delete('product');
    if (producten.length) fd.set('Producten', producten.join(', '));
    if (window.hpVoegHerkomstToe) window.hpVoegHerkomstToe(fd, '{d["segment"]}');
    var naam = fd.get('Naam'), org = fd.get('Organisatie');
    fd.set('_subject', 'Nieuwe aanvraag {d["menu"]} – ' + naam + (org ? ' (' + org + ')' : ''));
    fd.set('_replyto', fd.get('E-mail'));
    fd.set('_template', 'table');
    fd.set('_captcha', 'false');
    fd.set('Pagina', location.pathname);

    if (window.hpStuurNaarSheet) window.hpStuurNaarSheet(fd, 'Doelgroeppagina');
    fetch('https://formsubmit.co/info@hockeypolo.com', {{ method: 'POST', mode: 'no-cors', body: fd }})
      .then(function () {{
        if (window.hpMarkeerAanvraag) window.hpMarkeerAanvraag();
        window.location.href = window.hpUrl ? window.hpUrl('/bedankt') : '/bedankt';
      }})
      .catch(function () {{
        knop.disabled = false;
        knop.firstChild.textContent = 'Verstuur aanvraag ';
        melding.textContent = 'Verzenden lukte niet. Probeer het opnieuw of mail naar info@hockeypolo.com.';
      }});
  }});
}})();
</script>
</body>
</html>
"""


def main():
    alle = producten()
    stijl, kop, staart = onderdelen()
    for d in DOELGROEPEN:
        uit = WORTEL / f"{d['slug']}.html"
        uit.write_text(pagina(d, alle, stijl, kop, staart), encoding="utf-8")
        print(f"{uit.name} geschreven")


if __name__ == "__main__":
    main()
