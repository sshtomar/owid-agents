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
        # International Tourism Arrivals — Methodology

        Trend lines showing international tourist arrivals (millions) for 10 major
        destinations from 1995 to 2020. The COVID-19 crash in 2020 is the central story.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
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
               'excluding','G7','G20','HIPC','Euro']
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
    # Select 10 major destinations with 2019 + 2020 data
    # France/Hungary/Croatia excluded: their data counts same-day crossings, inflating totals
    selected = [
        "China", "Italy", "Hong Kong SAR, China", "Germany", "Japan",
        "Greece", "Austria", "Korea, Rep.", "Australia", "Indonesia"
    ]
    label_map = {
        "Hong Kong SAR, China": "Hong Kong",
        "Korea, Rep.": "South Korea"
    }

    years = list(range(1995, 2021))
    chart_data = []
    for cn in selected:
        if cn not in countries:
            print(f"MISSING: {cn}")
            continue
        cd = countries[cn]
        series = [round(cd[y] / 1e6, 2) if y in cd else None for y in years]
        label = label_map.get(cn, cn)
        chart_data.append({"n": label, "s": series, "y0": 1995})
        v2019 = cd.get(2019, 0)
        v2020 = cd.get(2020, 0)
        print(f"{cn}: 2019={v2019/1e6:.1f}M, 2020={v2020/1e6:.1f}M ({((v2020/v2019)-1)*100:.0f}%)")

    return chart_data, label_map, selected, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the full 1995–2020 growth trajectory and the
          2020 collapse in a single view
        - **Country selection**: Top 10 by 2019 arrivals among countries with both 2019 and 2020
          data; excluded France, Hungary, Croatia because their figures count same-day border
          crossings, making them outliers not comparable to the other destinations
        - **Time range**: 1995–2020; data stops here because 2021+ was recovery and many
          countries have gaps
        - **Highlights**: China grew from 46M to 163M; Hong Kong fell 94% in 2020; Japan
          fell 87%; Italy fell 60%
        - **COVID shading**: Vertical band over 2020 in accent color at low opacity
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
