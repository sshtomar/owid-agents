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
        # Childhood Leukaemia Survival by Country -- Methodology

        Horizontal bar chart showing 5-year age-standardized leukaemia survival
        rates for children across 40 countries. The gap between the best and
        worst performing countries exceeds 74 percentage points.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--CANCERSURVIVAL_CHILDREN_LEUKAEMIA.json"
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
        'SOM': 'Somalia', 'NER': 'Niger', 'COD': 'D.R. Congo', 'ETH': 'Ethiopia',
        'TZA': 'Tanzania', 'KEN': 'Kenya', 'GHA': 'Ghana', 'ZAF': 'South Africa',
        'EGY': 'Egypt', 'MAR': 'Morocco', 'MEX': 'Mexico', 'ARG': 'Argentina',
        'COL': 'Colombia', 'TUR': 'Turkey', 'IRN': 'Iran', 'PAK': 'Pakistan',
        'IDN': 'Indonesia', 'THA': 'Thailand', 'PHL': 'Philippines', 'KOR': 'South Korea',
        'SWE': 'Sweden', 'NOR': 'Norway', 'DNK': 'Denmark', 'FIN': 'Finland',
        'NLD': 'Netherlands', 'CHE': 'Switzerland', 'AUT': 'Austria', 'ESP': 'Spain',
        'PRT': 'Portugal', 'ITA': 'Italy', 'GRC': 'Greece', 'POL': 'Poland',
        'ROU': 'Romania', 'HRV': 'Croatia', 'HUN': 'Hungary', 'CZE': 'Czechia',
        'UKR': 'Ukraine', 'KAZ': 'Kazakhstan', 'BGD': 'Bangladesh', 'MMR': 'Myanmar',
        'NPL': 'Nepal', 'CMR': 'Cameroon', 'MOZ': 'Mozambique', 'ZMB': 'Zambia',
        'MDG': 'Madagascar', 'UGA': 'Uganda', 'SEN': 'Senegal', 'MLI': 'Mali',
        'BFA': 'Burkina Faso', 'GIN': 'Guinea', 'TCD': 'Chad', 'CAF': 'C. African Rep.',
        'AGO': 'Angola', 'LSO': 'Lesotho', 'GNB': 'Guinea-Bissau', 'BDI': 'Burundi',
        'ERI': 'Eritrea', 'BEN': 'Benin', 'HND': 'Honduras', 'NIC': 'Nicaragua',
        'CRI': 'Costa Rica', 'HTI': 'Haiti', 'LAO': 'Laos', 'PRK': 'North Korea',
        'DZA': 'Algeria', 'JOR': 'Jordan', 'PAN': 'Panama', 'SRB': 'Serbia',
        'LVA': 'Latvia', 'BEL': 'Belgium',
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

        - **Chart type**: Sorted horizontal bars — best for ranking 40 countries on a single metric
        - **Color**: Graduated from terra (#B34B3B) for <40% to deep green (#3D7A5A) for >85%
        - **Insight**: Finland (93.2%) vs. Central African Republic (18.6%) — a 74pp gap driven
          by healthcare access, chemotherapy availability, and health system capacity
        - **Year**: 2021 (single WHO estimate, age-standardized)
        """
    )
    return


@app.cell
def _(json, deduped):
    print(json.dumps(deduped, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
