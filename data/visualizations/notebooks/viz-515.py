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
        # ATMs per 100,000 Adults — Methodology

        This notebook documents the data pipeline behind viz-515.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--FB-ATM-TOTL-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_codes = {'OE','XC','XD','XF','XG','XH','XJ','XN','XO','XP','XQ','XT','XU',
                 'ZF','ZG','ZH','ZI','ZJ','ZQ','ZT','B8','Z7','T7','S4','V4','V1','V2',
                 'V3','T5','T6','T3','F2','1A','XI','XE','XL','XM','EU','8S'}
    by_c = {}
    for r in data:
        if r['value'] is not None and r['country'] not in agg_codes:
            by_c.setdefault(r['countryName'], {})[r['year']] = r['value']
    print(f"Countries: {len(by_c)}")
    return agg_codes, by_c


@app.cell
def _(by_c):
    targets = ['Japan', 'Germany', 'France', 'Australia', 'Canada', 'Korea, Rep.',
               'Brazil', 'India', 'China', 'Indonesia', 'Kenya', 'Ghana']
    for c in targets:
        if c in by_c:
            ys = by_c[c]
            yrs = sorted(ys.keys())
            vals = [ys[y] for y in yrs]
            peak = max(vals)
            peak_yr = yrs[vals.index(peak)]
            latest = ys[max(yrs)]
            trend = "declining" if latest < peak * 0.92 else "growing"
            print(f"  {c}: peak={peak:.0f} ({peak_yr}), latest={latest:.0f} [{trend}]")
    return (targets,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows rise, peak, and (for developed economies) decline
        - **Country selection**: 12 countries across income levels showing different trajectories
        - **Time range**: 2004–2023 (World Bank data window)
        - **Key insight**: Wealthy nations (Japan, Germany, France, Australia) are past peak ATM density
        - **Story**: Mobile banking is replacing physical ATMs in developed countries; emerging economies still expanding
        """
    )
    return


@app.cell
def _(by_c, json, targets):
    out = []
    for c in targets:
        if c in by_c:
            ys = by_c[c]
            series = [round(ys[2004 + j], 1) if (2004 + j) in ys else None for j in range(20)]
            while series and series[-1] is None:
                series.pop()
            valid = [v for v in series if v is not None]
            if len(valid) >= 8:
                name = 'South Korea' if c == 'Korea, Rep.' else c
                out.append({"n": name, "s": series, "y0": 2004})
    print(json.dumps(out, separators=(",", ":")))
    return (out,)


if __name__ == "__main__":
    app.run()
