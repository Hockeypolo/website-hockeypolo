#!/usr/bin/env python3
"""
Voegt het menu-item "Voor wie" (Bedrijven / Studenten / Evenementen) toe aan
de navigatie van alle pagina's.

Desktop: één item met een uitklapmenu, zodat de navbar niet breder wordt dan
nodig. Mobiel: drie losse regels direct onder Home.

Idempotent: draait zonder gevolgen opnieuw.

    python3 scripts/voeg-doelgroepmenu-toe.py
"""

from pathlib import Path

WORTEL = Path(__file__).resolve().parent.parent
BESTANDEN = ["index.html", "start-project.html", "bedankt-deel-je-idee.html",
             "bedrijven.html", "studenten.html", "evenementen.html"] + \
            sorted(p.name for p in WORTEL.glob("producten-*.html"))

DOELGROEPEN = [("bedrijven", "Bedrijven", "Bedrijfskleding en merchandise"),
               ("studenten", "Studenten", "Disputen, lustrum en skireis"),
               ("evenementen", "Evenementen", "Sportevents, festivals, beurzen")]

MARKER_CSS = "/* ═══ DOELGROEPMENU"
MARKER_HTML = 'class="nav-voorwie"'
MARKER_MOB = "mobile-menu-doelgroep"
MARKER_JS = "// doelgroepmenu"

CSS = """
    /* ═══ DOELGROEPMENU ("Voor wie") ═══════════════════════════════ */
    .nav-voorwie { position: relative; }
    .nav-voorwie-knop {
      display: inline-flex; align-items: center; gap: 5px;
      background: none; border: 0; padding: 0; cursor: pointer;
      font-family: var(--font-head); font-size: 12px; font-weight: 500;
      letter-spacing: .08em; text-transform: uppercase; color: var(--black);
      transition: color .2s;
    }
    .nav-voorwie-knop svg { width: 10px; height: 10px; stroke: currentColor; fill: none; stroke-width: 2.4; transition: transform .2s; }
    .nav-voorwie-knop:hover, .nav-voorwie.open .nav-voorwie-knop { color: var(--green); }
    .nav-voorwie.open .nav-voorwie-knop svg { transform: rotate(180deg); }
    .nav-voorwie-menu {
      position: absolute; top: calc(100% + 18px); left: 50%; transform: translateX(-50%);
      min-width: 260px; background: #fff; border: 1px solid var(--gray-200);
      border-radius: 12px; box-shadow: 0 16px 40px rgba(0,0,0,.12);
      padding: 8px; display: none; z-index: 210;
    }
    .nav-voorwie-menu::before { content: ''; position: absolute; left: 0; right: 0; top: -18px; height: 18px; }
    .nav-voorwie.open .nav-voorwie-menu { display: block; }
    @media (hover: hover) { .nav-voorwie:hover .nav-voorwie-menu { display: block; } }
    .nav-voorwie-menu a {
      display: block; padding: 10px 12px; border-radius: 8px;
      text-transform: none; letter-spacing: 0; font-size: 14px; font-weight: 600;
    }
    .nav-voorwie-menu a span { display: block; font-family: var(--font-body, Inter, sans-serif); font-size: 12px; font-weight: 400; color: var(--gray-600, #555); margin-top: 2px; }
    .nav-voorwie-menu a:hover { background: var(--gray-100, #f4f4f4); color: var(--black); }
    .nav-voorwie-menu a:hover span { color: var(--gray-600, #555); }
    .nav-links:has(.nav-voorwie) { gap: 24px; }
    .mobile-menu-doelgroep { color: var(--green) !important; }
"""

CHEVRON = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4"/></svg>'

DESKTOP = (
    '<li class="nav-voorwie"><button type="button" class="nav-voorwie-knop" aria-expanded="false" '
    'aria-haspopup="true">Voor wie ' + CHEVRON + '</button><div class="nav-voorwie-menu">' +
    "".join(f'<a href="/{s}">Voor {n.lower()}<span>{u}</span></a>' for s, n, u in DOELGROEPEN) +
    '</div></li>'
)

JS = """
<script>
// doelgroepmenu: klik/touch en toetsenbord voor "Voor wie"
(function () {
  document.querySelectorAll('.nav-voorwie').forEach(function (li) {
    var knop = li.querySelector('.nav-voorwie-knop');
    knop.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = li.classList.toggle('open');
      knop.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function () { li.classList.remove('open'); knop.setAttribute('aria-expanded', 'false'); });
    li.addEventListener('keydown', function (e) { if (e.key === 'Escape') { li.classList.remove('open'); knop.focus(); } });
  });
})();
</script>
"""


def mobiel(spa):
    def item(s, n):
        if spa:
            return f'<a class="mobile-menu-item {MARKER_MOB}" href="/{s}">Voor {n.lower()}</a>'
        return f'<a class="mobile-menu-item {MARKER_MOB}" href="/{s}">Voor {n.lower()}</a>'
    return "\n  " + "\n  ".join(item(s, n) for s, n, _ in DOELGROEPEN)


def verwerk(pad):
    tekst = pad.read_text(encoding="utf-8")
    orig = tekst
    spa = pad.name == "index.html"

    if MARKER_CSS not in tekst:
        # Laatste <style>-blok in <head> (index.html heeft vooraan een tijdelijk "no-flash"-blok)
        i = tekst.rindex("</style>", 0, tekst.index("</head>"))
        tekst = tekst[:i] + CSS + "  " + tekst[i:]

    if MARKER_HTML not in tekst:
        home = ('<li><a onclick="showPage(\'home\')" id="nav-home">Home</a></li>' if spa
                else '<li><a href="/">Home</a></li>')
        if home not in tekst:
            raise SystemExit(f"{pad.name}: Home-link in de navbar niet gevonden")
        tekst = tekst.replace(home, home + "\n      " + DESKTOP, 1)

    if f'class="mobile-menu-item {MARKER_MOB}"' not in tekst:
        home = ('<a class="mobile-menu-item" onclick="showPage(\'home\');closeMobileMenu()">Home</a>' if spa
                else '<a class="mobile-menu-item" href="/">Home</a>')
        if home not in tekst:
            raise SystemExit(f"{pad.name}: Home-link in het mobiele menu niet gevonden")
        tekst = tekst.replace(home, home + mobiel(spa), 1)

    if MARKER_JS not in tekst:
        i = tekst.rindex("</body>")
        tekst = tekst[:i] + JS + tekst[i:]

    if tekst != orig:
        pad.write_text(tekst, encoding="utf-8")
        return True
    return False


def main():
    n = 0
    for naam in BESTANDEN:
        pad = WORTEL / naam
        if pad.exists() and verwerk(pad):
            n += 1
    print(f"Doelgroepmenu toegevoegd of al aanwezig; {n} bestand(en) gewijzigd.")


if __name__ == "__main__":
    main()
