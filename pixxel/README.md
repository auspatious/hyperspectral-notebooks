# PIXXEL Data

[Pixxel](https://www.pixxel.space/) is a hyperspectral imaging startup.

Notebooks in this folder work with a sample image that was converted
to a Cloud Optimised Geotiff and hosted on S3. It's unlikely that this
image will continue to be hosted, so a new sample dataset will need
to be acquired.

Note that the simplest way to make a COG from a non-COG is to use
[rio-cogeo](https://github.com/cogeotiff/rio-cogeo)'s command
`rio convert <in-file> <out-file>`.