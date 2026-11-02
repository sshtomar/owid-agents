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
        # Rise of Megacities: Population in Urban Agglomerations over 1 Million -- Methodology

        Trend lines showing what share of each country's total population lives in urban
        agglomerations of more than one million people, from 1960 to 2024.
        Source: World Bank indicator EN.URB.MCTY.TL.ZS.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-URB-MCTY-TL-ZS.json"
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

    target = [
        "Japan", "China", "Brazil", "Colombia",
        "Korea, Rep.", "Argentina", "Australia", "Congo, Rep.",
        "Bolivia", "Chile",
    ]

    series = []
    for name in target:
        if name not in by_country:
            print(f"MISSING: {name}")
            continue
        pts = sorted(
            [{"y": yr, "v": round(v, 1)} for yr, v in by_country[name].items()
             if 1960 <= yr <= 2024],
            key=lambda x: x["y"]
        )
        if len(pts) >= 10:
            series.append({"n": name, "pts": pts})
            print(f"{name}: {pts[0]['y']} ({pts[0]['v']}) -> {pts[-1]['y']} ({pts[-1]['v']})")
    return by_country, series, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows 60-year arc of megacity growth
        - **Country selection**: Mix of fast-urbanizing Latin American and Asian economies
          plus Australia and Congo for contrast
        - **Time range**: 1960-2024, capturing the full post-war urbanization wave
        - **Highlights**: Japan's megacity share doubled; Congo grew from 18% to 65%;
          China has gone from near zero to 32% in 60 years
        """
    )
    return


@app.cell
def _(json, series):
    print(json.dumps(series, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
