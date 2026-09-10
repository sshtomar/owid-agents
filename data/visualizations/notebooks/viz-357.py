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
        # International Tourist Arrivals, 1995–2020 — Methodology

        Trend lines showing annual international tourist arrivals (millions) for the top
        10 destination countries from 1995 to 2020. The chart highlights the COVID-19
        collapse and the dramatic divergence in tourism scale across countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(list)
    for p in data:
        by_country[p["countryName"]].append(p)

    top10 = ["France","China","Italy","Hungary","Croatia","Hong Kong SAR, China","Germany","Greece","Canada","Japan"]
    series = []
    for country in top10:
        if country not in by_country:
            continue
        pts = sorted(
            [(x["year"], x["value"]) for x in by_country[country]
             if x["value"] is not None and 1995 <= x["year"] <= 2020]
        )
        name_short = country.replace("Hong Kong SAR, China", "Hong Kong")
        series.append({
            "n": name_short,
            "pts": [{"y": y, "v": round(v / 1e6, 1)} for y, v in pts]
        })
        y2019 = next((v for yr, v in pts if yr == 2019), None)
        y2020 = next((v for yr, v in pts if yr == 2020), None)
        print(f"{country}: 2019={y2019/1e6:.1f}M, 2020={y2020/1e6 if y2020 else 'N/A'}M")

    print(f"\n{len(series)} countries in chart")
    return by_country, series, top10


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows how each country's trajectory evolved over time
        - **Country selection**: Top 10 individual countries by 2019 arrivals with data available
        - **Time range**: 1995–2020 to capture full COVID shock
        - **COVID annotation**: Vertical dashed line + shaded band at 2020
        - **Labels**: Positioned at 2019 (pre-COVID) values with leader lines to 2020 endpoints
        - **Data gaps**: France missing 1998–2003; Greece missing 2007–2012 — rendered as line breaks
        - **Key insight**: France dominates at 218M in 2019 (many short cross-border trips counted);
          Hong Kong had the worst COVID crash (65M → 3.6M, -95%)
        """
    )
    return


@app.cell
def _(json, series):
    print(json.dumps(series, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
