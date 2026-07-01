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
        # Solar Electricity Generation 2010–2024 — Methodology

        Trend lines for the top 10 solar-generating countries from 2010 to 2024.
        China's exponential growth from <1 TWh to 839 TWh dominates; Brazil and
        Australia show late but accelerating surges.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-SOLAR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    by_cc_year = {}
    names_map = {}
    for r in data:
        by_cc_year.setdefault(r['country'], {})[r['year']] = r['value']
        names_map[r['country']] = r['countryName']

    year2024 = [(cc, by_cc_year[cc].get(2024, 0) or 0) for cc in by_cc_year]
    top10 = sorted(year2024, key=lambda x: -x[1])[:10]
    print("Top 10 in 2024:", top10)

    series_data = []
    for cc, _ in top10:
        s = [round(by_cc_year[cc].get(yr, 0) or 0, 2) for yr in range(2010, 2025)]
        series_data.append({'n': names_map[cc], 's': s, 'y0': 2010})

    for sd in series_data:
        print(f"  {sd['n']}: {sd['s'][0]} TWh (2010) → {sd['s'][-1]} TWh (2024)")
    return series_data, by_cc_year, names_map, top10


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows exponential/explosive growth over 15 years
        - **Countries**: Top 10 by 2024 generation (China, USA, India, Japan, Germany, Brazil,
          Spain, Australia, Italy, South Korea)
        - **Story**: China grew 1,200x. Brazil went from near-zero to 71 TWh in just 4 years.
          Germany and Italy plateaued after early leadership.
        - **Endpoint labels**: resolveCollisions() with 12px min-gap
        """
    )
    return


@app.cell
def _(json, series_data):
    print(json.dumps(series_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
