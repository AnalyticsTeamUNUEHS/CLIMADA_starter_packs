# Notebooks and pipeline scripts — Brazil adaptation exercise

This folder mixes two things:

- **The starter pack's original notebooks** (`01_...` through `06a_...`, `09_costbenefit.ipynb`): read/run these directly in Jupyter, per the pack's own README.
- **This exercise's deliverable notebooks** (`06b`, `10`, `11`, `12`) and the **numbered `.py` pipeline scripts** that built their inputs. See `../report/report_brazil_adaptation_exercise_en.pdf` for the full methodology and results.

## To reproduce the results

You do **not** need to re-run the numbered `.py` scripts. All the Entity/HDF5 files they produce are already committed under `../data/entity_files_calibrated/` and `../data/entity_files_adaptation/`, and notebooks `06b`, `10`, `11`, `12` are already executed with their outputs saved (including the figures in `../outputs/`). Just open a notebook and re-run it top to bottom (`climada_env`, see `../README.md`) to confirm you get the same numbers.

The `.py` scripts are kept for **provenance** — they show exactly how each input file was derived, in case you want to adapt this exercise to a new asset type or country. Run them from this directory (`notebooks/`), in numeric order, only if you want to rebuild the inputs from scratch.

## Script index, by pipeline phase

**1. Build the "relocation" Exposures HDF5 files** (Exposures-swap measure: the N highest-RP100-depth points get 60% of their value relocated, both a present-day and a growth-scaled 2050 variant)
- `01_build_relocated_exposures_schools.py` — 5 of 122 schools
- `02_build_relocated_exposures_residential.py` — 50 of 20,187 points
- `03_build_relocated_exposures_companies.py` — 20 of 4,366 businesses

**2. Add the first 3 adaptation measures per asset** (to the calibrated Entity file, one row per measure in the `measures` sheet)
- `04_add_measures_schools.py`
- `05_add_measures_residential.py`
- `06_add_measures_companies.py`

**3. Add 3 more measures each**, applying the exercise's "Brazil: +3 additional" rule uniformly across all three assets (Schools already had 3 shipped with the pack; Residential/Companies got these to reach 6 each)
- `07_add_more_measures_residential.py`
- `08_add_more_measures_companies.py`

**4. The JRC depth-damage curve fix** — the single most important correction in this exercise (see the report's "Headline finding"). Replaces Residential/Companies' day-duration-calibrated loss curves with the JRC (Huizinga et al. 2017) depth-damage curves, matching the mechanism already used (unlabeled) in the shipped Schools entity.
- `09_fix_depth_impact_functions_jrc.py`

**5. Refine measure parameters against the acceptance criteria** (no B/C ratio above 50 or NaN, no measure's benefit exceeding total climate risk; insurance attach/cover derived from the model's own exceedance curve)
- `10_refine_insurance_schools.py`
- `11_refine_residential_pre_jrc_fix.py` — **historical**: ran before script 09's fix; superseded by script 12 once the risk scale changed
- `12_refine_after_jrc_fix.py` — current, authoritative Residential/Companies refinement
- `13_refine_measures_above_bc_cap.py` — final re-costing pass for the 3 measures that came back with B/C > 50

**6. Notebook generators**
- `14_build_notebook_06b_calibration.py` — builds `06b_calibration_residential_companies.ipynb` from scratch (mirrors `06a`'s method)
- `15_fix_notebook_06b_conclusions_text.py` — small text correction to that notebook's conclusion
- `16_build_notebook_10_schools_v1.py` — first-pass builder for `10_costbenefit_additional_measures.ipynb` (from `09_costbenefit.ipynb`) — **historical**: several later figure/layout fixes were applied by hand directly to the notebook and are not reflected in this script
- `17_add_notebook_10_figure_exports_v1.py` — **historical**, first pass at exporting figures; superseded by 18
- `18_improve_notebook_10_figures.py` — legend/overlap fixes and the two decision-maker maps for notebook 10
- `19_build_notebook_11_12_generator.py` — **current, canonical** parametrized generator for both `11_costbenefit_residential.ipynb` and `12_costbenefit_companies.ipynb` (`python 19_build_notebook_11_12_generator.py residential|companies`); every subsequent fix (title/colorbar collision, marker color, z-order, JRC curve) was made here and both notebooks regenerated, so this script *does* fully reproduce their current state.

Notebook `10`'s exact current state is **not** fully reproducible from scripts 16-18 alone (some later fixes were applied as one-off edits and aren't preserved as separate scripts) — but since notebook 10 itself is saved fully executed, that's not a problem for reproducing results, only for reproducing *how it was built* from a blank notebook.

**7. Local calibration of the JRC curve's amplitude** — script 09's fix made the curve dimensionally correct (depth in meters) but left its amplitude as raw literature values, never validated against Porto Alegre. Applied to the depth raster whose flooded extent most closely matches the actual 2024 event (RP200 — see script docstring for the area-matching method), the raw JRC curve overestimated the real observed 2024 loss by ~20.7x for Residential and ~2.8x for Companies. This script rescales the MDD curve's amplitude by a single factor per asset (`observed 2024 loss / RP200-modelled loss`), keeping the JRC curve's shape, and recomputes insurance attach/cover from the corrected exceedance curve. Other measures' costs are left untouched (they're programme/infrastructure budgets, not something derived from the risk scale) — after this fix, Residential's 6 measures all come back with B/C < 1 (none currently cost-justified at their parametrized cost), while Companies' measures remain B/C > 1 (just with smaller margins). See `../report/report_brazil_adaptation_exercise_en.pdf`, section 2.5.1, for the full picture.
- `20_recalibrate_jrc_curve_rp200_anchor.py` — originally wrote `*_calibrated_measures_v2.xlsx` for Residential and Companies; those files have since replaced the pre-correction `*_calibrated_measures.xlsx` originals under `data/entity_files_adaptation/` (the superseded versions were removed, not kept, once the correction was final). Schools' own `_v2` file, from a separate fix, is unaffected by this script. Notebooks `11` and `12` reference the current (corrected) `*_calibrated_measures.xlsx` files directly.
