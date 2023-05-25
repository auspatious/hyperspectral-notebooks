# EMIT Notebook Examples

This repo contains a range of example for working with EMIT hypterspectral data.

## Authentication using a token from NASA Earth Data

To set up authentication so that you can load data, do the following:

1. Register for an account at [https://urs.earthdata.nasa.gov/home](https://urs.earthdata.nasa.gov/home)
2. Visit the `user_tokens` page (the "Generate Token" tab)
3. Generate a token and copy/save the string
4. Either:
   1. Export it as an environment variable, `export EARTHDATA_TOKEN=abcd...` or add it to your `.bashrc
   so that it's permanently exported; or
   2. Save it to a text file in your home directory, `echo "abcd..." > ~/EARTHDATA_TOKEN.txt` (or the
   equivalent on your platform)
5. There's a function in the [utils.py](utils.py) file that will load the token from these
   two locations for use in the notebooks.

## Selecting granules to load

Each notebook has a cell at the top that loads data. You can change the `granule` variable to
load a difference granule. To find other granules, you can explore the
[STAC API](https://radiantearth.github.io/stac-browser/#/external//cmr.earthdata.nasa.gov/cloudstac/LPCLOUD/collections/EMITL2ARFL.v001/)
or the [Data Portal](https://earth.jpl.nasa.gov/emit/data/data-portal/coverage-and-forecasts/).

A selection of reasonably cloud-free scenes have been listed below.

``` python
EMIT_L2A_RFL_001_20230316T045211_2307503_006  # Canberra
EMIT_L2A_RFL_001_20230330T000831_2308815_009  # Menindee
EMIT_L2A_RFL_001_20230312T230451_2307115_002  # Chowilla
EMIT_L2A_RFL_001_20230111T084724_2301105_003  # Jurien Bay
EMIT_L2A_RFL_001_20230316T045133_2307503_005  # Lake Hume
EMIT_L2A_RFL_001_20230401T014442_2309101_005  # Pilbara Coast west of Port Hedland
EMIT_L2A_RFL_001_20230316T045223_2307503_007  # Warragamba Dam and hazard reduction burn
EMIT_L2A_RFL_001_20230401T232248_2309115_011  # Coopers Creek
EMIT_L2A_RFL_001_20230116T044730_2301603_002  # Coorong
EMIT_L2A_RFL_001_20220901T022845_2224402_005  # Limmen Bight
EMIT_L2A_RFL_001_20230115T053714_2301503_007  # Lake Frome
EMIT_L2A_RFL_001_20230111T084712_2301105_002  # Pinnacles Cal/Val site
EMIT_L2A_RFL_001_20230322T031752_2308102_008  # St Vincent Gulf seagrass
EMIT_L2A_RFL_001_20230202T222219_2303314_009  # Bowen
EMIT_L2A_RFL_001_20230324T014237_2308301_002  # Melbourne
EMIT_L2A_RFL_001_20230112T062510_2301204_003  # Murray Mouth
EMIT_L2A_RFL_001_20230303T021147_2306201_022  # Quilpie
EMIT_L2A_RFL_001_20230310T012147_2306901_002  # Hamelin Pools
EMIT_L2A_RFL_001_20230401T014249_2309101_003  # Shark Bay Mid
EMIT_L2A_RFL_001_20230401T014301_2309101_004  # Shark Bay North
```
