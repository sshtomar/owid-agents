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
        # Youth Literacy Rate, 1975–2024 -- Methodology

        Trend lines for countries that began with very low youth literacy.
        Shows dramatic gains across South Asia and sub-Saharan Africa over 40+ years.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-ADT-1524-LT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    codes = {
        'BD': 'Bangladesh', 'BI': 'Burundi', 'ET': 'Ethiopia',
        'BF': 'Burkina Faso', 'EG': 'Egypt', 'IN': 'India',
        'IR': 'Iran', 'BJ': 'Benin', 'AF': 'Afghanistan'
    }
    by_code = {}
    for row in data:
        if row['country'] in codes and row['value'] is not None:
            code = row['country']
            if code not in by_code:
                by_code[code] = []
            by_code[code].append({"y": row['year'], "v": round(row['value'], 1)})

    chart = []
    for code, name in codes.items():
        if code in by_code:
            pts = sorted(by_code[code], key=lambda x: x['y'])
            chart.append({"n": name, "pts": pts})
            first = pts[0]
            last = pts[-1]
            print(f"  {name}: {first['v']}% ({first['y']}) -> {last['v']}% ({last['y']})  [+{last['v']-first['v']:.0f}pp]")
    return chart, codes, by_code


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with dots at measured years — surveys are infrequent
        - **Country selection**: Countries that started below 60% with at least 5 data points,
          prioritizing largest absolute gains
        - **Reference line**: 90% drawn as a dashed line — a common near-universal literacy threshold
        - **Story**: Iran reached 99% from 57% in under 50 years; India is now at 97%; even
          Burkina Faso has nearly doubled from 14% to 63%. Afghanistan shows gains despite conflict.
        """
    )
    return


@app.cell
def _(json, chart):
    print(json.dumps(chart, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
