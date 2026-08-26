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
        # Manufactures Exports as Share of Merchandise Exports -- Methodology

        Trend lines for 8 countries showing the share of manufactured goods in total
        merchandise exports, 1990–2023. Reveals contrasting industrialisation paths:
        East Asian rise, Brazil's commodity pivot, Indonesia's plateau.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--TX-VAL-MANF-ZS-UN.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(list)
    for row in data:
        if row["value"] is not None and 1990 <= row["year"] <= 2023:
            by_country[row["countryName"]].append((row["year"], row["value"]))

    selected = ["China", "Korea, Rep.", "Germany", "Japan", "Bangladesh",
                "India", "Brazil", "Indonesia"]
    series = {}
    for c in selected:
        pts = sorted(by_country.get(c, []), key=lambda x: x[0])
        if len(pts) >= 10:
            series[c] = pts
    print(f"Selected {len(series)} countries")
    for c, pts in series.items():
        print(f"  {c}: {pts[0][0]}-{pts[-1][0]}, {pts[-1][1]:.1f}% in {pts[-1][0]}")
    return by_country, selected, series


@app.cell
def _(series):
    values = [v for pts in series.values() for _, v in pts]
    print(f"Value range: {min(values):.1f}% - {max(values):.1f}%")
    return (values,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — best for showing how multiple countries evolved over time
        - **Country selection**: 8 countries covering mature manufacturers (Japan, Germany, Korea),
          a rising giant (China), a frontier exporter (Bangladesh), a pivot case (Brazil), and
          mixed trajectories (India, Indonesia)
        - **Time range**: 1990–2023 — covers the WTO era and China's entry
        - **Highlights**: China climbed from 78% to 92%; Brazil fell from 52% to 24% as commodity
          exports surged; Bangladesh rose to 95% driven by garments
        """
    )
    return


@app.cell
def _(json, series):
    chart_data = []
    for name, pts in series.items():
        chart_data.append({
            "n": name,
            "pts": [{"y": y, "v": round(v, 1)} for y, v in pts]
        })
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
