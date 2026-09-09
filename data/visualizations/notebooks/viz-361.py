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
        # Labor Productivity: GDP per Worker 1991-2024 -- Methodology

        Trend lines showing GDP per person employed (constant 2021 PPP $) from
        1991 to 2024. Reveals the dramatic convergence of East Asian economies
        and the relative stagnation of Southern Europe.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-GDP-PCAP-EM-KD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    TARGET = {
        'DE': 'Germany', 'FR': 'France', 'IT': 'Italy',
        'JP': 'Japan', 'KR': 'South Korea',
        'AU': 'Australia', 'CN': 'China', 'BR': 'Brazil', 'IN': 'India'
    }
    result = []
    for code, label in TARGET.items():
        pts = sorted([x for x in data if x['country'] == code and x['value'] is not None and x['year'] >= 1991], key=lambda x: x['year'])
        if pts:
            result.append({'n': label, 's': [round(x['value'] / 1000, 1) for x in pts], 'y0': pts[0]['year']})
            first, last = pts[0], pts[-1]
            growth = (last['value'] / first['value'] - 1) * 100
            print(f"{label}: ${first['value']:,.0f} ({first['year']}) -> ${last['value']:,.0f} ({last['year']}) = {growth:.0f}% growth")
    return result, TARGET


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines (1991-2024), values in thousands for readability
        - **Story**: China's worker output grew 14-fold (from $3k to $46k). South Korea
          converged toward Western European levels ($36k to $98k). Italy barely moved
          ($114k to $130k, 15% over 33 years). Japan also stagnated relatively.
          India and Brazil show steady but slow improvement.
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
