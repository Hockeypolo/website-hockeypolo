# -*- coding: utf-8 -*-
"""
Producttekst en -metadata voor de catalogus.

Dit bestand is bewust los van de generator gehouden zodat het makkelijk te
controleren en aan te passen is zonder in scriptlogica te hoeven duiken.

Per product:
  fotomap    -> mapnaam in hockeypolo_ai_fotografie/output_fotos
  slug       -> URL: /producten/{slug}  en bestand producten-{slug}.html
  naam       -> weergavenaam
  categorie  -> kleding | accessoires | promotie
  minQty     -> minimale afname in stuks
  desc       -> 1-2 zinnen, zelfde toon als de rest van de site
  specs      -> 3-4 korte kenmerken

De 9 producten die al op de site stonden houden hun bestaande tekst letterlijk.
De 18 nieuwe zijn door Claude geschreven en moeten inhoudelijk gecontroleerd
worden vóór de push naar main — vooral de minimale afnames.
"""

# Producten die WEL nieuwe fotografie hebben (27) — volgorde = volgorde op de site
PRODUCTEN = [
    # ── KLEDING ──────────────────────────────────────────────────────────
    {
        "fotomap": "t-shirts", "slug": "t-shirts", "naam": "T-shirts",
        "categorie": "kleding", "minQty": 15,
        "desc": "Hoogwaardige T-shirts volledig op maat bedrukt of geborduurd met jouw logo, tekst of ontwerp. Beschikbaar in tientallen kleuren en maten, geschikt voor elke gelegenheid.",
        "specs": ["Katoen of polyester blend", "Zeefdruk, DTG of borduurwerk",
                  "Alle kleuren en maten beschikbaar", "Geschikt voor kleine en grote aantallen"],
    },
    {
        "fotomap": "t-shirt-longsleeve", "slug": "longsleeve-t-shirts", "naam": "Longsleeve T-shirts",
        "categorie": "kleding", "minQty": 15,
        "desc": "T-shirts met lange mouwen, in hetzelfde katoen als onze reguliere shirts. Een logische keuze voor het tussenseizoen of als je meer bedrukbaar oppervlak wilt.",
        "specs": ["Katoen of polyester blend", "Zeefdruk, DTG of borduurwerk",
                  "Bedrukking ook op de mouw mogelijk", "Unisex pasvorm"],
    },
    {
        "fotomap": "t-shirt-oversized", "slug": "oversized-t-shirts", "naam": "Oversized T-shirts",
        "categorie": "kleding", "minQty": 15,
        "desc": "T-shirts met een ruimere, moderne snit en laag vallende schoudernaad. Populair bij studentenverenigingen en voor merchandise met een streetwear-uitstraling.",
        "specs": ["Zwaarder katoen, 180-220g", "Ruime snit, laag vallende schouder",
                  "Groot bedrukbaar vlak voor- en achterkant", "Unisex pasvorm"],
    },
    {
        "fotomap": "polo", "slug": "polos", "naam": "Polo's",
        "categorie": "kleding", "minQty": 15,
        "desc": "Klassieke polo's in piqué stof, beschikbaar in effen uitvoering of met contrasterende bies. Perfect voor sportclubs, bedrijven en studentenverenigingen.",
        "specs": ["100% katoen piqué", "Geborduurde of gedrukte branding",
                  "Effen of met streepdetail", "Unisex pasvorm beschikbaar"],
    },
    {
        "fotomap": "polo-longsleeve", "slug": "longsleeve-polos", "naam": "Longsleeve Polo's",
        "categorie": "kleding", "minQty": 15,
        "desc": "Polo's met lange mouwen in piqué stof. Netjes genoeg voor bedrijfskleding en warm genoeg voor buiten, met dezelfde borduurmogelijkheden als de korte variant.",
        "specs": ["100% katoen piqué", "Geborduurde branding op borst of mouw",
                  "Geknoopte placket", "Unisex pasvorm beschikbaar"],
    },
    {
        "fotomap": "hoodies", "slug": "hoodies", "naam": "Hoodies",
        "categorie": "kleding", "minQty": 10,
        "desc": "Warme hoodies in fleece of french terry, ideaal als clubkleding of dispuutsartikel. Voorzien van kangoeroezak en verstelbare capuchon.",
        "specs": ["280-320g fleece of french terry", "Zeefdruk of borduurwerk",
                  "Unisex snit", "Geschikt voor hoge aantallen"],
    },
    {
        "fotomap": "sweaters", "slug": "sweaters", "naam": "Sweaters",
        "categorie": "kleding", "minQty": 12,
        "desc": "Klassieke sweaters zonder capuchon, in stevig french terry. Een veelgevraagd basisstuk voor verenigingen die een rustiger alternatief voor de hoodie zoeken.",
        "specs": ["280-320g french terry", "Zeefdruk of borduurwerk",
                  "Geribde boorden aan hals, mouw en zoom", "Unisex snit"],
    },
    {
        "fotomap": "sweater-quarter-zip", "slug": "quarter-zip-sweaters", "naam": "Quarter-zip Sweaters",
        "categorie": "kleding", "minQty": 12,
        "desc": "Stijlvolle quarter-zip sweaters met ritssluiting bij de kraag. Populair als teamwear, dispuutsartikel en bedrijfskleding. Verkrijgbaar met geborduurde branding.",
        "specs": ["Fleece of french terry", "Rits bij kraag",
                  "Borduurwerk of print", "Meerdere kleuren beschikbaar"],
    },
    {
        "fotomap": "sportshirt", "slug": "sportshirts", "naam": "Sportshirts",
        "categorie": "kleding", "minQty": 15,
        "desc": "Functionele sportshirts in ademend materiaal, perfect voor hockey, voetbal en andere sporten. Verkrijgbaar in tweekleurig design met sublimatiemogelijkheden.",
        "specs": ["100% polyester, ademend", "Sublimatie of zeefdruk",
                  "Teamkleurenoptie", "Alle maten beschikbaar"],
    },
    {
        "fotomap": "tanktop-sport", "slug": "sport-tanktops", "naam": "Sport Tanktops",
        "categorie": "kleding", "minQty": 15,
        "desc": "Mouwloze sportshirts in ademend polyester. Veel gebruikt bij roeien, atletiek en zaalsporten, en als zomerartikel bij verenigingsevenementen.",
        "specs": ["100% polyester, sneldrogend", "Sublimatie of zeefdruk",
                  "Racerback of rechte snit", "Alle maten beschikbaar"],
    },
    {
        "fotomap": "shorts-sport", "slug": "sportbroeken", "naam": "Sportbroeken",
        "categorie": "kleding", "minQty": 15,
        "desc": "Lichte sportbroeken met elastische taille en koordje. Te combineren met onze sportshirts tot een compleet tenue in jouw clubkleuren.",
        "specs": ["100% polyester, sneldrogend", "Elastische taille met koord",
                  "Logodruk op pijp of taille", "Maat S t/m XXL"],
    },
    {
        "fotomap": "shorts-dames", "slug": "sportbroeken-dames", "naam": "Sportbroeken Dames",
        "categorie": "kleding", "minQty": 15,
        "desc": "Sportbroeken met een damespasvorm, verkrijgbaar in tweekleurige uitvoeringen. Sluit aan op onze sportshirts voor een doorlopende teamlijn.",
        "specs": ["100% polyester, sneldrogend", "Damespasvorm",
                  "Tweekleurige uitvoeringen", "Logodruk mogelijk"],
    },
    {
        "fotomap": "zwembroek-heren", "slug": "zwembroeken", "naam": "Zwembroeken",
        "categorie": "kleding", "minQty": 10,
        "desc": "Bedrukte zwembroeken voor roeiverenigingen, watersporten en evenementen. Voorzien van gekleurd koordje en logodruk op de zijkant.",
        "specs": ["100% polyester, sneldrogend", "Sublimatiemogelijkheid",
                  "Maat S t/m XXL", "Bedrukt koordje mogelijk"],
    },
    {
        "fotomap": "bomberjack", "slug": "bomberjacks", "naam": "Bomberjacks",
        "categorie": "kleding", "minQty": 10,
        "desc": "Bomberjacks met ritssluiting en geribde boorden. Een populair lustrum- en dispuutsartikel dat zich goed leent voor borduurwerk op rug en borst.",
        "specs": ["Waterafstotende buitenstof", "Gevoerd, met ritssluiting",
                  "Borduurwerk op borst of rug", "Unisex pasvorm"],
    },
    {
        "fotomap": "softshell-jas", "slug": "softshell-jassen", "naam": "Softshell Jassen",
        "categorie": "kleding", "minQty": 10,
        "desc": "Winddichte softshell jassen met fleecevoering. Veel gekozen als bedrijfskleding en voor verenigingen die het hele seizoen buiten staan.",
        "specs": ["Winddicht en waterafstotend", "Fleece binnenzijde",
                  "Geborduurd logo op borst", "Maat S t/m XXL"],
    },
    {
        "fotomap": "windjack", "slug": "windjacks", "naam": "Windjacks",
        "categorie": "kleding", "minQty": 10,
        "desc": "Lichte windjacks die klein op te vouwen zijn. Ideaal voor evenementen, sportdagen en als weerbestendig relatiegeschenk.",
        "specs": ["Lichtgewicht en winddicht", "Compact opvouwbaar",
                  "Zeefdruk of borduurwerk", "Unisex pasvorm"],
    },

    # ── ACCESSOIRES ──────────────────────────────────────────────────────
    {
        "fotomap": "buckethats", "slug": "bucket-hats", "naam": "Bucket Hats",
        "categorie": "accessoires", "minQty": 20,
        "desc": "Bucket hats met een brede rand, geborduurd met jouw logo of tekst. Een vast onderdeel van introductieweken en festivalmerchandise.",
        "specs": ["100% katoen twill", "Geborduurde branding",
                  "One size fits most", "Meerdere kleuren beschikbaar"],
    },
    {
        "fotomap": "buckethats-washed", "slug": "bucket-hats-washed", "naam": "Bucket Hats Washed",
        "categorie": "accessoires", "minQty": 20,
        "desc": "Bucket hats met een gewassen, licht vervaagde look. Zelfde model als de reguliere variant, maar met een zachtere stof en een gedragen uitstraling.",
        "specs": ["Gewassen katoen, zachte touch", "Vintage-uitstraling",
                  "Geborduurde branding", "One size fits most"],
    },
    {
        "fotomap": "denim-cap", "slug": "caps", "naam": "Caps",
        "categorie": "accessoires", "minQty": 20,
        "desc": "Caps met gebogen klep en verstelbare sluiting achter. Geborduurd met jouw logo, geschikt als clubartikel of relatiegeschenk.",
        "specs": ["Denim of katoen twill", "Verstelbare sluiting",
                  "Geborduurde branding op voorpand", "One size fits most"],
    },
    {
        "fotomap": "sjaals", "slug": "sjaals", "naam": "Sjaals",
        "categorie": "accessoires", "minQty": 20,
        "desc": "Op maat geweven of gebreide sjaals in jouw clubkleuren. Verkrijgbaar als supporterssjaal met franjes, volledig gepersonaliseerd met logo en tekst.",
        "specs": ["Geweven of gebreid", "Eigen kleur en logo", "Franjes naar keuze"],
    },
    {
        "fotomap": "tote-bag", "slug": "tote-bags", "naam": "Tote Bags",
        "categorie": "accessoires", "minQty": 20,
        "desc": "Katoenen schoudertassen met lange hengsels. Een praktisch en goedkoop merchandise-artikel dat lang meegaat en veel gebruikt wordt.",
        "specs": ["Stevig katoen canvas", "Lange schouderhengsels",
                  "Zeefdruk in meerdere kleuren", "Geschikt voor hoge aantallen"],
    },
    {
        "fotomap": "badslippers", "slug": "badslippers", "naam": "Badslippers",
        "categorie": "accessoires", "minQty": 20,
        "desc": "Badslippers met bedrukte band, verkrijgbaar met contrasterende zool. Veelgevraagd bij roeiverenigingen, zwemclubs en sportweekenden.",
        "specs": ["Zachte EVA-zool", "Bedrukte band met logo",
                  "Contrasterende zoolkleur mogelijk", "Maat 36 t/m 47"],
    },
    {
        "fotomap": "badjas", "slug": "badjassen", "naam": "Badjassen",
        "categorie": "accessoires", "minQty": 10,
        "desc": "Zachte badjassen in badstof, geborduurd met naam of logo. Populair bij roeiverenigingen, zwemclubs en als lustrumcadeau.",
        "specs": ["Badstof, 380-450g", "Geborduurde naam of logo",
                  "Met ceintuur en zijzakken", "Maat S t/m XXL"],
    },
    {
        "fotomap": "paraplu", "slug": "paraplus", "naam": "Paraplu's",
        "categorie": "accessoires", "minQty": 20,
        "desc": "Stijlvolle vouwparaplu's met bedrukte panelen in jouw clubkleur of logo. Ideaal als relatiegeschenk of evenementartikel.",
        "specs": ["Automatisch open/dicht", "Windproof frame",
                  "Panelen bedrukt naar keuze", "Geschikt voor reliëflogo"],
    },

    # ── PROMOTIE ─────────────────────────────────────────────────────────
    {
        "fotomap": "thermos", "slug": "thermosflessen", "naam": "Thermosflessen",
        "categorie": "promotie", "minQty": 20,
        "desc": "Dubbelwandige thermosflessen van roestvrij staal die dranken urenlang op temperatuur houden. Gegraveerd of bedrukt met jouw logo.",
        "specs": ["Roestvrij staal, dubbelwandig", "Houdt warm en koud",
                  "Lasergravure of rondom bedrukking", "500 ml"],
    },
    {
        "fotomap": "waterbottle", "slug": "waterflessen", "naam": "Waterflessen",
        "categorie": "promotie", "minQty": 20,
        "desc": "Herbruikbare waterflessen met logo, in meerdere kleuren. Een duurzaam relatiegeschenk dat dagelijks gebruikt wordt en dus lang zichtbaar blijft.",
        "specs": ["BPA-vrij", "Lekvrije dop",
                  "Rondom bedrukbaar", "Vaatwasserbestendig"],
    },
    {
        "fotomap": "vlag", "slug": "vlaggen", "naam": "Vlaggen",
        "categorie": "promotie", "minQty": 10,
        "desc": "Op maat gemaakte vlaggen voor verenigingen, evenementen en bedrijven. Volledig bedrukt met jouw logo, wapen of clubkleuren. Verkrijgbaar als beachflag, gevelvlag of lustrumvlag.",
        "specs": ["Polyester satijn of doek", "Volledige sublimatiemogelijkheid",
                  "Metalen ringen voor bevestiging"],
    },
]

# Producten zonder nieuwe fotografie. Hun pagina's blijven live (geen 404's,
# SEO blijft behouden) maar ze verschijnen niet in het overzicht of de zoekfunctie.
VERBORGEN_SLUGS = ["overhemden", "sokken", "schorten", "handdoeken", "mutsen"]

CATEGORIE_LABELS = {
    "kleding": "Kleding",
    "accessoires": "Accessoires",
    "promotie": "Promotie",
}
