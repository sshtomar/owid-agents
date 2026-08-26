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
        # Urban Primacy: Share of Urban Population in Largest City, 1995 vs 2022 -- Methodology

        Slope chart comparing urban primacy across 21 countries. Reveals which countries
        concentrate urban life in one dominant city vs. having distributed urban systems.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-URB-LCTY-UR-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = row["value"]

    selected = ["Argentina", "Armenia", "Bangladesh", "Chile", "China",
                "Denmark", "Dominican Republic", "Ecuador",
                "Egypt, Arab Rep.", "Ethiopia", "France", "Germany", "Ghana",
                "Greece", "Hungary", "India", "Indonesia", "Iraq", "Japan",
                "Kenya", "Korea, Rep."]
    name_display = {"Egypt, Arab Rep.": "Egypt", "Korea, Rep.": "South Korea"}

    chart_data = []
    for c in selected:
        yrs = by_country.get(c, {})
        a = yrs.get(1995) or yrs.get(1994) or yrs.get(1996)
        b = yrs.get(2022) or yrs.get(2021) or yrs.get(2023)
        if a is not None and b is not None:
            display = name_display.get(c, c)
            chart_data.append({"n": display, "a": round(a, 0), "b": round(b, 0)})
            diff = b - a
            print(f"{display}: {a:.0f}% -> {b:.0f}% ({'+' if diff>=0 else ''}{diff:.0f} pp)")

    print(f"\nTotal countries: {len(chart_data)}")
    return (by_country, chart_data, name_display, selected)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — shows both the level and direction of change
        - **Country selection**: 21 countries with notable primacy levels or changes
        - **Year pair**: 1995 vs 2022 — covers the post-1990 urbanisation wave
        - **Highlights**: Bangladesh rose from 31% to 42% as Dhaka boomed;
          Ethiopia fell from 27% to 18% as secondary cities grew;
          Germany and China remain near 3-5% with many competing large cities
        - **Color**: Warm tones for rising primacy, cool for stable, amber/terra for falling
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
