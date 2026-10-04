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
        # Energy Use per Capita -- Methodology

        Tracks energy consumption per capita (kg of oil equivalent)
        from 1990 to 2020 across countries spanning the full income range.
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
    selected_countries = [
        "Iceland","Canada","Korea, Rep.","Germany",
        "China","Brazil","Mexico","India","Bangladesh","Chad"
    ]
    name_map = {"Korea, Rep.": "South Korea"}
    from collections import defaultdict
    by_country = defaultdict(dict)
    for p in data:
        if p["countryName"] in selected_countries and p["value"] is not None:
            by_country[p["countryName"]][p["year"]] = p["value"]

    chart_data = []
    for country in selected_countries:
        if country in by_country:
            yr_dict = by_country[country]
            pts_sorted = sorted(yr_dict.items())
            sampled = [(yr, v) for yr, v in pts_sorted if yr % 5 == 0]
            display_name = name_map.get(country, country)
            chart_data.append({"n": display_name, "pts": [{"y": yr, "v": round(v, 0)} for yr, v in sampled]})
    print(f"Series: {len(chart_data)}")
    for s in chart_data:
        print(f"  {s['n']}: {s['pts'][0]['v']} -> {s['pts'][-1]['v']} kg oe")
    return chart_data, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows divergence over time
        - **Country selection**: 10 countries from richest (Iceland ~16k) to poorest (Chad ~200) energy users
        - **Time range**: 1990-2020, sampled every 5 years for clarity
        - **Highlights**: China's rapid climb; Germany's steady decline via efficiency; gap between rich and poor
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data))
    return


if __name__ == "__main__":
    app.run()
