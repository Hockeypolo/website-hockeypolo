#!/usr/bin/env python3
"""
Genereert producten-{slug}.html voor alle 27 producten met nieuwe fotografie.

Sjabloon = het bestaande producten-polos.html. Daaruit worden navbar, footer,
CSS en de USP-balk hergebruikt; alleen de productspecifieke delen worden
vervangen. Zo blijft de pagina identiek aan de rest van de site.

Nieuw t.o.v. de oude pagina's: galerij met alle hoeken, klikbare kleurstalen
die de hele fotoset wisselen, en modelfoto's vooraan.

    python3 scripts/genereer-productpaginas.py
"""

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from productteksten import OVER  # noqa: E402

WORTEL = Path(__file__).resolve().parent.parent
# Vast sjabloon, NIET producten-polos.html: dat bestand wordt door dit script
# zelf overschreven, waardoor een tweede run zijn eigen invoer kapotmaakt.
SJABLOON = Path(__file__).resolve().parent / "sjabloon-productpagina.html"
DATA = WORTEL / "producten-data.js"

# Labels voor alt-teksten en miniatuur-titels
SHOTLABELS = {
    "1_voorkant": "Voorkant", "2_achterkant": "Achterkant", "3_driekwart": "Driekwart",
    "4_gevouwen": "Gevouwen", "5_closeup_logo": "Detail logo", "6_closeup_stof": "Detail stof",
    "1_bovenaanzicht": "Bovenaanzicht", "2_driekwart": "Driekwart",
    "3_closeup_logo": "Detail logo", "4_closeup_zool": "Detail zool",
    "1_hangend_voorkant": "Hangend", "2_wapperend": "Wapperend",
    "4_closeup_logo": "Detail logo", "5_closeup_ringen": "Detail ringen",
    "1_dubbelgevouwen": "Dubbelgevouwen", "2_volledig_uitgelegd": "Uitgelegd",
    "4_closeup_breisel": "Detail breisel", "5_gedrapeerd": "Gedrapeerd",
    "3_achterkant": "Achterkant",
}


def e(s):
    return html.escape(str(s), quote=True)


def label(shot):
    if shot.startswith("model_"):
        return "In beweging" if shot.endswith("_beweging") else "Op model"
    return SHOTLABELS.get(shot, shot)


def laad_producten():
    js = DATA.read_text(encoding="utf-8")
    m = re.search(r"window\.HP_PRODUCTEN = (\[.*?\]);\n", js, re.S)
    return json.loads(m.group(1))


# ── Extra CSS + JS die op elke productpagina komt ────────────────────────
EXTRA_CSS = """
    /* ═══ Kleurkiezer + galerij (catalogus) ═══════════════════════ */
    .kleur-kiezer { margin-bottom: 22px; }
    .kleur-kop { font-family:var(--font-head); font-size:13px; font-weight:600;
      margin-bottom:10px; display:flex; align-items:baseline; gap:8px; flex-wrap:wrap; }
    .kleur-aantal { font-size:12px; font-weight:400; color:var(--gray-400); }
    .kleur-stalen { display:flex; flex-wrap:wrap; gap:8px; max-width:420px; }
    .kleur-staal { width:28px; height:28px; border-radius:50%; background:var(--sw);
      border:1px solid rgba(0,0,0,.16); padding:0; cursor:pointer;
      transition:transform .15s var(--ease), box-shadow .15s; }
    .kleur-staal:hover { transform:scale(1.12); }
    .kleur-staal:focus-visible { outline:2px solid var(--green); outline-offset:3px; }
    .kleur-staal.is-actief { box-shadow:0 0 0 2px #fff, 0 0 0 4px var(--green); }

    /* Hoofdfoto: volledig in beeld, niet bijgesneden.
       height:auto is nodig omdat een height-attribuut op de <img> anders de
       CSS aspect-ratio overrulet en de foto tot 1200px uitrekt.
       Productfoto's zijn 1:1, modelfoto's 4:5 — vandaar de is-portret-variant. */
    .product-detail-hero-img { height:auto; object-fit:contain; background:var(--gray-100); }
    .product-detail-hero-img.is-portret { aspect-ratio:4/5; }

    .product-detail-gallery { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:12px; }
    .product-detail-gallery button { padding:0; border:none; background:none; cursor:pointer; border-radius:10px; }
    .product-detail-gallery img { width:100%; height:auto; aspect-ratio:1; object-fit:contain;
      border-radius:10px; background:var(--gray-100); display:block; }
    .product-detail-gallery button.is-actief img { outline:2px solid var(--green); outline-offset:2px; }
    .product-detail-gallery button:focus-visible img { outline:2px solid var(--black); outline-offset:2px; }
    @media (max-width:640px){ .kleur-staal{ width:26px; height:26px; } }
"""

EXTRA_JS = """
<script src="/producten-data.js" defer></script>
<script>
// Kleurwissel + galerij. Werkt op HP_PRODUCTEN uit producten-data.js.
document.addEventListener('DOMContentLoaded', function () {
  var slug = document.body.dataset.product;
  var p = (window.HP_PRODUCTEN || []).find(function (x) { return x.slug === slug; });
  if (!p) return;

  var hero    = document.getElementById('pd-hero');
  var galerij = document.getElementById('pd-galerij');
  var naamEl  = document.getElementById('pd-kleurnaam');
  var stalen  = document.querySelectorAll('.kleur-staal');
  var actief  = p.kleuren[0];

  function foto(k, shot, maat) {
    return window.hpFoto(p.fotomap, k.slug, shot, maat);
  }
  // 1200px bestaat alleen voor de hoofdfoto en de modelfoto's
  function heeftGroot(k, shot) { return (k.groot || []).indexOf(shot) !== -1; }

  function toonShot(k, shot) {
    hero.src = foto(k, shot, heeftGroot(k, shot) ? 1200 : 600);
    hero.alt = p.naam + ' — ' + k.naam;
    hero.classList.toggle('is-portret', shot.indexOf('model_') === 0);
    galerij.querySelectorAll('button').forEach(function (b) {
      b.classList.toggle('is-actief', b.dataset.shot === shot);
    });
  }

  function bouwGalerij(k) {
    var shots = (k.modelfotos || []).concat(k.fotos);   // modelfoto vooraan
    galerij.innerHTML = shots.map(function (s) {
      // Geen width/height-attributen: die zouden de CSS aspect-ratio overrulen.
      // De vaste aspect-ratio in de CSS voorkomt al dat de layout verspringt.
      return '<button type="button" data-shot="' + s + '" aria-label="' + s + '">' +
             '<img src="' + foto(k, s, 300) + '" alt="" loading="lazy" /></button>';
    }).join('');
    toonShot(k, shots[0]);
  }

  function kies(k) {
    actief = k;
    naamEl.textContent = k.naam;
    stalen.forEach(function (b) {
      var aan = b.dataset.kleur === k.slug;
      b.classList.toggle('is-actief', aan);
      b.setAttribute('aria-checked', aan ? 'true' : 'false');
    });
    bouwGalerij(k);
    history.replaceState(null, '', '?kleur=' + k.slug);
  }

  stalen.forEach(function (b) {
    b.addEventListener('click', function () {
      var k = p.kleuren.find(function (x) { return x.slug === b.dataset.kleur; });
      if (k) kies(k);
    });
  });

  galerij.addEventListener('click', function (ev) {
    var b = ev.target.closest('button');
    if (b) toonShot(actief, b.dataset.shot);
  });

  // Deelbare kleur via ?kleur=
  var gevraagd = new URLSearchParams(location.search).get('kleur');
  var start = gevraagd && p.kleuren.find(function (x) { return x.slug === gevraagd; });
  kies(start || p.kleuren[0]);
});
</script>
"""


def bouw_pagina(sjabloon: str, p: dict) -> str:
    k = p["kleuren"][0]
    naam, over_titel, over_alineas = p["naam"], OVER[p["slug"]][0], OVER[p["slug"]][1]
    hoofdshot = (k.get("modelfotos") or k["fotos"])[0]
    hero_maat = 1200 if hoofdshot in k.get("groot", []) else 600
    hero_pad = f"/productfotos/{p['fotomap']}/{k['slug']}/{hoofdshot}-{hero_maat}.webp"
    portret = " is-portret" if hoofdshot.startswith("model_") else ""

    t = sjabloon

    # ── <head> ──
    t = re.sub(r"<title>.*?</title>",
               f"<title>{e(naam)} bedrukken met eigen logo | Hockeypolo</title>", t, count=1)
    t = re.sub(r'(<meta name="description" content=")[^"]*(")',
               lambda m: m.group(1) + e(p["omschrijving"]) + m.group(2), t, count=1)
    t = re.sub(r'(<link rel="canonical" href="https://hockeypolo\.com/producten/)[^"]*(")',
               lambda m: m.group(1) + p["slug"] + m.group(2), t, count=1)
    t = re.sub(r'(<meta property="og:url" content="https://hockeypolo\.com/producten/)[^"]*(")',
               lambda m: m.group(1) + p["slug"] + m.group(2), t, count=1)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
               lambda m: m.group(1) + e(naam) + " bedrukken met eigen logo | Hockeypolo" + m.group(2), t, count=1)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
               lambda m: m.group(1) + e(p["omschrijving"]) + m.group(2), t, count=1)
    t = re.sub(r'(<meta property="og:image" content="https://hockeypolo\.com)[^"]*(")',
               lambda m: m.group(1) + hero_pad + m.group(2), t, count=1)
    # preload wijst naar de nieuwe hero
    t = re.sub(r'(<link rel="preload" as="image" href=")[^"]*(")',
               lambda m: m.group(1) + hero_pad + m.group(2), t, count=1)

    # ── extra CSS vlak vóór het einde van de eerste <style> ──
    t = t.replace("\n  </style>", EXTRA_CSS + "\n  </style>", 1)

    # ── body krijgt het product mee voor de JS ──
    t = t.replace("<body>", f'<body data-product="{p["slug"]}">', 1)

    # ── hero ──
    t = re.sub(r"(<i>/</i> <span>)[^<]*(</span></div>)",
               lambda m: m.group(1) + e(naam) + m.group(2), t, count=1)
    t = re.sub(r"<h1>.*?</h1>", f"<h1>{e(naam)}</h1>", t, count=1)
    t = re.sub(r"(<h1>.*?</h1>\s*<p>).*?(</p>)",
               lambda m: m.group(1) + e(p["omschrijving"]) + m.group(2), t, count=1, flags=re.S)

    # ── media-kolom ──
    # Geen width/height-attributen: die overrulen de CSS aspect-ratio en rekken
    # de foto uit. De aspect-ratio in de CSS zorgt zelf voor een stabiele layout.
    media = f"""<img src="{hero_pad}" alt="{e(naam)} — {e(k['naam'])}" id="pd-hero"
             class="product-detail-hero-img{portret}" fetchpriority="high" />
        <div class="product-detail-gallery" id="pd-galerij"></div>"""
    t = re.sub(r'<img src="[^"]*" alt="[^"]*" class="product-detail-hero-img" />\s*'
               r'(<div class="product-detail-gallery">.*?</div>)?',
               media, t, count=1, flags=re.S)

    # ── kleurkiezer vóór de min-afname-pill ──
    stalen = "".join(
        f'<button type="button" class="kleur-staal" role="radio" aria-checked="false" '
        f'data-kleur="{kk["slug"]}" style="--sw:{kk["hex"]}" '
        f'aria-label="{e(kk["naam"])}" title="{e(kk["naam"])}"></button>'
        for kk in p["kleuren"]
    )
    n = len(p["kleuren"])
    kiezer = f"""<div class="kleur-kiezer">
        <div class="kleur-kop">Kleur: <strong id="pd-kleurnaam">{e(k['naam'])}</strong>
          <span class="kleur-aantal">{'1 kleur' if n == 1 else f'{n} kleuren beschikbaar'}</span></div>
        <div class="kleur-stalen" role="radiogroup" aria-label="Kies een kleur">{stalen}</div>
      </div>
      <div class="product-card-minafname">Min. afname {p['minQty']} stuks</div>"""
    t = re.sub(r'<div class="product-card-minafname">Min\. afname \d+ stuks</div>',
               kiezer, t, count=1)

    # ── kenmerk-chips ──
    chips = "\n".join(
        '          <div class="proj-detail-item"><svg viewBox="0 0 24 24">'
        '<path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="9"/></svg>' + e(s) + "</div>"
        for s in p["kenmerken"]
    )
    t = re.sub(r'(<div class="proj-details">\n).*?(\n      </div>)',
               lambda m: m.group(1) + chips + m.group(2), t, count=1, flags=re.S)

    # ── Over-tekst ──
    alineas = "\n".join(f"      <p>{e(a)}</p>" for a in over_alineas)
    t = re.sub(r'(<div class="product-detail-copy">\s*<h2>).*?(</h2>).*?(\n      </div>)',
               lambda m: m.group(1) + e(over_titel) + m.group(2) + "\n" + alineas + m.group(3),
               t, count=1, flags=re.S)

    # ── CTA-kop onderaan ──
    t = re.sub(r"(<h2>Vraag een offerte aan voor <em>).*?(</em></h2>)",
               lambda m: m.group(1) + e(naam) + m.group(2), t, count=1)

    # ── JS vlak voor </body> ──
    t = t.replace("</body>", EXTRA_JS + "</body>", 1)
    return t


def main():
    producten = laad_producten()
    sjabloon = SJABLOON.read_text(encoding="utf-8")
    for p in producten:
        pad = WORTEL / f"producten-{p['slug']}.html"
        nieuw = "bestaand" if pad.exists() else "NIEUW"
        pad.write_text(bouw_pagina(sjabloon, p), encoding="utf-8")
        print(f"  {pad.name:<44} {len(p['kleuren']):>2} kleuren  {nieuw}")
    print(f"\n{len(producten)} pagina's geschreven")


if __name__ == "__main__":
    main()
