import urllib.request
import json
from project import app, db
from project.models import Listing, Commutetime
import datetime
import googlemaps


gmaps = googlemaps.Client(key=app.config['API_KEY'])

mode_list = ['driving', 'walking', 'bicycling', 'transit']

# destination = '260 sheridan ave, Palo Alto, CA 94306'

def  calctime(current_apartment, work_location, cl_id):

    # if too far direct distance > 40mile
    if (work_location[0] - current_apartment[0])**2 + (work_location[1] - current_apartment[1])**2 >= 0.36:
        return 1
    
    
    # if 2 locations are already in Commutetime database, no need calculate again, but record cl_id
    stored_commutepair = Commutetime.query.filter_by(ori_geotag=str(current_apartment)).filter_by(dest_geotag=str(work_location)).all()
    if len(stored_commutepair) > 0:
#        print('Already in db')
#        print(len(stored_commutepair))
#        print(stored_commutepair[0].dri_time)
                
        try:     
            current_commutetime = Commutetime(
                req_time = datetime.datetime.now(),
                ori_geotag = stored_commutepair[0].ori_geotag,
                ori_lat = stored_commutepair[0].ori_lat,
                ori_lon = stored_commutepair[0].ori_lon,
                dest_geotag = stored_commutepair[0].dest_geotag,
                dest_lat = stored_commutepair[0].dest_lat,
                dest_lon = stored_commutepair[0].dest_lon,
                dri_time = stored_commutepair[0].dri_time,
                wlk_time = stored_commutepair[0].wlk_time,
                bik_time = stored_commutepair[0].bik_time,
                bus_time = stored_commutepair[0].bus_time,
                cl_id =cl_id,
            )
            db.session.add(current_commutetime)
            db.session.commit() 
        except Exception:
            return 5
                
        return 2

    moderecord = []
    for mode in mode_list:

        now = datetime.datetime.now()
        departure_time = now.replace(hour=8, minute=0) + datetime.timedelta(days=1)
        sorigin = str(current_apartment[0]) + ',' + str(current_apartment[1])
        sdest = str(work_location[0]) + ',' + str(work_location[1])
#        print(sorigin)
        directions_result = gmaps.directions(sorigin, sdest, mode=mode, departure_time=departure_time)
#        print('directions_result = {}'.format(directions_result))
        if not directions_result:
            return -1
        
        
        duration = directions_result[0]['legs'][0]['duration']['text']
        duration_traffic = duration
        if mode == 'driving':
            duration_traffic = directions_result[0]['legs'][0]['duration_in_traffic']['text']
        duration_sec = directions_result[0]['legs'][0]['duration']['value']
#        print(duration, duration_traffic, duration_sec)
    
        moderecord.append(duration)
#        print('moderecord = {}'.format(moderecord))
        
    try:
        current_commutetime = Commutetime(
            req_time = datetime.datetime.now(),
            ori_geotag = str(current_apartment),
            ori_lat = current_apartment[0],
            ori_lon = current_apartment[1],
            dest_geotag = str(work_location),
            dest_lat = work_location[0],
            dest_lon = work_location[1],
            dri_time = moderecord[0],
            wlk_time = moderecord[1],
            bik_time = moderecord[2],
            bus_time = moderecord[3],
            cl_id = cl_id
        )
        
        db.session.add(current_commutetime)
        db.session.commit() 
    except Exception:
        print('Commutetime table error')
        return 5 

    return 4
 
def comtime(work_location, lowprice, highprice): 
    if not work_location:
        work_location = ' '
    # Geocoding an address
    geocode_result = gmaps.geocode(work_location)
#    print('geocode_result = {}'.format(geocode_result))
    if not geocode_result:
        return -1
# [{'address_components': [{'short_name': '260', 'types': ['street_number'], 'long_name': '260'}, {'short_name': 'Sheridan Ave', 'types': ['route'], 'long_name': 'Sheridan Avenue'}, {'short_name': 'Evergreen Park', 'types': ['neighborhood', 'political'], 'long_name': 'Evergreen Park'}, {'short_name': 'Palo Alto', 'types': ['locality', 'political'], 'long_name': 'Palo Alto'}, {'short_name': 'Santa Clara County', 'types': ['administrative_area_level_2', 'political'], 'long_name': 'Santa Clara County'}, {'short_name': 'CA', 'types': ['administrative_area_level_1', 'political'], 'long_name': 'California'}, {'short_name': 'US', 'types': ['country', 'political'], 'long_name': 'United States'}, {'short_name': '94306', 'types': ['postal_code'], 'long_name': '94306'}], 'geometry': {'location_type': 'ROOFTOP', 'location': {'lng': -122.1409849, 'lat': 37.42632529999999}, 'viewport': {'southwest': {'lng': -122.1423973802915, 'lat': 37.4250065197085}, 'northeast': {'lng': -122.1396994197085, 'lat': 37.4277044802915}}, 'bounds': {'southwest': {'lng': -122.1413468, 'lat': 37.4261187}, 'northeast': {'lng': -122.14075, 'lat': 37.4265923}}}, 'formatted_address': '260 Sheridan Ave, Palo Alto, CA 94306, USA', 'place_id': 'ChIJwW8E---6j4ARWl7K2guxWtE', 'types': ['premise']}]

    lat = geocode_result[0]['geometry']['location']['lat']
    lon = geocode_result[0]['geometry']['location']['lng']
        # round to 0.001, ~100 meter distance
    work_location = (float("{0:.3f}".format(lat)), float("{0:.3f}".format(lon)))
#    print(work_location)

    apartments = Listing.query.all()

#    print(('work_location = {}, apartments =  {}').format(work_location, apartments))

    for apartment in apartments:
        calctime((apartment.lat, apartment.lon), work_location, apartment.cl_id)   
     
    # ordered table data 
    tabledata = Commutetime.query.filter_by(dest_geotag=str(work_location)).filter_by().order_by(Commutetime.dri_time).limit(30).all()
#    print('tabledata = {}'.format(tabledata))
    records = []
    for row in tabledata:
        current_row = [str(row.req_time), row.dest_geotag, row.dest_lat, row.dest_lon, row.ori_geotag, row.ori_lat, row.ori_lon, row.dri_time, row.wlk_time, row.bik_time, row.bus_time]
        records.append(current_row)
    
#    print(records)
    return records
