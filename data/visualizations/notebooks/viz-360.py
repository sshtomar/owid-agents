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
        # DTP Immunization Coverage — Methodology

        Trend lines showing the share of children aged 12–23 months vaccinated against
        diphtheria, tetanus, and pertussis (DTP) for 12 countries from 1980 to 2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-IMM-IDPT.json"
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

    eligible = {cn: d for cn, d in countries.items() if 1980 in d and 2023 in d}
    print(f"Countries with 1980-2023 data: {len(eligible)}")
    return countries, eligible, is_agg


@app.cell
def _(eligible):
    selected = [
        "Haiti", "Afghanistan", "India", "Bolivia",
        "Bhutan", "Iran, Islamic Rep.", "Jamaica", "Brazil",
        "Cuba", "Hungary", "Denmark", "Japan"
    ]
    label_map = {"Iran, Islamic Rep.": "Iran"}

    years = list(range(1980, 2024))
    chart_data = []
    for cn in selected:
        if cn not in eligible:
            print(f"NOT ELIGIBLE: {cn}")
            continue
        cd = eligible[cn]
        series = [round(cd[y], 1) if y in cd else None for y in years]
        label = label_map.get(cn, cn)
        chart_data.append({"n": label, "s": series, "y0": 1980})
        print(f"{cn}: 1980={cd[1980]:.0f}%, 2023={cd[2023]:.0f}%")

    return chart_data, label_map, selected, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the convergence story over 44 years
        - **Country selection**: Haiti and Afghanistan anchor the low end (still below 65%);
          Bhutan and Iran show dramatic rises from ~6–32% to 99%; developed nations
          (Hungary, Denmark, Japan) provide the upper benchmark
        - **Time range**: 1980–2023; all selected countries have data for the full range
        - **100% reference line**: Dashed horizontal at 100% as a target benchmark
        - **Highlights**: Bhutan rose from 6% (1980) to 99% (2023);
          Iran rose from 32% to 99%; Haiti has stagnated at 48–65% for decades
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
