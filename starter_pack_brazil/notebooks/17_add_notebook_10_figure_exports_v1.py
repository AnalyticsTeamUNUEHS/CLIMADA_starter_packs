"""Add 420-DPI figure exports to the three plotting cells of notebook 10.

Edits the existing plot cells in place (no duplicate plotting cells):
- cost-benefit bar chart      -> outputs/brazil_schools_cost_benefit.png
- benefits by return period   -> outputs/brazil_schools_benefits_by_return_period.png
- waterfall with averted risk -> outputs/brazil_schools_waterfall_averted_risk.png

Run from the notebooks/ directory with the climada_env environment.
"""
import nbformat

NB = "10_costbenefit_additional_measures.ipynb"
DPI = 420

nb = nbformat.read(NB, as_version=4)

SETUP = (
    "from pathlib import Path\n"
    "OUTPUT_DIR = Path(\"../outputs/\")\n"
    "OUTPUT_DIR.mkdir(exist_ok=True)\n"
)

edited = set()
for cell in nb.cells:
    if cell.cell_type != "code":
        continue
    src = cell.source
    if "plot_cost_benefit()" in src and "savefig" not in src:
        cell.source = (
            SETUP
            + "\nax = costben.plot_cost_benefit()\n"
            + f"ax.figure.savefig(OUTPUT_DIR / \"brazil_schools_cost_benefit.png\", dpi={DPI}, bbox_inches=\"tight\")\n"
        )
        edited.add("cost_benefit")
    elif "plot_event_view(" in src and "savefig" not in src:
        cell.source = (
            src.rstrip()
            + f"\nax.figure.savefig(OUTPUT_DIR / \"brazil_schools_benefits_by_return_period.png\", dpi={DPI}, bbox_inches=\"tight\")\n"
        )
        edited.add("event_view")
    elif "plot_arrow_averted(" in src and "savefig" not in src:
        cell.source = (
            src.rstrip()
            + f"\nax.figure.savefig(OUTPUT_DIR / \"brazil_schools_waterfall_averted_risk.png\", dpi={DPI}, bbox_inches=\"tight\")\n"
        )
        edited.add("waterfall")

assert edited == {"cost_benefit", "event_view", "waterfall"}, f"Only edited: {edited}"

# Final verification cell: figures exist and are non-trivial
code_verify = nbformat.v4.new_code_cell(
    "for f in [\n"
    "    \"brazil_schools_cost_benefit.png\",\n"
    "    \"brazil_schools_benefits_by_return_period.png\",\n"
    "    \"brazil_schools_waterfall_averted_risk.png\",\n"
    "]:\n"
    "    size = (OUTPUT_DIR / f).stat().st_size\n"
    "    assert size > 10_000, f\"{f} looks too small ({size} bytes)\"\n"
    "    print(f\"{f}: {size:,} bytes\")"
)
nb.cells.append(code_verify)

nbformat.write(nb, NB)
print(f"Edited cells: {sorted(edited)}; appended verification cell; total {len(nb.cells)} cells")
