"""Patch A: remove SVG-measure machinery; patch B will rebuild pages with canvas backgrounds."""
import re

path = r"C:\Users\sharm\Downloads\powerbi\_build\generate_pbip.py"
src = open(path, encoding="utf-8").read()

# ---- 1. remove the whole SVG measure block (from its comment to the PBIR GENERATION comment) ----
start_marker = "# SVG KPI CARDS (premium design: dark navy cards, gold accent, per Dashboard-Design repo patterns)"
end_marker = "# ---------------------------------------------------------------------------\n# PBIR GENERATION"
i = src.find(start_marker)
assert i != -1, "svg block start not found"
j = src.find(end_marker)
assert j != -1 and j > i, "pbir gen marker not found"
src = src[:i] + src[j:]

# ---- 2. remove simulate_svg_dax + check_all_svg_measures functions ----
i = src.find("def simulate_svg_dax")
j = src.find("def cross_checks() -> list:")
assert i != -1 and j != -1 and j > i
src = src[:i] + src[j:]

# ---- 3. remove the check_all_svg_measures() call ----
src = src.replace("    check_all_svg_measures()\n", "")

# ---- 4. native styled card replaces svg card ----
old_card = '''def card(svg_measure, x, y, w=236, h=110):
    return svg_card_visual(svg_measure, "_SVG Measures", x, y, w, h)'''
new_card = '''def card(entity, measure, x, y, w=224, h=74):
    """Native KPI card with white value on the navy canvas frame; label hidden (canvas paints title)."""
    qs = {"Data": {"projections": [projection(meas_field(entity, measure), entity, measure)]}}
    return make_visual("cardVisual", x, y, w, h, qs,
                       objects={
                           "value": [{"properties": {
                               "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
                               "fontSize": {"expr": {"Literal": {"Value": "28D"}}},
                           }, "selector": {"id": "default"}}],
                           "label": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}},
                                      "selector": {"id": "default"}}],
                       },
                       vco={"background": [{"properties": {"show": literal("false")}}],
                            "border": [{"properties": {"show": literal("false")}}],
                            "dropShadow": [{"properties": {"show": literal("false")}}],
                            "title": [{"properties": {"show": literal("false")}}]})'''
assert old_card in src, "card() not found"
src = src.replace(old_card, new_card, 1)

open(path, "w", encoding="utf-8", newline="\n").write(src)
print("patch A ok")
