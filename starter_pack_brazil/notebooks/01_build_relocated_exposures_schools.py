"""Build the relocated-schools Exposures HDF5 for the 'Partial relocation' measure.

Identifies the 5 schools with the highest RP100 flood depth and scales their
value to 40% (60% of the asset value considered relocated out of the flood zone).
Output is consumed by the Entity file's 'assets file' measure column.

Run from the notebooks/ directory with the climada_env environment.
"""
import copy
from pathlib import Path

import numpy as np
from climada.entity import Entity
from climada.hazard import Hazard

ENTITY_DIR = "../data/entity_files_adaptation/"
ENTITY_FILE = "Porto_Alegre_BRAZIL_Entity_Floods_Schools_calibrated_measures.xlsx"
entity_path = Path(ENTITY_DIR) / ENTITY_FILE

HAZARD_DIR = "../data/hazard/"
HAZARD_RETURN_PERIODS = [10, 20, 50, 100, 200, 500]
HAZARD_FILES = [f"PortoAlegre_RP{rp}_depth.tif" for rp in HAZARD_RETURN_PERIODS]
haz_paths = [Path(HAZARD_DIR) / f for f in HAZARD_FILES]

N_RELOCATE = 5
RELOCATION_RETAINED_FRACTION = 0.4  # 60% of value considered relocated away


def event_frequency_from_return_periods(return_periods):
    # Same conversion used in 09_costbenefit.ipynb
    rp_rev = copy.deepcopy(return_periods)[::-1]
    exceedance_frequency = np.array([1 / rp for rp in rp_rev])
    event_frequency = np.diff(np.concatenate([[0], exceedance_frequency]))
    return event_frequency[::-1]


entity = Entity.from_excel(entity_path)
entity.exposures.ref_year = 2025
entity.exposures.value_unit = "USD"

haz = Hazard.from_raster(
    files_intensity=haz_paths,
    attrs={
        "unit": "m",
        "event_name": [f"Return period {rp}" for rp in HAZARD_RETURN_PERIODS],
        "frequency": event_frequency_from_return_periods(HAZARD_RETURN_PERIODS),
    },
    haz_type="FL",
)

entity.exposures.assign_centroids(haz)

centr_col = "centr_FL"
gdf = entity.exposures.gdf.copy()
assert (gdf[centr_col] >= 0).all(), "Expected every school to match a hazard centroid"

rp100_row = HAZARD_RETURN_PERIODS.index(100)
depths_rp100 = haz.intensity[rp100_row, :].toarray().flatten()[gdf[centr_col].values]
gdf["rp100_depth"] = depths_rp100

top_n_idx = gdf.sort_values("rp100_depth", ascending=False).index[:N_RELOCATE]
assert (gdf.loc[top_n_idx, "rp100_depth"] > 0).all(), (
    "Selected schools must actually be flooded at RP100 — check hazard/exposure matching"
)

original_total_value = gdf["value"].sum()
gdf.loc[top_n_idx, "value"] = gdf.loc[top_n_idx, "value"] * RELOCATION_RETAINED_FRACTION
new_total_value = gdf["value"].sum()

assert new_total_value < original_total_value, "Relocation should reduce total exposed value"

relocated_exp = entity.exposures.copy(deep=True)
relocated_exp.set_gdf(gdf.drop(columns="rp100_depth"))
relocated_exp.ref_year = 2025
relocated_exp.value_unit = "USD"
relocated_exp.description = (
    "Schools exposure with partial relocation of the 5 highest-RP100-depth schools"
)

output_path = Path(ENTITY_DIR) / "Porto_Alegre_BRAZIL_Exposures_Schools_relocated.hdf5"
relocated_exp.write_hdf5(output_path)

print(f"Relocated schools (index): {list(top_n_idx)}")
print(f"RP100 depths of relocated schools: {gdf.loc[top_n_idx, 'rp100_depth'].round(2).tolist()} m")
print(f"Original total value: {original_total_value:,.2f} USD")
print(f"Relocated total value: {new_total_value:,.2f} USD")
print(f"Wrote: {output_path}")
