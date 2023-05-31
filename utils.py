import math

import holoviews as hv
import hvplot.xarray  # noqa: F401
import numpy as np
import xarray as xr
import os

from typing import Union, Optional


def get_earthdata_token():
    """
    Load the earthdata token from an environment variable or text file
    Requires either an EARTHDATA_TOKEN environment variable or a text file
    called EARTHDATA_TOKEN.txt in the users home directory.
    """
    try:
        token = os.environ["EARTHDATA_TOKEN"]
        print("Loaded token from EARTHDATA_TOKEN environment variable")
    except KeyError:
        try:
            # Open a text file from users home directory
            home = os.path.expanduser("~")
            with open(os.path.join(home, "EARTHDATA_TOKEN.txt")) as f:
                token = f.read().strip()
                print("Loaded token from EARTHDATA_TOKEN.txt file")
        except FileNotFoundError:
            raise ValueError(
                "No EARTHDATA_TOKEN environment variable or EARTHDATA_TOKEN.txt file found. See README.md"
            )
    return token


def hv_to_rio_geometry(hv_polygon: hv.Polygons) -> list:
    """Convert a HoloViews Polygons object to a GeoJSON-like geometry"""
    coordinates = [[x, y] for x, y in zip(hv_polygon["xs"], hv_polygon["ys"])]
    return [
        {
            "type": "Polygon",
            "coordinates": [coordinates],
        }
    ]


def hv_stream_to_rio_geometries(hv_polygon: hv.Polygons) -> list:
    """Convert a HoloViews polygon_stream object to a GeoJSON-like geometry"""

    geoms = [[x, y] for x, y in zip(hv_polygon["xs"], hv_polygon["ys"])]

    for geom in geoms:
        xs, ys = geom
        coordinates = [[x, y] for x, y in zip(xs, ys)]
        # Holoviews is stupid.
        coordinates.append(coordinates[0])

        yield [
            {
                "type": "Polygon",
                "coordinates": [coordinates],
            }
        ]


def band_index(ds, band):
    """Redundant method. It was used when there wasn't a band index"""
    return ds.sel(bands=band, method="nearest")


def gamma_adjust(
    ds: xr.Dataset,
    band: Union[str, int, float],
    brightness: float,
    replace_nans: Optional[bool] = True,
    replace_value: Optional[Union[int, float]] = 1,
):
    """
    Apply gamma scaling to a band in a dataset.

    Modified from `emit_tools.py`
    """
    # Define Reflectance Array
    array = ds["reflectance"].sel(bands=band, method="nearest").compute().data

    # Create exponent for gamma scaling - can be adjusted by changing
    # 0.2 - higher values 'brighten' the whole scene
    gamma = math.log(brightness) / math.log(np.nanmedian(array))

    # Apply scaling and clip to 0-1 range
    scaled = np.power(array, gamma).clip(0, 1)

    # Assign NA's to 1 so they appear white in plots
    if replace_nans:
        scaled = np.nan_to_num(scaled, nan=replace_value)

    return scaled


def get_rgb_dataset(
    ds: xr.Dataset,
    wavelengths: list[Union[int, float, str]],
    brightness: Union[float, list[float]],
) -> xr.Dataset:
    """
    Create an RGB dataset with scaled values for each band.

    This is overcomplicated, but it works, so it'll do for now.

    Modified from `emit_tools.py`
    """
    # This function works, but ideally we can do this in place rather
    # than creating a new dataset.

    r, g, b = wavelengths

    if type(brightness) in [tuple, list]:
        r_brightness, g_brightness, b_brightness = brightness
    else:
        r_brightness, g_brightness, b_brightness = brightness, brightness, brightness

    # Scale the Bands, r, g and b will be used for the rendered image
    r = gamma_adjust(ds, r, r_brightness)
    g = gamma_adjust(ds, g, g_brightness)
    b = gamma_adjust(ds, b, b_brightness)

    # Stack Bands and make an index
    rgb = np.stack([r, g, b])
    bds = np.array([0, 1, 2])

    # Pull lat and lon values from geocorrected arrays
    x = ds["longitude"].values
    y = ds["latitude"].values

    # Create new rgb xarray data array.
    data_vars = {"RGB": (["bands", "latitude", "longitude"], rgb)}
    coords = {
        "bands": (["bands"], bds),
        "latitude": (["latitude"], y),
        "longitude": (["longitude"], x),
    }
    attrs = ds.attrs
    ds_rgb = xr.Dataset(data_vars=data_vars, coords=coords, attrs=attrs)
    ds_rgb.coords["latitude"].attrs = ds["longitude"].attrs
    ds_rgb.coords["longitude"].attrs = ds["latitude"].attrs
    return ds_rgb


def build_interactive_map(ds: xr.Dataset, ds_rgb: xr.Dataset) -> hv.Layout:
    """
    Build an interactive map with a spectral plot that updates based on mouse hover.
    """
    # RGB image/map
    map = ds_rgb.hvplot.rgb(
        x="longitude", y="latitude", bands="bands", aspect="equal", frame_width=600
    )

    # Stream of X and Y positional data
    posxy = hv.streams.PointerXY(source=map, x=147.5, y=-42.7)
    clickxy = hv.streams.Tap(source=map, x=147.5, y=-42.7)

    # Function to build a new spectral plot based on mouse hover positional information retrieved from the RGB image using our full reflectance dataset
    def point_spectra(x, y):
        return ds.sel(longitude=x, latitude=y, method="nearest").hvplot.line(
            y="reflectance", x="wavelengths", color="#1b9e77", frame_width=400
        )

    # Function to build spectral plot of clicked location to show on hover stream plot
    def click_spectra(x, y):
        clicked = ds.sel(longitude=x, latitude=y, method="nearest")
        return clicked.hvplot.line(
            y="reflectance", x="wavelengths", color="black", frame_width=600
        ).opts(
            title=f"Latitude = {clicked.latitude.values.round(3)}, Longitude = {clicked.longitude.values.round(3)}"
        )

    # Define the Dynamic Maps
    point_dmap = hv.DynamicMap(point_spectra, streams=[posxy])
    click_dmap = hv.DynamicMap(click_spectra, streams=[clickxy])

    # Plot the Map and Dynamic Map side by side
    return hv.Layout(map + click_dmap * point_dmap).cols(1)
