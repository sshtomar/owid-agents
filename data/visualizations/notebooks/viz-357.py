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
        # Exclusive Breastfeeding Rates -- Methodology

        Tracks exclusive breastfeeding rates (% of infants under 6 months)
        across developing countries from 1986 to 2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NUT_BF_EBF.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    iso3_names = {
        "IND":"India","BGD":"Bangladesh","NGA":"Nigeria","ETH":"Ethiopia","PAK":"Pakistan",
        "KEN":"Kenya","GHA":"Ghana","ZMB":"Zambia","MOZ":"Mozambique","RWA":"Rwanda",
        "BFA":"Burkina Faso","ZWE":"Zimbabwe","MDG":"Madagascar","MWI":"Malawi",
        "IDN":"Indonesia","VNM":"Vietnam","BOL":"Bolivia","COL":"Colombia",
        "TZA":"Tanzania","COD":"D.R. Congo"
    }
    from collections import defaultdict
    by_country = defaultdict(dict)
    for p in data:
        if p["country"] in iso3_names and p["value"] is not None:
            yr = p["year"]
            c = iso3_names[p["country"]]
            if yr not in by_country[c] or p["value"] > by_country[c][yr]:
                by_country[c][yr] = p["value"]
    print(f"Countries with data: {len(by_country)}")
    return by_country, iso3_names


@app.cell
def _(by_country):
    selected = []
    for name, yr_dict in sorted(by_country.items()):
        pts_list = sorted(yr_dict.items())
        last_yr = pts_list[-1][0]
        if len(pts_list) >= 4 and last_yr >= 2015:
            last_v = pts_list[-1][1]
            selected.append({"n": name, "pts": pts_list, "last": last_v})
    selected.sort(key=lambda x: -x["last"])
    print(f"Countries for chart: {len(selected)}")
    for s in selected[:15]:
        print(f"  {s['n']}: {s['pts'][0][0]}-{s['pts'][-1][0]}, last={s['last']:.1f}%")
    return (selected,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows trajectory over time for multiple countries
        - **Country selection**: 15 developing countries with 4+ data points and recent data
        - **Time range**: 1986-2024 (survey data, so irregular intervals)
        - **Highlights**: Rwanda/Ethiopia maintained high rates; Kenya/Ghana/Zambia had dramatic rises
        """
    )
    return


@app.cell
def _(json, selected):
    chart_data = []
    for s in selected[:15]:
        chart_data.append({
            "n": s["n"],
            "pts": [{"y": yr, "v": round(v, 1)} for yr, v in s["pts"]]
        })
    print(json.dumps(chart_data))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
