import requests

class googleMapsAPI_Requests:
    def __init__(self, baseURL_googleMapsAPI, baseURL_googleMaps_addressToPlaceid, api_key):
        self.baseURL_googleMapsAPI = baseURL_googleMapsAPI
        self.baseURL_googleMaps_addressToPlaceid = baseURL_googleMaps_addressToPlaceid
        self.api_key = api_key

    def address_to_placeid(self, address):
        full_request = self.baseURL_googleMaps_addressToPlaceid+'?address='+address+'&key='+self.api_key
        print(full_request)
        response = requests.post(full_request)
        return response.json()['results'][0]['place_id']

    def calc_routes(self, place_id_org, place_id_dest, exp_time, travel_mode='DRIVE'):
        # https://developers.google.com/maps/documentation/routes?hl=en_US - Google's routes api guide
        # https://curlconverter.com/javascript/ - Converting curl command to other languages
        headers = {
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters',
        }
        json_data = {
            'origin': {
                'place_id' : place_id_org
            },
            'destination': {
                'place_id' : place_id_dest
            },
            'travelMode': travel_mode,
            'routingPreference': 'TRAFFIC_AWARE',
            'departureTime': exp_time,
            'computeAlternativeRoutes': True,
            'routeModifiers': {
                'avoidTolls': False,
                'avoidHighways': False,
                'avoidFerries': False,
            },
            'languageCode': 'en-US',
            'units': 'IMPERIAL',
        }
        # https://gist.github.com/ismaels/6636986 - decode polyline code
        response = requests.post(url=self.baseURL_googleMapsAPI, headers=headers, json=json_data)
        return response.json()

    def googleMaps_request(self, path_json):
        #print(address_to_placeid('https://maps.googleapis.com/maps/api/geocode/json', 'Washington'))
        
        # How to handle spaces in place name??
        
        origin_id = self.address_to_placeid(path_json['origin'])
        # origin_id = self.address_to_placeid('Natanya')

        destination_id = self.address_to_placeid(path_json['destination'])
        # destination_id = self.address_to_placeid('Ashdod')
        
        departure_time = path_json['time'] + ":0Z"  # datetime format: yyyy-dd-mmThh:mm:0Z
        print("time Zone *********", departure_time)
        #departure_time = '2023-10-15T15:01:23.045123456Z'
        resp = self.calc_routes(origin_id, destination_id , departure_time, travel_mode='DRIVE')
        
        return resp

    #url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
    #placeid_origin = 'ChIJH3w7GaZMHRURkD-WwKJy-8E'
    #placeid_destination = 'ChIJQX6gY9y8AhURWQAyTCEavqM'
    #args = [url, placeid_origin,placeid_destination, departure_time]
    
    #api_key='AIzaSyB3d-PspnvPDjkOTuYPbteyeyzgTDHsoBc'
    #url_toplaceid = 'https://maps.googleapis.com/maps/api/geocode/json'
    #place_id = address_to_placeid(url_toplaceid, 'Ashdod', api_key)
    #print('place id: ', place_id)
