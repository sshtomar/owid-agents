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
        # UHC Service Coverage Index — Methodology

        Slope chart comparing universal health coverage scores from the early 2000s to 2022–2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--UHC_INDEX_REPORTED.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    print(f"After filtering nulls: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    from collections import defaultdict
    country_data = defaultdict(list)
    for x in filtered:
        country_data[x["country"]].append((x["year"], x["value"], x["countryName"]))

    sel = ["NOR","CUB","CHN","BRA","CRI","CHL","IND","BTN","CPV","RWA","NPL","UGA","ETH","MDG","NER"]
    name_map = {"NOR":"Norway","CUB":"Cuba","CHN":"China","BRA":"Brazil","CRI":"Costa Rica",
                "CHL":"Chile","IND":"India","BTN":"Bhutan","CPV":"Cape Verde",
                "RWA":"Rwanda","NPL":"Nepal","UGA":"Uganda","ETH":"Ethiopia","MDG":"Madagascar","NER":"Niger"}

    slope_data = []
    for code in sel:
        pts = sorted(country_data[code])
        early = [p for p in pts if p[0] <= 2003]
        late = [p for p in pts if p[0] >= 2019]
        if early and late:
            a = early[0][1]
            b = late[-1][1]
            n = name_map.get(code, code)
            slope_data.append({"n": n, "a": a, "b": b})
            print(f"{n}: {a} -> {b} (+{b-a})")
    return slope_data, name_map, country_data, sel


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for comparing two time points across many countries
        - **Country selection**: 15 countries spanning the full range from Norway (89) to Niger (37),
          chosen to show both high performers and rapid gainers (Nepal +40, Rwanda +37, India +33)
        - **Time range**: Early 2000s (first available) vs most recent year (2019–2023)
        - **Color encoding**: Diverging warm/cool ramp by magnitude of gain
        - **Story**: The biggest improvements came from South Asia and East Africa; wealthy nations
          were already high and gained less in absolute terms
        """
    )
    return


@app.cell
def _(json, slope_data):
    print(json.dumps(slope_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
