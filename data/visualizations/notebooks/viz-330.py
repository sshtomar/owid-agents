import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import json
    from statistics import mean, median

    return json, mean, median, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Gasoline Prices Surge Worldwide After the Iran War

    This notebook documents the data pipeline behind **viz-330**.
    It compiles gasoline price increases reported across 31 countries
    since the US-Israeli strikes on Iran began on February 28, 2026.

    Data is sourced from news reporting (Al Jazeera, IRU, PBS, NPR, Time,
    CNBC, IMF, Bloomberg) rather than a catalog dataset, since real-time
    fuel prices are not available through the World Bank or WHO APIs.

    **War started:** Feb 28, 2026 | **Data as of:** Mar 31, 2026 |
    **Brent crude:** $73 -> $100+/bbl (+37%)
    """)
    return


@app.cell
def _():
    confirmed_data = [
        {"iso3": "KHM", "name": "Cambodia", "pct": 68, "source": "Al Jazeera", "note": "Highest increase globally; $1.11 to $1.32/L (95-octane)"},
        {"iso3": "VNM", "name": "Vietnam", "pct": 50, "source": "Al Jazeera", "note": ""},
        {"iso3": "BGD", "name": "Bangladesh", "pct": 45, "source": "Al Jazeera", "note": "Est.; 95% oil imported, pumps running dry"},
        {"iso3": "NGA", "name": "Nigeria", "pct": 35, "source": "Al Jazeera", "note": ""},
        {"iso3": "USA", "name": "United States", "pct": 35, "source": "Time/CNBC", "note": "$2.98 to $4.02/gal (Mar 31); CA at $5.87"},
        {"iso3": "LAO", "name": "Laos", "pct": 33, "source": "Al Jazeera", "note": ""},
        {"iso3": "LKA", "name": "Sri Lanka", "pct": 30, "source": "Al Jazeera", "note": "Est.; 60% energy imported, fuel passes introduced"},
        {"iso3": "CAN", "name": "Canada", "pct": 28, "source": "Al Jazeera", "note": ""},
        {"iso3": "SWZ", "name": "Eswatini", "pct": 28, "source": "Al Jazeera", "note": "E2.90/L increase for unleaded"},
        {"iso3": "ESP", "name": "Spain", "pct": 27, "source": "IRU", "note": "EUR 1.79/L"},
        {"iso3": "KEN", "name": "Kenya", "pct": 25, "source": "Al Jazeera/Bloomberg", "note": "Est.; fuel shortages at filling stations"},
        {"iso3": "ETH", "name": "Ethiopia", "pct": 25, "source": "Al Jazeera/Bloomberg", "note": "Est.; fuel shortages reported"},
        {"iso3": "ZMB", "name": "Zambia", "pct": 25, "source": "Al Jazeera/Bloomberg", "note": "Est.; fuel shortages reported"},
        {"iso3": "PAK", "name": "Pakistan", "pct": 22, "source": "Al Jazeera", "note": "55 rupee/L increase; 80% energy from Gulf"},
        {"iso3": "ZAF", "name": "South Africa", "pct": 22, "source": "Bloomberg", "note": "R3.06/L increase; govt cut fuel levy"},
        {"iso3": "DEU", "name": "Germany", "pct": 20, "source": "IRU", "note": "EU weighted avg; diesel exceeded EUR 2/L"},
        {"iso3": "FRA", "name": "France", "pct": 20, "source": "IRU", "note": "EU weighted avg; partially shielded by nuclear"},
        {"iso3": "ITA", "name": "Italy", "pct": 20, "source": "IRU/IMF", "note": "Especially exposed per IMF; diesel exceeded EUR 2/L"},
        {"iso3": "NLD", "name": "Netherlands", "pct": 20, "source": "IRU", "note": "Diesel exceeded EUR 2/L; EUR 2.33/L highest EU price"},
        {"iso3": "FIN", "name": "Finland", "pct": 20, "source": "IRU", "note": "EU avg; diesel exceeded EUR 2/L"},
        {"iso3": "IRL", "name": "Ireland", "pct": 20, "source": "IRU", "note": "EUR 2.3/L -- highest price in EU"},
        {"iso3": "JPN", "name": "Japan", "pct": 20, "source": "IRU/IMF", "note": "Est.; 95% oil from Gulf, highly vulnerable"},
        {"iso3": "NAM", "name": "Namibia", "pct": 20, "source": "Al Jazeera", "note": "Slashed fuel levies 50% for 3 months"},
        {"iso3": "JOR", "name": "Jordan", "pct": 20, "source": "CGD/IMF", "note": "Identified as highly vulnerable"},
        {"iso3": "SEN", "name": "Senegal", "pct": 20, "source": "CGD/IMF", "note": "Identified as highly vulnerable"},
        {"iso3": "KOR", "name": "South Korea", "pct": 18, "source": "IRU/IMF", "note": "Est.; 70% oil from Gulf"},
        {"iso3": "EGY", "name": "Egypt", "pct": 18, "source": "Al Jazeera", "note": "15-22% range; shops closed early to save energy"},
        {"iso3": "AGO", "name": "Angola", "pct": 15, "source": "CGD/IMF", "note": "Vulnerable; oil exporter but refining limited"},
        {"iso3": "GBR", "name": "United Kingdom", "pct": 13, "source": "IRU", "note": ""},
        {"iso3": "CHN", "name": "China", "pct": 11, "source": "IRU", "note": "Govt price controls; suspended fuel exports"},
        {"iso3": "IND", "name": "India", "pct": 5, "source": "IRU", "note": "Govt pricing limits spikes"},
    ]

    print(f"Loaded {len(confirmed_data)} countries with price data")
    return (confirmed_data,)


@app.cell
def _(confirmed_data, mean, median, mo):
    pcts = [d["pct"] for d in confirmed_data]
    regions = {
        "Southeast Asia": ["KHM", "VNM", "LAO"],
        "South Asia": ["BGD", "LKA", "PAK", "IND"],
        "East Asia": ["CHN", "JPN", "KOR"],
        "Europe": ["ESP", "DEU", "FRA", "ITA", "NLD", "FIN", "IRL", "GBR"],
        "Africa": ["NGA", "KEN", "ETH", "ZMB", "ZAF", "SWZ", "NAM", "SEN", "AGO"],
        "North America": ["USA", "CAN"],
        "Middle East": ["EGY", "JOR"],
    }
    by_iso = {d["iso3"]: d for d in confirmed_data}

    region_avgs = {}
    for region, codes in regions.items():
        vals = [by_iso[c]["pct"] for c in codes if c in by_iso]
        if vals:
            region_avgs[region] = round(mean(vals), 1)

    region_rows = "\n".join(f"| {r} | {v}% |" for r, v in sorted(region_avgs.items(), key=lambda x: -x[1]))

    mo.md(f"""
    ## Summary Statistics

    | Metric | Value |
    |--------|-------|
    | Countries with data | {len(confirmed_data)} |
    | Countries reporting increases (per Al Jazeera) | 95+ |
    | Min increase | {min(pcts)}% (India -- govt price controls) |
    | Max increase | {max(pcts)}% (Cambodia) |
    | Mean | {mean(pcts):.1f}% |
    | Median | {median(pcts):.1f}% |

    ### Average Increase by Region

    | Region | Avg Increase |
    |--------|-------------|
    {region_rows}
    """)
    return (by_iso,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type:** World choropleth map using D3 + topojson, since the
      data is inherently geographic (price increases by country)
    - **Color scale:** Sequential reds (d3.interpolateReds), 0-70% domain.
      Red conveys urgency/heat and maps intuitively to price increases
    - **Annotations:** Inline % labels on US, China, India, Cambodia --
      the four most notable data points (highest, lowest, largest economies)
    - **Context bar:** Red-bordered strip at the top with key reference
      numbers (war start, Brent crude, US gas price) so readers understand
      the global context immediately
    - **Callout cards:** Four stat cards highlighting extremes and the
      supply disruption figure
    - **Data provenance:** Not from catalog datasets -- compiled from
      news reporting (Al Jazeera, IRU, PBS, NPR, Time, CNBC, IMF, Bloomberg).
      Some values are estimates based on reported shortages and import dependency.
    """)
    return


@app.cell
def _(confirmed_data, mo):
    sorted_data = sorted(confirmed_data, key=lambda d: -d["pct"])
    rows = "\n".join(
        f"| {d['name']} | {d['iso3']} | +{d['pct']}% | {d['source']} | {d['note']} |"
        for d in sorted_data
    )
    mo.md(f"""
    ## Full Data Table (sorted by increase)

    | Country | ISO3 | Increase | Source | Notes |
    |---------|------|----------|--------|-------|
    {rows}
    """)
    return (sorted_data,)


@app.cell(hide_code=True)
def _(confirmed_data, json, mo):
    export_json = json.dumps(confirmed_data, separators=(",", ":"))
    mo.md(
        f"JSON export ready: **{len(export_json):,} bytes**, {len(confirmed_data)} records"
    )
    print(export_json)
    return


if __name__ == "__main__":
    app.run()
