"""Shared builder for the Residential (11) and Companies (12) cost-benefit
notebooks.

Both notebooks follow the exact same pattern already validated in
09_costbenefit.ipynb / 10_costbenefit_additional_measures.ipynb, including
the legend/label fixes applied to notebook 10 (in-bar measure names replaced
by a legend on the cost-benefit chart; explicit legend on the return-period
chart; the waterfall's 'Averted' text moved onto the arrow shaft). The two
notebooks differ only in:
- which Entity file / asset name they use
- Companies has an Exposures-swap measure (relocation), so it needs the
  present+future relocation HDF5 wiring that Residential does not
- Companies gets both decision-maker maps (expected annual impact, and the
  RP100-depth map with relocation markers); Residential only gets the first
  map, since it has no relocation measure to mark

Run from the notebooks/ directory with the climada_env environment, passing
the asset name as a command-line argument: "residential" or "companies".
"""
import sys

import nbformat

DPI = 420

ASSET_CONFIGS = {
    "residential": {
        "notebook": "11_costbenefit_residential.ipynb",
        "entity_file": "Porto_Alegre_BRAZIL_Entity_Floods_Residential_calibrated_measures.xlsx",
        "asset_label": "Residential",
        "n_measures": 6,
        "measure_names_hint": (
            "Home flood-proofing, Residential parametric insurance, "
            "City-wide drainage upgrade, Relocation of high-risk households, "
            "Community-based early warning system, Flood-resistant building "
            "codes for renovations"
        ),
        "has_relocation": True,
        "relocation_measure_name": "Relocation of high-risk households",
        "relocation_hdf5_present": "Porto_Alegre_BRAZIL_Exposures_Residential_relocated.hdf5",
        "relocation_hdf5_future": "Porto_Alegre_BRAZIL_Exposures_Residential_relocated_2050.hdf5",
        "output_prefix": "brazil_residential",
        "map_title_eai": "Residential exposure in Porto Alegre: expected annual impact (2025, no adaptation)",
        "eai_point_size": 2,
    },
    "companies": {
        "notebook": "12_costbenefit_companies.ipynb",
        "entity_file": "Porto_Alegre_BRAZIL_Entity_Floods_Companies_calibrated_measures.xlsx",
        "asset_label": "Companies",
        "n_measures": 6,
        "measure_names_hint": (
            "Portable flood barriers for businesses, Business interruption "
            "insurance, Relocation of high-risk businesses, Levee protecting "
            "the commercial district, Elevated inventory storage for "
            "retailers, Business continuity & supply chain diversification"
        ),
        "has_relocation": True,
        "relocation_measure_name": "Relocation of high-risk businesses",
        "relocation_hdf5_present": "Porto_Alegre_BRAZIL_Exposures_Companies_relocated.hdf5",
        "relocation_hdf5_future": "Porto_Alegre_BRAZIL_Exposures_Companies_relocated_2050.hdf5",
        "output_prefix": "brazil_companies",
        "map_title_eai": "Businesses in Porto Alegre: expected annual impact (2025, no adaptation)",
        "eai_point_size": 8,
    },
}


def build(asset_key):
    cfg = ASSET_CONFIGS[asset_key]
    cells = []
    md = lambda s: cells.append(nbformat.v4.new_markdown_cell(s))
    code = lambda s: cells.append(nbformat.v4.new_code_cell(s))

    md(
        f"# Cost-benefit calculations — {cfg['asset_label']}\n\n"
        f"This notebook applies the same cost-benefit pattern used in "
        "`09_costbenefit.ipynb` / `10_costbenefit_additional_measures.ipynb` "
        f"(Schools) to the **{cfg['asset_label']}** asset type, now that it "
        "has been calibrated (see `06b_calibration_residential_companies.ipynb`).\n\n"
        f"Measures: {cfg['measure_names_hint']}.\n\n"
        "All data and calculation steps mirror the Schools notebooks; the "
        "in-bar measure-name overlap on the cost-benefit chart, the missing "
        "legend on the return-period chart, and the waterfall arrow label "
        "overlap have already been fixed here (see FEEDBACK_measures_exercise.md)."
    )

    code(
        "from pathlib import Path\n"
        "\n"
        "ENTITY_DIR = \"../data/entity_files_adaptation/\"\n"
        f"ENTITY_FILE = \"{cfg['entity_file']}\"\n"
        "entity_path = Path(ENTITY_DIR) / ENTITY_FILE\n"
        "\n"
        "HAZARD_DIR = \"../data/hazard/\"\n"
        "HAZARD_RETURN_PERIODS = [10, 20, 50, 100, 200, 500]\n"
        "HAZARD_FILES = [f\"PortoAlegre_RP{rp}_depth.tif\" for rp in HAZARD_RETURN_PERIODS]\n"
        "haz_paths = [Path(HAZARD_DIR) / f for f in HAZARD_FILES]\n"
        "\n"
        "YEAR_PRESENT = 2025\n"
        "YEAR_FUTURE = 2050\n"
        "\n"
        "FUTURE_HAZARD_FREQUENCIES_PATH = \"../data/hazard/porto_alegre_rp_mapping_2025_2050.csv\""
    )

    md("### Create present-day and future Entity objects")

    code(
        "import copy\n"
        "from climada.entity import Entity, MeasureSet\n"
        "\n"
        "entity_present = Entity.from_excel(entity_path)\n"
        "entity_future = copy.deepcopy(entity_present)\n"
        "\n"
        "entity_present.exposures.ref_year = YEAR_PRESENT\n"
        "entity_present.exposures.value_unit = \"USD\"\n"
        f"entity_present.exposures.description = f\"{{YEAR_PRESENT}} {cfg['asset_label'].lower()} economic exposure\"\n"
        "\n"
        "entity_future.exposures.ref_year = YEAR_FUTURE\n"
        "entity_future.exposures.value_unit = \"USD\"\n"
        f"entity_future.exposures.description = f\"{{YEAR_FUTURE}} {cfg['asset_label'].lower()} economic exposure\"\n"
        "\n"
        "ECONOMIC_GROWTH_RATE = 0.02\n"
        "n_years = YEAR_FUTURE - YEAR_PRESENT\n"
        "growth = (1 + ECONOMIC_GROWTH_RATE) ** n_years\n"
        "\n"
        "new_gdf = entity_future.exposures.gdf\n"
        "new_gdf[\"value\"] = new_gdf[\"value\"] * growth\n"
        "entity_future.exposures.set_gdf(new_gdf)\n"
        "\n"
        "print(f\"Total value of exposures in {YEAR_PRESENT}: {entity_present.exposures.value.sum():,.2f} USD\")\n"
        "print(f\"Total value of exposures in {YEAR_FUTURE}: {entity_future.exposures.value.sum():,.2f} USD\")"
    )

    md("### Create present-day and future hazard objects")

    code(
        "import numpy as np\n"
        "import pandas as pd\n"
        "from climada.hazard import Hazard\n"
        "\n"
        "def event_frequency_from_return_periods(return_periods):\n"
        "    rp_rev = copy.deepcopy(return_periods)[::-1]\n"
        "    exceedance_frequency = np.array([1/rp for rp in rp_rev])\n"
        "    event_frequency = np.diff(np.concatenate([[0], exceedance_frequency]))\n"
        "    event_frequency = event_frequency[::-1]\n"
        "    return event_frequency\n"
        "\n"
        "event_frequency_present = event_frequency_from_return_periods(HAZARD_RETURN_PERIODS)\n"
        "\n"
        "haz_present = Hazard.from_raster(\n"
        "    files_intensity = haz_paths,\n"
        "    attrs={\n"
        "        'unit': 'm',\n"
        "        'event_name': [f'Return period {rp}' for rp in HAZARD_RETURN_PERIODS],\n"
        "        'frequency': event_frequency_present\n"
        "    },\n"
        "    haz_type='FL'\n"
        ")\n"
        "\n"
        "future_rps_df = pd.read_csv(Path(FUTURE_HAZARD_FREQUENCIES_PATH))\n"
        "assert future_rps_df[\"historical_return_period\"].tolist() == HAZARD_RETURN_PERIODS, \\\n"
        "    \"The return periods in the future frequencies file do not match the return periods of the hazard data\"\n"
        "\n"
        "future_rps = future_rps_df[\"future_return_period_2050\"]\n"
        "event_frequency_future = event_frequency_from_return_periods(future_rps)\n"
        "\n"
        "haz_future = copy.deepcopy(haz_present)\n"
        "haz_future.event_name = [f'Return period {rp}' for rp in future_rps]\n"
        "haz_future.frequency = event_frequency_future"
    )

    code(
        "entity_present.exposures.assign_centroids(haz_present)\n"
        "entity_future.exposures.assign_centroids(haz_future)"
    )

    if cfg["has_relocation"]:
        md(
            "### Future variant of the relocation measure\n\n"
            "The relocation measure swaps the Exposures for a pre-built HDF5 file. "
            "The present-day file holds 2025 values, but the future Entity's "
            "exposures include economic growth — pointing the future Entity's "
            "measure at the 2025 file would make the measure appear to 'remove' "
            "the growth too, overstating its benefit (see the equivalent fix for "
            "Schools in notebook 10 / FEEDBACK_measures_exercise.md). We already "
            "built both the present-day and 2050 relocated HDF5 files up front "
            "(see `scratch_build_relocated_companies.py`), so we only need to "
            "point the future Entity's measure at the 2050 file here."
        )
        code(
            f"MEASURE_RELOCATION = \"{cfg['relocation_measure_name']}\"\n"
            "\n"
            "entity_future.measures.get_measure(\"FL\", MEASURE_RELOCATION).exposures_set = str(\n"
            f"    Path(ENTITY_DIR) / \"{cfg['relocation_hdf5_future']}\"\n"
            ")\n"
            "\n"
            "from climada.entity import Exposures\n"
            "relocated_future_check = Exposures.from_hdf5(\n"
            f"    Path(ENTITY_DIR) / \"{cfg['relocation_hdf5_future']}\"\n"
            ")\n"
            "relocated_mask = (\n"
            "    relocated_future_check.gdf[\"value\"].values\n"
            "    < entity_future.exposures.gdf[\"value\"].values\n"
            ")\n"
            "print(f\"{relocated_mask.sum()} exposure points relocated in the future variant\")"
        )

    md(
        "## Cost-Benefit calculation\n\n"
        "We initialize a `CostBenefit` object and run the calculation with its `calc` method."
    )

    code(
        "from climada.engine import CostBenefit\n"
        "from climada.engine.cost_benefit import risk_aai_agg\n"
        "\n"
        "costben = CostBenefit()\n"
        "costben.calc(\n"
        "    haz_present,\n"
        "    entity_present,\n"
        "    haz_future=haz_future,\n"
        "    ent_future=entity_future,\n"
        "    assign_centroids=False\n"
        ")"
    )

    code(
        "names = entity_present.measures.get_names()[\"FL\"]\n"
        f"assert len(names) == {cfg['n_measures']}, f\"Expected {cfg['n_measures']} measures, got {{len(names)}}: {{names}}\"\n"
        "assert all(name in costben.cost_ben_ratio for name in names), \\\n"
        "    \"Missing cost_ben_ratio entry for some measure\"\n"
        "assert all(v == v for v in costben.benefit.values()), \"Found NaN in benefits\"  # v != v means NaN\n"
        f"print(f\"{{len(names)}} measures present, no NaN benefits:\", sorted(names))"
    )

    md("## Visualizations")

    code(
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
        "# CLIMADA writes each measure's name vertically inside its bar — replace with\n"
        "# a legend once there are enough measures for the labels to collide (see the\n"
        "# equivalent fix for Schools, notebook 10). Labels are padded with leading\n"
        "# spaces, so compare on the stripped text.\n"
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
        f"ax.set_title(\"Adaptation for {cfg['asset_label'].lower()} in Porto Alegre: benefit and benefit/cost, 2025\\u20132050\")\n"
        f"fig.savefig(OUTPUT_DIR / \"{cfg['output_prefix']}_cost_benefit.png\", dpi={DPI}, bbox_inches=\"tight\")"
    )

    code(
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
        f"ax.set_title(\"{cfg['asset_label']}: losses prevented by each measure, by return period (2050 frequencies)\")\n"
        f"fig.savefig(OUTPUT_DIR / \"{cfg['output_prefix']}_benefits_by_return_period.png\", dpi={DPI}, bbox_inches=\"tight\")"
    )

    code(
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
        "        text.set_position((text.get_position()[0] - 0.28, ax.get_ylim()[1] * 0.40))\n"
        "        text.set_color(\"white\")\n"
        "        text.set_fontsize(13)\n"
        f"fig.savefig(OUTPUT_DIR / \"{cfg['output_prefix']}_waterfall_averted_risk.png\", dpi={DPI}, bbox_inches=\"tight\")"
    )

    md(
        "### Map for decision-makers\n\n"
        f"Expected annual impact per exposure point (2025, no adaptation), over a "
        "Porto Alegre basemap, to show where the risk is concentrated."
    )

    code(
        "import contextily as ctx\n"
        "import matplotlib.pyplot as plt\n"
        "import matplotlib.colors as mcolors\n"
        "import cartopy.crs as ccrs\n"
        "from matplotlib.ticker import ScalarFormatter\n"
        "from climada.engine import ImpactCalc\n"
        "\n"
        "imp_present = ImpactCalc(\n"
        "    entity_present.exposures, entity_present.impact_funcs, haz_present\n"
        ").impact(save_mat=False, assign_centroids=False)\n"
        "\n"
        "ax = imp_present.plot_basemap_eai_exposure(\n"
        "    ignore_zero=True,\n"
        "    buffer=1500,\n"
        f"    s={cfg['eai_point_size']},\n"
        "    zoom=12,\n"
        "    url=ctx.providers.CartoDB.Positron,\n"
        "    cmap=\"autumn_r\",\n"
        "    figsize=(12, 10),\n"
        ")\n"
        "\n"
        "# The colorbar's automatic scientific-notation offset label (e.g. '1e6',\n"
        "# placed just above the colorbar) collides with a long, centered title\n"
        "# once values exceed 1e6. Force plain (non-scientific) tick labels instead\n"
        "# of fighting the collision with title placement/size.\n"
        "cbar_ax = ax.figure.axes[-1]\n"
        "fmt = ScalarFormatter(useOffset=False)\n"
        "fmt.set_scientific(False)\n"
        "cbar_ax.yaxis.set_major_formatter(fmt)\n"
        "\n"
        "# plot_basemap_eai_exposure() already calls ax.set_title(...) internally\n"
        "# (at the default center position) -- calling set_title again at the same\n"
        "# (default) position replaces it; passing loc='left' here instead would add\n"
        "# a *second*, independent title slot that overlaps the first\n"
        f"ax.set_title(\"{cfg['map_title_eai']}\", fontsize=13)\n"
        "\n"
        "# Overlay the 100-year flood-depth 'mancha' on top of the EAI points (as\n"
        "# with the relocation maps, the hazard patch is always drawn/kept above the\n"
        "# exposure layer -- zorder=5 puts it above the EAI scatter's default zorder).\n"
        "# `ax` here is a cartopy GeoAxes in Web Mercator (set up internally by\n"
        "# plot_basemap_eai_exposure for the contextily basemap), so raw lon/lat\n"
        "# values need transform=ccrs.PlateCarree() or they plot off in the corner\n"
        "# near the projection's origin instead of over Porto Alegre.\n"
        "rp100_idx = HAZARD_RETURN_PERIODS.index(100)\n"
        "depth = haz_present.intensity[rp100_idx, :].toarray().flatten()\n"
        "flooded = depth > 0.05\n"
        "sc_depth = ax.scatter(\n"
        "    haz_present.centroids.lon[flooded],\n"
        "    haz_present.centroids.lat[flooded],\n"
        "    c=depth[flooded], s=0.5, cmap=\"Blues\",\n"
        "    norm=mcolors.Normalize(0, 5), alpha=0.55, zorder=5,\n"
        "    transform=ccrs.PlateCarree(),\n"
        ")\n"
        "plt.colorbar(sc_depth, ax=ax, shrink=0.7, pad=0.12, label=\"100-year flood depth (m)\")\n"
        "\n"
        f"ax.figure.savefig(OUTPUT_DIR / \"{cfg['output_prefix']}_map_expected_annual_impact.png\", dpi={DPI}, bbox_inches=\"tight\")"
    )

    output_files = [
        f"{cfg['output_prefix']}_cost_benefit.png",
        f"{cfg['output_prefix']}_benefits_by_return_period.png",
        f"{cfg['output_prefix']}_waterfall_averted_risk.png",
        f"{cfg['output_prefix']}_map_expected_annual_impact.png",
    ]

    if cfg["has_relocation"]:
        md(
            "### Map: relocation measure\n\n"
            f"100-year flood depth with all exposure points and the {cfg['asset_label'].lower()} "
            "proposed for the relocation measure marked."
        )
        code(
            "import matplotlib.pyplot as plt\n"
            "import matplotlib.colors as mcolors\n"
            "\n"
            "rp100_idx = HAZARD_RETURN_PERIODS.index(100)\n"
            "depth = haz_present.intensity[rp100_idx, :].toarray().flatten()\n"
            "flooded = depth > 0.05\n"
            "\n"
            "fig2, ax2 = plt.subplots(figsize=(9, 10))\n"
            "\n"
            "# Draw order (and explicit zorder as a safety net): exposure points at the\n"
            "# bottom, the flood-depth 'mancha' (hazard patch) above them so it always\n"
            "# stays visible instead of being covered by dense exposure scatter, and the\n"
            "# relocation markers on top of everything so they remain a clear call-out.\n"
            "ax2.scatter(\n"
            "    entity_present.exposures.longitude, entity_present.exposures.latitude,\n"
            # Indigo, small, semi-transparent: plain black at this point density paints
            # solid black blobs that hide the basemap streets and the blue flood-depth
            # layer underneath; a lighter, translucent, non-competing color (distinct
            # from the blue hazard scale and the red relocation markers) shows density
            # as a gradient instead
            f"    s=3, c=\"#4b0082\", alpha=0.35, linewidths=0, zorder=1, label=\"{cfg['asset_label']}\",\n"
            ")\n"
            "\n"
            "sc = ax2.scatter(\n"
            "    haz_present.centroids.lon[flooded],\n"
            "    haz_present.centroids.lat[flooded],\n"
            "    c=depth[flooded], s=0.5, cmap=\"Blues\",\n"
            "    norm=mcolors.Normalize(0, 5), alpha=0.6, zorder=2,\n"
            ")\n"
            "plt.colorbar(sc, ax=ax2, shrink=0.7, label=\"100-year flood depth (m)\")\n"
            "\n"
            "ax2.scatter(\n"
            "    entity_present.exposures.longitude[relocated_mask],\n"
            "    entity_present.exposures.latitude[relocated_mask],\n"
            # Thin, smaller markers so tightly-clustered relocation points (some real
            # datasets have several within ~1 km of each other) read as an overlapping
            # cluster rather than merging into a solid block
            "    s=45, c=\"red\", marker=\"x\", linewidths=2, zorder=3, label=\"Proposed relocation\",\n"
            ")\n"
            "try:\n"
            "    ctx.add_basemap(ax2, crs=\"EPSG:4326\", source=ctx.providers.CartoDB.Positron, zoom=12)\n"
            "except Exception as err:\n"
            "    print(f\"Basemap unavailable ({err}); continuing without it\")\n"
            "ax2.set_xlabel(\"Longitude\")\n"
            "ax2.set_ylabel(\"Latitude\")\n"
            "ax2.legend(loc=\"upper left\")\n"
            f"ax2.set_title(\"Porto Alegre: 100-year flood depth, {cfg['asset_label'].lower()} and proposed relocations\")\n"
            f"fig2.savefig(OUTPUT_DIR / \"{cfg['output_prefix']}_map_rp100_depth_relocation.png\", dpi={DPI}, bbox_inches=\"tight\")"
        )
        output_files.append(f"{cfg['output_prefix']}_map_rp100_depth_relocation.png")

    files_literal = ",\n    ".join(f'"{f}"' for f in output_files)
    code(
        "for f in [\n"
        f"    {files_literal},\n"
        "]:\n"
        "    size = (OUTPUT_DIR / f).stat().st_size\n"
        "    assert size > 10_000, f\"{f} looks too small ({size} bytes)\"\n"
        "    print(f\"{f}: {size:,} bytes\")"
    )

    nb = nbformat.v4.new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nbformat.write(nb, cfg["notebook"])
    print(f"Wrote {cfg['notebook']} with {len(cells)} cells")


if __name__ == "__main__":
    asset_key = sys.argv[1] if len(sys.argv) > 1 else None
    assert asset_key in ASSET_CONFIGS, f"Usage: python {sys.argv[0]} [residential|companies]"
    build(asset_key)
