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

## Usage
### Alternative 1 (without python)
Avoid the python part and use the already running endpoint. It is running
on Heroku so it has its limitations. 

#### In the code editor
``` javascript
var checker = require('users/fitoprincipe/s2checker:main')

// Local endpoint. Uncomment this line if the server is running locally
//var endpoint = 'http://127.0.0.1:5000/check';
var endpoint = null;

var level = 'toa' // or 'sr'
var start = '2021-09-15'
var end = '2021-09-21'
var check = new checker.Checker(geometry, level, start, end, endpoint);

print(ui.Label('CHECK', null, check.url()))
```
https://code.earthengine.google.com/4a5472d6d80990ce58afa385cf5f9adc

If you hit an error that says:

> **Application error**: An error occurred in the application 
and your page could not be served. If you are the application 
owner, check your logs for details. You can do this from the 
Heroku CLI with the command

is because you are asking too much, to solve it decrease the area
of the geometry or the time window.

### Alternative 2 (with python)
If you run the server locally you can fetch more data, so you won't
hit the _Application error_. Also, you can modify the code to your needs
and even contribute to this project to make it better for everyone.

Steps:
1. Clone this repository
2. Create a virtual environment (for example: `s2checker`)
3. Activate the environment
4. Navigate to the repository folder
5. Install dependencies:
   >pip install -r requirements.txt
6. Create a new file in the repo folder called `.env` (text file)
7. Add the following to that file:
   > FLASK_ENV=development
   > HUB_USER=your_copernicus_hub_user
   > HUB_PASS=your_copernicus_hub_password
8. Run the server:
   >flask run
9. The server is running, now you can uncomment the `endpoint` line
   in the [code editor code](#in-the-code-editor)