# Visual Identity Guide
# Bangladesh Data Content Platform — Brand & Design System
# Version: 1.0 | Last Updated: February 2026
#
# PURPOSE: The Visual Designer Agent and all workflow nodes that generate
# or validate visuals MUST load this file. All visuals must comply with
# these rules. Non-compliant visuals are automatically rejected at Gate 4.

---

## 1. BRAND PHILOSOPHY

### Visual Voice
Every visual should feel like it was designed by a meticulous data journalist.
Clean. Honest. Readable. Never flashy at the expense of clarity.

### Core Principles
1. **Data first** — the chart/number is the hero, not the design
2. **Honest representation** — axes start at 0 unless explicitly justified; no distorted scales
3. **Mobile-first** — optimized for phone screens (small text is a failure)
4. **Source always visible** — watermark or citation is non-negotiable
5. **Bangladesh identity** — colors connect to national identity without being political

---

## 2. COLOR PALETTE

### Primary Colors (Use These Most)

| Name | Hex Code | RGB | Usage |
|---|---|---|---|
| **Bangladesh Green** | `#006A4E` | 0, 106, 78 | Primary bars, headers, key callouts, CTAs |
| **Liberation Red** | `#F42A41` | 244, 42, 65 | Highlights, important dates, UNESCO/target reference lines |
| **Clean White** | `#FFFFFF` | 255, 255, 255 | Background (primary), text on dark backgrounds |
| **Off-White** | `#F5F5F0` | 245, 245, 240 | Secondary background, card backgrounds |

### Secondary Colors (Accents, Use Sparingly)

| Name | Hex Code | Usage |
|---|---|---|
| **Dark Charcoal** | `#1A1A1A` | Body text, axis labels |
| **Medium Gray** | `#6B7280` | Secondary text, gridlines, annotations |
| **Light Gray** | `#E5E7EB` | Gridlines, dividers, subtle backgrounds |
| **Pale Green** | `#D1FAE5` | Positive trend highlights (subtle) |
| **Pale Red** | `#FEE2E2` | Negative trend highlights (subtle) |

### Color Usage Rules
- **Comparison charts (Period A vs Period B):** Use same color for both bars (Bangladesh Green) — avoid implying one period is "better" via color
- **Reference / benchmark lines:** Always use Liberation Red with a dashed line style
- **Positive trend:** Subtle Pale Green background or upward arrow — never celebratory
- **Negative trend:** Subtle Pale Red background — never alarmist
- **Neutral trend:** Standard colors, no special treatment

### What Is Forbidden
- Party-affiliated colors (Awami League blue, BNP green — even if they match ours, avoid compositions that could be read as partisan)
- Bright neons or gradients — looks unprofessional
- Black backgrounds — too harsh, not our brand
- Color-only encoding (must also use patterns/labels for accessibility)

---

## 3. TYPOGRAPHY

### Fonts

| Language | Font | Weights | Source |
|---|---|---|---|
| **Bangla** | Noto Sans Bengali | Regular (400), Bold (700) | Google Fonts (free) |
| **English** | Inter | Regular (400), SemiBold (600), Bold (700) | Google Fonts (free) |
| **Numbers / Data** | Inter | SemiBold (600) | Google Fonts (free) |

**Fallback:** If Noto Sans Bengali is not available, use Hind Siliguri (also Google Fonts).

### Font Sizes (for 1080x1080 Instagram canvas)

| Element | Size | Weight | Color |
|---|---|---|---|
| Main headline | 32–40px | Bold | `#1A1A1A` or white on dark bg |
| Sub-headline | 22–26px | SemiBold | `#1A1A1A` |
| Body / label text | 16–18px | Regular | `#1A1A1A` |
| Data callout (big number) | 48–64px | Bold | `#006A4E` |
| Source watermark | 12px | Regular | `#6B7280` at 70% opacity |
| Axis labels | 14px | Regular | `#6B7280` |

### Typography Rules
- Minimum font size in any visual: **12px** (nothing smaller, ever)
- Line height: 1.4–1.6x font size for readability
- Bangla and English text may appear on the same line; ensure font mixing looks clean
- Never use ALL CAPS for Bangla text
- English acronyms (GDP, BBS, UNESCO) always uppercase

---

## 4. CANVAS SIZES & LAYOUTS

### Supported Formats

| Platform | Size (px) | Aspect Ratio | DPI | File Format |
|---|---|---|---|---|
| **Instagram Feed** | 1080 × 1080 | 1:1 square | 72 | PNG |
| **Instagram Story** | 1080 × 1920 | 9:16 vertical | 72 | PNG |
| **Facebook Feed** | 1200 × 630 | 1.91:1 landscape | 72 | PNG |

**MVP scope:** Generate Instagram (1080×1080) first. Facebook (1200×630) is optional in MVP.

### Layout Zones (for 1080×1080)

```
┌─────────────────────────────────────────┐
│  HEADER ZONE (0 to 120px)               │
│  • Platform/brand name (small)          │
│  • Optional category tag                │
├─────────────────────────────────────────┤
│                                         │
│  HEADLINE ZONE (120px to 240px)         │
│  • Main Bangla headline                 │
│  • Max 2 lines                          │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│  CHART / DATA ZONE (240px to 860px)     │
│  • The chart, table, or big number      │
│  • This is the hero — give it space     │
│  • Minimum padding: 40px on all sides   │
│                                         │
├─────────────────────────────────────────┤
│  SOURCE ZONE (860px to 960px)           │
│  • "📊 Source: [Name]"                  │
│  • 12px, gray, left-aligned            │
├─────────────────────────────────────────┤
│  FOOTER ZONE (960px to 1080px)          │
│  • Brand mark or handle (optional)      │
│  • Topic tag or date                    │
└─────────────────────────────────────────┘
```

### Padding / Margins
- Outer margin: **40px** on all four sides (nothing bleeds to edge)
- Internal section spacing: **24px** minimum between elements

---

## 5. CHART TYPES & WHEN TO USE THEM

### Bar Chart (Most Common)
**Use for:** Comparing discrete values (Period A vs Period B, or multiple years)
**Rules:**
- Bars start at zero (never cut the y-axis)
- Label the value on top of each bar
- Maximum 6 bars per chart (more = use a line chart instead)
- Horizontal bars if labels are long text

### Line Chart
**Use for:** Trends over time (5+ data points)
**Rules:**
- Show data points clearly (dots on the line)
- Label the first and last values always
- Add a trend annotation if the direction is meaningful
- If comparing two lines (e.g., BD vs India), use different colors AND different line styles (solid vs dashed)

### Single Stat / Big Number
**Use for:** One striking statistic that needs no comparison
**Rules:**
- Number is very large (48px+) in Bangladesh Green
- Unit clearly labeled
- Context sentence below the number
- Most impactful format for mobile

### Table / Grid
**Use for:** Multiple metrics compared across multiple periods
**Rules:**
- Max 3 rows × 4 columns (more = unreadable on mobile)
- Alternate row colors for readability
- Column headers bold
- Values right-aligned

### What We Do Not Use
- 3D charts — distort data
- Pie charts with more than 4 segments — hard to read
- Donut charts — aesthetic but low information density
- Stacked area charts — too complex for our audience

---

## 6. STANDARD VISUAL TEMPLATES

### Template A: "Comparison Card" (Most Used)
```
[Bangla Headline — 2 lines max]

┌─────────────┐  ┌─────────────┐
│  Period A   │  │  Period B   │
│  1996-2001  │  │  2009-2024  │
│             │  │             │
│  Metric: X  │  │  Metric: Y  │
│  [Value]    │  │  [Value]    │
└─────────────┘  └─────────────┘

[Reference line or benchmark note]
[Source watermark]
```
**File naming:** `{topic_id}_comparison_ig.png`

### Template B: "Timeline Trend" (For Time Series)
```
[Bangla Headline]

[Line chart spanning time range]
[Annotated key events or inflection points]

[Source watermark]
```
**File naming:** `{topic_id}_timeline_ig.png`

### Template C: "Big Number" (For Single Stats)
```
[Context label — small text]

    [HUGE NUMBER]
    [unit / context]

[One-line explanation]
[Source watermark]
```
**File naming:** `{topic_id}_stat_ig.png`

---

## 7. MANDATORY ELEMENTS (Every Visual Must Have These)

| Element | Requirement | Failure = Reject |
|---|---|---|
| Source watermark | "📊 Source: [Name]" in bottom-left, 12px gray | YES |
| Outer margin | 40px on all sides | YES |
| Readable text | Minimum 12px, sufficient contrast | YES |
| Y-axis starts at zero | For bar charts always; line charts with justification | YES |
| Color from approved palette | No off-palette colors | YES |
| Font from approved list | Noto Sans Bengali + Inter only | YES |
| Correct canvas size | 1080×1080 for Instagram | YES |
| File size | < 1MB (optimize PNG) | YES |

---

## 8. BRAND COMPLIANCE VALIDATION CHECKLIST

The Gate 4 automated check must verify all of the following.
If any check fails, the visual is rejected and returned to the Visual Designer Agent.

```
COLOR CHECKS:
[ ] All colors used are from the approved palette (hex match ±5 tolerance)
[ ] No party-affiliated color compositions

TYPOGRAPHY CHECKS:
[ ] Fonts are Noto Sans Bengali or Inter only
[ ] Minimum font size is 12px or larger
[ ] No ALL CAPS Bangla text

LAYOUT CHECKS:
[ ] Canvas is exactly 1080×1080 (Instagram) or 1200×630 (Facebook)
[ ] Outer margins are at least 40px
[ ] No text or chart element bleeds to edge

DATA INTEGRITY CHECKS:
[ ] Bar charts start at zero
[ ] Data labels are visible on chart elements
[ ] Source watermark is present (regex: "Source:" or "📊")

FILE CHECKS:
[ ] File is PNG format
[ ] File size < 1MB
[ ] File is saved with correct naming convention: {topic_id}_{template}_{platform}.png
```

---

## 9. VISUAL DESIGNER AGENT INSTRUCTIONS

When generating a visual, follow this decision process:

```
1. READ the research data → identify the data type (comparison, trend, single stat)
2. SELECT template:
   - Two time periods being compared → Template A (Comparison Card)
   - 4+ data points over time → Template B (Timeline Trend)
   - One striking number → Template C (Big Number)
3. CHOOSE chart type:
   - Comparison with 2-6 bars → Bar chart
   - Trend with 5+ points → Line chart
   - Single figure → Big Number layout
4. APPLY brand colors:
   - Primary data → Bangladesh Green (#006A4E)
   - Reference/benchmark → Liberation Red (#F42A41) dashed
   - Background → White (#FFFFFF) or Off-White (#F5F5F0)
5. WRITE all text in correct fonts
6. ADD source watermark (bottom-left, 12px, #6B7280)
7. SAVE as PNG, 1080×1080, <1MB
8. SELF-VALIDATE against the checklist in Section 8
```

---

*This document should be updated when the visual brand evolves.*
*Changes require human approval and a Git commit.*
