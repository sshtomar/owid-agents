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
        # Poverty at $3/Day: Asia's Descent, Africa's Struggle -- Methodology

        Documents the data pipeline behind viz-363.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-POV-DDAY.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [r for r in data if r["value"] is not None]
    c_data = {}
    for r in filtered:
        c = r["countryName"]
        if c not in c_data:
            c_data[c] = {}
        c_data[c][r["year"]] = r["value"]
    print(f"Countries: {len(c_data)}")
    return c_data, filtered


@app.cell
def _(c_data, json):
    targets = ["China", "Indonesia", "India", "Bangladesh", "Brazil", "Ethiopia", "Kenya"]
    result = []
    for c in targets:
        if c not in c_data:
            continue
        pts = sorted(c_data[c].items())
        pts_filtered = [(y, round(v, 1)) for y, v in pts if 1990 <= y <= 2024]
        result.append({"n": c, "pts": [{"y": y, "v": v} for y, v in pts_filtered]})
    for r in result:
        print(f"{r['n']}: {r['pts'][0]['y']}-{r['pts'][-1]['y']}, max={max(p['v'] for p in r['pts']):.1f}, last={r['pts'][-1]['v']:.1f}")
    print(json.dumps(result, separators=(",", ":")))
    return result, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with explicit year-value pairs (data is sparse, not annual)
        - **Countries**: 7 nations spanning Asia, Latin America, and Sub-Saharan Africa
        - **Time range**: 1990-2024 (post-Cold War globalization era)
        - **Story**: China/Indonesia dropped from ~80% to near-zero; India/Bangladesh from 50% to 5-6%
        - **Contrast**: Ethiopia and Kenya show stagnation or regression in recent years
        - **Color**: Warm for biggest improvers, cool grey for laggards
        """
    )
    return


if __name__ == "__main__":
    app.run()
