#!/usr/bin/env python3
"""
Voegt de zwarte USP-balk toe boven de navbar, op alle HTML-pagina's.

De navbar staat overal `position:fixed; top:0; height:72px`. De balk komt
daarboven te staan; de hoogte zit in één CSS-variabele (--usp-h) zodat
nav-offset en pagina-padding automatisch meebewegen.

Idempotent: draait de wijziging niet twee keer door.

    python3 scripts/voeg-uspbalk-toe.py
"""

import re
import sys
from pathlib import Path

WORTEL = Path(__file__).resolve().parent.parent

BESTANDEN = ["index.html", "start-project.html", "bedankt-deel-je-idee.html"] + \
            sorted(p.name for p in WORTEL.glob("producten-*.html"))

CSS = """
    /* ═══ USP-BALK (boven de navbar) ═══════════════════════════════ */
    :root { --usp-h: 38px; }
    /* Vangt in één klap alle ankersprongen op: #kleding, #faq-levering, enz. */
    html { scroll-padding-top: calc(72px + var(--usp-h) + 18px); }
    .usp-bar {
      position: fixed; top: 0; left: 0; right: 0;
      height: var(--usp-h); z-index: 201;
      background: #000;
      color: rgba(255,255,255,.72);
      display: flex; align-items: center; justify-content: center;
      font-family: var(--font-head); font-size: 11px; font-weight: 500;
      letter-spacing: .1em; text-transform: uppercase;
      border-bottom: 1px solid rgba(255,255,255,.08);
    }
    .usp-inner { display: flex; align-items: center; gap: 48px; }
    .usp-item { display: flex; align-items: center; gap: 8px; white-space: nowrap; }
    .usp-item::before {
      content: ''; width: 4px; height: 4px; border-radius: 50%;
      background: var(--green); flex-shrink: 0;
    }
    .usp-item em { font-style: normal; color: var(--green); }
    @media (max-width: 900px) {
      .usp-bar { font-size: 10px; letter-spacing: .06em; }
      .usp-inner { gap: 24px; }
      .usp-item:nth-child(3) { display: none; }
    }
    @media (max-width: 640px) {
      :root { --usp-h: 34px; }
      .usp-item:nth-child(2) { display: none; }
    }
"""

HTML = """<div class="usp-bar">
  <div class="usp-inner">
    <span class="usp-item">Gratis ontwerpvoorstel</span>
    <span class="usp-item">Digitale proef vooraf</span>
    <span class="usp-item">Al 20+ jaar &middot; <em>500+ projecten</em></span>
  </div>
</div>
"""


def pas_aan(tekst: str, bestand: str):
    if "usp-bar" in tekst:
        return tekst, "al aanwezig"

    veranderingen = []

    # 1. CSS invoegen vlak vóór het einde van de laatste <style> in de <head>
    m = list(re.finditer(r"\n  </style>", tekst))
    if not m:
        return tekst, "GEEN </style> gevonden"
    laatste = m[0]  # de eerste </style> zit in de head; daar hoort de balk
    tekst = tekst[:laatste.start()] + "\n" + CSS + tekst[laatste.start():]
    veranderingen.append("css")

    # 2. nav-regels: top:0 -> top:var(--usp-h).  Sommige bestanden hebben er twee.
    n_nav = 0
    def nav_offset(mo):
        nonlocal n_nav
        n_nav += 1
        return mo.group(0).replace("top: 0;", "top: var(--usp-h);", 1) \
                          .replace("top:0;", "top:var(--usp-h);", 1)

    tekst = re.sub(r"nav \{[^}]*?position:\s*fixed;[^}]*?\}", nav_offset, tekst, flags=re.S)
    veranderingen.append(f"nav×{n_nav}")

    # 3. .page padding-top 72 -> 72 + balk
    voor = tekst
    tekst = tekst.replace(".page { display: none; padding-top: 72px; }",
                          ".page { display: none; padding-top: calc(72px + var(--usp-h)); }")
    tekst = tekst.replace(".page { padding-top:72px; }",
                          ".page { padding-top:calc(72px + var(--usp-h)); }")
    if tekst != voor:
        veranderingen.append("page")

    # 4. mobiel menu zakt mee
    voor = tekst
    tekst = tekst.replace("      top: 72px; left: 0; right: 0;",
                          "      top: calc(72px + var(--usp-h)); left: 0; right: 0;")
    tekst = tekst.replace(".mobile-menu { display:none; position:fixed; top:72px;",
                          ".mobile-menu { display:none; position:fixed; top:calc(72px + var(--usp-h));")
    if tekst != voor:
        veranderingen.append("mobielmenu")

    # 5. ankers: scroll-margin moet de hogere kop compenseren
    voor = tekst
    tekst = tekst.replace("scroll-margin-top: 90px;", "scroll-margin-top: calc(90px + var(--usp-h));")
    tekst = tekst.replace('scroll-margin-top:90px"', 'scroll-margin-top:calc(90px + var(--usp-h))"')
    if tekst != voor:
        veranderingen.append("ankers")

    # 6. HTML direct na <body>
    m = re.search(r"<body>\n", tekst)
    if not m:
        return tekst, "GEEN <body> gevonden"
    tekst = tekst[:m.end()] + "\n" + HTML + tekst[m.end():]
    veranderingen.append("html")

    return tekst, ", ".join(veranderingen)


def main():
    for naam in BESTANDEN:
        pad = WORTEL / naam
        if not pad.exists():
            print(f"  ! ontbreekt: {naam}")
            continue
        tekst = pad.read_text(encoding="utf-8")
        nieuw, verslag = pas_aan(tekst, naam)
        if nieuw != tekst:
            pad.write_text(nieuw, encoding="utf-8")
        print(f"  {naam:<38} {verslag}")


if __name__ == "__main__":
    main()
