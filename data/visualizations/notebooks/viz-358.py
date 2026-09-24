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
        # Old-Age Dependency Ratio — Methodology

        Trend lines showing the old-age dependency ratio (elderly people per 100 working-age
        adults) for 9 countries from 1960 to 2024. Japan is the extreme outlier.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
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
               'excluding','G7','G20','HIPC','Heavy']
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
        "Japan", "Italy", "Germany", "Finland", "France",
        "Korea, Rep.", "China", "Brazil", "India"
    ]
    label_map = {"Korea, Rep.": "South Korea"}

    years = list(range(1960, 2025))
    chart_data = []
    for cn in selected:
        if cn not in countries:
            print(f"MISSING: {cn}")
            continue
        cd = countries[cn]
        series = [round(cd[y], 1) if y in cd else None for y in years]
        label = label_map.get(cn, cn)
        chart_data.append({"n": label, "s": series, "y0": 1960})
        print(f"{cn}: 1960={cd.get(1960,'?'):.1f}, 2000={cd.get(2000,'?'):.1f}, 2024={cd.get(2024,'?'):.1f}")

    return chart_data, label_map, selected, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines over 64 years — essential to show the slow structural shift
          that separates aging countries from developing ones
        - **Country selection**: Japan (extreme outlier at 50.7%), three large W. European
          nations, Finland (also high), South Korea (fastest rising), China, Brazil, India
          (different trajectories from the global south)
        - **Time range**: 1960–2024; full range available and all selected countries have
          complete data
        - **Highlights**: Japan tripled its ratio from 8.9% (1960) to 50.7% (2024);
          South Korea is rising fastest among developing nations
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
