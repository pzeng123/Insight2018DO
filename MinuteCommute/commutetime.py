import urllib.request
import json
from app import app, db
from models import Listing, Commutetime
import datetime

api_key = app.config['API_KEY']
# Commutetime.query.delete()
# db.session.commit()

# input_path = 'position.txt'
# destination = '260 sheridan ave, Palo Alto, CA 94306'
mode_list = ['driving', 'walking', 'bicycling', 'transit']

# total_list=[]
# sort_by = 0

def  calctime(current_apartment, work_location):

    # if 2 locations are already in Commutetime database, no need calculate again
    if len(Commutetime.query.filter_by(ori_geotag=str(current_apartment)).filter_by(dest_geotag=str(work_location)).all()) > 0:
        print('Already in db')
        print(len(Commutetime.query.filter_by(ori_geotag=str(current_apartment)).filter_by(dest_geotag=str(work_location)).all()))
        print(Commutetime.query.filter_by(ori_geotag=str(current_apartment)).filter_by(dest_geotag=str(work_location)).all()[0].dri_time)
        return



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
            return        
        moderecord.append(duration_sec)
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
    )
    db.session.add(current_commutetime)
    db.session.commit() 
    
    # tabledata = Commutetime.query.filter_by(ori_geotag=str(work_location)).order_by(Commutetime.dri_time).all()
   
    # return tabledata

 
def comtime(work_location): 
    # destination = '260 sheridan ave, Palo Alto, CA 94306'    
    destination = work_location.replace(' ', '+')
    request = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + destination + '&key=' + api_key
    response = urllib.request.urlopen(request).read()
    destination_geo = json.loads(response)
    print(destination_geo)
    
#    destination_geo = {'results': [{'address_components': [{'long_name': '260', 'short_name': '260', 'types': ['street_number']}, {'long_name': 'Sheridan Avenue', 'short_name': 'Sheridan Ave', 'types': ['route']}, {'long_name': 'Evergreen Park', 'short_name': 'Evergreen Park', 'types': ['neighborhood', 'political']}, {'long_name': 'Palo Alto', 'short_name': 'Palo Alto', 'types': ['locality', 'political']}, {'long_name': 'Santa Clara County', 'short_name': 'Santa Clara County', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'California', 'short_name': 'CA', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United States', 'short_name': 'US', 'types': ['country', 'political']}, {'long_name': '94306', 'short_name': '94306', 'types': ['postal_code']}], 'formatted_address': '260 Sheridan Ave, Palo Alto, CA 94306, USA', 'geometry': {'bounds': {'northeast': {'lat': 37.4265923, 'lng': -122.14075}, 'southwest': {'lat': 37.4261187, 'lng': -122.1413468}}, 'location': {'lat': 37.42632529999999, 'lng': -122.1409849}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 37.4277044802915, 'lng': -122.1396994197085}, 'southwest': {'lat': 37.4250065197085, 'lng': -122.1423973802915}}}, 'place_id': 'ChIJwW8E---6j4ARWl7K2guxWtE', 'types': ['premise']}], 'status': 'OK'}
    
    try:
        lat = destination_geo['results'][0]['geometry']['location']['lat']
        lon = destination_geo['results'][0]['geometry']['location']['lng']
        # round to 0.001, ~100 meter distance
        work_location = (float("{0:.3f}".format(lat)), float("{0:.3f}".format(lon)))
    except Exception:
        print('input error')
        return     
       
    apartments = Listing.query.limit(3).all()

    print(('work_location = {}, apartments =  {}').format(work_location, apartments))

    for apartment in apartments:
        calctime((apartment.lat, apartment.lon), work_location)   
     
    # ordered table data    
    tabledata = Commutetime.query.filter_by(dest_geotag=str(work_location)).order_by(Commutetime.dri_time).limit(20).all()
    print('tabledata = {}'.format(tabledata))
    return tabledata

   
    # print('__________________________')
    # test = Commutetime.query.all()
    # print('testdata = {}'.format(test))
    # for t in test:
        # print(t.dri_time)
    
    
# with open(input_path, "r") as inputfile:
    # for current_apartment in inputfile:
        # endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
       
        # ## remove the last '\n' of the start point
        # current_apartment = current_apartment.strip()
        # origin = current_apartment
        # destination = destination.replace(' ', '+')
# #        print('****************************')        
# #        print(current_apartment)
        # with open('position2.txt', 'a') as f:
            # f.write(current_apartment)

        # current_list = [current_apartment]
        # for mode in mode_list:
            # travelmode = 'mode=' + mode +'&'
            # nav_request = travelmode + 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
            # request = endpoint + nav_request
            # #print(request)

            # response = urllib.request.urlopen(request).read()
            # directions = json.loads(response)


            # try:
                # duration = directions['routes'][0]['legs'][0]['duration']['text']
                # duration_sec = directions['routes'][0]['legs'][0]['duration']['value']
            # except Exception:
                # with open('position2.txt', 'a') as f:
                    # f.write('|' + '')
                # continue
# #            if duration_sec > 90*60:
# #                continue

# #            print('{}: {}'.format(mode, duration))
            # #print(directions['routes'][0]['legs'][0]['duration']['text'])
            # current_list.append(str(duration_sec))
            # with open('position2.txt', 'a') as f:
                # f.write('|' + str(duration_sec))
        # with open('position2.txt', 'a') as f:
            # f.write('\n')
        # total_list.append(current_list)
# with open('position3.txt', 'a') as f:
    # total_list.sort(key=lambda x: x[sort_by + 1])
    # for item in total_list:
        # f.write(str(item[0]) + '|' + str(item[sort_by + 1]))
        # f.write('\n')
     




        
       
