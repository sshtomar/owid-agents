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
        # The Labor Force Gender Gap, 2022 — Methodology

        Paired bar chart comparing male and female labor force participation rates
        for countries with the widest and narrowest gender gaps in 2022.
        """
    )
    return


@app.cell
def _(json, mo):
    path_m = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-TLF-CACT-MA-ZS.json"
    path_f = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-TLF-CACT-FE-ZS.json"
    dm = json.loads(path_m.read_text())
    df = json.loads(path_f.read_text())
    print(f"Male: {len(dm['data'])} rows, Female: {len(df['data'])} rows")
    return dm, df


@app.cell
def _(dm, df):
    exclude_kw = ['IDA', 'IBRD', 'Sub-Saharan', 'Least developed', 'Heavily indebted', 'Low income', 'Lower middle',
                  'Africa Eastern', 'Africa Western', 'dividend', 'Fragile', 'World', 'Upper middle',
                  'East Asia', 'South Asia', 'Latin America', 'Middle East', 'Europe', 'Central Asia',
                  'Arab World', 'Caribbean', 'Pacific', 'North America', 'OECD', 'Euro area',
                  'demographic', 'developing', 'small states', 'High income', 'Post-demographic',
                  'Central Europe', 'European Union']

    def get_2022(dataset):
        return {r['countryName']: round(r['value'], 1)
                for r in dataset['data']
                if r['value'] is not None and r['year'] == 2022 and r['country'] and len(r['country']) == 2
                and not any(kw.lower() in r['countryName'].lower() for kw in exclude_kw)}

    male_2022 = get_2022(dm)
    female_2022 = get_2022(df)
    both = [(c, male_2022[c], female_2022[c]) for c in male_2022 if c in female_2022]
    both.sort(key=lambda x: x[1] - x[2], reverse=True)
    chart_data = [{'n': c.replace('Egypt, Arab Rep.', 'Egypt').replace('Iran, Islamic Rep.', 'Iran').replace('Congo, Dem. Rep.', 'D.R. Congo').replace('Bahamas, The', 'Bahamas').replace('Gambia, The', 'Gambia'), 'm': m, 'f': f, 'gap': round(m - f, 1)}
                  for c, m, f in (both[:10] + both[-10:])]
    print(f"Total countries: {len(both)}, selected 20")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Paired horizontal bars — directly shows both rates and the gap between them
        - **Country selection**: 10 widest gaps + 10 narrowest to show the full spectrum
        - **Key story**: MENA and South Asia dominate the high-gap group; Sub-Saharan Africa shows near-parity
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
