# Mandi Rainfall Dashboard — Power BI Project

A premium Power BI dashboard built from five CSV exports of India's mandi (wholesale market)
prices and IMD district rainfall data.

![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-yellow) ![Format](https://img.shields.io/badge/format-PBIP%20%2B%20TMDL%20%2B%20PBIR-blue)

## What's inside

```
├── MandiRainfallDashboard.pbip          ← open this in Power BI Desktop
├── MandiRainfallDashboard.SemanticModel/   TMDL data model (8 tables, 46 measures)
├── MandiRainfallDashboard.Report/          PBIR report (4 pages, 38 visuals)
├── *.csv                                   source data (5 files)
└── _build/                                 generator + validation scripts (Python)
```

## Quick start

1. Install [Power BI Desktop](https://powerbi.microsoft.com/desktop) (free).
2. Open `MandiRainfallDashboard.pbip`.
3. Click **Refresh** to load the CSV data (queries reference the CSVs by path —
   keep the folder layout, or update the paths in **Transform data**).

## Pages

| Page | Contents |
|---|---|
| **Overview** | SVG KPI cards, avg price by commodity, records by commodity group, price by state, price summary table |
| **Prices vs MSP** | KPI cards, market price vs MSP by commodity, week-on-week trend, price gap ranking, MSP comparison table |
| **Market Explorer** | Commodity / group / state slicers, Top-10 markets chart (TopN filter), min-vs-max price range, full price table |
| **Rainfall** | Rainfall KPI cards, daily actual-vs-normal line, category donut, monthly comparison, state ranking |

## Design system

- **Full-canvas SVG backgrounds** — every page has a designed 1280x720 canvas
  (navy header band with gold rule, gold-accented KPI card frames, titled white
  section frames, footer stamp) registered in `RegisteredResources` and bound via
  `page.json` background — following the
  [Dashboard-Design patterns](https://github.com/Dashboard-Design/Power-BI-Design-Files).
  Visuals sit transparently inside the frames; all chrome is static and always renders.
- **MandiPremium V2 theme** — Economist-inspired palette (red `#E3120B`, teal `#0098A6`,
  gold `#FDBF11`), warm paper canvas, navy table headers, transparent visual surfaces.
- **KPI cards** — native `cardVisual` values in ink, labels hidden (canvas paints titles),
  full-number display units.
- **TopN filtering** — Market Explorer's "Top 10 Markets" uses a hand-authored PBIR
  TopN filter validated by `powerbi-report-author validate`.

## Data model

| Table | Source | Grain |
|---|---|---|
| Market Prices | New_Query CSV | market × commodity (records, avg/min/max price) |
| Latest Prices | Latest Market Prices CSV | same grain: latest price, trend, MSP deviation |
| MSP Analysis | Commodity MSP Analysis CSV | commodity (avg market price vs MSP) |
| Daily Rainfall | Daily Rainfall Trend CSV | district-day (63K rows) |
| Monthly Rainfall | District Monthly Rainfall CSV | district-month |
| Dim Commodity / Dim District / _SVG Measures | derived | hubs for filtering and card visuals |

"null" strings in the CSVs are cleaned in Power Query; rainfall categories
(LD/D/N/E/LE/NR/ND) get readable names and a sort order; month names sort chronologically.

## Rebuilding

The whole project is generated deterministically from `_build/generate_pbip.py`:

```bash
python _build/generate_pbip.py     # regenerate the .pbip from the CSVs
python _build/validate_pbip.py     # validate report JSON against official MS schemas
python _build/check_m.py           # sanity-check the Power Query code
```

Validation: every report JSON file passes the official Microsoft PBIR schemas,
`powerbi-report-author validate` reports 0 errors, and the TMDL model loads in
Tabular Editor 2.
