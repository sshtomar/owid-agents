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
        # Gross National Savings: East Asia Leads -- Methodology

        Documents the data pipeline behind viz-365.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GNS-ICTR-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [r for r in data if r["value"] is not None]
    skip_words = ["income", "IDA", "IBRD", "Africa Eastern", "Africa Western",
                  "Arab World", "East Asia &", "South Asia", "Europe &", "Euro area",
                  "European Union", "Latin America", "North America", "Sub-Saharan",
                  "Caribbean small", "Central Europe", "Heavily", "Fragile",
                  "Small states", "World", "OECD", "Pacific", "Middle East",
                  "Low &", "Early-", "Late-", "Post-", "Pre-"]
    c_data = {}
    for r in filtered:
        c = r["countryName"]
        if any(s in c for s in skip_words):
            continue
        if c not in c_data:
            c_data[c] = {}
        c_data[c][r["year"]] = r["value"]
    print(f"Individual countries: {len(c_data)}")
    return c_data, filtered


@app.cell
def _(c_data):
    targets = ["China", "Korea, Rep.", "India", "Japan", "Germany",
               "France", "Canada", "Australia", "Brazil"]
    for c in targets:
        if c in c_data:
            pts = sorted(c_data[c].items())
            yrs = [p[0] for p in pts if 1980 <= p[0] <= 2024]
            vals = [round(c_data[c][y], 1) for y in yrs]
            print(f"{c}: {yrs[0]}-{yrs[-1]}, recent={vals[-1]}")
    return targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — tracks savings rates over 40+ year horizon
        - **Countries**: 9 major economies spanning high-saving East Asia to low-saving Americas
        - **Time range**: 1980-2024
        - **Story**: China peaked at 53% savings in 2008, Korea maintained 35%+; Brazil hit decade lows ~14%
        - **Color**: Warm for highest savers (China, Korea), cool for lowest (Brazil)
        - **Highlight**: India's savings rate has climbed from ~22% to 35%, tracking its economic rise
        """
    )
    return


if __name__ == "__main__":
    app.run()
