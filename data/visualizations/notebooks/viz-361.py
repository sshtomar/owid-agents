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
        # Energy Use per Capita — Methodology

        Trend lines showing energy use (kg of oil equivalent per person) for 10 countries
        from 1990 to 2023. Shows the dramatic divergence between rich, stable users and
        rapidly rising developing economies.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_kw = ['income','region','world','small states','fragile','developing','IBRD','IDA','OECD',
               'Pacific','Africa','Asia','Caribbean','Americas','Arab','Saharan','Central','South',
               'North','East','West','Latin','Europe','dividend','blend','states','average','total',
               'excluding','G7','G20','HIPC']
    def is_agg(cn):
        return any(kw.lower() in cn.lower() for kw in skip_kw)

    countries = {}
    for row in data:
        cn = row["countryName"]
        if is_agg(cn) or row["value"] is None:
            continue
        if cn not in countries:
            countries[cn] = {}
        countries[cn][row["year"]] = row["value"]

    print(f"Individual countries: {len(countries)}")
    return countries, is_agg


@app.cell
def _(countries):
    selected = [
        "Canada", "Australia", "Germany", "France", "Japan",
        "Korea, Rep.", "China", "Brazil", "India", "Bangladesh"
    ]
    label_map = {"Korea, Rep.": "South Korea"}

    years = list(range(1990, 2024))
    chart_data = []
    for cn in selected:
        if cn not in countries:
            print(f"MISSING: {cn}")
            continue
        cd = countries[cn]
        series = [int(round(cd[y])) if y in cd else None for y in years]
        label = label_map.get(cn, cn)
        chart_data.append({"n": label, "s": series, "y0": 1990})
        v1990 = cd.get(1990)
        v_latest = None
        for y in range(2023, 2017, -1):
            if y in cd:
                v_latest = cd[y]
                break
        if v1990 and v_latest:
            print(f"{cn}: {v1990:.0f} -> {v_latest:.0f} kg OE ({((v_latest/v1990)-1)*100:.0f}%)")

    return chart_data, label_map, selected, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the 33-year structural divergence between
          countries that have plateaued or declined and those still rising
        - **Country selection**: Three high-use (Canada, Australia, Germany) showing plateau
          or decline; two mid-range declining (France, Japan); South Korea showing dramatic
          rise; China's transformation; Brazil/India/Bangladesh as developing comparators
        - **Time range**: 1990–2023
        - **Highlights**: South Korea tripled from 2,088 to 5,337 kg OE; China grew 3.7x
          from 773 to 2,851; Germany fell 34% from 4,422 to 2,928; Bangladesh at 288 is
          still only 4% of Canada's usage
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
