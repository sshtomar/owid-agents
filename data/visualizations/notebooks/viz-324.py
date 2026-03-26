import marimo
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    return (mo,)

@app.cell
def _(mo):
    mo.md("""# Malaria Incidence in High-Burden Countries

Estimated malaria cases per 1,000 population at risk, from the WHO Global Health Observatory (MALARIA_EST_INCIDENCE).

## Design Rationale

A line chart is the best choice here: it shows trends over time (2000-2024) for multiple countries simultaneously.
The key story is Rwanda's dramatic decline from ~180 in 2000 to ~37 in 2011, followed by a sharp resurgence
to ~308 in 2015 and ~213 in 2020. Ethiopia and India also show large declines. Most West/Central African
countries remain at high levels throughout the period.""")
    return

@app.cell
def _():
    import json
    return (json,)

@app.cell
def _(json, mo):
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--MALARIA_EST_INCIDENCE.json"
    _text = _path.read_text()
    _raw = json.loads(_text)
    meta = _raw["meta"]
    all_data = _raw["data"]
    mo.md(f"**{meta['title']}** -- {len(all_data)} total rows")
    return (meta, all_data)

@app.cell
def _(all_data, json, mo):
    _targets = ["UGA", "MOZ", "GHA", "NER", "TZA", "ETH", "RWA", "CMR", "NGA", "IND"]
    _name_map = {
        "UGA": "Uganda", "MOZ": "Mozambique", "GHA": "Ghana", "NER": "Niger",
        "TZA": "Tanzania", "ETH": "Ethiopia", "RWA": "Rwanda", "CMR": "Cameroon",
        "NGA": "Nigeria", "IND": "India"
    }
    _filtered = [d for d in all_data if d["country"] in _targets and d["value"] is not None]
    chart_data = [
        {"n": _name_map[d["country"]], "y": d["year"], "v": round(d["value"] * 10) / 10}
        for d in _filtered
    ]
    chart_data.sort(key=lambda d: (d["y"], -d["v"]))

    _countries = sorted(set(d["n"] for d in chart_data))
    _years = sorted(set(d["y"] for d in chart_data))
    mo.md(f"""## Summary Statistics

- **Countries**: {', '.join(_countries)}
- **Year range**: {min(_years)}-{max(_years)}
- **Data points**: {len(chart_data)}
- **Peak value**: {max(d['v'] for d in chart_data)} (per 1,000 pop at risk)
- **Lowest value**: {min(d['v'] for d in chart_data)}
""")
    return (chart_data,)

@app.cell
def _(chart_data, json, mo):
    chart_json = json.dumps(chart_data)
    mo.md(f"Exported {len(chart_data)} data points as JSON for the HTML visualization.")
    return (chart_json,)

if __name__ == "__main__":
    app.run()
