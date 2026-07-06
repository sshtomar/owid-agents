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
        # Anemia in Non-Pregnant Women — Methodology

        Slope chart comparing anemia prevalence among non-pregnant women (ages 15–49) in 2000 vs. 2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-ANM-NPRG-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    countries = sorted(set(d["countryName"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    values = [d["value"] for d in filtered]
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.1f} - {max(values):.1f}%")
    return countries, filtered, values, years


@app.cell
def _(filtered):
    selected = ["Gabon", "Benin", "Cote d'Ivoire", "India", "Ghana", "Cameroon",
                "Bangladesh", "Kenya", "Indonesia", "Brazil", "Ethiopia", "China", "Germany", "Australia"]
    slope_data = []
    for c in selected:
        rows_2000 = [x for x in filtered if x["countryName"] == c and x["year"] == 2000]
        rows_latest = [x for x in filtered if x["countryName"] == c and x["year"] >= 2020]
        if rows_2000 and rows_latest:
            a = round(rows_2000[0]["value"], 1)
            b = round(sorted(rows_latest, key=lambda x: -x["year"])[0]["value"], 1)
            slope_data.append({"n": c, "a": a, "b": b})
            print(f"{c}: {a}% -> {b}% ({b-a:+.1f}pp)")
    return slope_data, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — clearly shows direction and magnitude of change per country
        - **Countries**: 14 countries ranging from high-burden Africa to low-burden Europe/Australia
        - **Highlights**: India (50% → 54%) is the most prominent country where anemia worsened.
          Brazil (31% → 21%) and Ghana (46% → 35%) show the largest improvements. Germany and
          Australia are included to anchor the low end of the scale.
        - **Color**: Warm tones for worsening; cool/green for improvement
        """
    )
    return


@app.cell
def _(json, slope_data):
    print(json.dumps(slope_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
