from django.contrib import admin
from djangoapp.models import CarMake
from djangoapp.models import CarModel


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 10

class CarModelAdmin(admin.ModelAdmin):
    list_filter = ['car_make', 'type']
    autocomplete_fields = ['car_make']


class CarMakeAdmin(admin.ModelAdmin):
    search_fields = ['car_make']
    inlines = [CarModelInline]
    list_filter = ['name']


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
