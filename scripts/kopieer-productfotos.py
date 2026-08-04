#!/usr/bin/env python3
"""
Kopieert de productfoto's uit de Google Drive-fotoshoot naar de repo.

Scenario B (zie plan):
  - 300 px + 600 px  -> alle foto's
  - 1200 px          -> alleen de hoofdfoto (1_*) en de modelfoto's (model_*)
  - nooit 2400 px of de -1200.jpg fallbacks

Doelstructuur:
  productfotos/{product-slug}/{kleur-slug}/{basis}-{300|600|1200}.webp

Het script is idempotent: bestaande, even grote bestanden worden overgeslagen.
Google Drive levert bestanden traag aan (~1 s per bestand), daarom parallel.

Gebruik:
    python3 scripts/kopieer-productfotos.py            # kopieer
    python3 scripts/kopieer-productfotos.py --dry-run  # alleen tellen
"""

import argparse
import os
import re
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BRON = Path(
    "/Users/benjaminvansplunder/Library/CloudStorage/GoogleDrive-info@hockeypolo.com/"
    "Gedeelde drives/Hockeypolo/hockeypolo_ai_fotografie/output_fotos"
)
DOEL = Path(__file__).resolve().parent.parent / "productfotos"

# Maten die we meenemen per fototype
MATEN_ALLE = ("300", "600")
MATEN_GROOT = ("300", "600", "1200")

WERKERS = 16


def is_grote_foto(basis: str) -> bool:
    """Hoofdfoto's en modelfoto's worden groot getoond en krijgen ook 1200 px."""
    return basis.startswith("1_") or basis.startswith("model_")


def kleur_slug(mapnaam: str) -> str:
    """`tshirt_azuurblauw` -> `azuurblauw`; prefix vóór de eerste underscore eraf."""
    return mapnaam.split("_", 1)[1] if "_" in mapnaam else mapnaam


def verzamel_taken():
    """Loopt de bronboom af en levert (bronpad, doelpad)-paren op."""
    taken = []
    if not BRON.is_dir():
        sys.exit(f"FOUT: bronmap niet gevonden:\n  {BRON}")

    for productmap in sorted(p for p in BRON.iterdir() if p.is_dir()):
        product = productmap.name
        for kleurmap in sorted(k for k in productmap.iterdir() if k.is_dir()):
            webmap = kleurmap / "web"
            if not webmap.is_dir():
                print(f"  ! geen web/-map: {product}/{kleurmap.name}")
                continue

            kleur = kleur_slug(kleurmap.name)
            doelmap = DOEL / product / kleur

            # Basisnamen afleiden uit de originelen (fotosets verschillen per product)
            for origineel in sorted(kleurmap.glob("*.jpg")):
                basis = origineel.stem
                maten = MATEN_GROOT if is_grote_foto(basis) else MATEN_ALLE
                for maat in maten:
                    bron = webmap / f"{basis}-{maat}.webp"
                    if bron.exists():
                        taken.append((bron, doelmap / f"{basis}-{maat}.webp"))
    return taken


def kopieer(paar):
    bron, doel = paar
    try:
        # Idempotent: overslaan als het doel al bestaat met dezelfde grootte
        if doel.exists() and doel.stat().st_size == bron.stat().st_size:
            return ("overgeslagen", doel, None)
        doel.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(bron, doel)
        return ("gekopieerd", doel, None)
    except Exception as e:  # Drive kan tijdelijk weigeren
        return ("mislukt", doel, str(e))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="alleen tellen, niets kopiëren")
    args = ap.parse_args()

    print("Bronboom inlezen…")
    taken = verzamel_taken()
    totaal_bytes = sum(b.stat().st_size for b, _ in taken)
    print(f"  {len(taken)} bestanden, {totaal_bytes / 1048576:.0f} MB")

    if args.dry_run:
        return

    print(f"Kopiëren naar {DOEL} met {WERKERS} werkers…")
    tellers = {"gekopieerd": 0, "overgeslagen": 0, "mislukt": 0}
    fouten = []

    with ThreadPoolExecutor(max_workers=WERKERS) as pool:
        futures = [pool.submit(kopieer, t) for t in taken]
        for i, fut in enumerate(as_completed(futures), 1):
            status, doel, fout = fut.result()
            tellers[status] += 1
            if fout:
                fouten.append((doel, fout))
            if i % 250 == 0 or i == len(taken):
                print(f"  {i}/{len(taken)}  "
                      f"nieuw={tellers['gekopieerd']} "
                      f"over={tellers['overgeslagen']} "
                      f"mislukt={tellers['mislukt']}")

    print("\nKlaar:")
    for k, v in tellers.items():
        print(f"  {k:12} {v}")

    if fouten:
        print(f"\n{len(fouten)} mislukt — script opnieuw draaien om te herstellen:")
        for doel, fout in fouten[:10]:
            print(f"  {doel.name}: {fout}")
        sys.exit(1)


if __name__ == "__main__":
    main()
