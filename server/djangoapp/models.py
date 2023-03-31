from django.db import models
from django.utils.timezone import now
import datetime


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=250, default='Car Maker')
    description = models.CharField(max_length=1000)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'CarMake: {self.name}'

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=250, default='Car Model')
    dealer_id = models.IntegerField(null=False, default=1)
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    PICKUP = 'pickup'
    VANS = 'vans'
    MINIVANS = 'minivans'
    SPORT = 'sport'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (PICKUP, 'Pickup'),
        (VANS, 'Vans'),
        (MINIVANS, 'Minivans'),
        (SPORT, 'Sport'),
    ]
    type = models.CharField(
        choices=TYPE_CHOICES,
        default=SEDAN,
        max_length=10,
        null=False,
    )
    year = models.DateField(null=False, default=now)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'CarModel: {self.name}'

class CarDealer:
    '''CarDealer (python class) to hold dealer data'''
    ALLOWED_FIELDS = (
        'address',
        'city',
        'full_name',
        'id',
        'lat',
        'long',
        'short_name',
        'st',
        'state',
        'zip',
    )
    def __init__(self, **kwargs):
        for field in self.ALLOWED_FIELDS:
            setattr(self, field, kwargs.get(field))

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    '''DealerReview (python class) to hold dealer data'''
    ALLOWED_FIELDS = (
        'car_make',
        'car_model',
        'car_year',
        'dealership',
        'id',
        'name',
        'purchase_date',
        'purchase',
        'review',
        'sentimient',
    )

    def __init__(self, **kwargs):
        for field in self.ALLOWED_FIELDS:
            setattr(self, field, kwargs.get(field))
        if self.purchase_date:
            month, day, year = self.purchase_date.split('/')
            self.purchase_date = datetime.date(int(year), int(month), int(day))

    def __str__(self):
        return f'Review: {self.review}, Name: {self.name}'

