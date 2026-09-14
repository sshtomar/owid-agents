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
        # Youth Population Share (Ages 0–14) — Methodology

        Trend lines for 13 countries spanning all stages of the demographic transition,
        from Sub-Saharan Africa's high-youth populations to East Asia's dramatic declines.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-0014-TO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    SELECT = {'ET': 'Ethiopia', 'BF': 'Burkina Faso', 'CD': 'Congo, Dem. Rep.',
              'IN': 'India', 'ID': 'Indonesia', 'BD': 'Bangladesh',
              'BR': 'Brazil', 'AR': 'Argentina', 'CN': 'China',
              'DE': 'Germany', 'IT': 'Italy', 'JP': 'Japan', 'KR': 'Korea, Rep.'}

    by_country = defaultdict(list)
    for row in data:
        if row['country'] in SELECT and row['value'] is not None:
            by_country[row['country']].append(row)

    chart_data = []
    for cc, cname in SELECT.items():
        rows = sorted(by_country.get(cc, []), key=lambda r: r['year'])
        pts = [{'y': r['year'], 'v': round(r['value'], 1)} for r in rows if r['year'] % 5 == 0 or r['year'] == rows[-1]['year']]
        if pts:
            chart_data.append({'n': cname, 'pts': pts})

    print(f"Series: {[s['n'] for s in chart_data]}")
    for s in chart_data:
        print(f"  {s['n']}: {s['pts'][0]['v']}% (1960) → {s['pts'][-1]['v']}% (2024)")
    return chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — 65-year demographic story
        - **Country selection**: Diverse — Sub-Saharan Africa (still 40-46%), South/SE Asia (transitioning), Latin America (declining), East Asia/Europe (very low, aging)
        - **Color grouping**: Warm = high-youth countries, cool = aging countries
        - **Key story**: South Korea fell from 41% to 11% — the fastest-ever demographic transition. DRC has stayed near 46% for 60 years.
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
