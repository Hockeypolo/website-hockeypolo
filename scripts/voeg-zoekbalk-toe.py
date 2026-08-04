#!/usr/bin/env python3
"""
Voegt de productzoekfunctie toe aan de header van alle pagina's.

Een vergrootglas-icoon in de navbar opent een overlay met live resultaten.
Overlay in plaats van een inline veld, omdat de navbar bij 1280px met acht
menu-items geen ruimte heeft voor een zoekveld.

Zoekt in productnaam, categorie, kleurnamen en een synoniemenlijst.
Resultaten zijn echte links, zodat het zowel in de SPA als op de losse
pagina's werkt.

Idempotent.

    python3 scripts/voeg-zoekbalk-toe.py
"""

import re
import sys
from pathlib import Path

WORTEL = Path(__file__).resolve().parent.parent
BESTANDEN = ["index.html", "start-project.html", "bedankt-deel-je-idee.html"] + \
            sorted(p.name for p in WORTEL.glob("producten-*.html"))

CSS = """
    /* ═══ PRODUCTZOEKEN ═══════════════════════════════════════════ */
    .zoek-knop {
      width: 36px; height: 36px; border-radius: 6px;
      border: 1px solid var(--gray-200); background: none;
      display: grid; place-items: center; cursor: pointer;
      color: var(--black); flex-shrink: 0;
      transition: border-color .2s, background .2s, color .2s;
    }
    .zoek-knop:hover { border-color: var(--green); background: var(--green-dim); color: var(--green); }
    .zoek-knop svg { width: 15px; height: 15px; stroke: currentColor; fill: none; stroke-width: 2; }

    .zoek-overlay {
      position: fixed; inset: 0; z-index: 300;
      background: rgba(0,0,0,.45); backdrop-filter: blur(3px);
      display: none; align-items: flex-start; justify-content: center;
      padding: calc(var(--usp-h) + 100px) 20px 20px;
    }
    .zoek-overlay.open { display: flex; }
    .zoek-paneel {
      width: 100%; max-width: 560px; background: var(--white);
      border-radius: 14px; box-shadow: 0 24px 60px rgba(0,0,0,.28);
      overflow: hidden;
    }
    .zoek-veldrij { display: flex; align-items: center; gap: 10px; padding: 14px 18px; border-bottom: 1px solid var(--gray-200); }
    .zoek-veldrij svg { width: 17px; height: 17px; stroke: var(--gray-400); fill: none; stroke-width: 2; flex-shrink: 0; }
    .zoek-veld {
      flex: 1; border: none; outline: none; background: none;
      font-family: var(--font-body); font-size: 16px; color: var(--black);
    }
    .zoek-veld::placeholder { color: var(--gray-400); }
    .zoek-sluit {
      border: none; background: var(--gray-100); border-radius: 6px;
      font-family: var(--font-head); font-size: 11px; font-weight: 600;
      color: var(--gray-600); padding: 4px 8px; cursor: pointer;
    }
    .zoek-lijst { max-height: 60vh; overflow-y: auto; padding: 6px; }
    .zoek-rij {
      display: flex; align-items: center; gap: 12px;
      padding: 9px 10px; border-radius: 8px; cursor: pointer;
      text-decoration: none; color: inherit;
    }
    .zoek-rij[aria-selected="true"], .zoek-rij:hover { background: var(--gray-100); }
    .zoek-rij img { width: 44px; height: 44px; border-radius: 6px; object-fit: cover; background: var(--gray-100); flex-shrink: 0; }
    .zoek-rij-naam { font-family: var(--font-head); font-size: 14px; font-weight: 700; letter-spacing: -.01em; }
    .zoek-rij-meta { font-size: 12px; color: var(--gray-400); }
    .zoek-leeg { padding: 26px 16px; text-align: center; font-size: 14px; color: var(--gray-600); }
    @media (max-width: 640px) {
      .zoek-overlay { padding: calc(var(--usp-h) + 84px) 12px 12px; }
      .nav-hamburger + .zoek-knop, .zoek-knop { display: grid; }
    }
"""

KNOP = """      <button class="zoek-knop" id="zoek-knop" aria-label="Zoek in het assortiment">
        <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
      </button>
"""

OVERLAY = """
<div class="zoek-overlay" id="zoek-overlay" role="dialog" aria-modal="true" aria-label="Zoek in het assortiment">
  <div class="zoek-paneel">
    <div class="zoek-veldrij">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
      <input class="zoek-veld" id="zoek-veld" type="search" autocomplete="off"
             placeholder="Zoek een product, kleur of categorie…"
             role="combobox" aria-expanded="false" aria-controls="zoek-lijst" aria-autocomplete="list" />
      <button class="zoek-sluit" id="zoek-sluit" aria-label="Sluiten">ESC</button>
    </div>
    <div class="zoek-lijst" id="zoek-lijst" role="listbox" aria-label="Zoekresultaten"></div>
  </div>
</div>
<script src="/producten-data.js" defer></script>
<script>
(function () {
  // Synoniemen: wat mensen intypen is zelden de productnaam
  var SYNONIEMEN = {
    trui: ['sweaters','hoodies','quarter-zip-sweaters'],
    truien: ['sweaters','hoodies','quarter-zip-sweaters'],
    pet: ['caps','bucket-hats','bucket-hats-washed'],
    petten: ['caps','bucket-hats'],
    cap: ['caps'],
    hoed: ['bucket-hats','bucket-hats-washed'],
    tas: ['tote-bags'],
    tasje: ['tote-bags'],
    fles: ['waterflessen','thermosflessen'],
    drinkfles: ['waterflessen','thermosflessen'],
    beker: ['thermosflessen','waterflessen'],
    jas: ['bomberjacks','softshell-jassen','windjacks'],
    jassen: ['bomberjacks','softshell-jassen','windjacks'],
    shirt: ['t-shirts','sportshirts','polos','longsleeve-t-shirts','oversized-t-shirts'],
    broek: ['sportbroeken','sportbroeken-dames','zwembroeken'],
    korte: ['sportbroeken','sportbroeken-dames'],
    slippers: ['badslippers'],
    sokken: [], muts: [], mutsen: []
  };

  var knop = document.getElementById('zoek-knop');
  var overlay = document.getElementById('zoek-overlay');
  var veld = document.getElementById('zoek-veld');
  var lijst = document.getElementById('zoek-lijst');
  var sluit = document.getElementById('zoek-sluit');
  if (!knop || !overlay) return;
  var index = null, gekozen = -1;

  function normaliseer(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
  }

  function bouwIndex() {
    if (index || !window.HP_PRODUCTEN) return index;
    index = window.HP_PRODUCTEN.map(function (p) {
      var k = p.kleuren[0];
      var hoofd = k.fotos.filter(function (f) { return f.indexOf('1_') === 0; })[0] || k.fotos[0];
      var cat = (window.HP_CATEGORIEEN || {})[p.categorie] || p.categorie;
      return {
        slug: p.slug, naam: p.naam, cat: cat,
        aantal: p.kleuren.length,
        thumb: window.hpFoto(p.fotomap, k.slug, hoofd, 300),
        kleuren: p.kleuren.map(function (x) { return normaliseer(x.naam); }),
        zoek: normaliseer(p.naam + ' ' + cat + ' ' + p.kleuren.map(function (x) { return x.naam; }).join(' '))
      };
    });
    return index;
  }

  function zoek(term) {
    var t = normaliseer(term).trim();
    if (!t) return [];
    var idx = bouwIndex() || [];
    var syn = SYNONIEMEN[t] || [];
    var treffers = idx.filter(function (p) {
      return p.zoek.indexOf(t) !== -1 || syn.indexOf(p.slug) !== -1;
    });
    // exacte naamtreffers eerst
    treffers.sort(function (a, b) {
      return (normaliseer(b.naam).indexOf(t) === 0) - (normaliseer(a.naam).indexOf(t) === 0);
    });
    return treffers.slice(0, 7).map(function (p) {
      var kleurTreffer = p.kleuren.filter(function (k) { return k.indexOf(t) !== -1; })[0];
      return { p: p, kleur: (normaliseer(p.naam).indexOf(t) === -1) ? kleurTreffer : null };
    });
  }

  function toon(term) {
    var res = zoek(term);
    gekozen = -1;
    if (!term.trim()) { lijst.innerHTML = ''; veld.setAttribute('aria-expanded', 'false'); return; }
    if (!res.length) {
      lijst.innerHTML = '<div class="zoek-leeg">Niets gevonden voor &ldquo;' +
        term.replace(/[&<>"]/g, '') + '&rdquo;.<br><a href="/producten" style="color:var(--green)">Bekijk het hele assortiment</a></div>';
      veld.setAttribute('aria-expanded', 'false');
      return;
    }
    lijst.innerHTML = res.map(function (r, i) {
      var meta = r.kleur ? ('Kleur: ' + r.kleur) : (r.p.cat + ' · ' + r.p.aantal + (r.p.aantal === 1 ? ' kleur' : ' kleuren'));
      return '<a class="zoek-rij" role="option" aria-selected="false" id="zoek-r' + i + '" href="/producten/' + r.p.slug + '">' +
             '<img src="' + r.p.thumb + '" alt="" loading="lazy" />' +
             '<span><span class="zoek-rij-naam">' + r.p.naam + '</span><br>' +
             '<span class="zoek-rij-meta">' + meta + '</span></span></a>';
    }).join('');
    veld.setAttribute('aria-expanded', 'true');
  }

  function markeer(n) {
    var rijen = lijst.querySelectorAll('.zoek-rij');
    if (!rijen.length) return;
    gekozen = Math.max(0, Math.min(n, rijen.length - 1));
    rijen.forEach(function (r, i) { r.setAttribute('aria-selected', i === gekozen ? 'true' : 'false'); });
    rijen[gekozen].scrollIntoView({ block: 'nearest' });
    veld.setAttribute('aria-activedescendant', 'zoek-r' + gekozen);
  }

  function open() { overlay.classList.add('open'); veld.value = ''; lijst.innerHTML = ''; veld.focus(); }
  function dicht() { overlay.classList.remove('open'); veld.blur(); }

  knop.addEventListener('click', open);
  sluit.addEventListener('click', dicht);
  overlay.addEventListener('click', function (e) { if (e.target === overlay) dicht(); });
  veld.addEventListener('input', function () { toon(veld.value); });

  veld.addEventListener('keydown', function (e) {
    var rijen = lijst.querySelectorAll('.zoek-rij');
    if (e.key === 'ArrowDown') { e.preventDefault(); markeer(gekozen + 1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); markeer(gekozen - 1); }
    else if (e.key === 'Enter' && rijen.length) { e.preventDefault(); rijen[Math.max(0, gekozen)].click(); }
    else if (e.key === 'Escape') { dicht(); }
  });

  // "/" opent het zoekveld, maar niet tijdens het typen in een formulier
  document.addEventListener('keydown', function (e) {
    var inVeld = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName);
    if (e.key === '/' && !inVeld) { e.preventDefault(); open(); }
    if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) { e.preventDefault(); open(); }
  });
})();
</script>
"""


def pas_aan(tekst: str):
    if "zoek-overlay" in tekst:
        return tekst, "al aanwezig"
    veranderingen = []

    # CSS
    m = re.search(r"\n  </style>", tekst)
    if not m:
        return tekst, "GEEN </style>"
    tekst = tekst[:m.start()] + "\n" + CSS + tekst[m.start():]
    veranderingen.append("css")

    # Knop vóór .nav-socials
    voor = tekst
    tekst = re.sub(r'(\n\s*)(<div class="nav-socials">)', "\n" + KNOP + r"\1\2", tekst, count=1)
    if tekst != voor:
        veranderingen.append("knop")

    # Overlay + JS vóór </body>
    tekst = tekst.replace("</body>", OVERLAY + "</body>", 1)
    veranderingen.append("overlay")

    return tekst, ", ".join(veranderingen)


def main():
    for naam in BESTANDEN:
        pad = WORTEL / naam
        if not pad.exists():
            continue
        t = pad.read_text(encoding="utf-8")
        nieuw, verslag = pas_aan(t)
        if nieuw != t:
            pad.write_text(nieuw, encoding="utf-8")
        print(f"  {naam:<44} {verslag}")


if __name__ == "__main__":
    main()
