import os
import re
import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    # site name from env variable
    site_name = os.environ.get('SITE_NAME')
    pod_name = os.environ.get('POD_NAME') 
    # grab IP from env variable
    ip_address = get_ip()
    if ip_address =='': #ip_address is undefined, likely missing fall-back environment variable
        return render_template('error.html', pod_name=pod_name, site_name=site_name, error_status='Unable to get your IP address.')
    #if no zipcode in URL, guess based on geolocation
    try: 
        zipcode, country, lat, lng = get_location_by_ip(ip_address)
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        return render_template('error.html', pod_name=pod_name, site_name=site_name, error_status='Unable to reach the geolocation API. Try again later.')
    # error if the geo location places user out of the U.S.
    if country != 'US':
        return render_template('error.html', pod_name=pod_name, site_name=site_name, error_status=f'No data for country {country}.')
    #  get census data using geo coordinates
    try:
        county_name, county_population, density = get_census_data(lat, lng)
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        return render_template('error.html', pod_name=pod_name, site_name=site_name, error_status='Unable to reach the census data API.')
    # No errors, success path
    return render_template('index.html', pod_name=pod_name, site_name=site_name, zipcode=zipcode, county=county_name, population=county_population, density=density, lat=lat, lng=lng)
      
@app.route('/q', methods=['GET'])
def address_query():
    site_name = os.environ.get('SITE_NAME') 
    address_q = request.args['address']
    # 
    try:
        lat, lng = get_geo_by_address(address_q)
    #    testing = get_geo_by_address(address_q)
    # API didn't return what was expected
    except requests.exceptions.HTTPError:
        return render_template('error.html', site_name=site_name, error_status=f'Address {address_q} is not valid.')
    # catch other network issues 
    except requests.exceptions.RequestException:
        return render_template('error.html', site_name=site_name, error_status='Unable to reach the geolocation API server. Try again later.')
    #  get census data using geo coordinates
    if lat == "":
        return render_template('error.html', site_name=site_name, error_status=f'Address {address_q} is not valid.')
    try:
        county_name, county_population, density = get_census_data(lat, lng)
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        return render_template('error.html', site_name=site_name, error_status='Unable to reach the census data API.')
    # No errors, success path
    return render_template('index.html', site_name=site_name, address=address_q, county=county_name, population=county_population, density=density, lat=lat, lng=lng)
    #return f'json= {testing}'
    #return f'lat = {lat}, lng = {lng}'

@app.route('/load', methods=['GET'])
def load_all_cpus():
    from cpu_load_generator import load_all_cores
    load_all_cores(duration_s=30, target_load=0.9)  # generates load on all cores
    return "Load test done"

@app.route('/h', methods=['GET'])
def health_check():
    site_name = os.environ.get('SITE_NAME')
    return render_template('error.html', site_name=site_name, error_status=f"I'm up")

def get_ip():
    # GCP Cloud Run needs X-Forwarded_For
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr) 
    # For dev testing, get external IP from environment variable
    if (re.search('^192|^127|^0\.|^172|^10\.', ip_address)):
        ip_address = os.environ.get('DEV_EXT_IP')  
    return ip_address

def get_location_by_ip(ip_address):
    loc_api = requests.get(f'http://ip-api.com/json/{ip_address}')
    loc_api.raise_for_status()
    loc_data = loc_api.json()
    zipcode = loc_data['zip']
    country = loc_data['countryCode']
    lat = loc_data['lat']
    lng = loc_data['lon']
    return zipcode, country, lat, lng

def get_geo_by_address(address_input):
    address_query = requests.get(f'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address={address_input}&benchmark=2020&format=json')
    address_query.raise_for_status()
    
    address_query_json = address_query.json()
    ##return address_query_json["result"]["addressMatches"]
    #test_list = json.loads(address_query_json["result"]["addressMatches"])
    if len(address_query_json["result"]["addressMatches"]) != 0:
    #if address_query_json["result"]["addressMatches"] != "[]":
    #return address_query_json
        lat = address_query_json["result"]["addressMatches"][0]["coordinates"]["y"]
        lng = address_query_json["result"]["addressMatches"][0]["coordinates"]["x"]
    else:
        lat = ""
        lng = ""
    return lat, lng

def get_census_data(lat, lng):
    # the census API requires queries via FIPS geocodes, which we get via this coordinates query
    # see https://geo.fcc.gov/api/census/
    geocode = requests.get(f'https://geo.fcc.gov/api/census/block/find?latitude={lat}&longitude={lng}&showall=true&format=json')
    geocode.raise_for_status()

    geocodej = geocode.json()
    FIPS_code = geocodej["County"]["FIPS"]
    # get state and county codes from FIPS code
    state_code = FIPS_code[0:2]
    county_code = FIPS_code[2:5]
    
    # get county population from the census API
    population = requests.get(f'https://api.census.gov/data/2019/pep/population?get=POP,NAME,DENSITY&for=county:{county_code}&in=state:{state_code}')
    population.raise_for_status()
    pop_json = population.json()
    # grab the population value, convert to int
    county_population = int(pop_json[1][0])
    county_name = pop_json[1][1]
    density = float(pop_json[1][2])
    density = int(density)
    return county_name, county_population, density

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))