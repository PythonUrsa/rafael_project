from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.views.generic import TemplateView
import csv, json, logging
from fte_admin.models import GlobalSetting
from .models import Restaurant, City, Zone

logger = logging.getLogger('f2e.home.logger')


class PublicServerView(TemplateView):
    template_name = "base.html"


class RestaurantServerView(TemplateView):
    template_name = "base_restaurant.html"


def get_home_restaurants(request):
	'''
		GLOBAL SETTING used: MAIN_CITY
	'''

	city_id = request.GET.get('city', None)

	result = []

	if (city_id == None or city_id == ''):

		try:
			main_city_id = GlobalSetting.objects.get(key="MAIN_CITY")
			city = City.objects.get(id=main_city_id)
			zones = city.delivery_zones.all()
			for rest in Restaurant.objects.filter(featured=True, zones__in=zones)[:12]:
				result.append(rest.get_featured_data())
			return HttpResponse(json.dumps(result))

		except ObjectDoesNotExist:
			logger.exception("Error looking for zones in main city")
			for rest in Restaurant.objects.filter(featured=True)[:12]:
				result.append(rest.get_featured_data())
			return HttpResponse(json.dumps(result))

	elif not city_id == '':
		try:
			city = City.objects.get(id=city_id)
			zones = city.delivery_zones.all()
			for rest in Restaurant.objects.filter(featured=True, zones__in=zones)[:12]:
				result.append(rest.get_featured_data())
			return HttpResponse(json.dumps(result))

		except ObjectDoesNotExist:
			logger.exception("Error looking for zones in the city requested")
			for rest in Restaurant.objects.filter(featured=True)[:12]:
				result.append(rest.get_featured_data())
			return HttpResponse(json.dumps(result)) 



def get_city_list(request):

	result = []

	for c in City.objects.all():
		result.append(c.get_city_data())

	return HttpResponse(json.dumps(result))

def get_zone_list(request):

	result = []
	city_id = request.GET.get('city', None)

	if not (city_id == None or city_id == ''):
		try:
			city = City.objects.get(id=city_id)
			for z in city.delivery_zones.all():
				result.append(z.get_zone_data())
		except ObjectDoesNotExist:
			for z in Zone.objects.all():
				result.append(z.get_zone_data())
	else:
		for z in Zone.objects.all():
			result.append(z.get_zone_data())

	return HttpResponse(json.dumps(result))


def search_restaurants(request):

	result = []

	#city_id = request.GET.get('city', None)
	zone_id = request.GET.get('zone', None)
	text = request.GET.get('text', None)

	if (zone_id == None or zone_id == ''):
		return HttpResponse('Debe seleccionar un Sector para el envio')
	else:
		try:
			zone = Zone.objects.filter(id=zone_id)
			restaurants = Restaurant.objects.filter(zones__in=zone).order_by('name')
		except ObjectDoesNotExist:
			return HttpResponse('Debe seleccionar un Sector para el envio')

	if not (text == '' or text == None):
		restaurants = restaurants.filter(Q(main_food_type__name__icontains=text)|Q(secondary_food_type__name__icontains=text)|Q(name__icontains=text)).order_by('name')

	for rest in restaurants:
		result.append(rest.get_search_data())

	return HttpResponse(json.dumps(result))

def get_restaurant_menu(request):


	restaurant_id = request.GET.get('restaurant', None)

	if (restaurant_id == None or restaurant_id == ''):
		return HttpResponse('Debe seleccionar un Restaurante')
	else:
		try:
			restaurant = Restaurant.objects.get(id=restaurant_id)
			menu  = restaurant.get_menu()
			return HttpResponse(json.dumps(menu))
		except ObjectDoesNotExist:
			return HttpResponse('Debe seleccionar un Restaurante')








