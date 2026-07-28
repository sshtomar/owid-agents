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
        # Income Share of the Richest 10% -- Methodology

        Slope chart comparing the share of national income held by the top 10%
        of earners, early 2000s vs. most recent year (2018-2024). Shows the
        stark contrast between Latin America and Northern Europe.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-DST-10TH-10.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    by_country = {}
    for p in data:
        if p["value"] is None:
            continue
        c = p["countryName"]
        if c not in by_country:
            by_country[c] = []
        by_country[c].append((p["year"], p["value"]))

    picks = ['Colombia','Brazil','Chile','Costa Rica','Honduras','Kenya',
             'Bolivia','Indonesia','China','Germany','Greece','Australia',
             'Italy','Bangladesh','Denmark','Finland','Belgium','Czechia','Belarus']

    slope = []
    for c, pts in by_country.items():
        if c not in picks:
            continue
        pts.sort()
        early = [(y, v) for y, v in pts if 1998 <= y <= 2006]
        late = [(y, v) for y, v in pts if 2018 <= y <= 2024]
        if early and late:
            slope.append({"n": c, "a": round(early[-1][1], 1), "b": round(late[-1][1], 1)})

    slope.sort(key=lambda x: -x["b"])
    print(f"Countries: {len(slope)}")
    for s in slope:
        print(f"  {s['n']}: {s['a']}% -> {s['b']}% ({s['b']-s['a']:+.1f}pp)")
    return slope, by_country, picks


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (early 2000s vs. ~2022) to show direction of change
        - **Color**: Red/orange for high income concentration (>=38%), green for low
        - **Story**: Colombia and Brazil's top 10% take 40%+ of national income.
          Bolivia cut its top-10% share from 44% to 31%. Nordic countries cluster below 23%.
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
