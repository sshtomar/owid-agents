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
        # Crude Death Rate Since 1960 -- Methodology

        Shows how aging rich nations now have *rising* death rates while developing
        nations have achieved dramatic falls -- a counterintuitive demographic story.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-CDRT-IN.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = row["value"]

    selected = ["Japan", "Germany", "Korea, Rep.", "Brazil", "China", "India", "Bangladesh", "Ethiopia"]
    labels = {"Korea, Rep.": "S. Korea"}

    years = list(range(1960, 2025))
    result = []
    for country in selected:
        if country in by_country:
            vals = by_country[country]
            pts = [{"y": y, "v": round(vals[y], 2)} for y in years if y in vals]
            result.append({"n": labels.get(country, country), "pts": pts})

    print(f"Series: {[r['n'] for r in result]}")
    for r in result:
        pts = r["pts"]
        print(f"  {r['n']}: {pts[0]['y']} val={pts[0]['v']} -> {pts[-1]['y']} val={pts[-1]['v']}")
    return by_country, result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- annual time series shows trajectory clearly
        - **Country selection**: Contrasting stories -- Japan/Germany/S.Korea (aging, rising) vs
          India/Bangladesh/Ethiopia (developing, falling sharply); China added for 1960 famine spike
        - **Time range**: 1960-2024, full span of modern data
        - **Highlights**: Japan's rate tripled since 1977; Bangladesh fell from 22 to 5 (1960-2024);
          China's 1960 spike reflects the Great Leap Forward famine
        - **Color**: Warm tones for aging countries; cool greens for falling-rate countries
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
