"""Generate marimo methodology notebooks for all visualizations."""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
VIZ_INDEX = ROOT / "data" / "visualizations" / "index.json"
NOTEBOOKS_DIR = ROOT / "data" / "visualizations" / "notebooks"
DATASETS_DIR = ROOT / "data" / "catalog" / "datasets"

# -- Chart type grouping --------------------------------------------------

TIME_SERIES_TYPES = {"line chart", "trends over time", "stacked area chart"}
COMPARISON_TYPES = {
    "bar chart",
    "horizontal bar chart",
    "lollipop chart",
    "dot plot",
    "dot-plot",
    "diverging bar chart",
}
BEFORE_AFTER_TYPES = {"then vs now", "before and after", "slope chart", "dumbbell chart"}
MULTI_DATASET_TYPES = {
    "wealth vs health",
    "spending vs outcomes",
    "country scorecard",
    "dot-matrix scorecard",
}


def chart_group(chart_type: str) -> str:
    ct = chart_type.lower().strip()
    if ct in TIME_SERIES_TYPES:
        return "time_series"
    if ct in COMPARISON_TYPES:
        return "comparison"
    if ct in BEFORE_AFTER_TYPES:
        return "before_after"
    if ct in MULTI_DATASET_TYPES:
        return "multi_dataset"
    return "time_series"  # fallback


# -- Dataset metadata helpers ----------------------------------------------

def load_dataset_meta(did: str) -> dict | None:
    path = DATASETS_DIR / f"{did}.json"
    if not path.exists():
        return None
    raw = json.loads(path.read_text())
    return raw.get("meta")


def provider_label(provider: str) -> str:
    labels = {
        "world-bank": "World Bank",
        "who-gho": "WHO Global Health Observatory",
    }
    return labels.get(provider, provider)


# -- Escape helper ---------------------------------------------------------

def _esc(text: str) -> str:
    """Escape text for embedding inside triple-quoted Python strings."""
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("{", "{{").replace("}", "}}")


# -- Cell builders ---------------------------------------------------------

def cell_imports() -> str:
    return '''
@app.cell
def _():
    import marimo as mo
    return (mo,)
'''


def cell_title(title: str, description: str) -> str:
    t = _esc(title)
    d = _esc(description)
    return f'''
@app.cell
def _(mo):
    mo.md(
        """
        # {t}

        {d}
        """
    )
    return
'''


def cell_data_sources(dataset_ids: list[str]) -> str:
    """Build a markdown cell with human-readable data source info."""
    lines = []
    for did in dataset_ids:
        meta = load_dataset_meta(did)
        if meta is None:
            lines.append(f"- **`{did}`** -- dataset not in local catalog (data inlined in HTML)")
            continue
        source = meta.get("source", {})
        prov = provider_label(source.get("provider", "unknown"))
        indicator_name = _esc(source.get("indicatorName", meta.get("title", did)))
        desc = _esc(meta.get("description", ""))
        url = source.get("sourceUrl", "")
        line = f"- **{indicator_name}** ({prov})"
        if desc and desc != indicator_name:
            line += f"  \n  {desc}"
        if url:
            line += f"  \n  Source: [{_esc(url)}]({url})"
        lines.append(line)

    sources_md = "\n        ".join(lines)
    return f'''
@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        {sources_md}
        """
    )
    return
'''


def cell_data_imports() -> str:
    return '''
@app.cell
def _():
    import json
    import urllib.request
    import pandas as pd
    import altair as alt
    return json, urllib, pd, alt
'''


def cell_load_dataset(idx: int, did: str) -> str:
    """Load a dataset JSON into a pandas DataFrame."""
    v = f"df_{idx}"
    m = f"meta_{idx}"
    # Build the mo.md f-string as a raw string to avoid escaping issues
    md_expr = (
        f'{m}[\'title\']}}** -- '
        f'{{len({v})}} rows, '
        f'{{{v}[\'countryName\'].nunique()}} countries, '
        f'{{{v}[\'year\'].min()}}--'
        f'{{{v}[\'year\'].max()}}'
    )
    md_line = f'mo.md(f"**{{{md_expr}")'
    lines = [
        "",
        "@app.cell",
        "def _(json, urllib, pd, mo):",
        f'    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "{did}.json"',
        "    try:",
        "        _text = _path.read_text()",
        "    except AttributeError:",
        "        _text = urllib.request.urlopen(str(_path)).read().decode()",
        "    _raw = json.loads(_text)",
        f"    {m} = _raw[\"meta\"]",
        f"    {v} = pd.DataFrame(_raw[\"data\"])",
        f"    {v} = {v}.dropna(subset=[\"value\"])",
        f"    {md_line}",
        f"    mo.ui.table({v}.head(20))",
        f"    return ({v}, {m})",
    ]
    return "\n".join(lines) + "\n"


def cell_transformation_prose(group: str) -> str:
    explanations = {
        "time_series": (
            "For a time-series view we filter to the top countries by data completeness, "
            "then plot each country as a separate line over time."
        ),
        "comparison": (
            "For a comparison view we take the latest non-null value per country, "
            "then sort to show the ranking."
        ),
        "before_after": (
            "For a before/after view we take the earliest and latest observation per "
            "country and compute the change over time."
        ),
        "multi_dataset": (
            "For a multi-dataset view we merge the datasets on country and year, "
            "keeping only rows where all indicators have values."
        ),
    }
    text = _esc(explanations.get(group, explanations["time_series"]))
    return f'''
@app.cell
def _(mo):
    mo.md(
        """
        ## Transformation

        {text}
        """
    )
    return
'''


def cell_transform_time_series(n_datasets: int) -> str:
    """Transform + plot for time-series charts. Works with df_0."""
    return '''
@app.cell
def _(df_0, pd):
    _counts = df_0.groupby("countryName").size().reset_index(name="n")
    _top = _counts.nlargest(8, "n")["countryName"]
    transformed = df_0[df_0["countryName"].isin(_top)].copy()
    transformed = transformed.sort_values(["countryName", "year"])
    transformed
    return (transformed,)


@app.cell
def _(transformed, alt, mo):
    _chart = (
        alt.Chart(transformed)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("value:Q", title="Value"),
            color=alt.Color("countryName:N", title="Country"),
            tooltip=["countryName", "year", "value"],
        )
        .properties(width=700, height=400)
    )
    mo.ui.altair_chart(_chart)
    return
'''


def cell_transform_comparison(n_datasets: int) -> str:
    """Transform + plot for comparison charts."""
    return '''
@app.cell
def _(df_0, pd):
    _latest_year = df_0.groupby("countryName")["year"].max().reset_index()
    _latest_year.columns = ["countryName", "latest_year"]
    _merged = df_0.merge(_latest_year, left_on=["countryName", "year"], right_on=["countryName", "latest_year"])
    transformed = (
        _merged.sort_values("value", ascending=False)
        .head(20)
        .copy()
    )
    transformed
    return (transformed,)


@app.cell
def _(transformed, alt, mo):
    _chart = (
        alt.Chart(transformed)
        .mark_bar()
        .encode(
            x=alt.X("value:Q", title="Value"),
            y=alt.Y("countryName:N", title="Country", sort="-x"),
            color=alt.Color("value:Q", scale=alt.Scale(scheme="blues"), legend=None),
            tooltip=["countryName", "year", "value"],
        )
        .properties(width=700, height=500)
    )
    mo.ui.altair_chart(_chart)
    return
'''


def cell_transform_before_after(n_datasets: int) -> str:
    """Transform + plot for before/after charts."""
    return '''
@app.cell
def _(df_0, pd):
    _earliest = df_0.loc[df_0.groupby("countryName")["year"].idxmin()][["countryName", "year", "value"]]
    _earliest.columns = ["countryName", "start_year", "start_value"]
    _latest = df_0.loc[df_0.groupby("countryName")["year"].idxmax()][["countryName", "year", "value"]]
    _latest.columns = ["countryName", "end_year", "end_value"]
    _merged = _earliest.merge(_latest, on="countryName")
    _merged["delta"] = _merged["end_value"] - _merged["start_value"]
    transformed = _merged.sort_values("delta", ascending=False).head(20).copy()
    transformed
    return (transformed,)


@app.cell
def _(transformed, alt, pd, mo):
    _start = transformed[["countryName", "start_year", "start_value"]].rename(
        columns={"start_year": "year", "start_value": "value"}
    )
    _start["period"] = "start"
    _end = transformed[["countryName", "end_year", "end_value"]].rename(
        columns={"end_year": "year", "end_value": "value"}
    )
    _end["period"] = "end"
    _plot_df = pd.concat([_start, _end], ignore_index=True)

    _lines = (
        alt.Chart(_plot_df)
        .mark_line()
        .encode(
            x=alt.X("period:N", title="Period", sort=["start", "end"]),
            y=alt.Y("value:Q", title="Value"),
            detail="countryName:N",
            color=alt.Color("countryName:N", title="Country"),
            tooltip=["countryName", "period", "value"],
        )
    )
    _points = (
        alt.Chart(_plot_df)
        .mark_circle(size=60)
        .encode(
            x=alt.X("period:N", sort=["start", "end"]),
            y=alt.Y("value:Q"),
            color=alt.Color("countryName:N"),
            tooltip=["countryName", "period", "year", "value"],
        )
    )
    _chart = (_lines + _points).properties(width=500, height=400)
    mo.ui.altair_chart(_chart)
    return
'''


def cell_transform_multi_dataset(existing_datasets: list[str]) -> str:
    """Transform + plot for multi-dataset charts. Merges df_0 and df_1."""
    n = len(existing_datasets)
    if n < 2:
        # Fall back to comparison style if only 1 dataset available
        return cell_transform_comparison(1)

    # Build merge chain for first 2 datasets (scatter makes sense for 2)
    return '''
@app.cell
def _(df_0, df_1, meta_0, meta_1, pd):
    _d0 = df_0[["countryName", "year", "value"]].rename(columns={"value": "x_value"})
    _d1 = df_1[["countryName", "year", "value"]].rename(columns={"value": "y_value"})
    _merged = _d0.merge(_d1, on=["countryName", "year"])
    _latest_year = _merged.groupby("countryName")["year"].max().reset_index()
    _latest_year.columns = ["countryName", "latest_year"]
    transformed = _merged.merge(
        _latest_year, left_on=["countryName", "year"], right_on=["countryName", "latest_year"]
    ).drop(columns=["latest_year"])
    transformed
    return (transformed,)


@app.cell
def _(transformed, meta_0, meta_1, alt, mo):
    _chart = (
        alt.Chart(transformed)
        .mark_circle(size=80)
        .encode(
            x=alt.X("x_value:Q", title=meta_0["title"]),
            y=alt.Y("y_value:Q", title=meta_1["title"]),
            color=alt.Color("countryName:N", title="Country"),
            tooltip=["countryName", "year", "x_value", "y_value"],
        )
        .properties(width=600, height=400)
    )
    mo.ui.altair_chart(_chart)
    return
'''


def cell_highlights(highlights: list[str]) -> str:
    items = "\n        ".join(f"- {_esc(h)}" for h in highlights)
    return f'''
@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        {items}
        """
    )
    return
'''


# -- Main generator --------------------------------------------------------

def generate_notebook(viz: dict) -> str:
    vid = viz["id"]
    title = viz["title"]
    desc = viz["description"]
    dataset_ids = viz["datasetIds"]
    chart_type = viz["chartType"]
    highlights = viz["highlights"]
    group = chart_group(chart_type)

    existing_datasets = [d for d in dataset_ids if (DATASETS_DIR / f"{d}.json").exists()]

    cells = []
    cells.append(cell_imports())
    cells.append(cell_title(title, desc))
    cells.append(cell_data_sources(dataset_ids))
    cells.append(cell_data_imports())

    # Load each existing dataset
    for i, did in enumerate(existing_datasets):
        cells.append(cell_load_dataset(i, did))

    if existing_datasets:
        cells.append(cell_transformation_prose(group))

        if group == "time_series":
            cells.append(cell_transform_time_series(len(existing_datasets)))
        elif group == "comparison":
            cells.append(cell_transform_comparison(len(existing_datasets)))
        elif group == "before_after":
            cells.append(cell_transform_before_after(len(existing_datasets)))
        elif group == "multi_dataset":
            cells.append(cell_transform_multi_dataset(existing_datasets))

    cells.append(cell_highlights(highlights))

    # Assemble notebook
    body = "\n".join(cells)
    notebook = f'''import marimo

app = marimo.App(width="medium")

{body}

if __name__ == "__main__":
    app.run()
'''
    return notebook


def main():
    NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)

    with open(VIZ_INDEX) as f:
        index = json.load(f)

    viz_list = index["visualizations"]
    print(f"Found {len(viz_list)} visualizations")

    for viz in viz_list:
        vid = viz["id"]
        nb_path = NOTEBOOKS_DIR / f"{vid}.py"
        code = generate_notebook(viz)
        nb_path.write_text(code)
        print(f"  Generated {nb_path.name}")

    # Update index with notebookPath
    for viz in viz_list:
        viz["notebookPath"] = f"notebooks/{viz['id']}.py"

    index["lastUpdated"] = "2026-03-20T12:00:00.000Z"
    with open(VIZ_INDEX, "w") as f:
        json.dump(index, f, indent=2)
        f.write("\n")

    print(f"\nDone. Generated {len(viz_list)} notebooks.")
    print("Updated index.json with notebookPath for all entries.")


if __name__ == "__main__":
    main()
