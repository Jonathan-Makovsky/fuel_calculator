from flask import Flask, render_template, request
import sys

from src import db_request, google_maps_api_request

# To run from terminal: $ flask --app server run
# On run:
app = Flask(__name__)
db_obj = db_request.DB_Requests()   # Object to make the requests to DB
api_key='AIzaSyB3d-PspnvPDjkOTuYPbteyeyzgTDHsoBc'
base_url_api_route = 'https://routes.googleapis.com/directions/v2:computeRoutes'
base_url_api_addressToPlaceId = 'https://maps.googleapis.com/maps/api/geocode/json'
googleAPI_obj = google_maps_api_request.googleMapsAPI_Requests(base_url_api_route, base_url_api_addressToPlaceId, api_key) # Object to make the requests to googleMapsAPI

@app.route("/")
def home():
    return render_template('index2.html')

@app.route("/cars_query", methods=['POST'])
def cars_query():
    #print(request.headers.get('Content-Type'))
    request_data = request.get_json()
    #print("request Data:")
    #print(request_data)
    response = db_obj.car_request(request_data)
    #print("response Data:")
    #print(response)
    
    return response

@app.route("/submit_form", methods=['POST'])
def submit_form():
    request_data = request.get_json()
    
    print("request Data:")
    # request_data={'car': {'manufacturer_code': [7], 'model_code': [30], 'year_code': [11], 'engine_type_code': [1], 'engine_volume_code': [4], 'cols': ['average_consumption']}, 'path': {'origin': 'Tel Aviv, ישראל', 'destination': 'Bat Yam, ישראל', 'time': '2022-12-14T10:30:0Z'}, 'fuel': 'gasoline'}
    print(request_data)
    
    car_consumption = db_obj.car_request(request_data['car'])
    fuel_price = db_obj.fuelPrice_request(request_data['fuel'])

    #print("consumption: ", car_consumption)
    #print("fuel price: ",fuel_price)
    routes = googleAPI_obj.googleMaps_request(request_data['path'])
    print(routes)
    
    routes_info = routes['routes']
    
    # Fixed price wihout computing
    total_prices = [35.65 for i in range(len(routes_info))]

    response = {
        'routes' : [
            {
                'distance' : routes_info[i]['distanceMeters']/1000.0,
                'time' : ((int)(routes_info[i]['duration'][:-1]))/60.0, # format of duration: 'i...is'
                'total' : total_prices[i],
            }
            for i in range(len(routes_info))
        ],
        'consumption' : car_consumption,
        'price' : fuel_price,
    }

    # response = {
    #     'routes' : 
    #     [
    #         {
    #         'distance' : '12.5',
    #         'time' : '30',
    #         'total' : '35.6',
    #         },
    #     ],
    #     'consumption' : '11.5',
    #     'price' : '6.67',
    # }
    print("response Data:")
    print(response)
    
    return response
