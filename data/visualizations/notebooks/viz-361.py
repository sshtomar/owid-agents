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
        # GNI per Capita Since 1990 -- Methodology

        Sparkline grid showing GNI per capita (Atlas method) trajectories since 1990.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GNP-PCAP-CD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    TARGET = {
        "Japan": "Japan",
        "Germany": "Germany",
        "France": "France",
        "Korea, Rep.": "South Korea",
        "China": "China",
        "India": "India",
        "Brazil": "Brazil",
        "Indonesia": "Indonesia",
        "Bangladesh": "Bangladesh",
        "Ethiopia": "Ethiopia",
        "Ghana": "Ghana",
        "Kenya": "Kenya",
        "Colombia": "Colombia",
        "Argentina": "Argentina",
    }

    by_country = {}
    for r in data:
        cn = r["countryName"]
        if cn in TARGET and r["value"] is not None:
            label = TARGET[cn]
            if label not in by_country:
                by_country[label] = {}
            by_country[label][r["year"]] = r["value"]

    out = []
    for wb_name, label in TARGET.items():
        pts = by_country.get(label, {})
        if not pts:
            continue
        years = list(range(1990, 2025, 4))
        series = []
        for y in years:
            v = pts.get(y)
            if v is not None:
                series.append(round(v))
        if series:
            latest_y = max(pts.keys())
            l = pts[latest_y]
            e = pts.get(1990, series[0])
            out.append({"n": label, "s": series, "e": round(e), "l": round(l), "y0": 1990})

    out.sort(key=lambda x: x["l"], reverse=True)
    for o in out:
        print(f"{o['n']}: ${o['e']:,} -> ${o['l']:,}")
    return by_country, out, TARGET


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid -- shows many country trajectories in a compact view
        - **Country selection**: 14 diverse economies from Japan ($37k) to Ethiopia ($1.1k),
          including fast-growing South Korea and China
        - **Story**: South Korea went from $6.6k to $36.7k; China from $330 to $13.7k;
          Japan's income stagnated; Latin America volatile; Africa still very low
        """
    )
    return


@app.cell
def _(json, out):
    print(json.dumps(out, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
