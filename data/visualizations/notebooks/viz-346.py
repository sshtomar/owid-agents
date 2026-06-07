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

        Paired bar chart comparing male and female labor force participation rates.
        Datasets: wb--SL-TLF-CACT-MA-ZS and wb--SL-TLF-CACT-FE-ZS (World Bank, 1990-2024)
        """
    )
    return


@app.cell
def _(json, mo):
    path_m = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-TLF-CACT-MA-ZS.json"
    path_f = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-TLF-CACT-FE-ZS.json"
    dm = json.loads(path_m.read_text())
    df = json.loads(path_f.read_text())
    return dm, df


@app.cell
def _(dm, df):
    exclude_kw = ['IDA', 'IBRD', 'Sub-Saharan', 'Least developed', 'Heavily indebted', 'Low income',
                  'Africa Eastern', 'Africa Western', 'dividend', 'Fragile', 'World',
                  'East Asia', 'South Asia', 'Latin America', 'Middle East', 'Europe', 'Central Asia',
                  'Arab World', 'Caribbean', 'Pacific', 'North America', 'OECD', 'Euro area',
                  'demographic', 'High income', 'Central Europe', 'European Union']

    def get_2022(dataset):
        return {r['countryName']: round(r['value'], 1)
                for r in dataset['data']
                if r['value'] is not None and r['year'] == 2022 and r['country'] and len(r['country']) == 2
                and not any(kw.lower() in r['countryName'].lower() for kw in exclude_kw)}

    male_2022 = get_2022(dm)
    female_2022 = get_2022(df)
    both = [(c, male_2022[c], female_2022[c]) for c in male_2022 if c in female_2022]
    both.sort(key=lambda x: x[1] - x[2], reverse=True)
    chart_data = [{'n': c, 'm': m, 'f': f, 'gap': round(m - f, 1)}
                  for c, m, f in (both[:10] + both[-10:])]
    return (chart_data,)


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
