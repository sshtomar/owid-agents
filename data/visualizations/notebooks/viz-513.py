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
    mo.md("# Visualization Notebook — see HTML file for full methodology")
    return


if __name__ == "__main__":
    app.run()
