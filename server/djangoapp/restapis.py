import requests
import json
from djangoapp.models import CarDealer
from djangoapp.models import DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print(f'GET from {url}')

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url,
            headers={'Content-Type': 'application/json'},
            params=kwargs)
    except:
        # If any error occurs
        print('Network exception occurred')
    status_code = response.status_code
    print(f'With status {status_code}')
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


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
            results.append(dealer_review)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



