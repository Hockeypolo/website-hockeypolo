#!/usr/bin/env python3
"""
Werkt vercel.json (rewrites + cache-headers) en sitemap.xml bij.

Rewrites blijven expliciet per product: een wildcard /producten/:slug zou
elke typfout naar een niet-bestaand .html-bestand sturen en Vercels kale
404 tonen in plaats van door te vallen naar de SPA-catch-all.

    python3 scripts/genereer-routes.py
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from productteksten import VERBORGEN_SLUGS  # noqa: E402

WORTEL = Path(__file__).resolve().parent.parent
VERCEL = WORTEL / "vercel.json"
SITEMAP = WORTEL / "sitemap.xml"
DATA = WORTEL / "producten-data.js"


def slugs():
    js = DATA.read_text(encoding="utf-8")
    prod = json.loads(re.search(r"window\.HP_PRODUCTEN = (\[.*?\]);\n", js, re.S).group(1))
    return [p["slug"] for p in prod]


def werk_vercel_bij(alle):
    cfg = json.loads(VERCEL.read_text(encoding="utf-8"))

    # Alle bestaande product-rewrites eruit, de rest (sitemap, robots, catch-all) behouden
    overig = [r for r in cfg["rewrites"] if not r["source"].startswith("/producten/")]
    catchall = [r for r in overig if r["source"] == "/(.*)"]
    overig = [r for r in overig if r["source"] != "/(.*)"]

    nieuw = [{"source": f"/producten/{s}", "destination": f"/producten-{s}.html"} for s in alle]
    cfg["rewrites"] = overig + nieuw + catchall

    # Cache-headers: fotopaden zijn inhouds-stabiel (nieuwe kleur = nieuw pad),
    # de datalaag moet juist altijd vers zijn.
    cfg["headers"] = [
        {"source": "/productfotos/(.*)",
         "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
        {"source": "/producten-data.js",
         "headers": [{"key": "Cache-Control", "value": "public, max-age=0, must-revalidate"}]},
    ]

    VERCEL.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(nieuw)


def werk_sitemap_bij(alle):
    tekst = SITEMAP.read_text(encoding="utf-8")
    vandaag = date.today().isoformat()

    # Bestaande product-entries verwijderen, daarna opnieuw opbouwen
    tekst = re.sub(r"\s*<url>\s*<loc>https://hockeypolo\.com/producten/[^<]*</loc>.*?</url>",
                   "", tekst, flags=re.S)

    blok = "".join(
        f"\n  <url>\n    <loc>https://hockeypolo.com/producten/{s}</loc>\n"
        f"    <lastmod>{vandaag}</lastmod>\n"
        f"    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>"
        for s in alle
    )
    tekst = tekst.replace("</urlset>", blok + "\n</urlset>")
    SITEMAP.write_text(tekst, encoding="utf-8")
    return len(alle)


def main():
    zichtbaar = slugs()
    # Verborgen producten houden hun route en sitemap-entry: hun pagina's
    # blijven live, ze staan alleen niet meer in het overzicht.
    alle = zichtbaar + VERBORGEN_SLUGS

    n_rw = werk_vercel_bij(alle)
    n_sm = werk_sitemap_bij(alle)
    print(f"  vercel.json : {n_rw} product-rewrites ({len(zichtbaar)} zichtbaar + {len(VERBORGEN_SLUGS)} verborgen)")
    print(f"                + cache-headers voor /productfotos en producten-data.js")
    print(f"  sitemap.xml : {n_sm} product-URL's")


if __name__ == "__main__":
    main()
