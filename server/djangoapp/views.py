from django.shortcuts import render
from http import HTTPStatus
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from djangoapp.restapis import get_dealers_from_cf
from djangoapp.restapis import get_dealer_by_id_from_cf
from djangoapp.restapis import post_request
from djangoapp.models import CarModel
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page
def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def get_contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."

    return render(request, 'djangoapp/user_login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                password=password,
                username=username,
            )
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    '''render the index page with a list of dealerships'''
    context = {}
    allowed_filters = ('state', 'id',)
    if request.method == "GET":
        filters = {}
        for param in allowed_filters:
            if request.GET.get(param, None):
                filters[param] = request.GET[param]

        url = settings.GET_DEALERSHIP_CF_URL
        dealerships = get_dealers_from_cf(url, **filters)
        context['dealerships'] = dealerships

        return render(request, 'djangoapp/index.html', context)


# `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == 'GET':
        url = settings.GET_REVIEW_CF_URL
        context['reviews'] = get_dealer_by_id_from_cf(url, dealer_id)
        url = settings.GET_DEALERSHIP_CF_URL
        context['dealership'] = get_dealers_from_cf(url, id=dealer_id)[0]
        return render(request, 'djangoapp/dealer_details.html', context)

# `add_review` view to submit a review
def add_review(request, dealer_id):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseForbidden()

    context = {}
    if request.method == 'GET':
        context['dealer_id'] = dealer_id
        url = settings.GET_DEALERSHIP_CF_URL
        context['dealership'] = get_dealers_from_cf(url, id=dealer_id)[0]
        context['cars'] = CarModel.objects.filter(dealer_id=dealer_id)
        return render(request, 'djangoapp/add_review.html', context)

    if request.method != 'POST':
        return

    car_id = request.POST['car_id']
    car = CarModel.objects.get(id=car_id)
    month, day, year = request.POST['purchase_date'].split('/')
    purchase_date = datetime.date(int(year), int(month), int(day))
    review = {
        'car_make': car.car_make.name,
        'car_model': car.name,
        'car_year': car.year.year,
        'dealership': dealer_id,
        'name': f'{user.first_name} {user.last_name}',
        'purchase_date': purchase_date.strftime('%m/%d/%Y'),
        'purchase': request.POST.get('purchase', 'false'),
        'review': request.POST['review'],
    }

    url = settings.POST_REVIEW_CF_URL
    json_payload = { 'review': review }
    result = post_request(url, json_payload)

    if result.status_code == 204:
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)

    context = {}
    context['message'] = result.text
    return render(request, 'djangoapp/dealer_details.html', context)
