from sentinelsat import SentinelAPI, geojson_to_wkt


coords = '-68.45317820662159 -26.35042608088762 -62.36675242537159 -26.35042608088762 -62.36675242537159 -22.002031348439377 -68.45317820662159 -22.002031348439377 -68.45317820662159 -26.35042608088762'
start = '20210920'
end = '20210922'
ingee = 'S2B_MSIL1C_20210920T143729_N0301_R096_T19JEL_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19JEM_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19JEN_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19JFL_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19JFM_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19JFN_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19KEP_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19KEQ_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19KER_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19KFP_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19KFQ_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19KFR_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19KGQ_20210920T180332 S2B_MSIL1C_20210920T143729_N0301_R096_T19KGR_20210920T180332 S2B_MSIL1C_20210921T141049_N0301_R110_T20JMS_20210921T172924 S2B_MSIL1C_20210921T141049_N0301_R110_T20KNU_20210921T172924'
level = 'toa'


MATCH = {
    'identifier': 'PRODUCT_ID',
}


def get_api(user, password):
    return SentinelAPI(user, password, 'https://apihub.copernicus.eu/apihub')


def _date_gee(date):
    y = date[0:4]
    m = date[4:6]
    d = date[6:8]
    return '{}-{}-{}'.format(y, m, d)


class Checker:
    TEMPLATE = """
<table style="width:500px border:1px solid">
  <tr>
    <th>ESA ID</th>
    <th>Is available in GEE?</th>
    <th>Is online in S2 Hub?</th>
    <th>Code Editor</th>
  </tr>
  {content}
</table>
"""
    ROW = """
<tr style='background-color:{color}'>
  <td>{esaid}</td>
  <td>{ingee}</td>
  <td>{online}</td>
  <td>{codeeditor}</td>
</tr>"""

    def __init__(self, coords, start, end, level, ingee, api, 
                 match='identifier'):
        self.coords = coords
        self.level = level
        self.ingee = ingee
        self.start = start
        self.end = end
        self.api = api
        self.match = match
        self._products = None
            
    @property
    def start_gee(self):
        return _date_gee(self.start)

    @property
    def end_gee(self):
        return _date_gee(self.end)
    
    @property
    def ingeelist(self):
        return self.ingee.split(' ')
    
    @property
    def coordlist(self):
        coordlist = self.coords.split(' ')
        points = len(coordlist)
        indices = range(0, int(points), 2)
        final = []
        for i in indices:
            lon = float(coordlist[i])
            lat = float(coordlist[i+1])
            final.append((lon, lat))
        return final

    @property
    def products(self):
        if not self._products:
            products = self.api.query(
              self.footprint,
              date = (self.start, self.end),
              platformname = 'Sentinel-2',
              processinglevel = self.plevel
            )
            self._products = products
        return self._products
    
    def _isTOA(self):
        if self.level.lower() in ['l1c', 'level-1c', 'toa', 'level1c']:
            return True
        else:
            return False
    
    @property
    def plevel(self):
        return 'Level-1C' if self._isTOA() else 'Level-2A'
    
    def gee_ic_id(self):
        """ return GEE image collection id """
        toa = 'COPERNICUS/S2'
        sr = 'COPERNICUS/S2_SR'
        return toa if self._isTOA() else sr
    
    def gee_ic(self):
        return "ee.ImageCollection({})".format(self.gee_ic_id())
    
    def _product_id_to_gee_id(self, pid):
        pinfo = self.products[pid]
        identifier = pinfo['identifier']
        datastrip = pinfo['datastripidentifier']
        one = identifier.split('_')[2] 
        two = datastrip.split('_')[7][1:]
        three = identifier.split('_')[5]
        return '{}_{}_{}'.format(one, two, three)
    
    def gee_image(self, pid):
        icid = self.gee_ic_id()
        iid = self._product_id_to_gee_id(pid)
        return "ee.Image('{}/{}')".format(icid, iid)
    
    def code_editor(self, pid):
        template = 'var i = {}; print(i)'
        return template.format(self.gee_image(pid))
    
    def _createGeoJSON(self):
        polyDict = {
            'type': 'Polygon',
            'coordinates': [self.coordlist]
        }
        return polyDict
    
    @property
    def footprint(self):
        """ Get footprint from coordinates """
        # coords format: 'lon lat lon lat....'
        geojson = self._createGeoJSON()
        return geojson_to_wkt(geojson)
    
    def _get_hub_ids(self):
        ids = []
        for pid, v in dict(self.products).items():
            for key, value in v.items():
                if key == self.match:
                    if value not in ids:
                        ids.append([value, pid])
        return ids
    
    def check(self):
        hubIDs = self._get_hub_ids()
        data = []
        for hid, pid in hubIDs:
            online = self.api.is_online(pid)
            code = self.code_editor(pid)
            final = [hid, hid in self.ingeelist, online, code]
            data.append(final)
        return data
    
    def _format_row(self, row):
        esaid, ingee, online, code = row
        av = 'YES' if ingee else 'NO'
        onl = 'YES' if online else 'NO'
        color = 'green' if ingee else 'red'
        return self.ROW.format(color=color, esaid=esaid, 
                               ingee=av, online=onl, 
                               codeeditor=code)
    
    def create_html(self):
        """ Products is a list of ((esaID, available on gee, online in ESA,
        code in code editor), ...) """
        rows = self.check()
        htmlrows = ""
        for row in rows:
            data = self._format_row(row)
            htmlrows += data
        
        return self.TEMPLATE.format(content=htmlrows)
