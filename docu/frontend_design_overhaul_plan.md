# DripFit Frontend — Complete Design Overhaul

The current frontend uses a generic dark-mode SaaS aesthetic (deep blacks, purple/violet gradients, Inter/Outfit fonts) that is entirely misaligned with the DripFit brand direction: editorial warmth, skin-tone science, inclusive luxury. This plan replaces every visual layer — tokens, typography, components, and pages — with the correct aesthetic system, while leaving all business logic and API calls untouched.

---

## User Review Required

> [!IMPORTANT]
> **Full visual overhaul** — every page will look dramatically different after this change. The functionality (API calls, auth flow, routing) is preserved, but the aesthetic is completely replaced.

> [!WARNING]
> The current colour palette (deep black `#0a0a0f`, violet `#8b5cf6`, rose `#f43f5e`) will be fully removed and replaced with the warm ivory / deep ink / gold system. If you have any screenshots or design references you want preserved, save them first.

> [!NOTE]
> No new npm packages are required. The implementation uses only vanilla CSS + React SVG — no Tailwind, no component libraries.

---

## Proposed Changes

### 1 · Foundation — Fonts & HTML Shell

#### [MODIFY] [index.html](file:///d:/dripfit/Frontend/index.html)
- Replace Google Fonts link: load **Cormorant Garamond** (300, 400, 500, 600, 700, 700i) + **Plus Jakarta Sans** (300, 400, 500, 600, 700) instead of Outfit + Inter.
- Add `<meta name="theme-color">` with `#FAF7F2`.

---

### 2 · Design System — Global CSS

#### [MODIFY] [index.css](file:///d:/dripfit/Frontend/src/index.css)
Complete replacement. New token set:
```
--ivory:        #FAF7F2   (background base)
--ink:          #1A1208   (primary text)
--ink-soft:     #2D2114   (secondary text)
--ink-muted:    #7A6A55   (tertiary / placeholders)
--gold:         #C9A96E   (primary accent)
--gold-deep:    #B8760A   (high score amber)
--terracotta:   #C4714A   (mid score)
--dusty-rose:   #C4919A   (low score)
--surface-1:    #F5EFE6   (warm card bg, monk-safe off-white)
--surface-2:    #EDE4D6   (slightly deeper surface)
--surface-3:    #E4D8C5   (borders, dividers)
--teal-grade:   #2E7D72   (grade A)
--magenta-eth:  #8B1A5A   (ethnic/festive accent)
--forest-eth:   #1F5C3A   (ethnic secondary)
--purple-eth:   #4A2070   (ethnic tertiary)
```

Key style changes vs current:
- Background: `#FAF7F2` (warm ivory) not `#0a0a0f`
- Body font: `Plus Jakarta Sans` not `Inter`
- Display font: `Cormorant Garamond` not `Outfit`
- Monk swatches: warm gold ring on active, not violet
- Occasion chips: warm fill on active, not violet
- Score ring: animated conic-gradient in gold, not violet
- Upload zone: editorial dashed border in `--gold`, not generic dotted
- Cards: warm surface on `--surface-1`, warm shadow, not cold glass
- Buttons: gold-tinted primary, not purple gradient
- Navbar: warm ivory with `--surface-3` border, not dark glass
- Scrollbar: gold thumb

Motion tokens:
```css
--ease-calm: cubic-bezier(0.25, 0.46, 0.45, 0.94);
--trans-fast: 200ms var(--ease-calm);
--trans-score: 600ms var(--ease-calm);
--trans-grade: 400ms var(--ease-calm);
```

New utility classes:
- `.fade-up` — staggered entry animation (80ms delays)
- `.shimmer-warm` — cream shimmer skeleton (no cold grey)
- `.grade-reveal` — 400ms delayed fade-in
- `.score-ring-animate` — JS-driven animated ring

---

### 3 · Component Layer

#### [MODIFY] [Navbar.jsx](file:///d:/dripfit/Frontend/src/components/Navbar.jsx)
- Background: `rgba(250,247,242,0.92)` with warm blur
- Brand: `Cormorant Garamond` italic, `--ink` colour (no gradient fill)
- Nav tabs: warm hover state, `--gold` underline on active
- Tier badge: warm amber tone, not violet
- Sign-in button: warm gold outline style

#### [MODIFY] [FigureSVG.jsx](file:///d:/dripfit/Frontend/src/components/FigureSVG.jsx)
- **Head**: skin-tone aware hex — accepts `skinToneHex` prop, defaults to Monk 3 (`#C68642`)
- **Proportions**: revised to inclusive body — wider shoulders, natural waist, not hyper-stylised
- **Dupatta**: new optional region — if `dupatttaColour` prop provided, renders dupatta draped diagonally over torso/shoulder with culturally accurate diagonal path
- **Accessories**: neck region (collar/chain indicator), wrist (watch dot)
- **Arms**: natural articulation, 5px SVG stroke join
- **Transition animation**: `<animate>` or CSS transition on fill colour (200ms ease-in-out)
- **ARIA**: each region gets `role="img"` + `aria-label`
- Accept new props: `skinToneHex`, `gender` (defaults `'neutral'`), `dupatttaColour`, `kurta` boolean

#### [MODIFY] [OutfitComponents.jsx](file:///d:/dripfit/Frontend/src/components/OutfitComponents.jsx)
- **MonkSelector**: actual Monk Scale hex values (not approximations), warm gold ring on active, hover glow in swatch's own tint, `aria-label` with descriptive name (e.g. `"Monk 4 — medium warm brown"`)
- **OccasionPicker**: ethnic/festive pill gets jewel-toned magenta accent dot, active state warm-filled
- **ScoreRing**: animated on mount (600ms), gold conic-gradient, editorial callout layout not dashboard
- **ScoreBreakdown**: horizontal bars with warm amber fill, italic serif labels
- **OutfitResultCard**: 2-column editorial layout, figure dominates left, score cards right, generous spacing, persona in italic Cormorant Garamond
- **PersonaBadge**: italic serif, gold border, warm tint background

#### [NEW] [SkeletonLoader.jsx](file:///d:/dripfit/Frontend/src/components/SkeletonLoader.jsx)
- Warm cream shimmer skeleton for outfit loading state
- Matches the outfit card layout (figure placeholder + score placeholder)
- Uses `--surface-1` → `--surface-2` shimmer gradient, no cold grey

#### [NEW] [Toast.jsx replacement] — update existing [Toast.jsx](file:///d:/dripfit/Frontend/src/components/Toast.jsx)
- Warm ivory toast background, gold border for success, terracotta for error
- Cormorant Garamond message text

---

### 4 · Pages

#### [MODIFY] [HomePage.jsx](file:///d:/dripfit/Frontend/src/pages/HomePage.jsx)
- Hero: warm ivory background, radial gradient `rgba(201,169,110,0.08)` glow, not cold purple
- H1: Cormorant Garamond, `clamp(3rem, 8vw, 5.5rem)`, generous letter-spacing, italic span
- Hero tag: gold accent, warm surface background
- Feature cards: warm surface, gold icon containers
- Module cards: editorial numbered layout with large Cormorant ordinals
- Staggered `.fade-up` animation on section items (80ms delay each)

#### [MODIFY] [WardrobePage.jsx](file:///d:/dripfit/Frontend/src/pages/WardrobePage.jsx)
- Upload zone: editorial dashed border (`--gold`), "Drop a garment on the styling table" feel, warm hover state
- Wardrobe grid: masonry-feel with warm surface cards, `translateY(-3px)` hover lift + warm shadow
- Category badge: gold accent chip at bottom-left, not generic text
- Delete button: terracotta tone, not harsh red

#### [MODIFY] [OutfitPage.jsx](file:///d:/dripfit/Frontend/src/pages/OutfitPage.jsx)
- Controls panel: warm surface card (sticky), generous typography
- Loading state: `SkeletonLoader` with warm cream shimmer + contextual copy
- Result reveal: graceful fade-in on figure first, then score cards
- Tab switcher: warm editorial pill style
- Stats: italic serif sub-copy, not plain text

#### [MODIFY] [StyleMePage.jsx](file:///d:/dripfit/Frontend/src/pages/StyleMePage.jsx)
- Header: wider, more exploratory tone — "let's see what works for you today"
- Figure: wider aspect ratio (240px instead of 220px)
- Empty state: warm encouraging illustration placeholder
- Swipe alternative: arrow nav on desktop, touch hint on mobile

#### [MODIFY] [AnalyserPage.jsx](file:///d:/dripfit/Frontend/src/pages/AnalyserPage.jsx)
- Upload area: tall, centred, fitting-room-mirror feel — warm-toned frame with `--surface-3` border
- Analyse button: editorial gold CTA
- Grade display: large Cormorant Garamond letter (96px), `grade-reveal` 400ms fade
- Grade colours: A=`--teal-grade`, B=`--gold-deep`, C=`--terracotta`, D=`--dusty-rose` (never red)
- Tips list: warm surface cards, italic rationale text

#### [MODIFY] [SavedLooksPage.jsx](file:///d:/dripfit/Frontend/src/pages/SavedLooksPage.jsx)
- Look cards: warm surface, editorial score display in Cormorant (large serif)
- Persona in italic
- Colour swatches: larger circles with warm shadow
- Date: muted ink-soft, not harsh grey

---

## Open Questions

> [!IMPORTANT]
> **Gender toggle on the 2D figure** — should the figure have a gender selector (male/female/neutral) visible in the UI? Or should it be a hidden prop that the backend may eventually send? Currently `FigureSVG` has no gender prop.

> [!IMPORTANT]
> **Dupatta/ethnic SVG regions** — the brief mentions ethnic wear (kurta, dupatta, churidar) with cultural accuracy. Should these additional SVG regions appear only when `occasion === 'ethnic_festive'`, or always? The backend already categorises ethnic items — we can conditionally show dupatta drape based on the outfit items array.

> [!NOTE]
> **Anchor item upload on Outfit page** — the brief mentions "drop a garment on a styling table" UX for Module 1. Currently the OutfitPage has no anchor-upload — items come from the wardrobe. Should we add an optional anchor upload directly on the outfit page, or is the wardrobe upload the canonical flow?

---

## Verification Plan

### Automated
- `npm run build` — confirm zero errors after changes
- `npm run lint` — confirm no lint violations

### Browser Walkthrough (via browser_subagent)
- Navigate all 6 pages and capture screenshots for each
- Verify: warm ivory bg, Cormorant heading fonts, gold accents visible
- Verify: Monk swatches render correct skin-tone hex values with gold ring on active
- Verify: FigureSVG renders correctly with coloured regions
- Verify: Score ring animates on load
- Verify: Analyser grade letter uses correct colours (no red for D)
- Verify: Mobile navbar collapses gracefully
- Verify: No purple/violet/cold‐gray tones remain anywhere

### Manual
- Confirm font load: Cormorant Garamond display + Plus Jakarta Sans body
- Confirm WCAG contrast on gold `#C9A96E` over `#FAF7F2` — needs verification (gold on ivory can be borderline AA)
