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
    mo.md("""
    # Rural Population (% of Total) — Methodology

    Sparkline grid showing countries with the largest absolute decline in rural population
    share from 1960 to 2024. Documents the global urbanization wave.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-RUR-TOTL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    points = [r for r in data if r["value"] is not None]
    exclude_terms = ["World","Income","OECD","Arab World","Africa ","Asia ","Europe ","America","Caribbean",
                     "dividend","heavily","Fragile","IDA","IBRD","Euro area","Latin ","Sub-Saharan","South Asia",
                     "East Asia","Pacific","Central Asia","Middle East","North Africa","MENA","states"]
    def is_real_country(name):
        return not any(x.lower() in name.lower() for x in exclude_terms)
    real_pts = [r for r in points if is_real_country(r["countryName"])]
    print(f"Filtered to {len(real_pts)} real-country data points")
    return (real_pts,)


@app.cell
def _(real_pts, json):
    by_country = {}
    for r in real_pts:
        c = r["countryName"]
        if c not in by_country:
            by_country[c] = {}
        by_country[c][r["year"]] = r["value"]

    years = list(range(1960, 2025, 2))
    series_data = []
    for c, yd in by_country.items():
        if 1960 not in yd or 2024 not in yd:
            continue
        s = []
        for y in years:
            if y in yd:
                s.append(yd[y])
            else:
                prev_y = max((yy for yy in yd if yy < y), default=None)
                next_y = min((yy for yy in yd if yy > y), default=None)
                if prev_y and next_y:
                    t = (y - prev_y) / (next_y - prev_y)
                    s.append(yd[prev_y] + t * (yd[next_y] - yd[prev_y]))
                elif prev_y:
                    s.append(yd[prev_y])
                else:
                    s.append(None)
        if any(v is None for v in s):
            continue
        decline = s[0] - s[-1]
        series_data.append({"n": c, "s": [round(v, 1) for v in s], "e": round(s[0], 1), "l": round(s[-1], 1), "decline": decline})

    series_data.sort(key=lambda x: -x["decline"])
    top30 = series_data[:30]
    for item in top30:
        del item["decline"]

    print(f"Selected {len(top30)} countries with largest rural decline")
    print("Sample:", [(t["n"], t["e"], t["l"]) for t in top30[:5]])
    print(json.dumps(top30, separators=(",", ":")))
    return (top30,)


if __name__ == "__main__":
    app.run()
