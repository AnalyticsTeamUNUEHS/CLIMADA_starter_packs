"""Fix the conclusions markdown of the executed 06b notebook.

The generated text said the affected counts 'underestimate' observations for
both asset types; that is true for Companies but Residential OVERestimates
(78k modelled units vs 39k reported buildings). Markdown-only change, so no
re-execution is needed.
"""
import nbformat

NB = "06b_calibration_residential_companies.ipynb"
nb = nbformat.read(NB, as_version=4)

NEW_CONCLUSIONS = (
    "## Conclusions\n\n"
    "- The *affected* step functions cannot reconcile the model's flooded-point counts "
    "with the reported totals, in either direction: Companies can model at most ~4.0k "
    "affected businesses (the exposure dataset holds only 4,366 points) against 65.5k "
    "reported, while Residential models ~78k flooded units at the best threshold against "
    "39.4k reported *buildings* — the observations' definition of 'affected' and their "
    "counting unit don't match the exposure data. As 06a concludes for schools, resolving "
    "this needs aligned definitions or a complete asset registry, not further calibration.\n"
    "- The *loss* calibrations fit a family of near-equivalent curves; the choice inside "
    "that family (saturation < 30 days; effective damage cap free, and necessarily far "
    "below the schools' 70% because these exposure sets are much broader than the loss "
    "totals) is expert judgement and should be revisited with local input. Note the "
    "Companies fit saturates at the grid's lowest max_intensity (0.25 days, i.e. "
    "effectively a step): with a single loss observation the duration-dependence is "
    "unidentifiable, and 'every flooded business loses ~30%' fits as well as any curve.\n"
    "- The calibrated Entity files are written to `data/entity_files_calibrated/` and "
    "verified by re-reading them with CLIMADA and reproducing the calibrated losses "
    "(Residential 0.04%, Companies 0.75% from observations)."
)

for cell in nb.cells:
    if cell.cell_type == "markdown" and cell.source.startswith("## Conclusions"):
        cell.source = NEW_CONCLUSIONS
        break
else:
    raise ValueError("Conclusions cell not found")

nbformat.write(nb, NB)
print("Conclusions cell updated")
