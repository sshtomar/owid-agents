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
        # Tuberculosis Treatment Coverage — Methodology

        Documents the data pipeline behind viz-359.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--TB_1.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for x in data:
        if x['value'] is not None:
            by_country[x['country']][x['year']] = x['value']
    iso_map = {
        'IND': 'India', 'CHN': 'China', 'IDN': 'Indonesia', 'PHL': 'Philippines',
        'ETH': 'Ethiopia', 'VNM': 'Vietnam', 'ZAF': 'S. Africa', 'UGA': 'Uganda',
        'AGO': 'Angola', 'BRA': 'Brazil', 'RUS': 'Russia', 'KAZ': 'Kazakhstan',
        'SDN': 'Sudan', 'AZE': 'Azerbaijan', 'ZWE': 'Zimbabwe', 'CUB': 'Cuba',
        'NPL': 'Nepal', 'LKA': 'Sri Lanka', 'KHM': 'Cambodia', 'BOL': 'Bolivia',
        'PER': 'Peru', 'HTI': 'Haiti', 'BWA': 'Botswana'
    }
    slope_data = []
    for code, name in iso_map.items():
        v = by_country.get(code, {})
        early = [y for y in range(2000, 2008) if y in v]
        late = [y for y in range(2019, 2025) if y in v]
        if early and late:
            a, b = v[early[0]], v[late[-1]]
            slope_data.append({"n": name, "a": round(a), "b": round(b), "ya": early[0], "yb": late[-1]})
    slope_data.sort(key=lambda x: x['b'] - x['a'], reverse=True)
    for s in slope_data:
        print(f"  {s['n']}: {s['a']}% -> {s['b']}% ({s['b']-s['a']:+d})")
    return by_country, slope_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compare treatment coverage at two time points
        - **Country selection**: High TB burden countries with data in early 2000s and 2019-2024
        - **Highlights**: Indonesia gained 57 percentage points; Uganda reached 100%; Botswana regressed
        """
    )
    return


@app.cell
def _(json, slope_data):
    print(json.dumps(slope_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
