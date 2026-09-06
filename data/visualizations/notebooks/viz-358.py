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
        # Energy Use per Capita, 1990 vs 2023 -- Methodology

        Slope chart comparing per-capita energy use (kg of oil equivalent) across 16 countries.
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
    TARGET = {
        "Iceland": "Iceland",
        "Canada": "Canada",
        "Finland": "Finland",
        "Korea, Rep.": "South Korea",
        "Australia": "Australia",
        "Belgium": "Belgium",
        "Czechia": "Czechia",
        "Iran, Islamic Rep.": "Iran",
        "France": "France",
        "Japan": "Japan",
        "Germany": "Germany",
        "China": "China",
        "Brazil": "Brazil",
        "India": "India",
        "Ethiopia": "Ethiopia",
        "Bangladesh": "Bangladesh",
    }

    by_country = {}
    for r in data:
        cn = r["countryName"]
        if cn in TARGET and r["value"] is not None:
            label = TARGET[cn]
            if label not in by_country:
                by_country[label] = {}
            by_country[label][r["year"]] = r["value"]

    out = []
    for label in TARGET.values():
        pts = by_country.get(label, {})
        a = pts.get(1990)
        b = pts.get(2023) or pts.get(2022)
        if a and b:
            out.append({"n": label, "a": round(a), "b": round(b)})

    out.sort(key=lambda x: x["b"], reverse=True)
    for o in out:
        print(f"{o['n']}: {o['a']} -> {o['b']}")
    return by_country, out, TARGET


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (1990 vs 2023) -- shows two-point change clearly
        - **Country selection**: 16 countries spanning Iceland (geothermal anomaly), rich
          countries that cut usage (Germany, France, Czechia), fast-rising Asia (South Korea,
          China, Iran), and still-low developing countries (India, Bangladesh, Ethiopia)
        - **Story**: Europe decoupled growth from energy; East Asia surged as it industrialized
        """
    )
    return


@app.cell
def _(json, out):
    print(json.dumps(out, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
