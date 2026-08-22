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
        # Patent Applications — China's Rise — Methodology

        Documents the data pipeline for viz-359: trend lines showing patent
        applications by residents, 1985–2021, with China's exponential growth
        as the central story.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IP-PAT-RESD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    label_map = {"Korea, Rep.": "South Korea"}
    countries = ["China", "Japan", "Korea, Rep.", "Germany", "France", "India", "Brazil"]

    filtered = {}
    for country in countries:
        pts = sorted(
            [r for r in data if r["countryName"] == country and r["value"] is not None and r["year"] >= 1985],
            key=lambda x: x["year"]
        )
        every5 = [p for p in pts if p["year"] % 5 == 0]
        last = pts[-1] if pts else None
        if last and last["year"] not in [p["year"] for p in every5]:
            every5.append(last)
        if every5:
            label = label_map.get(country, country)
            filtered[label] = every5

    for name, pts in filtered.items():
        last = pts[-1]
        disp = f"{last['value']/1e6:.3f}M" if last["value"] >= 1e6 else f"{last['value']/1e3:.1f}K"
        print(f"  {name}: {pts[0]['year']}-{last['year']}, latest={disp}")
    return filtered, countries, label_map


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines on sqrt scale — raw counts vary 4 orders of magnitude; sqrt scale lets you see both China's explosive growth and smaller nations' trajectories
        - **Country selection**: Top innovators plus India and Brazil as emerging economies
        - **Time range**: 1985–2021, 5-year intervals — captures the pre-China era, the tipping point (~2010), and the post-2015 dominance
        - **Color**: China accent orange; Japan amber (was leader, now second); South Korea green (rapid rise from zero); others neutral
        - **Highlights**: China filed 350x more patents in 2021 than 1985; Japan filed fewer in 2021 than 2000; India is the next notable riser
        """
    )
    return


@app.cell
def _(json, filtered):
    colors = {
        "China": "#EA5E33",
        "Japan": "#F29A44",
        "South Korea": "#8BAD72",
        "Germany": "#A6C4A2",
        "France": "#C49A45",
        "India": "#5B9E78",
        "Brazil": "#C2C0B5"
    }
    chart_data = [
        {
            "n": name,
            "pts": [{"y": p["year"], "v": round(p["value"])} for p in pts],
            "col": colors.get(name, "#9A9890")
        }
        for name, pts in filtered.items()
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
