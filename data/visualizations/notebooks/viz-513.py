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
        # Disaster-Induced Internal Displacement -- Methodology

        Sparkline grid showing annual new displacement caused by natural disasters
        for 16 countries with the highest cumulative totals (2008-2023).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-IDP-NWDS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    SKIP = [
        "IDA","IBRD","income","Sub-","Asia Pacific","Europe","Pacific","America",
        "World","dividend","blend","Euro area","OECD","Arab World","Middle East",
        "Caribbean","Fragility","Conflict","Violence","Least developed","Heavily",
        "HIPC","South Asia","countries:","small states","Saharan","Eastern","Western",
        "Central","Northern","Organisation","only","Late-","Pre-","Early-",
        "Upper","Lower","High income","Low income","IDA & IBRD","excluding high",
        "Africa Eastern","Africa Western","East Asia","&"
    ]
    def is_country(row):
        name = row["countryName"]
        return not any(kw in name for kw in SKIP)

    country_data = [r for r in data if is_country(r)]
    country_years = {}
    for r in country_data:
        c = r["countryName"]
        if c not in country_years:
            country_years[c] = {}
        if r["value"] is not None:
            country_years[c][r["year"]] = r["value"]

    years = list(range(2008, 2024))
    totals = {c: sum(yd.values()) for c, yd in country_years.items()}
    sorted_countries = sorted(totals.items(), key=lambda x: -x[1])
    print("Top 20 countries:")
    for c, total in sorted_countries[:20]:
        print(f"  {c}: {total/1e6:.1f}M")
    return country_years, countries_data, is_country, sorted_countries, totals, years


@app.cell
def _(country_years, json, years):
    SELECTED = [
        "China","India","Bangladesh","Indonesia","Haiti","Colombia",
        "Japan","Brazil","Ethiopia","Kenya","Congo, Dem. Rep.",
        "Honduras","Afghanistan","Chile","Cambodia","Iran, Islamic Rep."
    ]
    NAME_MAP = {
        "Congo, Dem. Rep.": "DR Congo",
        "Iran, Islamic Rep.": "Iran",
    }

    chart_data = []
    for c in SELECTED:
        if c in country_years:
            yd = country_years[c]
            series = [yd.get(y, 0) for y in years]
            total = sum(series)
            peak = max(series)
            chart_data.append({
                "n": NAME_MAP.get(c, c),
                "s": series,
                "y0": 2008,
                "total": round(total / 1e6, 1),
                "peak": round(peak / 1e6, 2),
            })

    print(f"Chart data: {len(chart_data)} countries")
    for cd in chart_data:
        print(f"  {cd['n']}: total={cd['total']}M, peak={cd['peak']}M/yr")

    print()
    print("JSON:")
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
