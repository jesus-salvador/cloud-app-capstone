import requests
import json
from djangoapp.models import CarDealer
from djangoapp.models import DealerReview
from requests.auth import HTTPBasicAuth
from django.conf import settings


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print(f'GET from {url}')

    auth = None
    if api_key:
        auth = HTTPBasicAuth('apikey', api_key)

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url,
            headers={'Content-Type': 'application/json'},
            params=kwargs,
            auth=auth
        )
    except:
        # If any error occurs
        print('Network exception occurred')
    status_code = response.status_code
    print(f'With status {status_code}')
    json_data = json.loads(response.text)
    return json_data

# `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    return requests.post(url, params=kwargs, json=json_payload)


# get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request() with specified arguments
    json_result = get_request(url, **kwargs)
    if json_result:
        dealers = json_result["entries"]
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            car_dealer = CarDealer(**dealer)
            results.append(car_dealer)

    return results

# get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result['entries']
        for review in reviews:
            dealer_review = DealerReview(**review)
            # Watson NLU result
            dealer_review.sentimient = analyze_review_sentiments(dealer_review.review)
            results.append(dealer_review)

    return results


# `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    params = {}
    url = settings.WATSON_ANALIZER_URL
    url += '/v1/analyze'
    api_key = settings.WATSON_ANALIZER_API_KEY
    params['version'] =  '2022-04-07'
    params['text'] = text
    params['features'] = 'sentiment'
    params['return_analyzed_text'] = 'true'

    analyzed_result = get_request(url, api_key=api_key, **params)
    # Get the returned sentiment label such as Positive or Negative
    if analyzed_result.get('sentiment'):
        return analyzed_result['sentiment']['document']

    return analyzed_result

