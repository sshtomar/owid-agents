import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import json
    from pathlib import Path
    return json, mo, Path


@app.cell
def _(mo):
    mo.md(
        """
        # Wanted Fertility Rate — Methodology

        Documents the data pipeline behind viz-515: trend lines showing
        the decline in women's desired family size across 10 developing
        countries, based on household survey data.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-WFRT.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    non_null = [r for r in data if r["value"] is not None]
    countries = sorted(set(r["countryName"] for r in non_null))
    print(f"Total countries/entities: {len(countries)}")
    print("Countries:", countries)
    return countries, non_null


@app.cell
def _(non_null):
    selected = [
        "Ghana","Cameroon","Kenya","Ethiopia","Egypt, Arab Rep.",
        "Jordan","Indonesia","Colombia","India","Bangladesh"
    ]
    series_map = {}
    for r in non_null:
        if r["countryName"] in selected:
            series_map.setdefault(r["countryName"], []).append((r["year"], round(r["value"], 1)))

    for name, pts in series_map.items():
        pts.sort()
        print(f"{name}: {pts[0]} -> {pts[-1]}, {len(pts)} surveys")
    return selected, series_map


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with dots at survey points — because the
          wanted fertility rate is measured from household surveys (every 3–8 years),
          not annually; dots make the irregular cadence visible and honest
        - **Country selection**: 10 countries across Sub-Saharan Africa (Ghana,
          Cameroon, Kenya, Ethiopia), Middle East/North Africa (Egypt, Jordan),
          South/Southeast Asia (India, Bangladesh, Indonesia), and Latin America
          (Colombia) — covering the main developing-world contexts
        - **Reference line**: 2.1 replacement rate helps readers judge whether
          preferences are above or below long-run population stability
        - **Key insight**: Jordan has dropped from 3.9 (1990) to 1.9 (2023) —
          below replacement. Even in Sub-Saharan Africa, Kenya and Ghana have
          declined significantly. The story is aspirational change, not just
          contraceptive access.
        - **Measurement note**: Survey dates are irregular; each dot is one
          Demographic and Health Survey (DHS) or similar national survey
        """
    )
    return


@app.cell
def _(json, series_map):
    colors = {
        "Ghana": "#EA5E33",
        "Cameroon": "#F29A44",
        "Kenya": "#C49A45",
        "Ethiopia": "#8BAD72",
        "Egypt, Arab Rep.": "#5B9E78",
        "Jordan": "#3D7A5A",
        "Indonesia": "#A6C4A2",
        "Colombia": "#7A786F",
        "India": "#2B2A27",
        "Bangladesh": "#C4715A"
    }
    name_remap = {"Egypt, Arab Rep.": "Egypt"}
    chart_data = []
    for name, pts in series_map.items():
        pts_sorted = sorted(pts)
        chart_data.append({
            "n": name_remap.get(name, name),
            "pts": [{"y": y, "v": v} for y, v in pts_sorted],
            "col": colors.get(name, "#9A9890")
        })
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, colors, name_remap


if __name__ == "__main__":
    app.run()
