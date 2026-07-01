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
        # Breast Cancer 5-Year Survival Rates 2021 — Methodology

        Horizontal bar chart showing 5-year net survival rates for breast cancer
        by country and WHO income/regional grouping. Highlights the stark
        gap between high-income countries (87%) and low-income countries (42%).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--CANCERSURVIVAL_BREASTCANCER.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    groups = {
        'GLOBAL': 'Global', 'WB_HI': 'High income', 'WB_UMI': 'Upper-middle income',
        'WB_LMI': 'Lower-middle income', 'WB_LI': 'Low income',
        'AFR': 'Sub-Saharan Africa', 'AMR': 'Americas', 'EUR': 'Europe',
        'SEAR': 'South-East Asia', 'WPR': 'Western Pacific', 'EMR': 'East Mediterranean',
    }
    countries_sel = {
        'USA': 'USA', 'AUS': 'Australia', 'GBR': 'UK', 'JPN': 'Japan',
        'CHN': 'China', 'BRA': 'Brazil', 'IND': 'India',
        'ZAF': 'South Africa', 'TZA': 'Tanzania', 'NGA': 'Nigeria',
    }

    by_cc = {r['country']: r['value'] for r in data if r['value']}
    bar_data = []
    for cc, name in {**groups, **countries_sel}.items():
        if cc in by_cc:
            t = 'group' if cc in groups else 'country'
            bar_data.append({'n': name, 'v': round(by_cc[cc], 1), 'type': t})

    bar_data.sort(key=lambda x: -x['v'])
    print("Survival rates:")
    for b in bar_data:
        tag = "(group)" if b['type'] == 'group' else ""
        print(f"  {b['n']} {tag}: {b['v']}%")
    return bar_data, groups, countries_sel, by_cc


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — easy comparison across many entries
        - **Color**: Orange spectrum for countries by survival rate; cool green for groups/regions
        - **Reference line**: Global average (77.8%) as a dashed vertical line
        - **Story**: Japan, USA, Australia all exceed 90%. Nigeria at 27.7% reflects
          late-stage diagnosis (most women present with advanced disease) and limited
          oncology infrastructure. The income-group gap (87% vs 42%) is the starkest divide.
        """
    )
    return


@app.cell
def _(json, bar_data):
    print(json.dumps(bar_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
