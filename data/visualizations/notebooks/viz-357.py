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
        # Energy Use per Capita, 1990-2022 -- Methodology

        Trend lines showing per-capita total energy consumption (kg of oil equivalent)
        for 11 countries across the income spectrum. Highlights the persistent gap
        between high-income nations and low-income ones, and China's dramatic ascent.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected_codes = {'CA', 'AU', 'DE', 'FR', 'IR', 'CN', 'BR', 'IN', 'KE', 'ET', 'BD'}
    name_map = {
        'CA': 'Canada', 'AU': 'Australia', 'DE': 'Germany', 'FR': 'France',
        'IR': 'Iran', 'CN': 'China', 'BR': 'Brazil', 'IN': 'India',
        'KE': 'Kenya', 'ET': 'Ethiopia', 'BD': 'Bangladesh'
    }
    order = ['CA', 'AU', 'DE', 'FR', 'IR', 'CN', 'BR', 'IN', 'KE', 'ET', 'BD']

    by_country = {}
    for pt in data:
        c = pt['country']
        if c not in selected_codes or pt['value'] is None:
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][pt['year']] = pt['value']

    y0, yEnd = 1990, 2022
    chart_data = []
    for c in order:
        if c not in by_country:
            continue
        vals = by_country[c]
        s = [round(vals[y], 1) if y in vals else None for y in range(y0, yEnd + 1)]
        chart_data.append({'n': name_map[c], 'y0': y0, 's': s})
        last = next((v for v in reversed(s) if v is not None), None)
        print(f"{name_map[c]}: 1990={vals.get(1990, 0):.0f}, 2022={last}")
    return chart_data, by_country, name_map, order, selected_codes, y0, yEnd


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines (multi-series) -- shows 32-year trajectory for each country
        - **Country selection**: 11 countries spanning income spectrum; China included for its dramatic rise
        - **Color**: Warm tones for high-energy nations, cool for low-energy
        - **Story**: Canada uses 25x more energy per person than Bangladesh; China tripled from 773 to 2677 koe
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
