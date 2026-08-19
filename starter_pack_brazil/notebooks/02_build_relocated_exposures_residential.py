"""Build the relocated-residential Exposures HDF5 (present + 2050) for the
'Relocation of high-risk households' measure.

Mirrors scratch_build_relocated_companies.py, scaled up: Residential has
20,187 exposure points (vs Companies' 4,366), so we relocate the top 50
(vs 20) by RP100 flood depth -- roughly the same ~0.25-0.45% of points in
both cases.

Run from the notebooks/ directory with the climada_env environment.
"""
import copy
from pathlib import Path

import numpy as np
from climada.entity import Entity
from climada.hazard import Hazard

ENTITY_DIR = "../data/entity_files_calibrated/"
ENTITY_FILE = "Porto_Alegre_BRAZIL_Entity_Floods_Residential_calibrated.xlsx"
entity_path = Path(ENTITY_DIR) / ENTITY_FILE

OUTPUT_DIR = Path("../data/entity_files_adaptation/")
OUTPUT_DIR.mkdir(exist_ok=True)

HAZARD_DIR = "../data/hazard/"
HAZARD_RETURN_PERIODS = [10, 20, 50, 100, 200, 500]
HAZARD_FILES = [f"PortoAlegre_RP{rp}_depth.tif" for rp in HAZARD_RETURN_PERIODS]
haz_paths = [Path(HAZARD_DIR) / f for f in HAZARD_FILES]

N_RELOCATE = 50
RELOCATION_RETAINED_FRACTION = 0.4  # 60% of value considered relocated away

YEAR_PRESENT = 2025
YEAR_FUTURE = 2050
ECONOMIC_GROWTH_RATE = 0.02


def event_frequency_from_return_periods(return_periods):
    rp_rev = copy.deepcopy(return_periods)[::-1]
    exceedance_frequency = np.array([1 / rp for rp in rp_rev])
    event_frequency = np.diff(np.concatenate([[0], exceedance_frequency]))
    return event_frequency[::-1]


entity = Entity.from_excel(entity_path)
entity.exposures.ref_year = YEAR_PRESENT
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
assert (gdf[centr_col] >= 0).all(), "Expected every residential point to match a hazard centroid"

rp100_row = HAZARD_RETURN_PERIODS.index(100)
depths_rp100 = haz.intensity[rp100_row, :].toarray().flatten()[gdf[centr_col].values]
gdf["rp100_depth"] = depths_rp100

top_n_idx = gdf.sort_values("rp100_depth", ascending=False).index[:N_RELOCATE]
assert (gdf.loc[top_n_idx, "rp100_depth"] > 0).all(), (
    "Selected points must actually be flooded at RP100 — check hazard/exposure matching"
)

# --- Present-day (2025) relocated exposures ---
original_total_value = gdf["value"].sum()
gdf_present = gdf.drop(columns="rp100_depth").copy()
gdf_present.loc[top_n_idx, "value"] = gdf_present.loc[top_n_idx, "value"] * RELOCATION_RETAINED_FRACTION
new_total_value = gdf_present["value"].sum()
assert new_total_value < original_total_value, "Relocation should reduce total exposed value"

relocated_present = entity.exposures.copy(deep=True)
relocated_present.set_gdf(gdf_present)
relocated_present.ref_year = YEAR_PRESENT
relocated_present.value_unit = "USD"
relocated_present.description = (
    "Residential exposure with partial relocation of the 50 highest-RP100-depth points"
)
present_path = OUTPUT_DIR / "Porto_Alegre_BRAZIL_Exposures_Residential_relocated.hdf5"
relocated_present.write_hdf5(present_path)

# --- Future (2050) relocated exposures, scaled for economic growth ---
n_years = YEAR_FUTURE - YEAR_PRESENT
growth = (1 + ECONOMIC_GROWTH_RATE) ** n_years
gdf_future = gdf.drop(columns="rp100_depth").copy()
gdf_future["value"] = gdf_future["value"] * growth
gdf_future.loc[top_n_idx, "value"] = gdf_future.loc[top_n_idx, "value"] * RELOCATION_RETAINED_FRACTION

relocated_future = entity.exposures.copy(deep=True)
relocated_future.set_gdf(gdf_future)
relocated_future.ref_year = YEAR_FUTURE
relocated_future.value_unit = "USD"
relocated_future.description = (
    "2050 Residential exposure (grown) with partial relocation of the 50 "
    "highest-RP100-depth points"
)
future_path = OUTPUT_DIR / "Porto_Alegre_BRAZIL_Exposures_Residential_relocated_2050.hdf5"
relocated_future.write_hdf5(future_path)

print(f"RP100 depths of relocated points (min/max): "
      f"{gdf.loc[top_n_idx, 'rp100_depth'].min():.2f} / {gdf.loc[top_n_idx, 'rp100_depth'].max():.2f} m")
print(f"Original total value (2025): {original_total_value:,.2f} USD")
print(f"Relocated total value (2025): {new_total_value:,.2f} USD")
print(f"Unadapted total value (2050, grown): {(gdf['value'] * growth).sum():,.2f} USD")
print(f"Relocated total value (2050): {gdf_future['value'].sum():,.2f} USD")
print(f"Wrote: {present_path}")
print(f"Wrote: {future_path}")
