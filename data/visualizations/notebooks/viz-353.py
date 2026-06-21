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
        # Homicide Rates in the Americas -- Methodology

        Trend line chart showing intentional homicides per 100,000 people, 1990-2023,
        for 8 countries: 6 in the Americas plus Japan and Germany as low-rate baselines.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-IHR-PSRC-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    print(f"After filtering nulls: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    values = [d["value"] for d in filtered]
    years = sorted(set(d["year"] for d in filtered))
    print(f"Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.1f} - {max(values):.1f} per 100k")
    return values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows full trajectory 1990-2023 including spikes/turning points
        - **Country selection**: 6 high-rate Americas countries + Japan/Germany as safe baselines
        - **Key stories**: Colombia peaked at 86 (1991), now 25; Ecuador stable at 6 until 2019, then surged to 46
        - **Color**: Warm tones for high-rate countries, cool greens for Japan/Germany
        - **Reference line**: 10/100k crisis threshold dashed across chart
        - **Interactivity**: Hover any line shows country + year + rate; other lines dim to 10% opacity
        """
    )
    return


@app.cell
def _(json, filtered):
    picks = {"Jamaica", "Honduras", "Colombia", "Ecuador", "Guatemala", "Brazil", "Japan", "Germany"}
    by_country = {}
    for r in filtered:
        n = r["countryName"]
        if n in picks:
            if n not in by_country:
                by_country[n] = []
            by_country[n].append({"y": r["year"], "v": round(r["value"], 1)})

    chart_data = [{"n": n, "pts": sorted(v, key=lambda p: p["y"])} for n, v in by_country.items()]
    chart_data.sort(key=lambda s: -s["pts"][-1]["v"])
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
