"""Improve the decision-maker figures in notebook 10 and add Porto Alegre maps.

Fixes reported by the user:
- cost-benefit chart: 6 vertical in-bar labels overlap each other and the AAI
  marker -> replace with a colour legend, larger figure, title
- benefits-by-return-period chart: no legend -> explicit legend outside axes
- waterfall: 'Averted' arrow text overlaps the value label -> reposition onto
  the arrow shaft, larger figure
- no maps -> two new cells: (1) expected annual impact per school on a
  CartoDB basemap, (2) RP100 flood depth with all schools and the 5 proposed
  relocations highlighted

Run from the notebooks/ directory with the climada_env environment.
"""
import nbformat

NB = "10_costbenefit_additional_measures.ipynb"
DPI = 420

nb = nbformat.read(NB, as_version=4)

CELL_COST_BENEFIT = (
    "from pathlib import Path\n"
    "from matplotlib.patches import Patch\n"
    "\n"
    "OUTPUT_DIR = Path(\"../outputs/\")\n"
    "OUTPUT_DIR.mkdir(exist_ok=True)\n"
    "\n"
    "ax = costben.plot_cost_benefit()\n"
    "fig = ax.figure\n"
    "fig.set_size_inches(13, 7)\n"
    "\n"
    "# The default plot writes each measure's name vertically inside its bar, which\n"
    "# overlaps badly with 6 measures — replace those in-bar labels with a legend, but\n"
    "# keep the 'AAI'/'Tot risk' reference labels. CLIMADA pads these labels with\n"
    "# leading spaces, so compare on the stripped text.\n"
    "names = entity_present.measures.get_names()[\"FL\"]\n"
    "for text in list(ax.texts):\n"
    "    if text.get_text().strip() in names:\n"
    "        text.remove()\n"
    "\n"
    "names_sorted = sorted(names, key=lambda n: costben.benefit[n], reverse=True)\n"
    "handles = [\n"
    "    Patch(\n"
    "        facecolor=tuple(np.asarray(entity_present.measures.get_measure(\"FL\", n).color_rgb)[:3]),\n"
    "        label=n,\n"
    "    )\n"
    "    for n in names_sorted\n"
    "]\n"
    "ax.legend(handles=handles, loc=\"upper right\", title=\"Measures (largest benefit first)\")\n"
    "ax.set_title(\"Adaptation for schools in Porto Alegre: benefit and benefit/cost, 2025\\u20132050\")\n"
    f"fig.savefig(OUTPUT_DIR / \"brazil_schools_cost_benefit.png\", dpi={DPI}, bbox_inches=\"tight\")"
)

CELL_EVENT_VIEW = (
    "from matplotlib.patches import Patch\n"
    "\n"
    "ax = costben.plot_event_view(return_per=future_rps)\n"
    "fig = ax.figure\n"
    "fig.set_size_inches(12, 7)\n"
    "\n"
    "names = entity_present.measures.get_names()[\"FL\"]\n"
    "handles = [\n"
    "    Patch(\n"
    "        facecolor=tuple(np.asarray(entity_present.measures.get_measure(\"FL\", n).color_rgb)[:3]),\n"
    "        label=n,\n"
    "    )\n"
    "    for n in names\n"
    "]\n"
    "handles.append(Patch(facecolor=\"none\", edgecolor=\"black\", label=\"Total risk (no measures)\"))\n"
    "ax.legend(handles=handles, loc=\"upper left\", bbox_to_anchor=(1.02, 1.0))\n"
    "ax.set_title(\"Losses prevented by each measure, by return period (2050 frequencies)\")\n"
    f"fig.savefig(OUTPUT_DIR / \"brazil_schools_benefits_by_return_period.png\", dpi={DPI}, bbox_inches=\"tight\")"
)

CELL_WATERFALL = (
    "# Create a waterfall plot\n"
    "ax = costben.plot_waterfall(\n"
    "       haz_present, entity_present, haz_future, entity_future\n"
    "    )\n"
    "\n"
    "# Add an arrow showing averted risk\n"
    "costben.plot_arrow_averted(\n"
    "    axis=ax,\n"
    "    in_meas_names=entity_present.measures.get_names()['FL'],\n"
    "    accumulate=True,\n"
    "    combine=False,\n"
    "    risk_func=risk_aai_agg,\n"
    "    disc_rates=None,\n"
    "    imp_time_depen=1,\n"
    ")\n"
    "\n"
    "fig = ax.figure\n"
    "fig.set_size_inches(10, 7)\n"
    "ax.set_ylim(0, ax.get_ylim()[1] * 1.08)  # headroom so the bar value labels clear the arrow\n"
    "for text in ax.texts:\n"
    "    if text.get_text() == \"Averted\":\n"
    "        # Move the label from the arrow tip onto the shaft, in white for contrast\n"
    "        text.set_position((text.get_position()[0] - 0.28, ax.get_ylim()[1] * 0.40))\n"
    "        text.set_color(\"white\")\n"
    "        text.set_fontsize(13)\n"
    f"fig.savefig(OUTPUT_DIR / \"brazil_schools_waterfall_averted_risk.png\", dpi={DPI}, bbox_inches=\"tight\")"
)

MD_MAPS = (
    "### Maps for decision-makers\n\n"
    "Two Porto Alegre maps to accompany the charts:\n\n"
    "1. **Where the risk is** — expected annual impact per school (2025, no adaptation) "
    "over a city basemap, highlighting risk hotspots.\n"
    "2. **What the relocation measure does** — the 100-year flood depth footprint with all "
    "122 schools, marking the 5 schools proposed for partial relocation."
)

CELL_MAP_EAI = (
    "import contextily as ctx\n"
    "from climada.engine import ImpactCalc\n"
    "\n"
    "imp_present = ImpactCalc(\n"
    "    entity_present.exposures, entity_present.impact_funcs, haz_present\n"
    ").impact(save_mat=False, assign_centroids=False)\n"
    "\n"
    "ax = imp_present.plot_basemap_eai_exposure(\n"
    "    ignore_zero=True,\n"
    "    buffer=1500,\n"
    "    s=35,\n"
    "    zoom=12,\n"
    "    url=ctx.providers.CartoDB.Positron,\n"
    "    cmap=\"autumn_r\",\n"
    "    figsize=(9, 10),\n"
    ")\n"
    "ax.set_title(\"Schools in Porto Alegre: expected annual impact (2025, no adaptation)\")\n"
    f"ax.figure.savefig(OUTPUT_DIR / \"brazil_schools_map_expected_annual_impact.png\", dpi={DPI}, bbox_inches=\"tight\")"
)

CELL_MAP_RP100 = (
    "import matplotlib.pyplot as plt\n"
    "import matplotlib.colors as mcolors\n"
    "\n"
    "rp100_idx = HAZARD_RETURN_PERIODS.index(100)\n"
    "depth = haz_present.intensity[rp100_idx, :].toarray().flatten()\n"
    "flooded = depth > 0.05\n"
    "\n"
    "fig2, ax2 = plt.subplots(figsize=(9, 10))\n"
    "sc = ax2.scatter(\n"
    "    haz_present.centroids.lon[flooded],\n"
    "    haz_present.centroids.lat[flooded],\n"
    "    c=depth[flooded], s=0.5, cmap=\"Blues\",\n"
    "    norm=mcolors.Normalize(0, 5), alpha=0.6,\n"
    ")\n"
    "plt.colorbar(sc, ax=ax2, shrink=0.7, label=\"100-year flood depth (m)\")\n"
    "\n"
    "ax2.scatter(\n"
    "    entity_present.exposures.longitude, entity_present.exposures.latitude,\n"
    "    s=18, c=\"black\", label=\"Schools\",\n"
    ")\n"
    "ax2.scatter(\n"
    "    entity_present.exposures.longitude[relocated_mask],\n"
    "    entity_present.exposures.latitude[relocated_mask],\n"
    "    s=110, c=\"red\", marker=\"X\", label=\"Proposed partial relocation\",\n"
    ")\n"
    "try:\n"
    "    import contextily as ctx\n"
    "    ctx.add_basemap(ax2, crs=\"EPSG:4326\", source=ctx.providers.CartoDB.Positron, zoom=12)\n"
    "except Exception as err:  # tiles need internet; the map still works without them\n"
    "    print(f\"Basemap unavailable ({err}); continuing without it\")\n"
    "ax2.set_xlabel(\"Longitude\")\n"
    "ax2.set_ylabel(\"Latitude\")\n"
    "ax2.legend(loc=\"upper left\")\n"
    "ax2.set_title(\"Porto Alegre: 100-year flood depth, schools and proposed relocations\")\n"
    f"fig2.savefig(OUTPUT_DIR / \"brazil_map_rp100_depth_schools.png\", dpi={DPI}, bbox_inches=\"tight\")"
)

CELL_VERIFY = (
    "for f in [\n"
    "    \"brazil_schools_cost_benefit.png\",\n"
    "    \"brazil_schools_benefits_by_return_period.png\",\n"
    "    \"brazil_schools_waterfall_averted_risk.png\",\n"
    "    \"brazil_schools_map_expected_annual_impact.png\",\n"
    "    \"brazil_map_rp100_depth_schools.png\",\n"
    "]:\n"
    "    size = (OUTPUT_DIR / f).stat().st_size\n"
    "    assert size > 10_000, f\"{f} looks too small ({size} bytes)\"\n"
    "    print(f\"{f}: {size:,} bytes\")"
)

edited = set()
for i, cell in enumerate(nb.cells):
    if cell.cell_type != "code":
        continue
    src = cell.source
    if "plot_cost_benefit()" in src:
        cell.source = CELL_COST_BENEFIT
        cell.outputs = []
        edited.add("cost_benefit")
    elif "plot_event_view(" in src:
        cell.source = CELL_EVENT_VIEW
        cell.outputs = []
        edited.add("event_view")
    elif "plot_arrow_averted(" in src:
        cell.source = CELL_WATERFALL
        cell.outputs = []
        edited.add("waterfall")
        idx_waterfall = i
    elif "stat().st_size" in src:
        cell.source = CELL_VERIFY
        cell.outputs = []
        edited.add("verify")

assert edited == {"cost_benefit", "event_view", "waterfall", "verify"}, edited

# Insert the maps section between the waterfall cell and whatever follows it,
# unless it was already inserted on a previous run
already = any("plot_basemap_eai_exposure" in c.source for c in nb.cells if c.cell_type == "code")
if not already:
    nb.cells[idx_waterfall + 1:idx_waterfall + 1] = [
        nbformat.v4.new_markdown_cell(MD_MAPS),
        nbformat.v4.new_code_cell(CELL_MAP_EAI),
        nbformat.v4.new_code_cell(CELL_MAP_RP100),
    ]

nbformat.write(nb, NB)
print(f"Edited {sorted(edited)}, maps inserted: {not already}; total {len(nb.cells)} cells")
