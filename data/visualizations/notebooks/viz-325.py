import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # Inflation Across Major Economies (2000-2025)

        Comparing annual consumer price inflation rates for eight diverse economies
        using IMF World Economic Outlook data.

        ## Design rationale

        A multi-line chart is the right choice here because we are comparing
        trajectories over time across countries. The key story is the contrast
        between developed economies that cluster in the 0-5% range and outlier
        economies like Argentina and Turkiye that experience episodes of very
        high inflation. Argentina's 2024 peak at ~220% annual inflation utterly
        dominates the Y axis, but that contrast IS the story -- it shows how
        different monetary policy regimes produce wildly different outcomes.

        Post-COVID inflation spikes in 2022 are visible across all economies,
        including developed ones like the US, UK, and Germany reaching 8-9%.
        """
    )
    return


@app.cell
def _(mo):
    import json
    from pathlib import Path

    dataset_path = Path(mo.notebook_location()) / "public" / "catalog" / "datasets" / "imf--PCPIPCH.json"
    with open(dataset_path) as f:
        raw = json.load(f)

    mo.md(f"Loaded dataset with **{len(raw['data'])}** records.")
    return raw, json, Path


@app.cell
def _(raw):
    targets = ["USA", "GBR", "DEU", "JPN", "BRA", "IND", "TUR", "ARG"]
    name_map = {
        "USA": "United States",
        "GBR": "United Kingdom",
        "DEU": "Germany",
        "JPN": "Japan",
        "BRA": "Brazil",
        "IND": "India",
        "TUR": "Turkiye",
        "ARG": "Argentina",
    }

    filtered = [
        d for d in raw["data"]
        if d["country"] in targets and d["value"] is not None and 2000 <= d["year"] <= 2025
    ]

    chart_data = [
        {"n": name_map.get(d["country"], d["countryName"]), "y": d["year"], "v": round(d["value"], 1)}
        for d in filtered
    ]
    chart_data.sort(key=lambda d: (d["y"], -d["v"]))
    return targets, name_map, filtered, chart_data


@app.cell
def _(mo, filtered, targets, name_map):
    # Summary statistics per country
    rows = []
    for code in targets:
        country_data = [d for d in filtered if d["country"] == code]
        if not country_data:
            continue
        values = [d["value"] for d in country_data]
        name = name_map[code]
        rows.append({
            "Country": name,
            "Records": len(values),
            "Min (%)": round(min(values), 1),
            "Max (%)": round(max(values), 1),
            "Mean (%)": round(sum(values) / len(values), 1),
        })

    header = "| Country | Records | Min (%) | Max (%) | Mean (%) |\n|---|---|---|---|---|\n"
    body = "\n".join(
        f"| {r['Country']} | {r['Records']} | {r['Min (%)']} | {r['Max (%)']} | {r['Mean (%)']} |"
        for r in rows
    )
    mo.md("## Summary Statistics\n\n" + header + body)
    return


@app.cell
def _(mo, json, chart_data):
    mo.md(f"## Exported data\n\n{len(chart_data)} data points for visualization.")
    output = json.dumps(chart_data)
    return (output,)


if __name__ == "__main__":
    app.run()
