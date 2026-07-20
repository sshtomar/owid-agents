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
        # Railway Network Size, 1995–2021 — Methodology

        Trend lines comparing total railway route-km for 7 major networks,
        highlighting China's dramatic expansion against stable or shrinking European networks.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IS-RRS-TOTL-KM.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    target_map = {
        "China": "China", "India": "India", "Germany": "Germany",
        "France": "France", "Kazakhstan": "Kazakhstan",
        "Iran, Islamic Rep.": "Iran", "Korea, Rep.": "South Korea"
    }
    by_country = defaultdict(list)
    for row in data:
        cn = row["countryName"]
        if cn in target_map and row["value"] is not None:
            by_country[target_map[cn]].append({"y": row["year"], "v": int(row["value"])})
    for c in ["China","India","Germany","France","Kazakhstan","Iran","South Korea"]:
        if c in by_country:
            pts = sorted(by_country[c], key=lambda x: x["y"])
            print(f"{c}: {pts[0]['y']}–{pts[-1]['y']}, {pts[0]['v']:,} → {pts[-1]['v']:,} km")
    return by_country, target_map


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the divergent trajectories over 26 years clearly
        - **Country selection**: China (massive expansion), India (steady growth from higher base),
          Germany and France (network rationalization), Kazakhstan and Iran (moderate growth),
          South Korea (modest growth with new high-speed lines)
        - **Color**: China = accent orange (the standout story), India = warm orange, Europeans = green,
          Central Asia = amber/cool
        - **Story**: China nearly doubled its network (55k→110k km) while simultaneously building
          the world's largest high-speed rail system. Germany lost 8,000 km of track (line closures);
          France lost 4,000 km.
        """
    )
    return


@app.cell
def _(json, by_country):
    order = ["China","India","Germany","France","Kazakhstan","Iran","South Korea"]
    chart_data = [
        {"n": c, "pts": sorted(by_country[c], key=lambda x: x["y"])}
        for c in order if c in by_country
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
