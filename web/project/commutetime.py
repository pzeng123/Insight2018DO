import urllib.request
import json
from project import app, db
from models import Listing, Commutetime
import datetime

api_key = app.config['API_KEY']
mode_list = ['driving', 'walking', 'bicycling', 'transit']

# destination = '260 sheridan ave, Palo Alto, CA 94306'

def  calctime(current_apartment, work_location, cl_id):
    
    # if too far direct distance > 40mile
    if (work_location[0] - current_apartment[0])**2 + (work_location[1] - current_apartment[1])**2 >= 0.36:
        return 1
    
    
    # if 2 locations are already in Commutetime database, no need calculate again, but record cl_id
    stored_commutepair = Commutetime.query.filter_by(ori_geotag=str(current_apartment)).filter_by(dest_geotag=str(work_location)).all()
    if len(stored_commutepair) > 0:
        print('Already in db')
        print(len(stored_commutepair))
        print(stored_commutepair[0].dri_time)
                
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
        except Exception:
            return 5
                
        return 2

    moderecord = []
    for mode in mode_list:
        travelmode = 'mode=' + mode +'&'
        request = 'https://maps.googleapis.com/maps/api/directions/json?' + travelmode + 'origin=' + str(current_apartment[0]) + ',' + str(current_apartment[1])+ \
        '&destination=' + str(work_location[0]) + ',' + str(work_location[1])+ '&key=' + api_key
        response = urllib.request.urlopen(request).read()
        directions = json.loads(response)
        
        try:
            duration = directions['routes'][0]['legs'][0]['duration']['text']
            duration_sec = directions['routes'][0]['legs'][0]['duration']['value']
        except Exception:
            return 3        
        moderecord.append(duration)
        
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
    except Exception:
        return 5 
    db.session.add(current_commutetime)
    db.session.commit() 
    return 4
 
def comtime(work_location, lowprice, highprice): 
    destination = work_location.replace(' ', '+')
    request = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + destination + '&key=' + api_key
    response = urllib.request.urlopen(request).read()
    print('respons ={}').format(response)

    destination_geo = json.loads(response)
    if destination_geo['status'] == "ZERO_RESULTS":
        print('Wrong Input, Please input again')
        return -1
#    print(destination_geo)
#    destination_geo = {'results': [{'address_components': [{'long_name': '260', 'short_name': '260', 'types': ['street_number']}, {'long_name': 'Sheridan Avenue', 'short_name': 'Sheridan Ave', 'types': ['route']}, {'long_name': 'Evergreen Park', 'short_name': 'Evergreen Park', 'types': ['neighborhood', 'political']}, {'long_name': 'Palo Alto', 'short_name': 'Palo Alto', 'types': ['locality', 'political']}, {'long_name': 'Santa Clara County', 'short_name': 'Santa Clara County', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'California', 'short_name': 'CA', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United States', 'short_name': 'US', 'types': ['country', 'political']}, {'long_name': '94306', 'short_name': '94306', 'types': ['postal_code']}], 'formatted_address': '260 Sheridan Ave, Palo Alto, CA 94306, USA', 'geometry': {'bounds': {'northeast': {'lat': 37.4265923, 'lng': -122.14075}, 'southwest': {'lat': 37.4261187, 'lng': -122.1413468}}, 'location': {'lat': 37.42632529999999, 'lng': -122.1409849}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 37.4277044802915, 'lng': -122.1396994197085}, 'southwest': {'lat': 37.4250065197085, 'lng': -122.1423973802915}}}, 'place_id': 'ChIJwW8E---6j4ARWl7K2guxWtE', 'types': ['premise']}], 'status': 'OK'}
    
    try:
        lat = destination_geo['results'][0]['geometry']['location']['lat']
        lon = destination_geo['results'][0]['geometry']['location']['lng']
        # round to 0.001, ~100 meter distance
        work_location = (float("{0:.3f}".format(lat)), float("{0:.3f}".format(lon)))
    except Exception:
        print('input error')
        return -1    
       
    apartments = Listing.query.limit(16).all()

    print(('work_location = {}, apartments =  {}').format(work_location, apartments))

    for apartment in apartments:
        calctime((apartment.lat, apartment.lon), work_location, apartment.cl_id)   
     
    # ordered table data    
    tabledata = Commutetime.query.filter_by(dest_geotag=str(work_location)).filter_by().order_by(Commutetime.dri_time).limit(20).all()
    print('tabledata = {}'.format(tabledata))
    records = []
    for row in tabledata:
        current_row = [str(row.req_time), row.dest_geotag, row.dest_lat, row.dest_lon, row.ori_geotag, row.ori_lat, row.ori_lon, row.dri_time, row.wlk_time, row.bik_time, row.bus_time]
        records.append(current_row)
    
    print(records)
    return records

