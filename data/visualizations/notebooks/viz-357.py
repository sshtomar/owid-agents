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
        # Population Growth Rate, 1970–2024 -- Methodology

        Trend lines showing annual population growth (%) for eight major economies.
        Reveals the global demographic transition: Japan and South Korea now in
        negative growth, China just crossed zero, while Ethiopia remains above 2.5%.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-GROW.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    picks = {
        'JP': 'Japan', 'DE': 'Germany', 'KR': 'Korea',
        'CN': 'China', 'BR': 'Brazil', 'IN': 'India',
        'ET': 'Ethiopia', 'CA': 'Canada'
    }
    by_code = {}
    for row in data:
        if row['country'] in picks and row['value'] is not None and row['year'] >= 1970:
            code = row['country']
            if code not in by_code:
                by_code[code] = []
            by_code[code].append({"y": row['year'], "v": round(row['value'], 3)})

    chart = []
    for code, name in picks.items():
        if code in by_code:
            pts = sorted(by_code[code], key=lambda x: x['y'])
            chart.append({"n": name, "pts": pts})

    for s in chart:
        last = s['pts'][-1]
        print(f"  {s['n']}: latest {last['y']} = {last['v']:+.3f}%")
    return chart, picks, by_code


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows continuous trajectory from 1970 to 2024
        - **Country selection**: Mix of shrinking (Japan, Germany, Korea), slowing (China, India, Brazil),
          and still-growing (Ethiopia) economies, plus Canada as a stable immigration-driven case
        - **Reference line**: 0% drawn in medium grey to make the crossing point obvious
        - **Color scheme**: Warm tones for countries now negative or near-zero; cool green for still-growing
        - **Story**: The speed of convergence toward zero (and below) is the insight — it took Japan 30 years;
          China may have reached it within a decade of policy reversal
        """
    )
    return


@app.cell
def _(json, chart):
    print(json.dumps(chart, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
