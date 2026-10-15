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
        # Services Sector GDP Share Slope Chart — Methodology

        Slope chart comparing services value added (% of GDP) in 1990 vs 2022
        across 24 countries with the largest absolute change.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-SRV-TOTL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_terms = ['income', 'World', 'OECD', 'IDA', 'IBRD', 'Pacific', 'Arab', 'Caribbean',
                  'states', 'region', 'countries', 'dividend', 'fragile', 'small', 'Africa Eastern',
                  'Africa Western', 'Middle East', 'Latin America', 'South Asia', 'Sub-Saharan',
                  'North America', 'Euro area', 'European Union']
    countries = {}
    for row in data:
        c = row['countryName']
        if row['value'] is not None and not any(x.lower() in c.lower() for x in skip_terms):
            if c not in countries:
                countries[c] = {}
            countries[c][row['year']] = round(row['value'], 1)
    good = {c: v for c, v in countries.items() if 1990 in v and 2022 in v}
    print(f"Countries with 1990 and 2022 data: {len(good)}")
    diffs = {c: v[2022] - v[1990] for c, v in good.items()}
    sorted_by_change = sorted(diffs.items(), key=lambda x: abs(x[1]), reverse=True)[:24]
    for c, delta in sorted_by_change[:5]:
        print(f"  {c}: {good[c][1990]:.1f} -> {good[c][2022]:.1f} (Δ{delta:+.1f}pp)")
    return countries, diffs, good, sorted_by_change


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compares two time points, shows direction of structural change
        - **Threshold line**: 50% marks when services overtake agriculture + industry combined
        - **Notable stories**: Georgia and Bulgaria shifted from ~33% to ~60%; Chad reversed from 50% to 28%
        - **Color**: Orange-red = services rising fast (structural shift); green = services falling (resource economies)
        """
    )
    return


if __name__ == "__main__":
    app.run()
