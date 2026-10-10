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
        # Bird Species Threatened by Country — Methodology

        Dataset: wb--EN-BIR-THRD-NO (World Bank / IUCN)
        Indicator: Number of bird species classified as threatened, per country, 2022.
        Top 20 countries by count.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-BIR-THRD-NO.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    import re

    def is_real_country(code):
        if not re.match(r'^[A-Z]{2}$', code):
            return False
        excluded_starts = set('ZXVTFSO')
        if code[0] in excluded_starts:
            return False
        return code not in {'OE', '4E', 'EU'}

    yr2022 = sorted(
        [d for d in data if d.get('year') == 2022 and d.get('value') is not None and is_real_country(d.get('country', ''))],
        key=lambda x: -x['value']
    )
    print(f"Countries in 2022: {len(yr2022)}")
    print("Top 5:", [(d['countryName'], int(d['value'])) for d in yr2022[:5]])
    return (yr2022,)


@app.cell
def _(json, yr2022):
    name_map = {
        "Congo, Dem. Rep.": "DR Congo",
        "Korea, Rep.": "South Korea",
        "Iran, Islamic Rep.": "Iran",
        "Cote d'Ivoire": "Côte d'Ivoire",
        "Gambia, The": "Gambia",
        "Congo, Rep.": "Congo",
        "Brunei Darussalam": "Brunei",
    }
    top20 = [
        {"n": name_map.get(d["countryName"], d["countryName"]), "v": int(d["value"])}
        for d in yr2022[:20]
    ]
    print(json.dumps(top20, separators=(",", ":")))
    return (top20,)


if __name__ == "__main__":
    app.run()
