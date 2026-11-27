"""From provinces to autonomous communities.

Concepts: reading data, attribute and spatial filters, CRS,
reprojection, area, dissolve, classified maps and export.
"""
from pathlib import Path
import sys

import matplotlib.pyplot as plt

from geopandas_download_data import load_provinces

ROOT = Path(__file__)
DATA_DIR =  ROOT / "data"
OUT_DIR = ROOT / "outputs"
OUT_CRS = "EPSG:25830"

breakpoint()

OUT_DIR.mkdir(exist_ok=True)

# Read data (downloaded on first run, then cached in DATA_DIR)
prov = load_provinces(DATA_DIR)
breakpoint()

# Explore the downloaded dataframe
print(f"Downloaded (Geo)DataFrame properties:")
print(f"\t- Shape (nrow, ncol): {prov.shape}")
print(f"\t- Coordinate Reference System: {prov.crs}")
print(f"\t- Number of geometries per geometry type:")
print(prov.geom_type.value_counts())

# Select only target columns for the example and rename them
esp = prov[["name", "region", "geometry"]].rename(
    columns={"name": "provincia", "region": "ccaa"}
)
print(f"Selected CCAAs: {', '.join(esp['ccaa'].unique())}")
breakpoint()

# Spatial filter with .cx: Peninsula + Baleares (no Canaries)
esp = esp.cx[-10:5, 35:44]
esp.plot("ccaa")
# plt.show()
breakpoint()

# Area in degrees is meaningless (geopandas warns about it)
# Comment this line after checking the message to hide it
print(esp.area.head(1))
sys.exit()

# Reproject to ETRS89 / UTM 30N, official CRS for mainland Spain
esp = esp.to_crs(OUT_CRS)
esp["area_km2"] = esp.area / 1e6

# Sanity check: Badajoz should be the largest (around 21,700 km2)
print("\nProvinces sorted by area (km2):")
print(esp.sort_values("area_km2", ascending=False).head(2))
sys.exit()

# Dissolve: merge provinces into CCAAs
ccaa = esp.dissolve(
    by="ccaa",
    aggfunc={"area_km2": "sum", "provincia": "count"}
)
breakpoint()

ccaa = ccaa.rename(columns={"provincia": "n_provincias"}).reset_index()
breakpoint()

print("\nCCAAs sorted by area (km2):")
print(ccaa.sort_values("area_km2", ascending=False).head(2))
sys.exit()

# BONUS: Classified map
fig, ax = plt.subplots(figsize=(10, 8))
ccaa.plot(
    column="area_km2",
    scheme="Quantiles",
    k=4,
    cmap="BuGn",
    legend=True,
    legend_kwds={
        "title": "Area (km2)",
        "loc": "lower right",
        "fmt": "{:.1f}"
    },
    ax=ax
)
esp.boundary.plot(ax=ax, color="white", linewidth=0.1)
ccaa.boundary.plot(ax=ax, color="black", linewidth=0.5)

# Add labels inside the prior map
for row in ccaa.itertuples():
    point = row.geometry.representative_point()
    ax.annotate(
        str(row.n_provincias),
        (point.x, point.y),
        ha="center",
        fontsize=9
    )

ax.set_title("CCAA by area (number = provinces)")
ax.set_axis_off()
fig.savefig(
    OUT_DIR / "ccaa_area.png",
    dpi=150,
    bbox_inches="tight"
)
plt.show()

# Export to GeoPackage (driver inferred from the extension)
out_fp = OUT_DIR / "spain_gis.gpkg"
esp.to_file(out_fp, layer="provincias")
ccaa.to_file(out_fp, layer="ccaa")
print(f"\nSaved layers to {out_fp}")
