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
        # Intentional Homicide Rate — Methodology

        Trend lines for 12 countries, 1990–2023, from World Bank indicator VC.IHR.PSRC.P5.
        Uses a log scale to show the 3-order-of-magnitude range from Japan (0.2) to El Salvador (138).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-IHR-PSRC-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = ['Jamaica','Ecuador','Honduras','Colombia','Brazil','El Salvador',
                'India','Canada','Estonia','Germany','Japan','Korea, Rep.']

    by_country = {}
    for r in data:
        c = r["countryName"]
        if c in selected and r["value"] is not None:
            if c not in by_country:
                by_country[c] = []
            by_country[c].append((r["year"], r["value"]))

    for c in selected:
        if c in by_country:
            pts = sorted(by_country[c])
            print(f"{c}: {pts[0][0]}–{pts[-1][0]}, latest={pts[-1][1]:.1f}")
    return by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows change over time for multiple entities
        - **Scale**: Log (base 10) — data spans 0.2 to 138, log scale shows all countries
        - **Countries**: Diverse regions; El Salvador shows the world's most dramatic decline
        - **Colors**: Warm (red/orange) for high recent rates, cool green for low rates
        - **Highlights**: Colombia fell 71% since 1991 peak; Ecuador surged 7x since 2015
        """
    )
    return


@app.cell
def _(json, by_country, selected):
    chart_data = []
    for c in selected:
        if c not in by_country:
            continue
        pts = sorted(by_country[c])
        chart_data.append({"n": c, "pts": [{"y": yr, "v": round(v, 2)} for yr, v in pts]})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
