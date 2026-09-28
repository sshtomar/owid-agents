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
        # Income Share Held by the Poorest 20% -- Methodology

        Slope chart comparing early-2000s vs. recent income share for the bottom quintile
        across 13 countries. Uses World Bank indicator SI.DST.FRST.20.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-DST-FRST-20.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    print(f"After filtering nulls: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for x in filtered:
        by_country[x['countryName']][x['year']] = round(x['value'], 2)

    selected = [
        'Colombia', 'Honduras', 'Brazil', 'Argentina', 'Chile',
        'Germany', 'Kenya', 'China', 'France', 'Indonesia',
        'Finland', 'Czechia', 'India'
    ]

    results = []
    for c in selected:
        if c not in by_country:
            print(f"MISSING: {c}")
            continue
        yvals = by_country[c]
        early = {y: v for y, v in yvals.items() if 1993 <= y <= 2005}
        late = {y: v for y, v in yvals.items() if y >= 2016}
        if not early or not late:
            print(f"SKIPPING {c}: no early or late data")
            continue
        ey = max(early.keys())
        ly = max(late.keys())
        results.append({"n": c, "a": yvals[ey], "ay": ey, "b": yvals[ly], "by": ly})

    results.sort(key=lambda x: x['b'])
    print(f"\n{len(results)} countries selected")
    for r in results:
        pp = r['b'] - r['a']
        sign = "+" if pp >= 0 else ""
        print(f"  {r['n']}: {r['a']}% ({r['ay']}) -> {r['b']}% ({r['by']})  {sign}{pp:.1f}pp")
    return by_country, results, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- two-point comparison makes the before/after contrast
          immediately readable; coloring by direction of change adds a quick summary layer.
        - **Country selection**: Deliberately spans the full range: Latin America's highly
          unequal distribution (Colombia 3.2%, Honduras 3.7%) vs. Czechia/India at 9-10%.
          European countries show a slight recent decline suggesting middle-class squeeze.
        - **Time points**: ~2004 (most common early measurement) vs. ~2022-2024 (most recent).
        - **Highlights**: Latin American countries cluster below 6%; India's poor receive
          over 10% -- one of the highest shares globally; European countries are losing ground.
        """
    )
    return


@app.cell
def _(json, results):
    print(json.dumps(results, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
