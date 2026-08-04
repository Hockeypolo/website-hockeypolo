#!/usr/bin/env python3
"""
Genereert producten-data.js uit de gekopieerde fotoboom + scripts/productteksten.py

Draai dit ná scripts/kopieer-productfotos.py.

    python3 scripts/genereer-productdata.py

De uitvoer (producten-data.js) wordt gecommit; de site heeft geen build-stap.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from productteksten import PRODUCTEN, CATEGORIE_LABELS  # noqa: E402

try:
    from PIL import Image
except ImportError:
    sys.exit("FOUT: Pillow ontbreekt.  pip3 install Pillow")

WORTEL = Path(__file__).resolve().parent.parent
FOTOS = WORTEL / "productfotos"
UITVOER = WORTEL / "producten-data.js"

# ── Kleurnamen ───────────────────────────────────────────────────────────
# De fotomappen gebruiken Nederlands en Engels door elkaar. Deze tabel maakt
# er één Nederlandse weergavenaam van. Handmatig en controleerbaar.
KLEURNAMEN = {
    # Engels -> Nederlands
    "black": "Zwart", "blue": "Blauw", "white": "Wit", "navy": "Marineblauw",
    "frenchnavy": "Marineblauw", "darkblue": "Donkerblauw", "lightblue": "Lichtblauw",
    "cobaltblue": "Kobaltblauw", "grayblue": "Grijsblauw", "mistyblue": "Mistblauw",
    "darkgreen": "Donkergroen", "forestgreen": "Bosgroen", "olivegreen": "Olijfgroen",
    "olive": "Olijfgroen", "morningmistgreen": "Zachtgroen", "lightgray": "Lichtgrijs",
    "graphiteblack": "Grafietzwart", "darkshadow": "Antraciet",
    "midnightcamo": "Camouflage donker", "peachpink": "Perzikroze",
    "orange": "Oranje", "cherry": "Kersrood", "turquoise": "Turquoise", "mint": "Mint",
    # Nederlands
    "antraciet": "Antraciet", "azuurblauw": "Azuurblauw", "blauw": "Blauw",
    "bordeaux": "Bordeauxrood", "bordeauxrood": "Bordeauxrood", "bruin": "Bruin",
    "donkerblauw": "Donkerblauw", "donkergrijs": "Donkergrijs", "donkergroen": "Donkergroen",
    "donkerrood": "Donkerrood", "felrood": "Felrood", "felroze": "Felroze",
    "flessengroen": "Flessengroen", "geel": "Geel", "grijs": "Grijs",
    "grijsmelange": "Grijs melange", "groen": "Groen", "hemelsblauw": "Hemelsblauw",
    "houtskoolgrijs": "Houtskoolgrijs", "indigoblauw": "Indigoblauw",
    "kakigroen": "Kakigroen", "khaki": "Khaki", "klassiekrood": "Klassiekrood",
    "koningsblauw": "Koningsblauw", "lavendelblauw": "Lavendelblauw",
    "lichtgrijs": "Lichtgrijs", "lichtroze": "Lichtroze", "limegroen": "Limegroen",
    "marineblauw": "Marineblauw", "middengrijs": "Middengrijs", "mokkabruin": "Mokkabruin",
    "naturel": "Naturel", "oker": "Oker", "olijfgroen": "Olijfgroen", "oranje": "Oranje",
    "paars": "Paars", "petrolgroen": "Petrolgroen", "poederroze": "Poederroze",
    "rood": "Rood", "roze": "Roze", "wit": "Wit", "zand": "Zand", "zwart": "Zwart",
}

# Prefixen in mapnamen die geen kleur aanduiden maar een modelvariant
LOSSE_PREFIXEN = ("longsleeve_", "ls_", "dames_")

onbekende_kleuren = Counter()


def kleurnaam(slug: str) -> str:
    """`ls_marineblauw` -> 'Marineblauw', `wassing_zwart` -> 'Zwart (washed)'."""
    s = slug

    for pre in LOSSE_PREFIXEN:
        if s.startswith(pre):
            s = s[len(pre):]

    achtervoegsel = ""

    # gewassen uitvoering: buckethat_wassing_khaki
    if s.startswith("wassing_"):
        s = s[len("wassing_"):]
        achtervoegsel = " (washed)"

    # badslipper_donkerblauw_zool_rode_band -> Donkerblauw / rode zool
    m = re.match(r"^(.*?)_zool_(.*?)_band$", s)
    if m:
        basis, zool = m.group(1), m.group(2).replace("_", " ")
        return f"{_enkel(basis)} / {zool} zool"

    # lichtgrijs_melange
    if s.endswith("_melange"):
        return _enkel(s[: -len("_melange")]) + " melange" + achtervoegsel

    # genummerde variant: blauw_2
    m = re.match(r"^(.*?)_(\d+)$", s)
    if m:
        return f"{_enkel(m.group(1))} {m.group(2)}{achtervoegsel}"

    # tweekleurig: navy_wit, zwart_zwart, grijsmelange_zwart
    if "_" in s:
        delen = s.split("_")
        if all(d in KLEURNAMEN for d in delen):
            if len(set(delen)) == 1:
                return _enkel(delen[0]) + achtervoegsel
            return " / ".join(_enkel(d) for d in delen) + achtervoegsel

    return _enkel(s) + achtervoegsel


def _enkel(s: str) -> str:
    if s in KLEURNAMEN:
        return KLEURNAMEN[s]
    onbekende_kleuren[s] += 1
    return s.replace("_", " ").capitalize()


# ── Hexkleur afleiden ────────────────────────────────────────────────────
def hex_uit_foto(pad: Path) -> str:
    """
    Mediane kleur van het product, met de (bijna-witte) studioachtergrond eruit.

    Mediaan i.p.v. gemiddelde omdat die niet vervuild raakt door logo's,
    schaduwen en highlights.
    """
    with Image.open(pad) as im:
        im = im.convert("RGB").resize((64, 64), Image.Resampling.BILINEAR)
        # middelste 60% — daar zit het product, niet de rand van de studio
        im = im.crop((13, 13, 51, 51))
        pixels = list(im.getdata())

    # achtergrond (bijna wit) en harde schaduw (bijna zwart) negeren
    kern = [p for p in pixels if not (p[0] > 235 and p[1] > 235 and p[2] > 235)]
    if len(kern) < 40:          # bijna alles wit -> het product ís wit
        kern = pixels

    kern.sort(key=lambda p: p[0] * 299 + p[1] * 587 + p[2] * 114)  # op helderheid
    r, g, b = kern[len(kern) // 2]
    return f"#{r:02x}{g:02x}{b:02x}"


# ── Fotoboom uitlezen ────────────────────────────────────────────────────
def lees_kleuren(product_slug_map: Path):
    kleuren = []
    for kleurmap in sorted(p for p in product_slug_map.iterdir() if p.is_dir()):
        bestanden = [f.name for f in kleurmap.glob("*.webp")]
        if not bestanden:
            continue

        # basisnamen + welke maten beschikbaar zijn
        basissen = {}
        for naam in bestanden:
            m = re.match(r"^(.*)-(\d+)\.webp$", naam)
            if m:
                basissen.setdefault(m.group(1), set()).add(int(m.group(2)))

        product_fotos = sorted(b for b in basissen if not b.startswith("model_"))
        model_fotos = sorted(b for b in basissen if b.startswith("model_"))
        groot = sorted(b for b, maten in basissen.items() if 1200 in maten)

        # hex uit de hoofdfoto (1_*), anders de eerste beschikbare
        hoofd = next((b for b in product_fotos if b.startswith("1_")),
                     product_fotos[0] if product_fotos else None)
        if hoofd is None:
            continue
        hexkleur = hex_uit_foto(kleurmap / f"{hoofd}-600.webp")

        kleuren.append({
            "slug": kleurmap.name,
            "naam": kleurnaam(kleurmap.name),
            "hex": hexkleur,
            "fotos": product_fotos,
            "modelfotos": model_fotos,
            "groot": groot,
        })
    return kleuren


def main():
    if not FOTOS.is_dir():
        sys.exit(f"FOUT: {FOTOS} bestaat niet. Draai eerst kopieer-productfotos.py")

    uitvoer = []
    for p in PRODUCTEN:
        map_ = FOTOS / p["fotomap"]
        if not map_.is_dir():
            print(f"  ! fotomap ontbreekt, overgeslagen: {p['fotomap']}")
            continue
        kleuren = lees_kleuren(map_)
        if not kleuren:
            print(f"  ! geen kleuren gevonden: {p['fotomap']}")
            continue
        uitvoer.append({
            "slug": p["slug"],
            "naam": p["naam"],
            "fotomap": p["fotomap"],
            "categorie": p["categorie"],
            "minQty": p["minQty"],
            "omschrijving": p["desc"],
            "kenmerken": p["specs"],
            "kleuren": kleuren,
        })
        print(f"  {p['naam']:<26} {len(kleuren):>2} kleuren, "
              f"{sum(len(k['fotos']) + len(k['modelfotos']) for k in kleuren):>3} foto's")

    js = (
        "/* AUTOMATISCH GEGENEREERD — niet met de hand aanpassen.\n"
        "   Bron: scripts/genereer-productdata.py + scripts/productteksten.py\n"
        "   Opnieuw genereren:  python3 scripts/genereer-productdata.py           */\n"
        "window.HP_CATEGORIEEN = " + json.dumps(CATEGORIE_LABELS, ensure_ascii=False) + ";\n"
        "window.HP_PRODUCTEN = " + json.dumps(uitvoer, ensure_ascii=False, indent=1) + ";\n"
        "/* Pad naar een foto. maat: 300 | 600 | 1200 (1200 alleen voor 'groot') */\n"
        "window.hpFoto = function (fotomap, kleurSlug, basis, maat) {\n"
        "  return '/productfotos/' + fotomap + '/' + kleurSlug + '/' + basis + '-' + maat + '.webp';\n"
        "};\n"
    )
    UITVOER.write_text(js, encoding="utf-8")

    tot_k = sum(len(p["kleuren"]) for p in uitvoer)
    tot_f = sum(len(k["fotos"]) + len(k["modelfotos"]) for p in uitvoer for k in p["kleuren"])
    print(f"\n{UITVOER.name}: {len(uitvoer)} producten, {tot_k} kleuren, {tot_f} foto's "
          f"({UITVOER.stat().st_size / 1024:.0f} kB)")

    if onbekende_kleuren:
        print("\nLET OP — kleurnamen zonder vertaling (vul KLEURNAMEN aan):")
        for naam, n in onbekende_kleuren.most_common():
            print(f"  {naam}  ({n}x)")


if __name__ == "__main__":
    main()
