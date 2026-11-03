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
        # Stock Market Capitalization (% of GDP) — Methodology

        This notebook documents the data pipeline behind viz-512.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--CM-MKT-LCAP-GD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_codes = {'OE','XC','XD','XF','XG','XH','XJ','XN','XO','XP','XQ','XT','XU',
                 'ZF','ZG','ZH','ZI','ZJ','ZQ','ZT'}
    by_c = {}
    for r in data:
        if r['value'] is not None and r['country'] not in agg_codes:
            by_c.setdefault(r['countryName'], {})[r['year']] = r['value']
    print(f"Countries: {len(by_c)}")
    targets = ['Japan', 'Germany', 'India', 'Canada', 'Australia', 'Korea, Rep.',
               'France', 'Brazil', 'China', 'Israel']
    for c in targets:
        if c in by_c:
            ys = by_c[c]
            pts = sorted(ys.items())
            print(f"  {c}: {pts[0][0]}-{pts[-1][0]}, latest={pts[-1][1]:.1f}%")
    return agg_codes, by_c, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — highlights long-run growth with crash events visible
        - **Country selection**: 10 major economies; Hong Kong excluded (financial hub, 1000%+ of GDP)
        - **Time range**: 1975–2024 (start of World Bank data)
        - **Highlights**: Japan bubble (1989), dot-com bust (2000), GFC (2008), India surge (2024)
        - **Story**: Stock markets have grown dramatically relative to GDP since the 1990s
        """
    )
    return


@app.cell
def _(by_c, json, targets):
    out = []
    for c in targets:
        if c in by_c:
            ys = by_c[c]
            pts = [{"y": yr, "v": round(val, 1)} for yr, val in sorted(ys.items())]
            name = 'South Korea' if c == 'Korea, Rep.' else c
            if len(pts) >= 10:
                out.append({"n": name, "pts": pts})
    print(json.dumps(out, separators=(",", ":")))
    return (out,)


if __name__ == "__main__":
    app.run()
