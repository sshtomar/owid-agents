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
        # Deindustrialization: Manufacturing's Shrinking Share of GDP -- Methodology

        Slope chart comparing early-1990s vs. 2024 manufacturing value added as % of GDP
        for 10 countries. Uses World Bank indicator NV.IND.MANF.ZS.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-IND-MANF-ZS.json"
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

    target = ['China', 'Germany', 'Korea, Rep.', 'Brazil', 'India', 'France',
              'Japan', 'Indonesia', 'Bangladesh', 'Canada']

    results = []
    for c in target:
        if c not in by_country:
            print(f"MISSING: {c}")
            continue
        yvals = by_country[c]
        early_candidates = [y for y in yvals if 1990 <= y <= 2000]
        late_candidates = [y for y in yvals if y >= 2020]
        if not early_candidates or not late_candidates:
            print(f"SKIPPING {c}")
            continue
        ey = min(early_candidates)
        ly = max(late_candidates)
        results.append({"n": c, "a": yvals[ey], "ay": ey, "b": yvals[ly], "by": ly})

    results.sort(key=lambda x: -x['a'])
    print(f"\n{len(results)} countries:")
    for r in results:
        pp = r['b'] - r['a']
        sign = "+" if pp >= 0 else ""
        print(f"  {r['n']}: {r['a']:.1f}% ({r['ay']}) -> {r['b']:.1f}% ({r['by']})  {sign}{pp:.1f}pp")
    return by_country, results, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- two-point comparison shows which countries
          gained or lost industrial share in roughly 30 years.
        - **Country selection**: Spans advanced economies (Germany, Japan, France),
          middle-income (Brazil, Indonesia), and emerging manufacturers (Bangladesh, India).
          Korea is the outlier that maintained its manufacturing share.
        - **Time points**: Early 1990s (first available year) vs. most recent 2020+.
        - **Highlights**: Bangladesh nearly doubled its manufacturing share (13% -> 22%)
          as garment exports boomed; France fell from 16% to just under 10% (deindustrialization);
          Korea is remarkably stable at ~25-27%, bucking the rich-country trend.
        """
    )
    return


@app.cell
def _(json, results):
    print(json.dumps(results, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
