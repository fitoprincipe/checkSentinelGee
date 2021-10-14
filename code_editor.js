// Draw a geometry
var endpoint = 'http://127.0.0.1:5000/check'
var start = '2021-09-20'
var end = '2021-09-21'

var format_footprint = function(geom) {
  var newcoords = []
  var coords = geom.bounds().coordinates().getInfo()[0]
  for (var i in coords) {
    var coord = coords[i]
    var lon = coord[0]
    var lat = coord[1]
    newcoords.push(lon)
    newcoords.push(lat)
  }
  return newcoords.join(' ')
}

var check_S2_available = function(col, roi, start, end, level) {
  var start = ee.Date(start)
  var end = ee.Date(end)
  var coords = format_footprint(roi)
  var start = start.format('yMMdd').getInfo()
  var end = end.format('yMMdd').getInfo()
  var ingee = col.aggregate_array('PRODUCT_ID').join(' ').getInfo()

  var params = "?coords="+coords+"&start="+start+"&end="+end+"&ingee="+ingee+"&level="+level
  var url = endpoint+params
  return url
}

var check_S2TOA_available = function(roi, start, end) {
  start = ee.Date(start)
  end = ee.Date(end).advance(1, 'day')
  roi = roi.bounds()
  Map.addLayer(roi)
  var col = ee.ImageCollection('COPERNICUS/S2')
              .filterBounds(roi)
              .filterDate(start, end)
  return check_S2_available(col, roi, start, end, 'toa')
}

var url = check_S2TOA_available(geometry, start, end)
print(ui.Label('CHECK', null, url))