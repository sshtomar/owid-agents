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
        # Nuclear Electricity: Diverging Paths 1990-2024 -- Methodology

        Trend lines showing the % of electricity generated from nuclear sources
        for key nuclear nations, revealing sharply different policy trajectories.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NUCL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    COUNTRIES = {
        'FR': 'France', 'HU': 'Hungary', 'FI': 'Finland',
        'BE': 'Belgium', 'KR': 'South Korea', 'DE': 'Germany',
        'JP': 'Japan', 'CN': 'China'
    }
    result = []
    for code, label in COUNTRIES.items():
        pts = sorted([x for x in data if x['country'] == code and x['value'] is not None and x['year'] >= 1990], key=lambda x: x['year'])
        if pts:
            result.append({'n': label, 's': [round(x['value'], 2) for x in pts], 'y0': pts[0]['year']})
            print(f"{label}: {pts[0]['year']}-{pts[-1]['year']}, 1990={pts[0]['value']:.1f}%, last={pts[-1]['value']:.1f}%")
    return result, COUNTRIES


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines (1990-2024) to show policy divergence
        - **Key events**: Fukushima (2011) annotation marks Japan's sudden crash
        - **Story**: France maintained ~65-78% throughout; Germany deliberately
          phased out nuclear (28% in 1990 → ~1.4% in 2023); Japan collapsed after
          Fukushima (32% → near 0%) then slowly recovered; China grew from 0% to 4.6%
          and is rapidly building new capacity.
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
