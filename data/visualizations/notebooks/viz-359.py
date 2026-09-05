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
        # Gross Savings as % of GDP, 1980-2023 -- Methodology

        Trend lines showing national saving rates for major economies over four decades.
        Reveals the stark divergence between East Asian high-savers and the West.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GNS-ICTR-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    selected = ['China', 'Korea, Rep.', 'Germany', 'Japan', 'India', 'France', 'Brazil']

    by_country = defaultdict(dict)
    for p in data:
        if p['countryName'] in selected and p['value'] is not None:
            by_country[p['countryName']][p['year']] = p['value']

    result = []
    for c in selected:
        yrs = by_country.get(c, {})
        series = []
        for yr in range(1980, 2024):
            v = yrs.get(yr)
            series.append(round(v, 1) if v is not None else None)
        display = c.replace('Korea, Rep.', 'South Korea')
        result.append({'n': display, 's': series, 'y0': 1980})

    for r in result:
        vals = [v for v in r['s'] if v is not None]
        recent = [v for v in r['s'][-5:] if v is not None]
        print(f"{r['n']}: avg={sum(vals)/len(vals):.1f}%, recent={sum(recent)/len(recent):.1f}%")
    return result, by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines to show long-run savings dynamics
        - **Country selection**: Mix of high-saving East Asia, major European economies, Brazil
        - **Story**: China's savings rate climbed from ~34% in the early 1980s to over 51%
          at its peak in 2008, far exceeding any other large economy. South Korea has held
          a consistently high 30-40%. Brazil has been in long-run structural savings decline.
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
