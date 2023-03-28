import os
import re
import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    #if no query string, use geolocation
    # site name from env variable
    site_name = os.environ.get('SITE_NAME')
    pod_name = os.environ.get('POD_NAME') 
    # grab IP from env variable
    ip_address = get_ip()
    if ip_address =='': #ip_address is undefined, likely missing fall-back environment variable
        return render_template('error.html', pod_name=pod_name, site_name=site_name, error_status='Unable to get your IP address.')
    # Look up country code using IP address
    try: 
        country_code = get_country_code_by_ip(ip_address)
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        return render_template('error.html', pod_name=pod_name, site_name=site_name, error_status='Unable to reach the geolocation API. Try again later.')
    # query based on country code
    try:
        country_data = get_country_data_by_code(country_code)
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        # show an error
        return render_template('error.html', pod_name=pod_name, site_name=site_name, error_status='No countries match your query. Try again.')
    # No errors, success path
    return render_template('index.html', pod_name=pod_name, site_name=site_name, country_name=country_data[0], population=country_data[1], density=country_data[2], map=country_data[3], flag=country_data[4] )
      
@app.route('/q/<country_name>')
def get_country_search(country_name):
    site_name = os.environ.get('SITE_NAME')
    pod_name = os.environ.get('POD_NAME')
    # name based query  
    try:
        response = requests.get(f'https://restcountries.com/v3.1/name/{country_name}')
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        return render_template('error.html', pod_name=pod_name, site_name=site_name, error_status='The Rest Countries API appears to be down. Try again later.')
    # unless we got a 200 code, error out
    if response.status_code != 200:
        return render_template('error.html', pod_name=pod_name, site_name=site_name, error_status='No countries match your query. Try again.')
    json_data = response.json()[0]
    country_data = parse_api_data(json_data)
    return render_template('index.html', pod_name=pod_name, site_name=site_name, country_name=country_data[0], population=country_data[1], density=country_data[2], map=country_data[3], flag=country_data[4] )

def get_country_data_by_code(country_code):
    # we got data from the country param query
    try:
        response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}')
        json_data = response.json()[0]
        country_data = parse_api_data(json_data)
        return country_data
    # no match for query
    except:
        raise

def parse_api_data(data):
    name = data['name']['common']
    population = data['population']
    area = data['area']
    population_density = population / area
    map = data['maps']['googleMaps']
    flag = data['flags']['png']

    country_data = [ name, population, population_density, map, flag ]
    return country_data


def get_ip():
    # GCP Cloud Run needs X-Forwarded_For
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr) 
    # For dev testing, get external IP from environment variable
    if (re.search('^192|^127|^0\.|^172|^10\.', ip_address)):
        ip_address = os.environ.get('DEV_EXT_IP')  
    return ip_address

def get_country_code_by_ip(ip_address):
    loc_api = requests.get(f'http://ip-api.com/json/{ip_address}')
    loc_api.raise_for_status()
    loc_data = loc_api.json()
    country_code = loc_data['countryCode']
    return country_code

@app.route('/h', methods=['GET'])
def health_check():
    site_name = os.environ.get('SITE_NAME')
    return render_template('error.html', site_name=site_name, error_status=f"I'm up")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))