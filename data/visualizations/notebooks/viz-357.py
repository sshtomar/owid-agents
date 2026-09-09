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
        # The Aging World: Old-Age Dependency Ratios 1960-2024 -- Methodology

        Trend lines showing how the ratio of older dependents (65+) per 100
        working-age people (15-64) has evolved across contrasting economies.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    COUNTRIES = {
        'JP': 'Japan', 'DE': 'Germany', 'IT': 'Italy', 'FR': 'France',
        'KR': 'South Korea', 'CN': 'China', 'IN': 'India', 'BR': 'Brazil', 'TD': 'Chad'
    }
    result = []
    for code, label in COUNTRIES.items():
        pts = sorted([x for x in data if x['country'] == code and x['value'] is not None], key=lambda x: x['year'])
        if pts:
            result.append({'n': label, 's': [round(x['value'], 2) for x in pts], 'y0': pts[0]['year']})
            latest = pts[-1]
            print(f"{label}: {pts[0]['year']}-{latest['year']}, last={latest['value']:.1f}")
    return result, COUNTRIES


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines (1960-2024) to show long-run trajectory
        - **Country selection**: Japan (most extreme), Western Europe (high), South Korea
          (rapidly aging from low base), China/Brazil/India (rising), Chad (stays young)
        - **Story**: Japan surged from 9 per 100 workers in 1960 to 51 today.
          South Korea is following the same path decades later. India and Brazil are
          rising slowly while Sub-Saharan Africa (Chad) stays below 5.
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
