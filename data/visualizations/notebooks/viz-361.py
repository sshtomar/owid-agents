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
        # Electricity from Natural Gas (1990–2024) -- Methodology

        Documents the data pipeline behind viz-361.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NGAS-ZS.json"
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
    print(f"Value range: {min(values):.1f}% - {max(values):.1f}%")
    return countries, filtered, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- tracking % of electricity from gas 1990-2024
        - **Country selection**: Mix of gas-dominant MENA countries (Algeria, Iran, Egypt),
          European transitions (Italy, Greece), and fuel-diverse countries (China, India, Germany)
        - **Story**: Algeria/Iran/Egypt have always run on gas. Italy shifted up sharply.
          Israel built gas infrastructure from scratch. India and China barely use gas.
        """
    )
    return


@app.cell
def _(json, filtered):
    target = [
        "Italy", "Japan", "Germany", "France", "Greece", "China",
        "Algeria", "Iran, Islamic Rep.", "Egypt, Arab Rep.", "Bangladesh",
        "Israel", "India"
    ]
    labels = {"Iran, Islamic Rep.": "Iran", "Egypt, Arab Rep.": "Egypt"}
    chart_data = []
    for name in target:
        pts = sorted([d for d in filtered if d["countryName"] == name], key=lambda x: x["year"])
        if not pts:
            continue
        sampled = [p for p in pts if (p["year"] - 1990) % 2 == 0 or p["year"] == 2024]
        sampled = sorted(sampled, key=lambda x: x["year"])
        label = labels.get(name, name)
        vals = [round(p["value"], 1) for p in sampled]
        chart_data.append({"n": label, "s": vals, "y0": sampled[0]["year"], "step": 2})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
