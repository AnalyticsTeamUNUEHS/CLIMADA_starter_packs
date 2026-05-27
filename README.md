# CLIMADA Starter Packs

<div style="text-align: center">
<img src="build/logo_CLIMADA.png" alt="CLIMADA logo" height="80"/>
</div>

<div style="text-align: center">
<img src="build/logo_unu.svg" alt="UNU-EHS logo" height="80" style="padding-left:20px; padding-right:20px" />
<img src="build/logo_IDB.jpg" alt="IDB logo" height="80" style="padding-left:20px; padding-right:20px"/>
</div>

This repository contains risk analysis starter packs to use with the CLIMADA platform. They include the code and data for you to run analyses, including comments explaining choices and assumptions.

The starter packs are designed to show different parts of CLIMADA in action, and are designed as an accompaniment to teaching materials and to the full, in-depth CLIMADA documentation at [https://climada-python.readthedocs.io/](https://climada-python.readthedocs.io/).


## Contents


### Peru: high resolution flooding in the city of Ica

A study into flood impacts in the city of Ica, Peru, looking at impacts on houses, people and roads and how they change in the future. Particular issues covered:

- Working with return period hazard data
- Handling very high resolution return period flood footprint data, and matching exposures to nearby flood locations
- Calibration to observations from multiple events


### Brazil: event reconstruction in Porto Alegre

A study into flood impacts in the city of Porto Alegre, Brazil. Reconstructing damage curves for the event for homes, businesses and schools using loss data. Particular issues covered:

- Calibrating to event losses from multiple administrative units


### El Salvador: national drought modelling

A simple probabilistic drought model implemented for El Salvador under climate change. Particular issues covered:

- Working with probabilistic hazard data
- Using low-resolution regional statistics in a risk analysis


## Setup

- Clone this repository to your local machine, or download a ZIP of this folder by clicking the green 'Code' dropdown above followed by the 'Download ZIP' button. 
- Set up a virtual environment with CLIMADA installed. The CLIMADA [Getting Started](https://climada-python.readthedocs.io/en/stable/getting-started/index.html) guide explains how.
- If necessary, set up Jupyter notebooks. You can look up how do this at a system level, which allows the functionality to be reused across environments, or on the command line you can activate your virtual environment (covered in the guide linked above) and run `mamba install jupyter` (you can replace `mamba` with `conda` or with the relevant installation instruction for your environment manager.)
- Either: Open the folder in your preferred development environment and activate the virtual environment. OR: from the command line activate your virtual environment (covered in the guide linked above) and run `jupyter notebook`.
- Run these notebooks. You may need to edit the filepaths at the start of each file. Throughout the notebooks parameters can be changed, and datasets can be modified and improved. We encourage you to explore.


## Contributing

This analysis is intended to support teaching materials and is still under development. If any of the code doesn't work, if something could be added to improve the analysis, or if something could be explained more clearly, please let us know. You can do this by creating a GitHub Issue, or by contacting us by email.


## Acknowledgements

This project is funded by the [Inter-American Development Bank](https://www.iadb.org). We thank them for their ideas, guidance and support!