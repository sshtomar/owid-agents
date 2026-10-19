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
        # Psychiatrists per 100,000 Population — Methodology

        Documents the data pipeline behind viz-514: horizontal bar chart
        showing the 6,000-fold gap in mental health workforce between
        the richest and poorest countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--MH_6.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    non_null = [r for r in data if r["value"] is not None]
    sorted_d = sorted(non_null, key=lambda x: -x["value"])
    print(f"Total countries: {len(sorted_d)}")
    print(f"Range: {sorted_d[-1]['value']:.3f} – {sorted_d[0]['value']:.2f} per 100,000")
    print("\nTop 5:")
    for r in sorted_d[:5]:
        print(f"  {r['country']}: {r['value']:.2f}")
    print("Bottom 5:")
    for r in sorted_d[-5:]:
        print(f"  {r['country']}: {r['value']:.3f}")
    return non_null, sorted_d


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — most intuitive for ranking
          countries by a single metric; horizontal layout accommodates long
          country names
        - **Selection**: Top 15 (highest workforce) + 5 mid-range + bottom 14
          (lowest workforce) to show the extreme poles while hinting at the
          middle (many countries cluster between 1–10)
        - **Key finding**: Norway has 48 psychiatrists per 100,000; Chad 0.007.
          The ratio is ~6,800:1. Sub-Saharan Africa operates with essentially
          zero specialist mental health coverage.
        - **Color encoding**: Diverging by coverage level (green = adequate,
          red = critical shortage), reinforcing the inequality story
        - **Measurement note**: Data are from ~2013–2017 surveys and represent
          psychiatrists working in the formal mental health sector only
        """
    )
    return


@app.cell
def _(json, sorted_d):
    name_map = {
        "NOR":"Norway","CHE":"Switzerland","MCO":"Monaco","NZL":"New Zealand",
        "POL":"Poland","FIN":"Finland","ARG":"Argentina","FRA":"France",
        "NLD":"Netherlands","SWE":"Sweden","BEL":"Belgium","LTU":"Lithuania",
        "LUX":"Luxembourg","EST":"Estonia","CAN":"Canada","SRB":"Serbia",
        "RUS":"Russia","MNE":"Montenegro","BIH":"Bosnia","BGR":"Bulgaria",
        "ZMB":"Zambia","TZA":"Tanzania","TGO":"Togo","MOZ":"Mozambique",
        "LBR":"Liberia","SLE":"Sierra Leone","BFA":"Burkina Faso","MLI":"Mali",
        "SSD":"South Sudan","GIN":"Guinea","CAF":"Central African Rep.",
        "NER":"Niger","BDI":"Burundi","TCD":"Chad","MHL":"Marshall Islands"
    }
    top15 = sorted_d[:15]
    mid5 = sorted_d[30:35]
    bot14 = sorted_d[-14:]
    selected = top15 + mid5 + bot14

    chart_data = [
        {"n": name_map.get(r["country"], r.get("countryName") or r["country"]), "v": round(r["value"], 3)}
        for r in selected
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return bot14, chart_data, mid5, name_map, selected, top15


if __name__ == "__main__":
    app.run()
