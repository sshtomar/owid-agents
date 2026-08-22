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
        # Old-Age Dependency Ratio — Methodology

        Documents the data pipeline for viz-357: trend lines showing how
        elderly dependency ratios have changed from 1960 to 2024 across
        a diverse set of countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected_countries = [
        "Japan", "Italy", "Germany", "France", "China",
        "India", "Brazil", "Korea, Rep.", "Canada", "Kenya"
    ]
    label_map = {"Korea, Rep.": "South Korea"}

    filtered = {}
    for country in selected_countries:
        pts = sorted(
            [r for r in data if r["countryName"] == country and r["value"] is not None],
            key=lambda x: x["year"]
        )
        every5 = [p for p in pts if p["year"] % 5 == 0]
        if pts and pts[-1]["year"] not in [p["year"] for p in every5]:
            every5.append(pts[-1])
        if every5:
            label = label_map.get(country, country)
            filtered[label] = every5

    print(f"Countries loaded: {list(filtered.keys())}")
    for name, pts in filtered.items():
        print(f"  {name}: {pts[0]['year']}-{pts[-1]['year']}, latest={pts[-1]['value']:.1f}")
    return filtered, selected_countries, label_map


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows how dependency ratios diverged over 6 decades
        - **Country selection**: Covers rich-world aging leaders (Japan, Italy, Germany), fast-risers (South Korea), and emerging economies still young (India, Kenya, Brazil)
        - **Time range**: 1960–2024 at 5-year intervals to reduce clutter while preserving shape
        - **Y scale**: Linear 0–55, enough headroom for Japan's current 50.7
        - **Color**: Warm-to-cool ramp by 2024 value; high = orange/red, low = green
        - **Highlights**: Japan at 50.7 is far ahead; South Korea's steepening slope signals next crisis
        """
    )
    return


@app.cell
def _(json, filtered, label_map):
    chart_data = []
    for name, pts in filtered.items():
        chart_data.append({
            "n": name,
            "pts": [{"y": p["year"], "v": round(p["value"], 1)} for p in pts]
        })
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
