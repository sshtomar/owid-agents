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

        Slope chart comparing the income share held by the top decile from the early 2000s
        to the most recent survey. Focuses on countries with available data at both timepoints.
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
    for row in data:
        if row['value'] is not None and len(row['country']) == 2:
            n = row['countryName']
            if n not in by_country:
                by_country[n] = []
            by_country[n].append((row['year'], round(row['value'], 1)))

    slope = []
    for name, pts in by_country.items():
        pts_sorted = sorted(pts)
        early = [(y, v) for y, v in pts_sorted if 1999 <= y <= 2006]
        late  = [(y, v) for y, v in pts_sorted if y >= 2018]
        if early and late:
            ey, ev = max(early, key=lambda x: x[0])
            ly, lv = max(late, key=lambda x: x[0])
            slope.append({"n": name, "a": ev, "ay": ey, "b": lv, "by": ly})

    slope.sort(key=lambda x: x['a'], reverse=True)
    for s in slope[:20]:
        ch = s['b'] - s['a']
        print(f"  {s['n']}: {s['a']}% ({s['ay']}) -> {s['b']}% ({s['by']})  [{ch:+.1f}pp]")
    return slope, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points with connecting lines is ideal for
          showing directional change across many countries simultaneously
        - **Country selection**: Countries with survey data near 2000–2006 AND after 2018
        - **Color encoding**: Red/warm tones for countries where top-10% share increased;
          green/cool for those where it fell
        - **Story**: Most Latin American countries reduced top-decile concentration, often sharply
          (Bolivia -13pp, Honduras -12pp). A few Eastern European countries went the other way
          (Bulgaria +8pp). Congo DR bucked the African trend by increasing.
        """
    )
    return


@app.cell
def _(json, slope):
    short_names = {
        "Dominican Republic": "Dominican Rep.",
        "Iran, Islamic Rep.": "Iran",
        "Congo, Dem. Rep.": "Congo DR",
        "Gambia, The": "Gambia"
    }
    out = [{"n": short_names.get(s['n'], s['n']), "a": s['a'], "ay": s['ay'],
            "b": s['b'], "by": s['by']} for s in slope[:23]]
    print(json.dumps(out, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
