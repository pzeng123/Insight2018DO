from sqlalchemy import Column, String, Integer, DateTime, Float
from project.base import Base

class MyLog(Base):
	"""
	A table to store log record
	"""
	__tablename__ = 'log'
	id = Column(Integer, primary_key=True)
	logtime = Column(DateTime)
	
	def __init__(self, logtime):
		self.logtime = logtime

	def __repr__(self):
		return '<logtime {}>'.format(self.logtime)

class Listing(Base):
	"""
	A table to store data on craigslist listings.
	"""

	__tablename__ = 'listings'

	id = Column(Integer, primary_key=True)
	link = Column(String(120), unique=True)
	ptime = Column(DateTime)
	geotag = Column(String(64))
	lat = Column(Float)
	lon = Column(Float)
	name = Column(String(120))
	price = Column(Float)
	location = Column(String(120))
	cl_id = Column(String(64), unique=True)
	area = Column(String(120))


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



class Commutetime(Base):
	"""
	A table to store commute time between work location and post listings.
	"""

	__tablename__ = 'commutetimedata'

	id = Column(Integer, primary_key=True)
	req_time = Column(DateTime,  unique=True)
	dest_geotag = Column(String(64))
	dest_lat = Column(Float)
	dest_lon = Column(Float)
	ori_geotag = Column(String(64))
	ori_lat = Column(Float)
	ori_lon = Column(Float)
	dri_time = Column(String(32))
	wlk_time = Column(String(32))
	bik_time = Column(String(32))
	bus_time = Column(String(32))
	cl_id = Column(String(64))

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
