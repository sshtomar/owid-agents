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
        # Age Dependency Ratio Since 1960 -- Methodology

        Trend lines showing the ratio of dependents (children + elderly) to the
        working-age population across world regions. Sub-Saharan Africa's persistent
        high ratio contrasts with East Asia's dramatic fall -- the "demographic dividend".
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND.json"
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

    selected = [
        "Sub-Saharan Africa",
        "Middle East & North Africa",
        "South Asia",
        "Latin America & Caribbean",
        "East Asia & Pacific",
        "Europe & Central Asia",
        "Japan",
        "China",
    ]
    years = list(range(1960, 2025, 5))
    years[-1] = 2024

    result = []
    for c in selected:
        if c in by_country:
            vals = by_country[c]
            pts = [{"y": y, "v": round(vals[y], 1)} for y in years if y in vals]
            if pts:
                result.append({"n": c, "pts": pts})

    for r in result:
        pts = r["pts"]
        print(f"{r['n']}: {pts[0]['y']}={pts[0]['v']} -> {pts[-1]['y']}={pts[-1]['v']}")
    return by_country, result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows trajectory over 64 years clearly
        - **Series**: 6 World Bank regions + Japan and China for individual-country contrast
        - **Key stories**:
          - Sub-Saharan Africa: persistently high (~79-95%) -- 1 worker supporting 4-5 dependents
          - East Asia/China: dramatic fall from 80% to 43% -- classic demographic dividend
          - Japan: rising again (now elderly-driven) after falling through 1990s
          - Latin America and South Asia: converging toward Europe levels
        - **Threshold**: dashed line at 50% -- below = more workers than dependents
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
