# OWID Agents

Agent-driven data discovery and visualization system using World Bank and WHO public datasets.

## Project Structure

- `src/` - Core library (types, catalog helpers, API clients)
- `cli/` - CLI tools that Claude Code invokes as an agent
- `frontend/` - React + Vite frontend (gallery, dataset browser)
- `data/` - Flat JSON storage (catalog + generated visualizations)
- `prompts/` - Role instructions for discovery and visualization workflows

## Running

```bash
# API server (port 3001)
npx tsx cli/serve.ts

# Frontend dev server (port 5173, proxies /api to 3001)
cd frontend && npm run dev

# Both together
npm run dev
```

## Agent Workflows

### Discovery (find and save datasets)

```bash
# Search for indicators
npx tsx cli/discover.ts search --provider world-bank --topic "population"
npx tsx cli/discover.ts search --provider who-gho --query "mortality"

# Preview data
npx tsx cli/discover.ts fetch --provider world-bank --indicator SP.POP.TOTL

# Save to catalog
npx tsx cli/discover.ts save --provider world-bank --indicator SP.POP.TOTL \
  --title "Total Population" --topics "population,demographics"

# Check catalog
npx tsx cli/catalog.ts list
npx tsx cli/catalog.ts show --id wb--SP-POP-TOTL
npx tsx cli/catalog.ts stats
```

See `prompts/discovery.md` for full discovery agent instructions.

### Visualization (generate charts)

1. Read `data/catalog/index.json` to see available datasets
2. Read dataset files from `data/catalog/datasets/`
3. Write self-contained HTML files (Observable Plot from CDN) to `data/visualizations/viz/`
4. Update `data/visualizations/index.json` with the new entry

See `prompts/visualization.md` for full visualization agent instructions.

## Conventions

- Dataset IDs: `wb--<indicator>` or `who--<indicator>` (dots replaced with dashes)
- Viz IDs: `viz-001`, `viz-002`, etc. (sequential)
- All generated HTML must be self-contained (inline data, CDN scripts)
- HTML is rendered in the frontend via sandboxed iframes
