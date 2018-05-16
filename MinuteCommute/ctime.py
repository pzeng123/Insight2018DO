import urllib.request
import json
from manage import app

api_key = app.config['API_KEY']
input_path = 'position.txt'
destination = '260 sheridan ave, Palo Alto, CA 94306'
mode_list = ['driving', 'walking', 'bicycling', 'transit']

total_list=[]
sort_by = 0



with open(input_path, "r") as inputfile:
    for current_appartment in inputfile:
        endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
       
        ## remove the last '\n' of the start point
        current_appartment = current_appartment.strip()
        origin = current_appartment
        destination = destination.replace(' ', '+')
#        print('****************************')        
#        print(current_appartment)
        with open('position2.txt', 'a') as f:
            f.write(current_appartment)

        current_list = [current_appartment]
        for mode in mode_list:
            travelmode = 'mode=' + mode +'&'
            nav_request = travelmode + 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
            request = endpoint + nav_request
            #print(request)

            response = urllib.request.urlopen(request).read()
            directions = json.loads(response)


            try:
                duration = directions['routes'][0]['legs'][0]['duration']['text']
                duration_sec = directions['routes'][0]['legs'][0]['duration']['value']
            except Exception:
                with open('position2.txt', 'a') as f:
                    f.write('|' + '')
                continue
#            if duration_sec > 90*60:
#                continue

#            print('{}: {}'.format(mode, duration))
            #print(directions['routes'][0]['legs'][0]['duration']['text'])
            current_list.append(str(duration_sec))
            with open('position2.txt', 'a') as f:
                f.write('|' + str(duration_sec))
        with open('position2.txt', 'a') as f:
            f.write('\n')
        total_list.append(current_list)
with open('position3.txt', 'a') as f:
    total_list.sort(key=lambda x: x[sort_by + 1])
    for item in total_list:
        f.write(str(item[0]) + '|' + str(item[sort_by + 1]))
        f.write('\n')
     




        
       
