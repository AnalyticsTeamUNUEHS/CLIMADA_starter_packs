# Starter Pack: Flood risk in Porto Alegre, Brazil

<div align="center" style="text-align: center; margin: 1.25rem 0 0.75rem 0;">
<img src="../build/logo_CLIMADA.png" alt="CLIMADA logo" height="80" />
</div>

<div align="center" style="text-align: center; margin: 0.75rem 0 1.5rem 0; white-space: nowrap;">
<img src="../build/logo_unu.svg" alt="UNU-EHS logo" height="80" style="margin: 0 18px; vertical-align: middle;" />
<img src="../build/logo_IDB.jpg" alt="IDB logo" height="80" style="margin: 0 18px; vertical-align: middle;" />
</div>

This contains the code and documentation for a flood risk analysis for Porto Alegre in Rio Grande do Sul, Brazil. The notebooks explore impacts on housing, businesses and schools.

## Setup

- Clone this repository to your local machine, or download a ZIP of this folder by clicking the green 'Code' dropdown above followed by the 'Download ZIP' button. 
- Set up a virtual environment with containing CLIMADA. The CLIMADA [Getting Started](https://climada-python.readthedocs.io/en/stable/getting-started/index.html) guide explains how.
- If necessary, set up Jupyter notebooks. You can look up how do this at a system level, which allows the functionality to be reused across environments, or on the command line you can activate your virtual environment (covered in the guide linked above) and run `mamba install jupyter` (you can replace `mamba` with `conda` or with the relevant installation instruction for your environment manager.)
- Either: Open the folder in your preferred development environment and activate the virtual environment. OR: from the command line activate your virtual environment (covered in the guide linked above) and run `jupyter notebook`.
- Run these notebooks. You may need to edit the filepaths at the start of each file. Throughout the notebooks parameters can be changed, and datasets can be modified and improved. We encourage you to explore.

## Structure

- The data/ folder contains all the required input data
- The notebooks/ folder goes through the risk analysis step by step:
    - 01_entity_exposures.ipynb – Mapping the exposed assets
    - 02_entity_impact_functions.ipynb – Visualising the impact functions
    - 03_hazard.ipynb – Mapping the hazard data
    - 04_uncalibrated_risk.ipynb – Running a risk calculation with the uncalibrated data
    - 05_observations.ipynb - Examine the observations data
    - 06a_calibration_schools.ipynb - Calibrating impact functions for schools
    - 09_costbenefit.ipynb - Running a cost-benefit assessment for adaptation measures
- The starter_pack_brazil.html file contains these notebooks and their output in a single HTML file

## Adaptation and cost-benefit exercise (Residential, Companies)

Built on top of the notebooks above, this exercise extends the cost-benefit assessment from
Schools to all three asset types and adds a depth-damage curve correction found along the way:

- 06b_calibration_residential_companies.ipynb – Calibrating impact functions for Residential and Companies (mirrors 06a's method)
- 10_costbenefit_additional_measures.ipynb – Schools cost-benefit with 6 measures (the original 3 plus 3 more)
- 11_costbenefit_residential.ipynb / 12_costbenefit_companies.ipynb – The same 6-measure cost-benefit assessment applied to Residential and Companies

The headline finding is a depth-damage curve fix: Residential and Companies originally used
day-duration-calibrated loss curves; these are replaced with the JRC (Huizinga et al. 2017)
depth-damage curves already used (unlabeled) in the shipped Schools entity. See
`report/report_brazil_adaptation_exercise_en.pdf` (or the Portuguese
`report_brazil_adaptation_exercise_pt.pdf`) for the full methodology, results for all 18
measures (6 per asset x 3 assets), and this finding's derivation. `notebooks/README.md`
indexes the numbered `.py` pipeline scripts that built the inputs for these notebooks —
they aren't needed to reproduce the results (all Entity/HDF5 outputs are already committed
under `data/`), only for provenance or adapting the exercise to a new asset type or country.

`outputs/` holds the resulting figures (cost-benefit charts, benefits by return period,
waterfall, expected-annual-impact maps, and depth maps with relocation points) for all
three asset types.


## Contributing

This analysis is intended to support teaching materials and is still under development. If any of the code doesn't work, if something could be added to improve the analysis, or if something could be explained more clearly, please let us know. You can do this by creating a GitHub Issue, or by contacting us by email.
