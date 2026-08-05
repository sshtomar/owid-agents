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
        # Decline in Open Defecation — Methodology

        Slope chart comparing % of population practicing open defecation in 2000 vs 2022,
        from World Bank indicator SH.STA.ODFC.ZS. Shows countries with the most dramatic
        sanitation progress and those where the problem persists.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-ODFC-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected_names = ['Cambodia','Burkina Faso','India','Ethiopia','Chad','Benin',
                      'Cabo Verde','Haiti','Guinea-Bissau','Bolivia','Indonesia',
                      'Ghana','Bangladesh']

    by_country = {}
    for r in data:
        c = r["countryName"]
        if c in selected_names and r["value"] is not None:
            if c not in by_country:
                by_country[c] = {}
            by_country[c][r["year"]] = r["value"]

    def get_nearest(yrs, target):
        for off in [0, -1, 1, -2, 2]:
            if target + off in yrs:
                return round(yrs[target + off], 2)
        return None

    chart_data = []
    for c in selected_names:
        if c not in by_country:
            continue
        yrs = by_country[c]
        a = get_nearest(yrs, 2000)
        b = get_nearest(yrs, 2022)
        if a is not None and b is not None:
            chart_data.append({"n": c, "a": a, "b": b})
            print(f"{c}: {a:.1f}% → {b:.1f}% (−{a-b:.1f}pp)")
    return by_country, chart_data, selected_names


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compares 2000 vs 2022 for countries that started high
        - **Countries**: Selected where 2000 rate exceeded 15% to show meaningful change
        - **Colors**: Diverging green-to-red based on percentage-point decline
        - **Highlights**: Cambodia −76pp, India −61pp (Swachh Bharat campaign); Chad nearly unchanged at 63%
        """
    )
    return


if __name__ == "__main__":
    app.run()
