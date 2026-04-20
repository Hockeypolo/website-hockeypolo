# Hockeypolo Website Project

## Project Overzicht

**Bedrijf**: Hockeypolo — maatwerk teamkleding voor hockeyverenigingen in Nederland  
**Taal**: Volledig Nederlands (interface, code, communicatie)  
**Deployment**: `git push` → GitHub → Vercel (auto-deploy binnen 30-60 sec)

Dit project bestaat uit **twee aparte onderdelen**:
1. **Hoofdwebsite** (`index.html`) — publieke marketingwebsite
2. **Sourcing Dashboard** (`hockeypolo-sourcing/`) — intern inkoop- en leveranciersbeheer

---

## Architectuur

```
Website Folder/
├── index.html                    # Volledige marketingwebsite (HTML/CSS/JS)
├── vercel.json                   # Vercel deployment config
├── *.jpg / *.jpeg                # Foto's van klantprojecten
└── hockeypolo-sourcing/          # Next.js sourcing dashboard
    ├── src/app/                  # Next.js App Router pagina's
    ├── src/components/           # React componenten (layout + ui)
    ├── src/lib/                  # Hulpfuncties, constanten, templates
    ├── prisma/                   # Schema en SQLite database (dev.db)
    └── package.json
```

---

## 1. Hoofdwebsite (index.html)

### Tech
- Pure HTML + CSS + JavaScript — geen framework, geen build-stap
- Dev-server: `npx serve` op poort **3001**
- Navigatie: JavaScript SPA via `showPage(naam)` (toont/verbergt secties)

### Paginavolgorde (bewust gekozen klantreis)
1. **Home** — Hero slideshow, bedrijfswaarden, productoverzicht, "Zo werkt het", gallery, reviews, Instagram feed, CTA
2. **Producten** — Filterbar + 4-koloms productgrid
3. **Impressies** — Masonry fotogallery (6 klantprojecten)
4. **Blog** — Artikelgrid met categorietags (Teamwear, Tips, Cases, Trends)
5. **Over Ons** — Bedrijfsinformatie + team
6. **F.A.Q.** — Accordion-stijl veelgestelde vragen
7. **Contact** — Contactformulier + bedrijfsgegevens

**Logica achter de volgorde**: Interesse wekken (Producten/Impressies) → Vertrouwen opbouwen (Blog) → Actie ondernemen (Contact)

### Stijlgids

**Kleuren**
| Rol | Waarde |
|-----|--------|
| Primair (groen) | `#00A652` |
| Tekst / neutraal | Zwart / wit |
| Achtergrond accenten | Lichtgrijs |

**Typografie**
| Element | Font | Gewicht | Grootte |
|---------|------|---------|---------|
| Koppen / titels | Space Grotesk | 700 | `clamp(32px, 3vw, 46px)` |
| Hero titel | Space Grotesk | 700 | `clamp(42px, 5vw, 72px)` |
| Navigatie | Inter | 400 | 12px, uppercase, `letter-spacing: .08em` |
| Body tekst | Inter | 400–600 | 1rem |

Beide fonts via Google Fonts geladen.

**Layout**
- Responsive breakpoint: `@media (max-width: 640px)`
- Fluid typography met `clamp()` voor koppen
- CSS Grid voor productgrid en secties
- Flexbox voor navigatie en knoppen
- Aspect-ratio constraints op afbeeldingen (bijv. `3/4` portret)

### Kritieke patronen

**Masonry gallery — gebruik CSS `columns`, NIET CSS Grid**
```css
.gallery { column-count: 3; }
```
CSS Grid creëert witte ruimte bij ongelijke hoogtes. Met `column-count` stroomt de browser items top-to-bottom per kolom en balanceert hoogtes automatisch.

**Afbeeldingen in gallery**: Base64 embedded in de HTML.

**Instagram feed**: LightWidget iframe embed, lichtgrijze achtergrond passend bij sitesstijl.

**Analytics**: Vercel Analytics `<script>` tag in `<head>`.

---

## 2. Sourcing Dashboard (hockeypolo-sourcing/)

### Tech — versies zijn kritiek
| Package | Versie | Reden |
|---------|--------|-------|
| Next.js | 14.2.x | Stabiel, App Router |
| Tailwind CSS | **v3** (niet v4) | v4 is incompatibel met Next.js 14 |
| Prisma | **v6** (niet v7) | v7 geeft problemen met Next.js 14 |
| shadcn/ui | v3-compatible | Gebouwd op Radix UI |
| TypeScript | 5 | |

Dev-server: `npm run dev` op poort **3002** (vanuit `hockeypolo-sourcing/`)

### Stijlgids Dashboard

**Kleuren (HSL CSS-variabelen)**
| Variabele | Waarde | Gebruik |
|-----------|--------|---------|
| `--background` | `216 28% 6%` (#0b0f14) | Paginaachtergrond |
| `--card` | `220 26% 12%` (#111827) | Kaarten |
| `--primary` | `148 100% 33%` (#00A652) | Groen accent |
| `--foreground` | `214 32% 91%` (#e2e8f0) | Primaire tekst |
| `--muted-foreground` | `215 16% 62%` (#94a3b8) | Subtiele tekst |
| `--border` | `217 33% 17%` (#1e293b) | Randen |

**Typografie**: DM Sans (400, 500, 600, 700) via Google Fonts  
**Thema**: Donker (dark mode by default, ingesteld via class)  
**Border radius**: `--radius: 0.75rem` (12px)

### Pagina's
| Route | Doel |
|-------|------|
| `/search` | Alibaba zoekquery-generator + leverancier toevoegen |
| `/suppliers` | Leveranciersbeheer (tabel, filters, status, sterrenrating) |
| `/compare` | Leveranciers vergelijken met gewogen scoreberekening |
| `/messages` | Berichttemplates genereren (eerste contact, follow-up, onderhandelen) |
| `/catalog` | Productcatalogus met margeberekeningen per seizoen |
| `/planner` | Seizoensplanner met taken, prioriteiten en deadlines |

### Database (Prisma + SQLite)

**Schema modellen**: `Supplier`, `Product`, `ProductSupplier`, `Message`, `SearchQuery`, `PlannerItem`

**Naamgeving**: PascalCase voor modellen, camelCase voor velden  
**Seed**: `prisma/seed.ts` voor initiële testdata

**API routes** volgen het patroon `/api/[resource]` met GET/POST en `/api/[resource]/[id]` met PATCH/DELETE.

### Planner seizoenen
| Seizoen | Kleur | Emoji |
|---------|-------|-------|
| Voorjaar | #4ade80 | 🌱 |
| Zomer | #facc15 | ☀️ |
| Herfst | #f97316 | 🍂 |
| Winter | #60a5fa | ❄️ |
| Lustrum | #c084fc | 🎉 |
| Kerst/Eindjaar | #ef4444 | 🎄 |

### Catalogus margecodering
- Groen: ≥ 50%
- Geel: ≥ 30%
- Rood: < 30%

---

## Deployment

```bash
# Hoofdwebsite publiceren
git add .
git commit -m "beschrijving"
git push  # Vercel deployt automatisch

# Dashboard lokaal starten
cd hockeypolo-sourcing
npm run dev  # http://localhost:3002
```

Vercel deployt alleen de `index.html` en bijbehorende assets uit de root. Het dashboard draait alleen lokaal.

---

## Naamgeving & Codepatronen

### Hoofdwebsite
- CSS-klassen: BEM-achtig (`.hero`, `.product-grid`, `.reviews-section`, `.stagger-card`)
- Alle stijlen in `<style>`-tag in de HTML
- Eén `@media (max-width: 640px)` blok voor alle mobiele stijlen
- Staggered animaties met CSS `transform` en `opacity`

### Dashboard
- Componentstructuur: `src/components/layout/` (Sidebar, Header, MobileNav) + `src/components/ui/` (shadcn)
- State management: React hooks + `fetch()` met async/await — geen externe state library
- Path alias: `@/*` → `./src/*`
- `cn()` utility uit `lib/utils.ts` voor Tailwind classnames samenvoegen

---

## Klantprojecten (gallery)

Huidige volgorde in masonry gallery (kolom 1 → 2 → 3):
- KWF Bruggenloop, Botlek Dispuutsblouses → Apollo Lustrum → Meatboys Event, Philips Innovation

Afbeeldingsbestanden in de root: `apache1.jpg`, `botlek1.JPG`, `keizersnee1.JPG`, `ovide1.jpg`, `phia*.jpeg`, `ruis*.JPG`, `twijfelaar1.jpg`, `Fraters_KWF2026_*.jpg`, `Keizersnee_KWF2026_*.jpg`
