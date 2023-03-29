from django.db import models
from django.utils.timezone import now


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
    pass

class DealerReview:
    '''DealerReview (python class) to hold dealer data'''
    pass

