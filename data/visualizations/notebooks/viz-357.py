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
        # UHC Service Coverage Index: ~2000 vs ~2023 -- Methodology

        Slope chart comparing the WHO Universal Health Coverage Service Coverage Index
        for countries that have observations near 2000 and near 2023. Highlights
        rapid gains in low-income countries versus smaller improvements from already
        high baselines.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--UHC_INDEX_REPORTED.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    # ISO 3-letter code -> display name for selected countries
    selected = {
        'NPL': 'Nepal',
        'IND': 'India',
        'COM': 'Comoros',
        'ETH': 'Ethiopia',
        'CHN': 'China',
        'PAK': 'Pakistan',
        'PRY': 'Paraguay',
        'NOR': 'Norway',
        'CUB': 'Cuba',
        'ECU': 'Ecuador',
        'CRI': 'Costa Rica',
        'NLD': 'Netherlands',
        'MNG': 'Mongolia',
        'DZA': 'Algeria',
        'JOR': 'Jordan',
    }

    by_country = {}
    for row in data:
        c = row['country']
        if c in selected and row['value'] is not None:
            if c not in by_country:
                by_country[c] = {}
            by_country[c][row['year']] = row['value']

    slope = []
    for code, name in selected.items():
        yrs = by_country.get(code, {})
        a = next((yrs[y] for y in [2000, 2001, 2002] if y in yrs), None)
        b = next((yrs[y] for y in [2023, 2022, 2021] if y in yrs), None)
        if a is not None and b is not None:
            slope.append({'n': name, 'a': int(a), 'b': int(b)})

    slope.sort(key=lambda x: x['a'])
    print(f"Series: {len(slope)}")
    for s in slope:
        print(f"  {s['n']}: {s['a']} -> {s['b']} ({s['b']-s['a']:+d} pts)")
    return slope, by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (~2000 vs ~2023) to highlight gains across
          the coverage spectrum
        - **Color**: Diverging green-amber ramp by improvement magnitude
        - **Story**: Nepal (+40 pts), India (+33), Comoros (+27) are the standout
          improvers. Norway and Netherlands advanced from already high bases.
          Jordan is the only country in the selection that slightly declined.
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
