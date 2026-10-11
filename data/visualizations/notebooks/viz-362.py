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
        # Energy Use per Capita — Methodology

        Trend lines chart showing kg of oil equivalent per person, 1990–2024.
        Uses a log scale because the range spans two orders of magnitude (Bangladesh ~288
        to South Korea ~5,564).
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
    TARGET = {"KR", "DE", "JP", "AU", "FR", "CN", "BR", "IN", "BD"}
    LABELS = {
        "KR": "South Korea", "DE": "Germany", "JP": "Japan",
        "AU": "Australia", "FR": "France", "CN": "China",
        "BR": "Brazil", "IN": "India", "BD": "Bangladesh"
    }
    from collections import defaultdict
    by_c = defaultdict(list)
    for r in data:
        if r.get("value") is not None and r["country"] in TARGET:
            by_c[r["country"]].append({"y": r["year"], "v": round(r["value"], 1)})
    print(f"Countries with data: {len(by_c)}")
    return TARGET, LABELS, by_c, defaultdict


@app.cell
def _(by_c, LABELS):
    ORDER = ["KR", "AU", "DE", "JP", "FR", "CN", "BR", "IN", "BD"]
    chart_data = []
    for c in ORDER:
        rows = sorted(by_c[c], key=lambda x: x["y"])
        rows_f = [r for r in rows if 1990 <= r["y"] <= 2024]
        s = [r["v"] for r in rows_f]
        y0 = rows_f[0]["y"]
        chart_data.append({"n": LABELS[c], "s": s, "y0": y0})
        print(f"{LABELS[c]}: {y0}-{rows_f[-1]['y']}, first={s[0]:.0f}, latest={s[-1]:.0f}")
    return ORDER, chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows each country's full trajectory 1990–2024
        - **Log scale**: Range spans 114–16248 kg; log scale makes relative changes visible at all levels
        - **Country selection**: 9 countries across all income levels telling the core story of energy transition
        - **Highlights**: China's 4x rise; Germany/Japan's efficiency decline; South Asia's persistent energy poverty
        """
    )
    return


@app.cell
def _(json, chart_data):
    import json as _json
    print(_json.dumps(chart_data, separators=(",", ":")))
    return
