"""Patch B2: canvas builder + new build_pages (frames painted in page background SVG, visuals inside frames)."""

path = r"C:\Users\sharm\Downloads\powerbi\_build\generate_pbip.py"
src = open(path, encoding="utf-8").read()

START = "def build_pages():"
END = "THEME_JSON = {"
i = src.find(START)
j = src.find(END)
assert i != -1 and j != -1 and j > i

NEW = '''CANVASES = []  # (svg filename, svg content) collected by build_pages, written by build_report_root


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def canvas_svg(title, subtitle, kpi_frames, section_frames):
    """Page background: warm paper canvas, navy header band, KPI frames, white section frames."""
    p = []
    p.append("<svg width='1280' height='720' viewBox='0 0 1280 720' xmlns='http://www.w3.org/2000/svg'>")
    p.append("<rect width='1280' height='720' fill='#F2EFE6'/>")
    p.append("<rect width='1280' height='72' fill='#1B2A38'/>")
    p.append("<rect x='0' y='68' width='240' height='4' fill='#FDBF11'/>")
    p.append("<text x='28' y='32' font-family='Segoe UI Semibold' font-size='20' letter-spacing='1' fill='#FFFFFF'>" + esc(title) + "</text>")
    p.append("<text x='28' y='54' font-family='Segoe UI' font-size='11' fill='#A9B6C2'>" + esc(subtitle) + "</text>")
    for x, y, t in kpi_frames:
        p.append("<rect x='%d' y='%d' width='236' height='112' rx='10' fill='#1B2A38'/>" % (x, y))
        p.append("<rect x='%d' y='%d' width='5' height='96' fill='#FDBF11'/>" % (x, y + 8))
        p.append("<text x='%d' y='%d' font-family='Segoe UI' font-size='10' letter-spacing='1.2' fill='#A9B6C2'>" % (x + 18, y + 24) + esc(t) + "</text>")
    for x, y, w, h, t in section_frames:
        p.append("<rect x='%d' y='%d' width='%d' height='%d' rx='10' fill='#FFFFFF' stroke='#E2DCCC' stroke-width='1'/>" % (x, y, w, h))
        p.append("<text x='%d' y='%d' font-family='Segoe UI Semibold' font-size='12.5' fill='#17202B'>" % (x + 16, y + 26) + esc(t) + "</text>")
    p.append("<text x='1256' y='712' text-anchor='end' font-family='Segoe UI' font-size='9' fill='#9AA08F'>DATA: AGMARKNET + IMD | BUILT 21 NOV 2026</text>")
    p.append("</svg>")
    return "".join(p)


def build_pages():
    pages = []
    page_order = []
    pages_json = {"$schema": SCHEMA_PAGES}

    def new_page(display, svg_name, svg):
        pid = hexid()
        page_order.append(pid)
        CANVASES.append((svg_name, svg))
        return pid

    # ---------------- Page 1: Overview ----------------
    p1 = new_page("Overview", "overview_bg.svg", canvas_svg(
        "MANDI MARKET INTELLIGENCE", "Prices - markets and commodity coverage across India",
        [(16, 88, "STATES COVERED"), (262, 88, "MANDI MARKETS"), (508, 88, "COMMODITIES"),
         (754, 88, "PRICE RECORDS"), (1000, 88, "AVG MARKET PRICE")],
        [(16, 214, 624, 240, "AVG MARKET PRICE BY COMMODITY"), (656, 214, 608, 240, "SHARE OF RECORDS BY GROUP"),
         (16, 466, 624, 238, "AVG MARKET PRICE BY STATE"), (656, 466, 608, 238, "COMMODITY PRICE SUMMARY")]))
    v = [
        card(MP, "States Count", 24, 124),
        card(MP, "Markets Count", 270, 124),
        card(MP, "Commodities Count", 516, 124),
        card(MP, "Mandi Records", 762, 124),
        card(MP, "Avg Market Price", 1008, 124),
        column_chart(None, MP, "Commodity", [("measure", "Avg Market Price")],
                     24, 246, 608, 200, sort=sort_by(MP, "measure", "Avg Market Price")),
        donut(None, DC, "Commodity Group", [("measure", "Mandi Records")],
              664, 246, 592, 200, y_entity=MP),
        bar_chart(None, MP, "State", [("measure", "Avg Market Price")],
                  24, 498, 608, 198, sort=sort_by(MP, "measure", "Avg Market Price")),
        table(None, [
            (DC, "Commodity", "column"),
            (MP, "Avg Market Price", "measure"),
            (MP, "Min Market Price", "measure"),
            (MP, "Max Market Price", "measure"),
            (LP, "Latest Avg Price", "measure"),
        ], 664, 498, 592, 198),
    ]
    pages.append((p1, "Overview", v))

    # ---------------- Page 2: Prices vs MSP ----------------
    p2 = new_page("Prices vs MSP", "mspbp_bg.svg", canvas_svg(
        "PRICE VS MSP ANALYSIS", "Where markets trade against government support prices",
        [(16, 88, "COMMODITIES TRACKED"), (262, 88, "AVERAGE MSP"), (508, 88, "ABOVE MSP"),
         (754, 88, "MEDIAN DEVIATION"), (1000, 88, "MEDIAN GAP VS MSP")],
        [(16, 214, 812, 240, "MARKET PRICE VS MSP BY COMMODITY"), (844, 214, 420, 240, "WEEK-ON-WEEK TREND"),
         (16, 466, 624, 238, "PRICE GAP VS MSP BY COMMODITY"), (656, 466, 608, 238, "MSP COMPARISON DETAIL")]))
    v = [
        card(MS, "Commodities Tracked", 24, 124),
        card(MS, "Avg MSP", 270, 124),
        card(LP, "% Above MSP", 516, 124),
        card(LP, "Median Deviation %", 762, 124),
        card(LP, "Median Deviation from MSP", 1008, 124),
        column_chart(None, MS, "Commodity",
                     [("measure", "Avg Commodity Market Price"), ("measure", "Avg MSP")],
                     24, 246, 796, 200),
        donut(None, LP, "Trend", [("measure", "Markets Reporting")], 852, 246, 404, 200),
        bar_chart(None, MS, "Commodity", [("measure", "Avg Price Gap vs MSP")],
                  24, 498, 608, 198, sort=sort_by(MS, "measure", "Avg Price Gap vs MSP")),
        table(None, [
            (DC, "Commodity Group", "column"),
            (MS, "Commodity", "column"),
            (MS, "Avg Market Price", "column"),
            (MS, "Average MSP", "column"),
            (MS, "Price Difference", "column"),
            (MS, "Records", "column"),
        ], 664, 498, 592, 198),
    ]
    pages.append((p2, "Prices vs MSP", v))

    # ---------------- Page 3: Market Explorer ----------------
    p3 = new_page("Market Explorer", "explorer_bg.svg", canvas_svg(
        "MARKET EXPLORER", "Every mandi, every commodity - slice and search",
        [],
        [(16, 88, 220, 96, "COMMODITY"), (16, 196, 220, 96, "COMMODITY GROUP"), (16, 304, 220, 96, "STATE"),
         (16, 412, 220, 292, "PRICE TREND"), (252, 88, 504, 296, "TOP 10 MARKETS BY AVG PRICE"),
         (772, 88, 492, 296, "MIN VS MAX PRICE BY COMMODITY"), (252, 396, 1012, 308, "ALL MARKET PRICES")]))
    v = [
        slicer(DC, "Commodity", 24, 120),
        slicer(DC, "Commodity Group", 24, 228),
        slicer(MP, "State", 24, 336),
        donut(None, LP, "Trend", [("measure", "Markets Reporting")], 24, 444, 204, 252),
        bar_chart(None, MP, "Market", [("measure", "Avg Market Price")],
                  260, 120, 488, 256, sort=sort_by(MP, "measure", "Avg Market Price"),
                  filter_config=[topn_filter(MP, "Market", "Avg Market Price", 10)]),
        column_chart(None, MP, "Commodity",
                     [("measure", "Min Market Price"), ("measure", "Max Market Price")],
                     780, 120, 476, 256, labels=False),
        table(None, [
            (MP, "State", "column"),
            (MP, "District", "column"),
            (MP, "Market", "column"),
            (MP, "Commodity", "column"),
            (MP, "Records", "column"),
            (MP, "Avg Market Price", "measure"),
            (MP, "Min Market Price", "measure"),
            (MP, "Max Market Price", "measure"),
            (LP, "Latest Avg Price", "measure"),
            (LP, "Median Deviation %", "measure"),
        ], 260, 428, 996, 268),
    ]
    pages.append((p3, "Market Explorer", v))

    # ---------------- Page 4: Rainfall ----------------
    p4 = new_page("Rainfall", "rainfall_bg.svg", canvas_svg(
        "RAINFALL MONITOR", "District-level rainfall against long-term normals",
        [(16, 88, "ACTUAL RAINFALL"), (262, 88, "NORMAL RAINFALL"), (508, 88, "DEPARTURE"),
         (754, 88, "DISTRICTS MONITORED")],
        [(1000, 88, 264, 112, "FILTER BY STATE"),
         (16, 214, 812, 240, "DAILY RAINFALL - ACTUAL VS NORMAL"), (844, 214, 420, 240, "DISTRICT-DAYS BY CATEGORY"),
         (16, 466, 624, 238, "MONTHLY RAINFALL VS NORMAL"), (656, 466, 608, 238, "ACTUAL RAINFALL BY STATE")]))
    v = [
        card(DR, "Total Actual Rainfall", 24, 124),
        card(DR, "Total Normal Rainfall", 270, 124),
        card(DR, "Rainfall Departure %", 516, 124),
        card(DD, "Districts Monitored", 762, 124),
        slicer(DD, "State", 1008, 120, 248, 68),
        line_chart(None, DR, "Date",
                   [("measure", "Total Actual Rainfall"), ("measure", "Total Normal Rainfall")],
                   24, 246, 796, 200),
        donut(None, DR, "Category Name", [("measure", "Days Count")], 852, 246, 404, 200),
        column_chart(None, MR, "Month Name",
                     [("measure", "Monthly Rainfall Total"), ("measure", "Monthly Normal Total")],
                     24, 498, 608, 198, labels=True),
        bar_chart(None, DD, "State", [("measure", "Total Actual Rainfall")],
                  664, 498, 592, 198, y_entity=DR,
                  sort=sort_by(DR, "measure", "Total Actual Rainfall")),
    ]
    pages.append((p4, "Rainfall", v))

    # ---------------- write ----------------
    pages_dir = os.path.join(REP, "definition", "pages")
    for idx, (pid, display, visuals) in enumerate(pages):
        pdir = os.path.join(pages_dir, pid)
        page_json = {
            "$schema": SCHEMA_PAGE,
            "name": pid,
            "displayName": display,
            "displayOption": "FitToPage",
            "height": 720,
            "width": 1280,
            "objects": {"background": [{
                "properties": {
                    "transparency": {"expr": {"Literal": {"Value": "0D"}}},
                    "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#F2EFE6'"}}}}},
                    "image": {"image": {
                        "name": {"expr": {"Literal": {"Value": "'%s'" % CANVASES[idx][0]}}}},
                        "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources",
                                                                 "PackageType": 1,
                                                                 "ItemName": CANVASES[idx][0]}}},
                        "scaling": {"expr": {"Literal": {"Value": "'Fill'"}}},
                    }},
                }
            }]},
        }
        write_json(os.path.join(pdir, "page.json"), page_json)
        for vis in visuals:
            VISUALS_BY_PAGE.setdefault(pid, []).append(vis)
            vid = vis["name"]
            write_json(os.path.join(pdir, "visuals", vid, "visual.json"), vis)
    pages_json["pageOrder"] = page_order
    pages_json["activePageName"] = page_order[0]
    write_json(os.path.join(pages_dir, "pages.json"), pages_json)


'''

src = src[:i] + NEW + src[j:]

open(path, "w", encoding="utf-8", newline="\n").write(src)
print("patch B2 ok")
