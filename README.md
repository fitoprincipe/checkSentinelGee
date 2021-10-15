# GEE Sentinel Checker

Check if Google Earth Engine (GEE) is missing a Sentinel image by
calling the Copernicus Open Hub API.

This is a Flask (python) application that you can deploy or run locally.

The query parameters are:
- **coords**: the coordinates of the polygon to check. Must be the coordinates of a simple rectangle. Must be a string as follows: "lat lon lat lon..."
- **start**: the start date (inclusive). Format: yyyyMMdd
- **end**: the end date (exclusive). Format: yyyyMMdd
- **ingee**: the ids list of the images available on GEE taken from "PRODUCT_ID" property of the images. Must be a string as follows: "id1 id2 id3..."
- **level**: the processing level of the images (options: 'toa', 'sr')

The file `code_editor.js` contains an example on how to use this web app.