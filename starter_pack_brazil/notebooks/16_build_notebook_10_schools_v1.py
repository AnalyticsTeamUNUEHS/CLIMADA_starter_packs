"""Generate 10_costbenefit_additional_measures.ipynb from 09_costbenefit.ipynb.

Changes relative to 09:
1. ENTITY_FILE points to the v2 Entity (6 measures).
2. New cell after assign_centroids: builds the *future* variant of the
   relocation HDF5 (values include economic growth) and points the future
   Entity's relocation measure at it — without this the measure would
   spuriously 'remove' economic growth and overstate its benefit.
3. Sanity-check cell after costben.calc (6 measures, no NaN benefits).

Run from the notebooks/ directory with the climada_env environment.
"""
import nbformat

SRC = "09_costbenefit.ipynb"
DST = "10_costbenefit_additional_measures.ipynb"

nb = nbformat.read(SRC, as_version=4)

# --- 1. Point at the v2 Entity file and retitle ---
replaced_entity = False
for cell in nb.cells:
    if cell.cell_type == "code" and "Porto_Alegre_BRAZIL_Entity_Floods_Schools_calibrated_measures.xlsx" in cell.source:
        cell.source = cell.source.replace(
            "Porto_Alegre_BRAZIL_Entity_Floods_Schools_calibrated_measures.xlsx",
            "Porto_Alegre_BRAZIL_Entity_Floods_Schools_calibrated_measures_v2.xlsx",
        )
        replaced_entity = True
assert replaced_entity, "ENTITY_FILE line not found"

assert nb.cells[0].cell_type == "markdown"
nb.cells[0].source = (
    "# Cost-benefit calculations — extended with 3 additional measures\n\n"
    "This notebook extends `09_costbenefit.ipynb` for the Workshop 3 intersessional "
    "exercise. It uses the v2 Entity file, which adds three measures to the original "
    "three (River dredging, Rebuilding levees, Early warning system):\n\n"
    "- **School floor raising** — raises school floors by 40 cm "
    "(hazard linear transform, `a=1, b=-0.4`)\n"
    "- **Portfolio flood insurance for schools** — portfolio-level risk transfer "
    "(attachment/cover derived from the model's own exceedance curve)\n"
    "- **Partial relocation of high-risk schools** — the 5 schools with the highest "
    "RP100 flood depth have 60% of their value relocated out of the flood zone "
    "(Exposures swap via HDF5)\n\n"
    "All other data and calculation steps are identical to notebook 09."
)

# --- 2. Insert the future-relocation cell after assign_centroids ---
idx_assign = next(
    i for i, c in enumerate(nb.cells)
    if c.cell_type == "code" and "assign_centroids(haz_present)" in c.source
)

md_reloc = nbformat.v4.new_markdown_cell(
    "### Future variant of the relocation measure\n\n"
    "The 'Partial relocation of high-risk schools' measure swaps the Exposures for a "
    "pre-built HDF5 file. The present-day file holds 2025 values, but the future "
    "Entity's exposures include economic growth — if the future Entity's measure "
    "pointed at the 2025 file, the measure would appear to 'remove' the growth too "
    "and its benefit would be overstated. So we build a future variant (grown values, "
    "same 5 schools at 40%) and point the future Entity's measure at it.\n\n"
    "This is done *after* `assign_centroids` so the saved file already carries the "
    "hazard-centroid matching."
)

code_reloc = nbformat.v4.new_code_cell(
    "from climada.entity import Exposures\n"
    "\n"
    "RELOCATION_RETAINED_FRACTION = 0.4\n"
    "MEASURE_RELOCATION = \"Partial relocation of high-risk schools\"\n"
    "\n"
    "relocated_present = Exposures.from_hdf5(\n"
    "    Path(ENTITY_DIR) / \"Porto_Alegre_BRAZIL_Exposures_Schools_relocated.hdf5\"\n"
    ")\n"
    "\n"
    "# Identify the relocated schools by comparing values with the unmodified present entity\n"
    "relocated_mask = (\n"
    "    relocated_present.gdf[\"value\"].values\n"
    "    < entity_present.exposures.gdf[\"value\"].values\n"
    ")\n"
    "assert relocated_mask.sum() == 5, f\"Expected 5 relocated schools, found {relocated_mask.sum()}\"\n"
    "\n"
    "future_gdf = entity_future.exposures.gdf.copy()\n"
    "future_gdf.loc[relocated_mask, \"value\"] = (\n"
    "    future_gdf.loc[relocated_mask, \"value\"] * RELOCATION_RETAINED_FRACTION\n"
    ")\n"
    "relocated_future = entity_future.exposures.copy(deep=True)\n"
    "relocated_future.set_gdf(future_gdf)\n"
    "relocated_future.ref_year = YEAR_FUTURE\n"
    "\n"
    "relocated_future_path = Path(ENTITY_DIR) / \"Porto_Alegre_BRAZIL_Exposures_Schools_relocated_2050.hdf5\"\n"
    "relocated_future.write_hdf5(relocated_future_path)\n"
    "\n"
    "entity_future.measures.get_measure(\"FL\", MEASURE_RELOCATION).exposures_set = str(\n"
    "    relocated_future_path\n"
    ")\n"
    "\n"
    "print(f\"Future relocated exposures written to {relocated_future_path}\")\n"
    "print(f\"Unadapted future total value: {entity_future.exposures.gdf['value'].sum():,.2f} USD\")\n"
    "print(f\"Adapted (relocated) future total value: {future_gdf['value'].sum():,.2f} USD\")"
)

nb.cells[idx_assign + 1:idx_assign + 1] = [md_reloc, code_reloc]

# --- 3. Insert the sanity-check cell after costben.calc ---
idx_calc = next(
    i for i, c in enumerate(nb.cells)
    if c.cell_type == "code" and "costben.calc(" in c.source
)

code_sanity = nbformat.v4.new_code_cell(
    "names = entity_present.measures.get_names()[\"FL\"]\n"
    "assert len(names) == 6, f\"Expected 6 measures, got {len(names)}: {names}\"\n"
    "assert all(name in costben.cost_ben_ratio for name in names), \\\n"
    "    \"Missing cost_ben_ratio entry for some measure\"\n"
    "assert all(v == v for v in costben.benefit.values()), \"Found NaN in benefits\"  # v != v means NaN\n"
    "print(\"6 measures present, no NaN benefits:\", sorted(names))"
)

nb.cells.insert(idx_calc + 1, code_sanity)

nbformat.write(nb, DST)
print(f"Wrote {DST} with {len(nb.cells)} cells (source had {len(nb.cells) - 3})")
