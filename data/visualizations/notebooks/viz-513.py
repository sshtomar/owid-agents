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
        # Hydropower Slope Chart — Methodology

        Slope chart comparing electricity from hydropower (TWh) in 2000 vs 2024
        for the top 15 hydro-producing countries (viz-513).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-HYDRO.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(json, data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for pt in data:
        if pt["value"] is not None:
            by_country[pt["countryName"]][pt["year"]] = pt["value"]

    top15 = [
        "China", "Brazil", "Canada", "United States of America",
        "Russian Federation (the)", "India", "Norway", "Viet Nam",
        "Japan", "Turkey", "Venezuela (Bolivarian Republic of)",
        "France", "Sweden", "Ethiopia", "Tajikistan"
    ]

    name_map = {
        "United States of America": "USA",
        "Russian Federation (the)": "Russia",
        "Viet Nam": "Vietnam",
        "Venezuela (Bolivarian Republic of)": "Venezuela",
    }

    chart_data = []
    for name in top15:
        display = name_map.get(name, name)
        if name in by_country and 2000 in by_country[name] and 2024 in by_country[name]:
            chart_data.append({
                "n": display,
                "a": round(by_country[name][2000], 1),
                "b": round(by_country[name][2024], 1),
            })

    chart_data.sort(key=lambda x: -x["b"])
    values = [x["b"] for x in chart_data]
    print(f"Countries: {len(chart_data)}, range: {min(values):.1f}-{max(values):.1f} TWh")
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
