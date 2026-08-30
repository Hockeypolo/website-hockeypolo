#!/usr/bin/env python3
"""
Bouwt het productoverzicht in index.html opnieuw op uit producten-data.js.

Vervangt alles tussen de markers CATALOGUS:START / CATALOGUS:EINDE binnen
<div class="product-groups">. Bij de eerste run worden die markers geplaatst.
Idempotent: elke volgende run vervangt alleen het blok ertussen.

    python3 scripts/genereer-overzicht.py
"""

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from productteksten import VERBORGEN_SLUGS, CATEGORIE_LABELS  # noqa: E402

WORTEL = Path(__file__).resolve().parent.parent
INDEX = WORTEL / "index.html"
DATA = WORTEL / "producten-data.js"

START = "    <!-- CATALOGUS:START — gegenereerd door scripts/genereer-overzicht.py -->"
EINDE = "    <!-- CATALOGUS:EINDE -->"

# Verborgen producten: naam voor de 'ook leverbaar'-regel
VERBORGEN_NAMEN = {
    "overhemden": "Overhemden", "sokken": "Sokken", "schorten": "Schorten",
    "handdoeken": "Handdoeken", "mutsen": "Mutsen",
}

MAX_STALEN = 6   # kleurstalen op de kaart; de rest als "+N"

# Hover-foto per product overschrijven. Standaard pakt de kaart de eerste
# modelfoto, maar bij kleine accessoires draagt het model het product zo klein
# (of buiten beeld) dat de hover niet laat zien waar je naar kijkt. Dan liever
# een tweede productfoto onder een andere hoek.
HOVER_OVERRIDE = {
    "caps": "3_driekwart",
}


def laad_producten():
    js = DATA.read_text(encoding="utf-8")
    m = re.search(r"window\.HP_PRODUCTEN = (\[.*?\]);\n", js, re.S)
    if not m:
        sys.exit("FOUT: kon HP_PRODUCTEN niet uit producten-data.js lezen")
    return json.loads(m.group(1))


def e(s):
    """HTML-escape; producten heten o.a. Polo's, dus dit is niet optioneel."""
    return html.escape(str(s), quote=True)


def hoofdfoto(p, k):
    """Basisnaam van de primaire foto (1_*), anders de eerste."""
    return next((f for f in k["fotos"] if f.startswith("1_")), k["fotos"][0])


def kaart(p):
    k = p["kleuren"][0]
    basis = hoofdfoto(p, k)
    pad = f"/productfotos/{p['fotomap']}/{k['slug']}/{basis}"

    # Hover-beeld: override waar ingesteld, anders de eerste modelfoto
    hover = ""
    hpad = None
    if p["slug"] in HOVER_OVERRIDE:
        shot = HOVER_OVERRIDE[p["slug"]]
        if shot in k["fotos"]:
            hpad = f"/productfotos/{p['fotomap']}/{k['slug']}/{shot}"
    else:
        model = next((mk for mk in p["kleuren"] if mk.get("modelfotos")), None)
        if model:
            hpad = f"/productfotos/{p['fotomap']}/{model['slug']}/{model['modelfotos'][0]}"
    if hpad:
        hover = (f'\n          <img src="{hpad}-600.webp" alt="" aria-hidden="true"'
                 f' loading="lazy" decoding="async" class="pc-hoverfoto" />')

    # Kleurstalen
    stalen = "".join(
        f'<span class="pc-staal" style="background:{kk["hex"]}" title="{e(kk["naam"])}"></span>'
        for kk in p["kleuren"][:MAX_STALEN]
    )
    rest = len(p["kleuren"]) - MAX_STALEN
    if rest > 0:
        stalen += f'<span class="pc-staal-meer">+{rest}</span>'

    n = len(p["kleuren"])
    kleurtekst = "1 kleur" if n == 1 else f"{n} kleuren"

    # Zoektermen voor de zoekfunctie (kleurnamen meegenomen)
    zoek = " ".join([p["naam"], CATEGORIE_LABELS[p["categorie"]]] +
                    [kk["naam"] for kk in p["kleuren"]]).lower()

    return f"""        <a href="/producten/{p['slug']}" class="product-card reveal" data-cat="{p['categorie']}" data-zoek="{e(zoek)}">
          <div class="product-card-img-wrap">
            <img src="{pad}-300.webp"
                 srcset="{pad}-300.webp 300w, {pad}-600.webp 600w"
                 sizes="(max-width:640px) 46vw, (max-width:1023px) 46vw, (max-width:1439px) 30vw, 22vw"
                 width="600" height="600" loading="lazy" decoding="async"
                 alt="{e(p['naam'])} — {e(k['naam'])}" />{hover}
            <span class="pc-kleurbadge">{kleurtekst}</span>
          <div class="imp-overlay"><div class="imp-overlay-title">{e(p['naam'])}</div><div class="imp-overlay-sub">Klik voor meer info</div></div>
          <div class="imp-expand"><svg viewBox="0 0 24 24"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg></div>
          </div>
          <div class="product-card-title">{e(p['naam'])}</div>
          <div class="product-card-body">
            <div class="product-card-minafname">Min. afname {p['minQty']} stuks</div>
            <div class="product-card-desc">{e(p['omschrijving'])}</div>
            <div class="pc-stalen" aria-hidden="true">{stalen}</div>
            <button class="btn-meer-info" tabindex="-1">Meer info <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 8h10M8 3l5 5-5 5"/></svg></button>
          </div>
        </a>"""


def bouw_blok(producten):
    per_cat = {}
    for p in producten:
        per_cat.setdefault(p["categorie"], []).append(p)

    # Filterbalk
    tellingen = " ".join(
        f'<button class="prod-filter" data-filter="{c}">{CATEGORIE_LABELS[c]} '
        f'<span>{len(per_cat.get(c, []))}</span></button>'
        for c in ("kleding", "accessoires", "promotie") if per_cat.get(c)
    )
    delen = [
        START,
        '    <div class="prod-filterbar" role="group" aria-label="Filter op categorie">',
        f'      <button class="prod-filter is-actief" data-filter="alles">Alles <span>{len(producten)}</span></button>',
        f'      {tellingen}',
        '    </div>',
    ]

    for cat in ("kleding", "accessoires", "promotie"):
        lijst = per_cat.get(cat, [])
        if not lijst:
            continue
        delen.append(f'    <h3 class="product-group-title" id="{cat}">{CATEGORIE_LABELS[cat]}</h3>')
        delen.append('    <div class="product-grid">')
        delen += [kaart(p) for p in lijst]
        delen.append('    </div>')

    # Producten zonder nieuwe fotografie: pagina's blijven live, dus wel linken
    overig = " &middot; ".join(
        f'<a href="/producten/{s}">{VERBORGEN_NAMEN[s]}</a>' for s in VERBORGEN_SLUGS
    )
    delen.append(f'    <p class="producten-overig">Ook leverbaar, op aanvraag: {overig}</p>')
    delen.append(EINDE)
    return "\n".join(delen)


def main():
    producten = laad_producten()
    blok = bouw_blok(producten)
    tekst = INDEX.read_text(encoding="utf-8")

    if START in tekst:
        nieuw = re.sub(re.escape(START) + r".*?" + re.escape(EINDE), blok, tekst, flags=re.S)
        wat = "blok vervangen"
    else:
        # eerste run: alles binnen <div class="product-groups"> … vervangen
        m = re.search(r'(<div class="product-groups">\n)(.*?)(\n    </div>\n  </div>\n\n  <div class="cta-section">)',
                      tekst, re.S)
        if not m:
            sys.exit("FOUT: kon het product-groups blok niet vinden in index.html")
        nieuw = tekst[:m.start(2)] + blok + tekst[m.end(2):]
        wat = "markers geplaatst + blok vervangen"

    if nieuw == tekst:
        print("  geen wijziging")
        return
    INDEX.write_text(nieuw, encoding="utf-8")

    per_cat = {}
    for p in producten:
        per_cat.setdefault(p["categorie"], []).append(p)
    print(f"  {wat}")
    for c in ("kleding", "accessoires", "promotie"):
        print(f"    {CATEGORIE_LABELS[c]:<14} {len(per_cat.get(c, []))} producten")
    print(f"    verborgen      {len(VERBORGEN_SLUGS)} (wel gelinkt, niet in het grid)")


if __name__ == "__main__":
    main()
