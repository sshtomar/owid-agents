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
        # Under-5 Mortality: Male vs Female (2023) — Methodology

        Documents the data pipeline behind viz-511.
        Compares male and female under-5 mortality rates across 92 countries to reveal the gender survival gap.
        """
    )
    return


@app.cell
def _(json, mo):
    fe_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-MORT-FE.json"
    ma_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-MORT-MA.json"
    fe_raw = json.loads(fe_path.read_text())
    ma_raw = json.loads(ma_path.read_text())
    fe_data = fe_raw["data"]
    ma_data = ma_raw["data"]
    print(f"Female dataset: {len(fe_data)} points")
    print(f"Male dataset: {len(ma_data)} points")
    return fe_data, fe_raw, ma_data, ma_raw


@app.cell
def _(fe_data, ma_data):
    agg_words = ['Africa', 'Asia', 'Europe', 'income', 'dividend', 'IDA', 'IBRD',
                 'states', 'situations', 'blend', 'Pacific', 'Caribbean', 'Euro',
                 'Latin', 'Middle', 'Eastern', 'Western', 'Central', 'Southern',
                 'Northern', 'OECD', 'World', 'classification', 'heavily']

    def is_country(name):
        return not any(w.lower() in name.lower() for w in agg_words)

    fe_2023 = {p['country']: p['value'] for p in fe_data if p.get('year') == 2023 and p.get('value') is not None}
    ma_2023 = {p['country']: p['value'] for p in ma_data if p.get('year') == 2023 and p.get('value') is not None}
    fe_names = {p['country']: p['countryName'] for p in fe_data if p.get('year') == 2023}

    common = set(fe_2023.keys()) & set(ma_2023.keys())
    pts = []
    for code in common:
        name = fe_names.get(code, code)
        if is_country(name) and name:
            pts.append({'c': name, 'f': round(fe_2023[code], 1), 'm': round(ma_2023[code], 1)})

    pts.sort(key=lambda x: -x['f'])
    pts = [p for p in pts if p['f'] > 1]
    print(f"Final scatter points: {len(pts)}")
    return agg_words, common, fe_2023, fe_names, is_country, ma_2023, pts


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Scatter plot — each dot is a country, position shows (female rate, male rate)
        - **Key insight**: In nearly all countries, boys face higher under-5 mortality than girls
        - **Diagonal line**: equality line; countries above it have higher male than female mortality
        - **Color**: Warm orange/red for high-mortality countries, cool green for low-mortality
        - **Story**: Only India is very slightly below the line; everywhere else boys are more vulnerable
        """
    )
    return


@app.cell
def _(json, pts):
    print(json.dumps(pts, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
