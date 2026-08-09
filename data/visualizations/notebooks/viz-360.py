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
        # Sex Ratio at Birth -- Methodology

        Trend lines showing male births per female birth for countries with
        historically elevated sex ratios (son preference). World Bank SP.POP.BRTH.MF.
        Biological norm is ~1.05.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-BRTH-MF.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = ['China', 'Korea, Rep.', 'Azerbaijan', 'Armenia', 'India',
                'Albania', 'Viet Nam', 'Georgia', 'Japan']
    filtered = [r for r in data if r["value"] is not None and r["countryName"] in selected]
    print(f"Filtered to {len(filtered)} rows for {len(set(r['countryName'] for r in filtered))} countries")
    return (filtered,)


@app.cell
def _(filtered):
    years = sorted(set(d["year"] for d in filtered))
    values = [d["value"] for d in filtered]
    print(f"Year range: {years[0]}-{years[-1]}")
    print(f"Ratio range: {min(values):.4f} - {max(values):.4f}")
    print(f"Biological norm: ~1.05")
    return years, values


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows how son preference changed over decades
        - **Country selection**: Countries with documented son-preference via ultrasound sex selection
        - **Reference line**: 1.05 biological norm
        - **Key story**: South Korea normalized; China and Azerbaijan still well above norm
        - **Subsampled**: Every 5 years to reduce HTML size while preserving trend shape
        """
    )
    return


@app.cell
def _(json, filtered):
    from collections import defaultdict
    SAMPLE_YEARS = set(range(1960, 2025, 5)) | {2024}
    series = defaultdict(dict)
    for r in filtered:
        if r["year"] in SAMPLE_YEARS:
            name = r["countryName"].replace(", Rep.", "").replace("Korea", "South Korea").replace("Viet Nam", "Vietnam")
            series[name][r["year"]] = r["value"]
    chart_data = [
        {"n": name, "pts": [{"y": y, "v": round(v, 4)} for y, v in sorted(pts.items())]}
        for name, pts in series.items()
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
