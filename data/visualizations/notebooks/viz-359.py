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
        # Intentional Homicides — Methodology

        Documents the trend lines visualization showing homicide rate
        trajectories for 8 countries from 2000 to 2023.
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
    import re
    country_data = {}
    for pt in data:
        code = pt["country"]
        if re.match(r"^[A-Z]{2}$", code) and pt["value"] is not None:
            cn = pt["countryName"]
            yr = pt["year"]
            if cn not in country_data:
                country_data[cn] = {}
            country_data[cn][yr] = pt["value"]
    focus = ["Colombia", "Honduras", "Jamaica", "Ecuador", "Brazil", "Estonia", "Finland", "Japan"]
    for cn in focus:
        if cn in country_data:
            v2000 = country_data[cn].get(2000, "N/A")
            v2023 = country_data[cn].get(2023, "N/A")
            print(f"{cn}: 2000={v2000}, 2023={v2023}")
    return cn, code, country_data, focus, pt, re, v2000, v2023, yr


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — yearly data 2000–2023 shows trajectories clearly
        - **Country selection**: Mix of high-rate (Latin America) and low-rate (Europe, Asia) for contrast; Ecuador chosen for its alarming recent rise
        - **Color**: Warm tones for high-rate, cool for improving, grey for already-low
        - **Story**: Colombia's reform success; Ecuador's crisis (drug trafficking explosion); Jamaica's persistent high rate; Japan near zero throughout
        """
    )
    return


@app.cell
def _(country_data, focus, json):
    years = list(range(2000, 2024))
    chart_data = []
    for name in focus:
        if name in country_data:
            pts = [{"y": yr, "v": round(country_data[name][yr], 2)} for yr in years if yr in country_data[name]]
            if len(pts) >= 10:
                chart_data.append({"n": name, "pts": pts})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, name, pts, years, yr


if __name__ == "__main__":
    app.run()
