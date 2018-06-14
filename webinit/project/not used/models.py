from project import db
#from sqlalchemy.dialects.postgresql import JSON

## 2 SQL Tables: 'Listing' and 'Commutetime'

class Listing(db.Model):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(120), unique=True)
    ptime = db.Column(db.DateTime)
    geotag = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    location = db.Column(db.String(120))
    cl_id = db.Column(db.String(64), unique=True)
    area = db.Column(db.String(120))
	

    def __init__(self, link, ptime, lat, lon, name, price, location, cl_id, area):
        self.link = link
        self.ptime = ptime
        self.lat = lat
        self.lon = lon
        self.name = name
        self.price = price
        self.location = location
        self.cl_id = cl_id
        self.area = area



    def __repr__(self):
        return '<cl_id {}>'.format(self.cl_id)
        
        
        
class Commutetime(db.Model):
    """
    A table to store commute time between work location and post listings.
    """

    __tablename__ = 'commutetimedata'

    id = db.Column(db.Integer, primary_key=True)
    req_time = db.Column(db.DateTime,  unique=True)
    dest_geotag = db.Column(db.String(64))
    dest_lat = db.Column(db.Float)
    dest_lon = db.Column(db.Float)
    ori_geotag = db.Column(db.String(64))
    ori_lat = db.Column(db.Float)
    ori_lon = db.Column(db.Float)
    dri_time = db.Column(db.String(32))
    wlk_time = db.Column(db.String(32))
    bik_time = db.Column(db.String(32))
    bus_time = db.Column(db.String(32))
    cl_id = db.Column(db.String(64))

    def __init__(self, req_time, dest_geotag, dest_lat, dest_lon, ori_geotag, ori_lat, ori_lon, dri_time, wlk_time, bik_time, bus_time, cl_id):
        self.req_time = req_time
        self.dest_geotag = dest_geotag
        self.dest_lat = dest_lat
        self.dest_lon = dest_lon
        self.ori_geotag = ori_geotag
        self.ori_lat = ori_lat
        self.ori_lon = ori_lon
        self.dri_time = dri_time
        self.wlk_time = wlk_time
        self.bik_time = bik_time
        self.bus_time = bus_time
        self.cl_id = cl_id
    
    
    def __repr__(self):
        return '<{} ---> {}>'.format(self.ori_geotag, self.dest_geotag)
