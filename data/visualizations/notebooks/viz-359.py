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
        # Youth Population Share (Ages 0–14) — Methodology

        Sparkline grid of 12 countries showing the share of population aged 0–14, 1960–2023,
        from World Bank indicator SP.POP.0014.TO.ZS. Reveals the global demographic transition.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-0014-TO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = ['Chad','Angola','Ethiopia','Bangladesh','India','Indonesia',
                'Brazil','China','Italy','Germany','Japan','Korea, Rep.']

    by_country = {}
    for r in data:
        c = r["countryName"]
        if c in selected and r["value"] is not None:
            if c not in by_country:
                by_country[c] = {}
            by_country[c][r["year"]] = r["value"]

    chart_data = []
    for c in selected:
        if c not in by_country:
            continue
        yrs = by_country[c]
        series = [round(yrs.get(yr, 0) or 0, 1) for yr in range(1960, 2024)]
        v1960 = round(yrs.get(1960, 0), 1)
        v2023 = round(yrs.get(2023, 0), 1)
        chart_data.append({"n": c, "s": series, "e": v1960, "l": v2023, "y0": 1960})
        print(f"{c}: {v1960:.1f}% (1960) → {v2023:.1f}% (2023)")
    return by_country, chart_data, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — shows many entities' time series compactly
        - **Sorted**: Descending by 2023 value (highest youth share first)
        - **Countries**: Mix of still-high (Sub-Saharan Africa), transition (South/SE Asia), and post-transition (East Asia, Europe)
        - **Highlights**: Korea dropped from 41% to 11% in 63 years; Chad barely moved at 47%
        """
    )
    return


if __name__ == "__main__":
    app.run()
