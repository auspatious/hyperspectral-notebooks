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
