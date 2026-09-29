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
        # Depression Prevalence by Country (2015) -- Methodology

        This notebook documents the data pipeline behind viz-361, a horizontal bar chart
        showing estimated population-based depression prevalence across countries in 2015.
        The data comes from WHO's Global Depression Occurrence study, covering 183 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--GDO_q35.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    ISO3 = {
        "AFG":"Afghanistan","ALB":"Albania","DZA":"Algeria","AGO":"Angola","ARG":"Argentina",
        "ARM":"Armenia","AUS":"Australia","AUT":"Austria","AZE":"Azerbaijan","BHS":"Bahamas",
        "BGD":"Bangladesh","BRB":"Barbados","BLR":"Belarus","BEL":"Belgium","BEN":"Benin",
        "BOL":"Bolivia","BWA":"Botswana","BRA":"Brazil","BGR":"Bulgaria","BDI":"Burundi",
        "KHM":"Cambodia","CMR":"Cameroon","CAN":"Canada","TCD":"Chad","CHL":"Chile",
        "CHN":"China","COL":"Colombia","COD":"DR Congo","CRI":"Costa Rica","HRV":"Croatia",
        "CUB":"Cuba","CZE":"Czechia","DNK":"Denmark","DOM":"Dominican Rep.","ECU":"Ecuador",
        "EGY":"Egypt","SLV":"El Salvador","EST":"Estonia","ETH":"Ethiopia","FIN":"Finland",
        "FRA":"France","GEO":"Georgia","DEU":"Germany","GHA":"Ghana","GRC":"Greece",
        "GTM":"Guatemala","GUY":"Guyana","HND":"Honduras","HUN":"Hungary","IND":"India",
        "IDN":"Indonesia","IRN":"Iran","IRQ":"Iraq","IRL":"Ireland","ISR":"Israel",
        "ITA":"Italy","JAM":"Jamaica","JPN":"Japan","JOR":"Jordan","KAZ":"Kazakhstan",
        "KEN":"Kenya","KOR":"South Korea","KWT":"Kuwait","LAO":"Laos","LVA":"Latvia",
        "LBN":"Lebanon","LBR":"Liberia","LTU":"Lithuania","LUX":"Luxembourg",
        "MDG":"Madagascar","MWI":"Malawi","MYS":"Malaysia","MLI":"Mali","MLT":"Malta",
        "MUS":"Mauritius","MEX":"Mexico","MDA":"Moldova","MNG":"Mongolia","MAR":"Morocco",
        "MOZ":"Mozambique","MMR":"Myanmar","NAM":"Namibia","NPL":"Nepal","NLD":"Netherlands",
        "NZL":"New Zealand","NIC":"Nicaragua","NER":"Niger","NGA":"Nigeria","NOR":"Norway",
        "PAK":"Pakistan","PAN":"Panama","PNG":"Papua New Guinea","PRY":"Paraguay",
        "PER":"Peru","PHL":"Philippines","POL":"Poland","PRT":"Portugal","ROU":"Romania",
        "RUS":"Russia","RWA":"Rwanda","WSM":"Samoa","SAU":"Saudi Arabia","SEN":"Senegal",
        "SRB":"Serbia","SGP":"Singapore","SVK":"Slovakia","SVN":"Slovenia",
        "SLB":"Solomon Islands","SOM":"Somalia","ZAF":"South Africa","ESP":"Spain",
        "LKA":"Sri Lanka","SDN":"Sudan","SWE":"Sweden","CHE":"Switzerland","TWN":"Taiwan",
        "TJK":"Tajikistan","TZA":"Tanzania","THA":"Thailand","TLS":"Timor-Leste",
        "TGO":"Togo","TON":"Tonga","TTO":"Trinidad","TUN":"Tunisia","TUR":"Turkey",
        "UGA":"Uganda","UKR":"Ukraine","ARE":"UAE","GBR":"UK","USA":"United States",
        "URY":"Uruguay","UZB":"Uzbekistan","VUT":"Vanuatu","VEN":"Venezuela",
        "VNM":"Vietnam","YEM":"Yemen","ZMB":"Zambia","ZWE":"Zimbabwe","MKD":"N. Macedonia",
        "FSM":"Micronesia","BHR":"Bahrain","KIR":"Kiribati","MDV":"Maldives",
        "MRT":"Mauritania","OMN":"Oman","QAT":"Qatar","SSD":"South Sudan","STP":"Sao Tome",
        "SUR":"Suriname","SWZ":"Eswatini","SYR":"Syria","TKM":"Turkmenistan",
        "COG":"Congo","BFA":"Burkina Faso","CYP":"Cyprus","BIH":"Bosnia","FJI":"Fiji",
        "GAB":"Gabon","GMB":"Gambia","GIN":"Guinea","GNB":"Guinea-Bissau","HTI":"Haiti",
        "KGZ":"Kyrgyzstan","LSO":"Lesotho","LBY":"Libya","BLZ":"Belize",
        "CAF":"C. African Rep.","COM":"Comoros","DJI":"Djibouti","ERI":"Eritrea",
        "GNQ":"Eq. Guinea","BTN":"Bhutan","CIV":"Ivory Coast","ISL":"Iceland",
        "PRK":"North Korea","MNE":"Montenegro","SLE":"Sierra Leone"
    }
    pts = []
    for row in data:
        if row["value"] is not None:
            name = ISO3.get(row["country"])
            if name:
                pts.append({"n": name, "v": round(row["value"], 2)})
    pts.sort(key=lambda x: -x["v"])
    print(f"Countries with names: {len(pts)}")
    print("Top 5:", pts[:5])
    return (pts,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart sorted by value -- best for ranked comparisons across many entities
        - **Selection**: Top 22 countries by depression prevalence; all data from 2015
        - **Insight**: High-income, English-speaking and post-Soviet countries report highest rates --
          likely reflecting both real burden and greater diagnosis/reporting
        - **Caveats**: Data reflects estimated prevalence based on available surveys; under-diagnosis
          in low-income countries may lead to underestimation
        """
    )
    return


@app.cell
def _(json, pts):
    chart_data = pts[:22]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
