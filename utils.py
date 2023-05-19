import numpy as np
import xarray as xr
import math
import holoviews as hv
import hvplot.xarray  # noqa: F401


def band_index(ds, band):
    return np.nanargmin(abs(ds["wavelengths"].values - band))


def gamma_adjust(ds, band, brightness):
    # Define Reflectance Array
    array = ds["reflectance"].sel(bands=band).data
    # Create exponent for gamma scaling - can be adjusted by changing 0.2 - higher values 'brighten' the whole scene
    gamma = math.log(brightness) / math.log(np.nanmean(array))
    # Apply scaling and clip to 0-1 range
    scaled = np.power(array, gamma).clip(0, 1)
    # Assign NA's to 1 so they appear white in plots
    scaled = np.nan_to_num(scaled, nan=1)
    return scaled


def get_dataset(ds, wavelengths, brightness):
    r, g, b = wavelengths
    # This function works, but ideally we can do this in place rather
    # than creating a new dataset.

    # Tidy up the variable naming below so that wavelength values aren't hard coded into variable names...
    band_1 = band_index(ds, r)
    band_2 = band_index(ds, g)
    band_3 = band_index(ds, b)

    # Scale the Bands, r, g and b will be used for the rendered image
    r = gamma_adjust(ds, band_1, brightness)
    g = gamma_adjust(ds, band_2, brightness)
    b = gamma_adjust(ds, band_3, brightness)

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


def build_interactive_map(ds, ds_rgb):
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
    hv.Layout(map + click_dmap * point_dmap).cols(1)