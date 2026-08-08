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
        # Raised Fasting Blood Glucose Prevalence, ~2006 — Methodology

        This notebook documents the data pipeline behind viz-361.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NCD_GLUC_04.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    # Filter to 2006 (best single-year coverage: 36 country-level entries)
    # Exclude regional aggregates (non 3-letter codes)
    by_country = defaultdict(list)
    for p in data:
        if p["year"] == 2006 and p["value"] is not None and len(p["country"]) == 3:
            by_country[p["country"]].append(p["value"])
    averaged = {c: round(sum(vs)/len(vs), 1) for c, vs in by_country.items()}
    sorted_countries = sorted(averaged.items(), key=lambda x: x[1], reverse=True)
    print(f"Countries in 2006: {len(sorted_countries)}")
    print("Top 10:", sorted_countries[:10])
    return averaged, by_country, sorted_countries


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — single-year country ranking
        - **Year selected**: 2006 (peak single-year coverage: 36 entries)
        - **Indicator**: % of adults with fasting blood glucose >= 7.0 mmol/L (diagnostic threshold for diabetes)
        - **Story**: Pacific island states and Middle Eastern countries show the highest prevalence, driven by dietary transitions and rising obesity
        - **Threshold line**: 7% marked as a clinical risk indicator
        """
    )
    return


@app.cell
def _(json, sorted_countries):
    cmap = {
        'FJI': 'Fiji', 'SLB': 'Solomon Is.', 'BHS': 'Bahamas', 'TUR': 'Turkey',
        'TUN': 'Tunisia', 'MYS': 'Malaysia', 'BRN': 'Brunei', 'MDV': 'Maldives',
        'ARG': 'Argentina', 'GAB': 'Gabon', 'CUB': 'Cuba', 'THA': 'Thailand',
        'UZB': 'Uzbekistan', 'NPL': 'Nepal', 'RUS': 'Russia', 'DJI': 'Djibouti',
        'BLR': 'Belarus', 'EST': 'Estonia', 'LVA': 'Latvia', 'MNE': 'Montenegro',
        'LKA': 'Sri Lanka', 'HRV': 'Croatia', 'CZE': 'Czech Rep.', 'SEN': 'Senegal',
        'PER': 'Peru', 'ISR': 'Israel', 'SWE': 'Sweden', 'DEU': 'Germany',
        'FRA': 'France', 'LSO': 'Lesotho', 'SOM': 'Somalia', 'NGA': 'Nigeria',
        'GBR': 'UK',
    }
    # Exclude regional codes (EMR etc.)
    chart_data = [{"n": cmap[c], "v": v} for c, v in sorted_countries if c in cmap]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
