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
        # UHC Service Coverage Index 2023 — Methodology

        Horizontal bar chart showing WHO's Universal Health Coverage index for 35 countries with 2023 data.
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
    iso_names = {
        'NZL': 'New Zealand', 'NOR': 'Norway', 'NLD': 'Netherlands', 'CHN': 'China',
        'KWT': 'Kuwait', 'CRI': 'Costa Rica', 'ARE': 'UAE', 'BRB': 'Barbados',
        'COL': 'Colombia', 'UKR': 'Ukraine', 'BHS': 'Bahamas', 'UZB': 'Uzbekistan',
        'TTO': 'Trinidad & Tobago', 'ZAF': 'South Africa', 'KGZ': 'Kyrgyzstan',
        'VNM': 'Vietnam', 'DZA': 'Algeria', 'MNG': 'Mongolia', 'IND': 'India',
        'ARM': 'Armenia', 'PER': 'Peru', 'BOL': 'Bolivia', 'FSM': 'Micronesia',
        'NPL': 'Nepal', 'KEN': 'Kenya', 'PAK': 'Pakistan', 'COM': 'Comoros',
        'GNQ': 'Eq. Guinea', 'TZA': 'Tanzania', 'LBR': 'Liberia', 'BDI': 'Burundi',
        'SDN': 'Sudan', 'COD': 'DR Congo', 'CAF': 'C. African Rep.', 'ETH': 'Ethiopia'
    }
    region_codes = {'AFR', 'AMR', 'EUR', 'EMR', 'SEAR', 'WPR', 'WB_HI', 'WB_LMI', 'WB_NAR', 'WB_UMI', 'GLB'}

    yr2023 = [r for r in data if r['year'] == 2023 and r['value'] is not None and r['country'] not in region_codes and r['country'] in iso_names]
    chart_data = sorted(
        [{'n': iso_names[r['country']], 'v': r['value']} for r in yr2023],
        key=lambda x: -x['v']
    )
    print(f"Countries with 2023 data: {len(chart_data)}")
    print(f"Range: {chart_data[-1]['v']} (lowest: {chart_data[-1]['n']}) to {chart_data[0]['v']} (highest: {chart_data[0]['n']})")
    return chart_data, iso_names, region_codes, yr2023


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — best for ranked categorical comparison across many entities
        - **Country selection**: All 35 individual countries with 2023 UHC index data (excluding WHO/World Bank regional aggregates)
        - **Color encoding**: Green gradient for high scores (≥80), amber for mid-range (50–69), red for lowest (<40)
        - **Key story**: New Zealand and Norway lead at 89; Ethiopia scores 33 — a 56-point gap reflecting structural health system differences
        - **Reference lines**: Dashed lines at 50 and 80 mark meaningful thresholds
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
