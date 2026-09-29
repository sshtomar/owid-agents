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
        # Nuclear Electricity Share: 1990 vs 2023 -- Methodology

        This notebook documents the data pipeline behind viz-358, a slope chart
        comparing nuclear electricity's share of total production between 1990 and
        the most recent year available, revealing which countries are expanding,
        phasing out, or newly adopting nuclear power.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NUCL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    COUNTRIES = [
        "France", "Belgium", "Hungary", "Czechia", "Bulgaria", "Finland",
        "Korea, Rep.", "Slovakia", "Switzerland", "Ukraine", "Sweden",
        "Armenia", "Belarus", "United Kingdom", "United States", "Canada",
        "Japan", "Germany", "China", "India",
    ]
    by_country = {}
    for row in data:
        if row["countryName"] in COUNTRIES and row["value"] is not None:
            by_country.setdefault(row["countryName"], {})[row["year"]] = row["value"]

    print("Available countries:")
    for c in COUNTRIES:
        if c in by_country:
            vs = by_country[c]
            recent_yr = max(y for y in vs if y >= 2020)
            v1990 = vs.get(1990, 0.0)
            print(f"  {c}: 1990={v1990:.1f}%, {recent_yr}={vs[recent_yr]:.1f}%")
    return COUNTRIES, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- before/after comparison at two time points
        - **Before**: 1990 (start of modern post-Cold War energy era)
        - **After**: 2023 or 2024 (most recent year with data)
        - **Color**: Red for decline, green for growth, grey for stable
        - **Highlights**:
          - Germany: 27.7% -> 1.4% (phase-out policy post-Fukushima, completed 2023)
          - Japan: 23.2% -> 9.5% (Fukushima shutdown)
          - France: still dominant at 66.8%
          - Armenia, Belarus: 0% -> ~30% (new plants)
          - Czechia, Bulgaria: grew from lower base
        """
    )
    return


@app.cell
def _(json, COUNTRIES, by_country):
    LABELS = {
        "Korea, Rep.": "South Korea",
        "United Kingdom": "UK",
        "United States": "USA",
    }
    chart_data = []
    for c in COUNTRIES:
        if c not in by_country:
            continue
        vs = by_country[c]
        v1990 = vs.get(1990, 0.0)
        recent_yr = max((y for y in vs if y >= 2020), default=None)
        if recent_yr is None:
            recent_yr = max(vs.keys())
        vrecent = vs[recent_yr]
        label = LABELS.get(c, c)
        chart_data.append({"n": label, "a": round(v1990, 1), "b": round(vrecent, 1), "yr": recent_yr})

    chart_data.sort(key=lambda x: -x["b"])
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
