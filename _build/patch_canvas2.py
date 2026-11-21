"""Patch B: canvas background system - title_vco(None), canvas builder, new build_pages, theme v2, resource packages."""
import re

path = r"C:\Users\sharm\Downloads\powerbi\_build\generate_pbip.py"
src = open(path, encoding="utf-8").read()

# ---- 1. title_vco: None -> hidden title ----
old = '''def title_vco(text):
    return {"title": [{
        "properties": {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "text": {"expr": {"Literal": {"Value": f"'{text}'"}}},
        }
    }]}'''
new = '''def title_vco(text):
    if text is None:
        return {"title": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]}
    return {"title": [{
        "properties": {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "text": {"expr": {"Literal": {"Value": f"'{text}'"}}},
        }
    }]}'''
assert old in src
src = src.replace(old, new, 1)

# ---- 2. slicer: header off (canvas paints titles), transparent bg ----
old = '''def slicer(entity, col, display, x, y, w=220, h=110):
    qs = {"Values": {"projections": [projection(col_field(entity, col), entity, col)]}}
    objects = {
        "data": [{"properties": {"mode": literal("'Dropdown'")}}],
        "header": [{"properties": {"show": literal("true"), "text": literal(f"'{display}'")}}],
    }
    return make_visual("slicer", x, y, w, h, qs, objects=objects)'''
new = '''def slicer(entity, col, display, x, y, w=204, h=56):
    qs = {"Values": {"projections": [projection(col_field(entity, col), entity, col)]}}
    objects = {
        "data": [{"properties": {"mode": literal("'Dropdown'")}}],
        "header": [{"properties": {"show": literal("false")}}],
    }
    return make_visual("slicer", x, y, w, h, qs, objects=objects,
                       vco={"background": [{"properties": {"show": literal("false")}}],
                            "border": [{"properties": {"show": literal("false")}}],
                            "title": [{"properties": {"show": literal("false")}}]})'''
assert old in src
src = src.replace(old, new, 1)

open(path, "w", encoding="utf-8", newline="\n").write(src)
print("patch B part 1 ok")
