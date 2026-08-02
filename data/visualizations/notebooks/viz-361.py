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
        # Energy Use per Capita, 1990–2024 -- Methodology

        Trend lines (log scale) showing energy consumption per person (kg of oil
        equivalent) from 1990 to 2024 for 10 countries. Displays the 55:1 gap
        between Iceland and Bangladesh and China's threefold rise.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    TARGETS = ['Iceland', 'Bahrain', 'Canada', 'Finland', 'Australia',
               'Germany', 'China', 'Brazil', 'India', 'Bangladesh']

    result = []
    for target in TARGETS:
        pts = sorted(
            [{"y": r['year'], "v": round(r['value'])} for r in data if r['countryName'] == target and r['value']],
            key=lambda x: x['y']
        )
        if pts:
            result.append({"n": target, "pts": pts})
            print(f'{target}: {pts[0]["y"]}-{pts[-1]["y"]}, {pts[0]["v"]:,} -> {pts[-1]["v"]:,}')

    return result, TARGETS


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines on log scale — log scale prevents Iceland/Bahrain dominating
          the chart and makes relative growth rates visually comparable
        - **Country selection**: 10 countries spanning the full range from Bangladesh (288) to Iceland (15,997)
        - **Key insight**: China tripled its per-capita energy use 1990–2023; Germany fell by 36%;
          Iceland's extreme values reflect geothermal energy and aluminum smelting
        - **Y-axis**: Log10 scale from 100 to 20,000 kg of oil equivalent
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
