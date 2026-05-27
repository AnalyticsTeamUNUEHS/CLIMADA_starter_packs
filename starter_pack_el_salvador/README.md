# Starter Pack: Drought risk in El Salvador

<div style="text-align: center">
<img src="../build/logo_CLIMADA.png" alt="CLIMADA logo" height="80"/>
</div>

<div style="text-align: center">
<img src="../build/logo_unu.svg" alt="UNU-EHS logo" height="80" style="padding-left:20px; padding-right:20px" />
<img src="../build/logo_IDB.jpg" alt="IDB logo" height="80" style="padding-left:20px; padding-right:20px"/>
</div>

This contains the code and documentation for a drought risk analysis for El Salvador. The notebooks explore impacts on maize, beans and sorghum.

## Setup

- Clone this repository to your local machine, or download a ZIP of this folder by clicking the green 'Code' dropdown above followed by the 'Download ZIP' button. 
- Set up a virtual environment with CLIMADA installed. The CLIMADA [Getting Started](https://climada-python.readthedocs.io/en/stable/getting-started/index.html) guide explains how.
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
- The starter_pack_el_salvador.html file contains these notebooks and their output in a single HTML file


## Contributing

This analysis is intended to support teaching materials and is still under development. If any of the code doesn't work, if something could be added to improve the analysis, or if something could be explained more clearly, please let us know. You can do this by creating a GitHub Issue, or by contacting us by email.
