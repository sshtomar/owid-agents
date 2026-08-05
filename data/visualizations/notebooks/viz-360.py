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
        # HIV Incidence Rate — Methodology

        Trend lines for 9 series (8 countries + Sub-Saharan Africa regional average), 1990–2024,
        from World Bank indicator SH.HIV.INCD.ZS. Tracks new HIV infections per 1,000 uninfected
        people ages 15–49. Shows the epidemic's peak in the 1990s and subsequent decline.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-HIV-INCD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = ["Eswatini","Botswana","Kenya","Cote d'Ivoire","Central African Republic",
                "Cameroon","Ethiopia","Haiti","Sub-Saharan Africa"]

    by_country = {}
    for r in data:
        c = r["countryName"]
        if c in selected and r["value"] is not None:
            if c not in by_country:
                by_country[c] = {}
            by_country[c][r["year"]] = r["value"]

    for c in selected:
        if c in by_country:
            yrs = by_country[c]
            peak_yr = max(yrs, key=lambda y: yrs[y])
            latest = sorted(yrs.items())[-1]
            print(f"{c}: peak={yrs[peak_yr]:.1f} ({peak_yr}), 2024={latest[1]:.2f}")
    return by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows epidemic trajectory over time
        - **Scale**: Linear (0–55 per 1,000)
        - **Countries**: Hardest-hit countries in southern/eastern Africa + Caribbean + regional average
        - **Highlights**: Eswatini peaked at 50.4/1,000 in 1997; Botswana fell from 50 to 3.1 by 2024
        - Sub-Saharan Africa average shown as dashed line for regional context
        """
    )
    return


if __name__ == "__main__":
    app.run()
