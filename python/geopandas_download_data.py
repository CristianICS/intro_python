"""Download and cache Natural Earth layers for Spain.

Helpers to download the data from the Natural Earth CDN and store
a Spain-only copy as GeoPackage, so later runs work offline.
"""
from pathlib import Path

import geopandas as gpd

NE_URL = "https://naciscdn.org/naturalearth/10m"
SPAIN_BBOX = (-19.0, 27.0, 5.0, 44.5)  # lon/lat, includes the Canaries

def _read_ne(theme, layer, bbox=None):
    """Read a zipped Natural Earth shapefile with lower-case columns."""
    url = f"{NE_URL}/{theme}/{layer}.zip"
    gdf = gpd.read_file(url, bbox=bbox)
    gdf.columns = gdf.columns.str.lower()
    return gdf.loc[:, ~gdf.columns.duplicated()]


def _cached(download_folder, name, download):
    """Return a cached GeoPackage, or download it and save it first.

    `download` is a function: it is only called when there is no cache.
    """
    download_folder = Path(download_folder)
    download_path = download_folder / (name + ".gpkg")
    if not download_path.exists():
        print(f"Downloading '{name}' (first run only)...")
        gdf = download()
        download_folder.mkdir(parents=True, exist_ok=True)
        gdf.to_file(download_path, driver="GPKG")

    return gpd.read_file(download_path)


def _download_provinces():
    prov = _read_ne("cultural", "ne_10m_admin_1_states_provinces")
    return prov[prov["admin"] == "Spain"].reset_index(drop=True)


def _download_cities():
    cities = _read_ne("cultural", "ne_10m_populated_places")
    return cities[cities["adm0name"] == "Spain"].reset_index(drop=True)


def _download_rivers():
    # bbox filters while reading: only nearby features are loaded
    return _read_ne("physical", "ne_10m_rivers_lake_centerlines",
                    bbox=SPAIN_BBOX)


def load_provinces(download_folder):
    """Spanish provinces (Natural Earth admin-1), EPSG:4326."""
    return _cached(download_folder, "provincias", _download_provinces)


def load_cities(download_folder):
    """Spanish populated places, EPSG:4326."""
    return _cached(download_folder, "ciudades", _download_cities)


def load_rivers(download_folder):
    """Rivers around Spain, read with a bounding-box filter, EPSG:4326."""
    return _cached(download_folder, "rios", _download_rivers)
