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
        # Patent Applications by Residents — Methodology

        This notebook documents the pipeline behind the trend-lines visualization of
        resident patent applications across 10 major innovating countries, 2000–2021.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IP-PAT-RESD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    exclude = ['East ', 'West ', 'World', ' income', 'OECD', ' Asia', 'Africa', 'Europe',
               'America', 'Pacific', 'Arab', 'Caribbean', 'IDA', 'IBRD', 'fragile',
               'Fragile', 'Heavily', 'HIPC', 'small states', 'Sub-Saharan', 'Latin',
               'Central ', 'Developing', 'dividend', 'North America', 'South Asia', 'Middle East']

    pts = [p for p in data if p['value'] is not None and not any(t in p.get('countryName','') for t in exclude)]
    by_country = defaultdict(dict)
    for p in pts:
        by_country[p['countryName']][p['year']] = p['value']

    focus = ['China', 'Japan', 'Korea, Rep.', 'Germany', 'India', 'France',
             'Iran, Islamic Rep.', 'Brazil', 'Italy', 'Indonesia']
    name_map = {'Korea, Rep.': 'South Korea', 'Iran, Islamic Rep.': 'Iran'}

    chart_data = []
    for c in focus:
        if c not in by_country:
            continue
        vals = by_country[c]
        pts_list = [{'y': yr, 'v': round(vals[yr])} for yr in range(2000, 2022) if yr in vals]
        if len(pts_list) >= 10:
            name = name_map.get(c, c)
            chart_data.append({'n': name, 'pts': pts_list})

    print(f"Series: {len(chart_data)}")
    for s in chart_data:
        first = s['pts'][0]
        last = s['pts'][-1]
        print(f"  {s['n']}: {first['v']:,} ({first['y']}) -> {last['v']:,} ({last['y']})")
    return chart_data, by_country, pts


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with log-scale Y axis — the range spans 157 (Indonesia 2000)
          to 1,426,644 (China 2021), making linear scale unreadable.
        - **Country selection**: 10 countries covering the largest patent filers in 2021
          and notable risers (India, Iran, Indonesia).
        - **Time range**: 2000–2021 — the period of China's extraordinary rise from 5th to dominant.
        - **Story**: China grew 56x in 21 years; Japan declined 40%; India grew 12x from a low base.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
