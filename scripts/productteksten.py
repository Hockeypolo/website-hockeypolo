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


# ── "Over {product}"-teksten voor de detailpagina's ──────────────────
# De 9 producten die al een pagina hadden houden hun bestaande tekst;
# de 18 nieuwe zijn geschreven door Claude en moeten gecontroleerd worden.
OVER = {
    't-shirts': (
        'Over t-shirts',
        [
            'T-shirts zijn het meest veelzijdige product in ons assortiment: geschikt voor sportverenigingen, studentenverenigingen, bedrijfsuitjes en evenementen. Je kiest zelf de kleur, het materiaal en de manier van personaliseren — van een klein logo op de borst tot een groot ontwerp over de hele rug.',
            'We bedrukken met zeefdruk of DTG (direct-to-garment) en borduren waar dat een steviger of premium resultaat geeft. Voor kleine oplages is DTG vaak voordeliger, bij grotere aantallen is zeefdruk vaak de scherpste keuze — we adviseren je hier kosteloos in.',
        ]),
    'longsleeve-t-shirts': (
        'Over longsleeve T-shirts',
        [
            'Longsleeve T-shirts zijn dezelfde kwaliteit als onze reguliere shirts, maar met lange mouwen. Daardoor zijn ze het hele jaar door draagbaar en populair bij verenigingen die één shirt voor meerdere seizoenen willen.',
            'De mouw biedt extra bedrukbaar oppervlak: veel klanten zetten het logo op de borst en een naam, jaartal of tekst op de mouw. Wij adviseren je graag over de combinatie.',
        ]),
    'oversized-t-shirts': (
        'Over oversized T-shirts',
        [
            'Oversized T-shirts hebben een ruimere snit en een laag vallende schoudernaad. Die vorm sluit aan bij hoe merchandise nu gedragen wordt en is vooral gewild bij studentenverenigingen en introductiecommissies.',
            'Door het zwaardere katoen en het grote bedrukbare vlak komen full-front en full-back ontwerpen goed tot hun recht. Voor grote prints is dit het shirt dat we het vaakst adviseren.',
        ]),
    'polos': (
        "Over polo's",
        [
            "Onze polo's zijn gemaakt van piqué katoen en zijn een vaste keuze voor sportclubs, studentenverenigingen en bedrijven die representatief voor de dag willen. Effen uitvoeringen ogen strak en zakelijk, een contrasterende bies geeft net dat sportieve accent.",
            "Logo's borduren we standaard op de borst; grotere ontwerpen bedrukken we. De pasvorm is unisex en beschikbaar in de meeste maten, zodat je hele team of vereniging in dezelfde stijl gekleed gaat.",
        ]),
    'longsleeve-polos': (
        "Over longsleeve polo's",
        [
            'De longsleeve polo combineert de nette uitstraling van een polo met de warmte van lange mouwen. Een logische keuze voor bedrijven en verenigingen die er ook in het najaar verzorgd uit willen zien.',
            'Het logo borduren we standaard op de borst; op de mouw is eveneens branding mogelijk. De pasvorm is unisex en beschikbaar in de gangbare maten.',
        ]),
    'hoodies': (
        'Over hoodies',
        [
            'Hoodies zijn dé klassieker voor clubkleding en dispuutsartikelen: warm, comfortabel en herkenbaar. Wij werken met stevige fleece of het iets luxere french terry, beide voorzien van kangoeroezak en verstelbare capuchon.',
            'Bij grotere aantallen is zeefdruk het meest kosteneffectief; voor een premium uitstraling borduren we het logo op de borst of mouw. Populair bij lustrums, jaarclubs en teamuitjes waar je elkaar op straat wilt herkennen.',
        ]),
    'sweaters': (
        'Over sweaters',
        [
            'Sweaters zijn het rustige alternatief voor de hoodie: dezelfde warme french terry, maar zonder capuchon. Veel verenigingen kiezen ze als basisstuk waarvan jaarlijks nieuwe lichtingen besteld worden.',
            'Geribde boorden aan hals, mouw en zoom houden het model in vorm. Borduurwerk op de borst geeft een premium uitstraling, zeefdruk is voordeliger bij hogere aantallen.',
        ]),
    'quarter-zip-sweaters': (
        'Over quarter-zip sweaters',
        [
            'De quarter-zip is de sweater die net iets formeler oogt dan een hoodie, zonder in te leveren op comfort. De rits bij de kraag geeft een strakke afwerking die goed past bij bedrijfskleding, dispuutsuitjes en teamwear buiten het veld.',
            'We borduren het logo doorgaans op de borst voor een premium finish, maar bedrukken kan ook. Verkrijgbaar in meerdere kleuren zodat de sweater aansluit bij je bestaande huisstijl of clubkleuren.',
        ]),
    'sportshirts': (
        'Over sportshirts',
        [
            'Functionele sportshirts in ademend polyester, ontworpen om te presteren tijdens hockey, voetbal en andere sporten. Sublimatie maakt een volledig bedrukt, naadloos ontwerp mogelijk — inclusief kleurverloop en scherpe teamkleuren-combinaties.',
            'Wil je zelf spelen met kleuren en indeling? Gebruik onze online ontwerptool en zie direct hoe jouw teamshirt eruitziet, voordat je een aanvraag indient.',
        ]),
    'sport-tanktops': (
        'Over sporttanktops',
        [
            'Mouwloze sportshirts in ademend polyester, gemaakt voor intensieve inspanning. Veel gebruikt bij roeien, atletiek en zaalsporten, waar bewegingsvrijheid in de schouders telt.',
            'Sublimatie maakt een volledig doorlopend ontwerp mogelijk, inclusief clubkleuren en rugnummers. Ook geschikt als zomerartikel bij verenigingsevenementen.',
        ]),
    'sportbroeken': (
        'Over sportbroeken',
        [
            'Lichte sportbroeken met elastische taille en koordje, in hetzelfde ademende polyester als onze sportshirts. Samen vormen ze een compleet tenue in jouw clubkleuren.',
            'Het logo drukken we op de pijp of bij de taille. Bij teamtenues stemmen we de kleuren van shirt en broek exact op elkaar af.',
        ]),
    'sportbroeken-dames': (
        'Over sportbroeken voor dames',
        [
            'Sportbroeken met een damespasvorm, verkrijgbaar in tweekleurige uitvoeringen. Ze sluiten aan op onze sportshirts, zodat een gemengd team er als één geheel uitziet.',
            'De tweekleurige uitvoering leent zich goed voor clubkleuren: de hoofdkleur voor de broek, de tweede kleur als accent. Logodruk is op meerdere posities mogelijk.',
        ]),
    'zwembroeken': (
        'Over zwembroeken',
        [
            'Bedrukte zwembroeken zijn een vaste waarde bij roeiverenigingen en watersportclubs. Sneldrogend polyester, een sublimatiemogelijkheid voor een volledig bedrukt ontwerp, en een bedrukt koordje als extra detail.',
            'Beschikbaar van maat S tot en met XXL, zodat een compleet team of vereniging in dezelfde uitstraling het water in kan.',
        ]),
    'bomberjacks': (
        'Over bomberjacks',
        [
            'Bomberjacks zijn een vast onderdeel van lustrum- en dispuutscollecties. De stevige buitenstof en geribde boorden geven het model zijn herkenbare vorm, en de jas gaat jaren mee.',
            'De rug biedt ruimte voor een groot geborduurd of gedrukt ontwerp; op de borst komt meestal het logo of een naam. Dit is bij uitstek het artikel waar leden zuinig op zijn.',
        ]),
    'softshell-jassen': (
        'Over softshell jassen',
        [
            'Softshell jassen zijn winddicht en waterafstotend, met een zachte fleecevoering aan de binnenzijde. Daarmee zijn ze geschikt voor iedereen die veel buiten staat, van bouwplaats tot sportveld.',
            'Als bedrijfskleding zijn ze een veilige keuze: netjes genoeg voor klantcontact, praktisch genoeg voor dagelijks gebruik. Het logo borduren we standaard op de borst.',
        ]),
    'windjacks': (
        'Over windjacks',
        [
            'Lichte windjacks die compact op te vouwen zijn en nauwelijks ruimte innemen. Ideaal voor evenementen, sportdagen en als weerbestendig relatiegeschenk.',
            'Ondanks het lage gewicht is de stof winddicht en waterafstotend. Zeefdruk of borduurwerk is op borst, rug en mouw mogelijk.',
        ]),
    'bucket-hats': (
        'Over bucket hats',
        [
            'Bucket hats met een brede rand, geborduurd met jouw logo of tekst. Ze zijn de afgelopen jaren uitgegroeid tot een vast onderdeel van introductieweken en festivalmerchandise.',
            'Het katoenen twill houdt zijn vorm en is goed te borduren. One size fits most, waardoor je bij het bestellen geen maatverdeling hoeft uit te vragen.',
        ]),
    'bucket-hats-washed': (
        'Over washed bucket hats',
        [
            'Dezelfde bucket hat, maar met een gewassen afwerking: zachtere stof en een licht vervaagde kleur. Het resultaat oogt gedragen en minder uitgesproken dan de reguliere uitvoering.',
            'De vintage-uitstraling past goed bij collecties waarin ook oversized shirts en sweaters zitten. Borduurwerk komt op de gewassen stof mooi tot zijn recht.',
        ]),
    'caps': (
        'Over caps',
        [
            'Caps met een gebogen klep en een verstelbare sluiting achter. Een klassiek clubartikel dat het hele jaar door gedragen wordt en zich uitstekend leent voor borduurwerk.',
            'Door de verstelbare sluiting past één maat vrijwel iedereen. Het logo borduren we op het voorpand; op de zijkant of achterzijde is aanvullende branding mogelijk.',
        ]),
    'sjaals': (
        'Over sjaals',
        [
            'Een supporterssjaal in de eigen clubkleuren is een van de meest gevraagde artikelen bij sportclubs en studentenverenigingen. We weven of breien op maat, inclusief franjes als je daarvoor kiest, en verwerken logo en tekst volledig naar wens.',
            'Sjaals worden vaak besteld rond een lustrum of jubileum — hou rekening met een iets langere doorlooptijd vanwege de weeftechniek, en neem op tijd contact op als je een vaste datum hebt.',
        ]),
    'tote-bags': (
        'Over tote bags',
        [
            'Katoenen schoudertassen met lange hengsels: goedkoop in aanschaf, maar jarenlang zichtbaar. Als merchandise leveren ze per euro waarschijnlijk de meeste exposure van ons hele assortiment.',
            'Het canvas is stevig genoeg voor dagelijks gebruik. Zeefdruk in meerdere kleuren is mogelijk, en juist bij hoge aantallen zakt de prijs per stuk snel.',
        ]),
    'badslippers': (
        'Over badslippers',
        [
            'Badslippers met een bedrukte band, verkrijgbaar met een contrasterende zool. Veelgevraagd bij roeiverenigingen, zwemclubs en sportweekenden.',
            'De zool is van zachte EVA en licht van gewicht. Door band- en zoolkleur te combineren maak je de slipper helemaal in de clubkleuren.',
        ]),
    'badjassen': (
        'Over badjassen',
        [
            'Zachte badjassen in badstof, geborduurd met een naam of logo. Bij roeiverenigingen en zwemclubs zijn ze een vast artikel, en als lustrumcadeau worden ze zelden weggegeven.',
            'Wij borduren standaard op de borst; een naam op de rug is een veelgevraagde toevoeging. De jassen zijn er in de gangbare maten met ceintuur en zijzakken.',
        ]),
    'paraplus': (
        "Over paraplu's",
        [
            "Stijlvolle vouwparaplu's met bedrukte panelen in jouw clubkleur of logo, ideaal als relatiegeschenk of promotieartikel bij evenementen. Het automatische open/dicht-mechanisme en het windproof frame maken hem praktisch in gebruik.",
            'Een reliëflogo is mogelijk voor een subtiele, premium afwerking. Kies zelf hoeveel panelen bedrukt worden — van een enkel accent tot een volledig doorlopend ontwerp.',
        ]),
    'thermosflessen': (
        'Over thermosflessen',
        [
            'Dubbelwandige thermosflessen van roestvrij staal die warme en koude dranken urenlang op temperatuur houden. Een relatiegeschenk dat dagelijks gebruikt wordt.',
            'Lasergravure geeft een strak, blijvend resultaat in het staal; rondom bedrukken kan ook. Beide technieken zijn bestand tegen langdurig gebruik.',
        ]),
    'waterflessen': (
        'Over waterflessen',
        [
            'Herbruikbare waterflessen met logo, in meerdere kleuren. Een duurzaam alternatief voor wegwerpflesjes dat bovendien lang zichtbaar blijft bij de ontvanger.',
            'De flessen zijn BPA-vrij, lekvrij afgesloten en vaatwasserbestendig. Rondom bedrukken maakt een ontwerp over de volledige fles mogelijk.',
        ]),
    'vlaggen': (
        'Over vlaggen',
        [
            'Op maat gemaakte vlaggen voor verenigingen, evenementen en bedrijven — van beachflag tot gevelvlag of lustrumvlag. Volledige sublimatie maakt het mogelijk om je logo, wapen of clubkleuren over de hele vlag door te laten lopen.',
            'Afgewerkt met metalen ringen voor eenvoudige bevestiging. Vlaggen worden vaak in kleine oplage besteld — ook een enkel exemplaar voor een jubileum of opening is bij ons mogelijk.',
        ]),
}
