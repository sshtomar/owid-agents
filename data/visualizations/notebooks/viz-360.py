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
        # Income Share of Lowest 20%, ~2000 vs ~2020 -- Methodology

        Slope chart comparing the share of national income held by the bottom quintile.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-DST-FRST-20.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    EXCLUDE = ['World','Income','Asia','Africa','Europe','America','Caribbean',
               'Pacific','Fragile','OECD','Arab','East','Sub-Sah','South','Central',
               'Latin','North','Middle','developing','High','Low','Smal','Euro',
               'IDA','IBRD','Least','Heavily']
    NAMES = {
        "Russian Federation": "Russia",
        "Venezuela, RB": "Venezuela",
        "Egypt, Arab Rep.": "Egypt",
    }

    by_country = {}
    for r in data:
        cn = r["countryName"]
        if any(x in cn for x in EXCLUDE):
            continue
        if r["value"] is None:
            continue
        if cn not in by_country:
            by_country[cn] = {}
        by_country[cn][r["year"]] = r["value"]

    out = []
    for cn, pts in by_country.items():
        early = [(y, v) for y, v in pts.items() if 1995 <= y <= 2005]
        late = [(y, v) for y, v in pts.items() if y >= 2018]
        if early and late:
            a_y, a = sorted(early)[-1]
            b_y, b = sorted(late)[-1]
            label = NAMES.get(cn, cn)
            out.append({"n": label, "a": round(a, 1), "b": round(b, 1)})

    out.sort(key=lambda x: x["b"])
    final = out[:8] + out[-8:]
    seen = set()
    deduped = []
    for x in final:
        if x["n"] not in seen:
            seen.add(x["n"])
            deduped.append(x)
    for f in deduped:
        print(f"{f['n']}: {f['a']}% -> {f['b']}%")
    return by_country, deduped, out, EXCLUDE, NAMES


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (~2000 vs ~2020)
        - **Country selection**: 8 least equal (Colombia, Brazil, Honduras) vs 8 most equal
          (India surprisingly high, Belarus, Kazakhstan showing improvement)
        - **Story**: Latin America stuck at the bottom despite growth; Central Asian countries
          improved dramatically; Northern Europe and India relatively equal
        """
    )
    return


@app.cell
def _(json, deduped):
    print(json.dumps(deduped, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
