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
        # Breast Cancer 5-Year Survival by Country -- Methodology

        Horizontal bar chart showing 5-year net survival rates for breast cancer
        across 40 countries (2021 WHO estimates). The disparity reflects access
        to early screening, surgery, radiotherapy and systemic treatment.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--CANCERSURVIVAL_BREASTCANCER.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    ISO3 = {
        'USA': 'United States', 'GBR': 'United Kingdom', 'FRA': 'France',
        'DEU': 'Germany', 'JPN': 'Japan', 'CHN': 'China', 'IND': 'India',
        'BRA': 'Brazil', 'CAN': 'Canada', 'AUS': 'Australia', 'NGA': 'Nigeria',
        'SOM': 'Somalia', 'COD': 'D.R. Congo', 'ETH': 'Ethiopia', 'GHA': 'Ghana',
        'ZAF': 'South Africa', 'EGY': 'Egypt', 'MEX': 'Mexico', 'ARG': 'Argentina',
        'COL': 'Colombia', 'TUR': 'Turkey', 'IRN': 'Iran', 'PAK': 'Pakistan',
        'IDN': 'Indonesia', 'THA': 'Thailand', 'MYS': 'Malaysia', 'KOR': 'South Korea',
        'SWE': 'Sweden', 'NOR': 'Norway', 'DNK': 'Denmark', 'FIN': 'Finland',
        'NLD': 'Netherlands', 'BEL': 'Belgium', 'CHE': 'Switzerland', 'AUT': 'Austria',
        'ESP': 'Spain', 'ITA': 'Italy', 'POL': 'Poland', 'ROU': 'Romania',
        'HUN': 'Hungary', 'CZE': 'Czechia', 'UKR': 'Ukraine', 'KAZ': 'Kazakhstan',
        'BGD': 'Bangladesh', 'IDN': 'Indonesia', 'NPL': 'Nepal',
        'CMR': 'Cameroon', 'MOZ': 'Mozambique', 'ZMB': 'Zambia', 'RWA': 'Rwanda',
        'UGA': 'Uganda', 'TGO': 'Togo', 'BEN': 'Benin', 'MLI': 'Mali',
        'GIN': 'Guinea', 'TCD': 'Chad', 'CAF': 'C. African Rep.',
        'LSO': 'Lesotho', 'GNB': 'Guinea-Bissau', 'BDI': 'Burundi',
        'NGA': 'Nigeria', 'SWZ': 'Eswatini', 'SOM': 'Somalia',
        'PER': 'Peru', 'CHL': 'Chile', 'LTU': 'Lithuania', 'ALB': 'Albania',
        'ISR': 'Israel', 'SYR': 'Syria', 'KHM': 'Cambodia', 'PRK': 'North Korea',
        'OMN': 'Oman', 'LKA': 'Sri Lanka',
    }

    SKIP = {'GLOBAL','AFR','AMR','EMR','EUR','SEAR','WPR','WB_LI','WB_LMI','WB_UMI','WB_HI'}

    seen = set()
    named = []
    for row in data:
        c = row['country']
        if c not in seen and c not in SKIP and c in ISO3:
            seen.add(c)
            named.append({'n': ISO3[c], 'v': round(row['value'], 1)})

    named.sort(key=lambda x: x['v'])

    mid = named[10:-10]
    stride = max(1, len(mid) // 20)
    selected = named[:10] + mid[::stride][:20] + named[-10:]
    deduped = []
    names_seen = set()
    for r in selected:
        if r['n'] not in names_seen:
            names_seen.add(r['n'])
            deduped.append(r)
    deduped.sort(key=lambda x: x['v'])

    print(f"Selected: {len(deduped)} countries")
    print(f"Range: {deduped[0]['v']}% ({deduped[0]['n']}) to {deduped[-1]['v']}% ({deduped[-1]['n']})")
    return deduped, named, ISO3, SKIP


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sorted horizontal bars — standard for ranking countries on survival outcomes
        - **Color**: Diverging from terra red (<40%) to deep green (>85%)
        - **Key insight**: Sweden achieves 92.5% 5-year survival; Central African Republic just 24.6%
          — a 68pp gap largely explained by mammography access, treatment availability and stage at diagnosis
        - **Year**: 2021 WHO estimate (age-standardized net survival, both sexes)
        """
    )
    return


@app.cell
def _(json, deduped):
    print(json.dumps(deduped, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
