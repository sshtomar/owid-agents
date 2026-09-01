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
        # Energy Use Per Capita 1990–2024 — Methodology

        Trend lines showing divergent energy consumption trajectories across 10 countries.
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
    targets = {
        'Iceland': 'Iceland', 'Canada': 'Canada', 'Finland': 'Finland',
        'Korea, Rep.': 'South Korea', 'Australia': 'Australia',
        'Germany': 'Germany', 'Japan': 'Japan',
        'China': 'China', 'Brazil': 'Brazil', 'India': 'India'
    }
    from collections import defaultdict
    by_country = defaultdict(list)
    for r in data:
        if r['value'] is not None and r['countryName'] in targets:
            by_country[r['countryName']].append({'y': r['year'], 'v': round(r['value'])})
    chart_data = [
        {'n': targets[c], 'pts': sorted(by_country[c], key=lambda x: x['y'])}
        for c in targets if c in by_country
    ]
    for item in chart_data:
        first, last = item['pts'][0], item['pts'][-1]
        change = (last['v'] - first['v']) / first['v'] * 100
        print(f"  {item['n']}: {first['v']} ({first['y']}) -> {last['v']} ({last['y']}) ({change:+.0f}%)")
    return by_country, chart_data, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows 34-year trajectory for 10 countries
        - **Country selection**: High-income declining nations (Iceland, Canada, Germany, Japan, Australia), rising Asia (China, South Korea), and low-income growing (India, Brazil)
        - **Key stories**:
          - Iceland's geothermal/hydro economy produces the highest per-capita figure (~16,000 kg)
          - China tripled from 773 kg (1990) to 2,851 kg (2023) — the steepest rise
          - Germany declined from 4,422 to 2,825 — energy efficiency at work
          - India at 763 kg remains far below developed nations despite steady growth
        - **Y-axis**: 0–20,000 kg oil equivalent to show full range including Iceland outlier
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
