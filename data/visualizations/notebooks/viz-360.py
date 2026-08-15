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
        # Sex Ratio at Birth — Methodology

        Trend lines 1960-2024 showing male births per female births for 6 countries
        with the most pronounced evidence of sex-selective practices. The natural
        biological ratio is approximately 1.05 males per female.
        China's ratio peaked at 1.18 around 2002-2006 and has since declined as the
        one-child policy was relaxed; Azerbaijan and Armenia show similar but later spikes
        tied to ultrasound availability and son preference.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-BRTH-MF.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = round(row["value"], 4)

    select = ["China", "India", "Azerbaijan", "Armenia", "Korea, Rep.", "Georgia"]
    result = []
    for c in select:
        if c not in by_country:
            print(f"Missing: {c}")
            continue
        yv = by_country[c]
        pts = [{"y": y, "v": yv[y]} for y in range(1960, 2025, 2) if y in yv]
        name = "South Korea" if c == "Korea, Rep." else c
        result.append({"n": name, "pts": pts})
        print(f"{name}: peak={max(p['v'] for p in pts):.3f}, latest={pts[-1]['v']:.3f}")
    return result, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with reference line at 1.05 (biological baseline)
        - **Country selection**: 6 countries with the most extreme or historically notable
          sex-selective ratios: China, India, Azerbaijan, Armenia, South Korea (peaked 1990),
          Georgia (moderate but visible)
        - **Reference line**: 1.05 is the biological baseline (natural sex ratio at birth)
        - **Highlights**: China peaked at 1.18 (2002-2006) then declined after policy relaxation;
          South Korea corrected fastest after reaching 1.16 in 1990
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
