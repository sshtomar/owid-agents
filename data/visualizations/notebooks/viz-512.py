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
        # Cereal Yield 1961–2024 — Methodology

        Trend lines showing cereal yield (kg/hectare) for 12 countries from 1961 to 2024.
        The Green Revolution and subsequent agricultural modernization multiplied yields worldwide.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-YLD-CREL-KG.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    import re
    agg_codes = {'ZH','ZI','ZJ','ZQ','ZT','ZG','ZF','ZE','ZD','ZC','ZB','ZA','OE',
                 '1A','1W','4E','7E','8S','B8','S3','XC','XD','XE','XN','XO','XP','XQ','XT','XU','EU'}
    countries = {}
    for row in data:
        code = row['country']
        if code in agg_codes: continue
        if not re.match(r'^[A-Z]{2}$', code): continue
        if row['value'] is None: continue
        n = row['countryName']
        if n not in countries: countries[n] = {}
        countries[n][row['year']] = row['value']
    selected = ['China', 'India', 'Bangladesh', 'Brazil', 'Germany',
                'France', 'Argentina', 'Ethiopia', 'Japan', 'Indonesia',
                'Australia', 'Egypt, Arab Rep.']
    chart_data = []
    for name in selected:
        if name not in countries: continue
        yv = countries[name]
        pts = [{'y': y, 'v': round(v)} for y, v in sorted(yv.items()) if 1961 <= y <= 2024]
        short_name = name.replace(', Arab Rep.', '')
        chart_data.append({'n': short_name, 'pts': pts})
    for cd in chart_data:
        p0, p1 = cd['pts'][0]['v'], cd['pts'][-1]['v']
        pct = (p1 - p0) / p0 * 100
        print(f"{cd['n']}: {p0} -> {p1} kg/ha (+{pct:.0f}%)")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the full 63-year trajectory of the Green Revolution
          and its aftermath.
        - **Country selection**: Diverse mix of large agricultural producers across regions.
          Egypt stands out as already having high yields in 1961 (Nile irrigation). Japan
          started highest among developing countries but grew least. China's trajectory is
          the steepest in absolute terms.
        - **Color encoding**: Improvement band by % yield growth from 1961 to 2024.
          China's 445% growth gets the deepest green.
        - **Story**: The Green Revolution transformed food production globally. China's
          yield grew 5x; even Ethiopia—starting from a very low base—nearly quadrupled.
          Australia shows high climate volatility with erratic year-to-year swings.
        """
    )
    return


if __name__ == "__main__":
    app.run()
