# Starter Pack: Flood risk in Porto Alegre, Brazil

This contains the code and documentation for a flood risk analysis for Porto Alegre in Rio Grande do Sul, Brazil. The notebooks explore impacts on housing, businesses and schools.

## How to use

- Clone this repository to your local machine, or download a ZIP of this folder by clicking the green 'Code' dropdown above. 
- Set up a virtual environment with CLIMADA installed. The CLIMADA [Getting Started](https://climada-python.readthedocs.io/en/stable/getting-started/index.html) guide explains how.
- Open the folder in your preferred development environment and activate the virtual environment.
- Run these notebooks. You may need to edit the filepaths at the start of each file. Throughout the notebooks parameters can be changed, and datasets can be modified and improved. We encourage you to explore!


## Structure

- The data/ folder contains all the required input data
- The notebooks/ folder goes through the risk analysis step by step:
    - 01_entity_exposures.ipynb – Mapping the exposed assets
    - 02_entity_impact_functions.ipynb – Visualising the impact functions
    - 03_hazard.ipynb – Mapping the hazard data
    - 04_uncalibrated_risk.ipynb – Running a risk calculation with the uncalibrated data
    - 05a_calibration_housing.ipynb - Calibrating the risk calculation for housing
- The starter_pack_brazil.html file contains these notebooks and their output in a single HTML file


## Contributing

This analysis is intended to support teaching materials and is still under development. If any of the code doesn't work, if something could be added to improve the analysis, or if something could be explained more clearly, please let us know. You can do this by creating a GitHub Issue, or by contacting us by email.
