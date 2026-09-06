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
        # Pre-Primary Enrollment Gap, ~1990 vs ~2020 -- Methodology

        Slope chart comparing pre-primary school enrollment rates across 15 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRE-ENRR.json"
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
        "Egypt, Arab Rep.": "Egypt",
        "Iran, Islamic Rep.": "Iran",
        "Korea, Rep.": "South Korea",
        "Congo, Dem. Rep.": "DR Congo",
        "Cote d'Ivoire": "Cote d'Ivoire",
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
        a_opts = [(y, v) for y, v in pts.items() if 1988 <= y <= 1993]
        b_opts = [(y, v) for y, v in pts.items() if 2018 <= y <= 2022]
        if a_opts and b_opts:
            a = sorted(a_opts)[-1][1]
            b = sorted(b_opts)[-1][1]
            label = NAMES.get(cn, cn)
            out.append({"n": label, "a": round(a, 1), "b": round(b, 1)})

    out.sort(key=lambda x: x["b"], reverse=True)
    # Select diverse top 6, mid 4, bottom 5
    selected = out[:6] + out[len(out)//2-2:len(out)//2+2] + out[-5:]
    seen = set()
    final = []
    for x in selected:
        if x["n"] not in seen:
            seen.add(x["n"])
            final.append(x)
    for f in final:
        print(f"{f['n']}: {f['a']} -> {f['b']}")
    return by_country, final, out, EXCLUDE, NAMES


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (~1990 vs ~2020) -- clear before/after comparison
        - **Country selection**: Top enrollers (Australia, Belgium, Israel), strong improvers
          (Ghana, Iran), middle (Kazakhstan, Croatia), and very low Sub-Saharan countries
          (Burkina Faso, DR Congo, Djibouti) with minimal improvement
        - **Story**: Wealthy countries started high; some emerging economies caught up fast;
          Sub-Saharan Africa still below 20%
        """
    )
    return


@app.cell
def _(json, final):
    print(json.dumps(final, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
