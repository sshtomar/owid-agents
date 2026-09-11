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
    mo.md("# Solar Installed Capacity Sparkline Grid — Methodology\n\nSparkline grid of top 24 countries by installed solar capacity (GW), 2000–2025. Data from Ember.")
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--CAP-SOLAR.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    agg_keywords = ["World", "income", "countries", "states", "dividend", "IBRD", "IDA",
                    "Asia", "Africa", "Latin", "Arab", "OECD", "Euro", "Heavily", "Caribbean",
                    "Sub-Saharan", "Eastern", "Western", "Central", "Northern", "Middle"]
    by_country = {}
    for row in data:
        c = row["countryName"]
        if any(kw in c for kw in agg_keywords) or row["value"] is None:
            continue
        by_country.setdefault(c, {})[row["year"]] = row["value"]

    top24 = sorted(by_country.items(), key=lambda x: x[1].get(2025, x[1].get(2024, 0)), reverse=True)[:24]
    labels = {"United States of America": "USA", "United Kingdom": "UK", "Viet Nam": "Vietnam", "South Korea": "S. Korea"}

    chart_data = []
    for cname, lookup in top24:
        years = list(range(2000, 2026))
        series = [round(lookup.get(y, 0), 2) for y in years]
        nm = labels.get(cname, cname)
        chart_data.append({"n": nm, "s": series, "e": series[0], "l": series[-1], "y0": 2000})

    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
