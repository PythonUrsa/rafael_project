from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from food_to_eat import settings
from .views import get_home_restaurants, get_city_list, get_zone_list, search_restaurants,get_restaurant_menu,\
PublicServerView, RestaurantServerView



urlpatterns = patterns('fte_restaurants.views',
    url(r'^ajax/get_home_restaurants/', get_home_restaurants, name="get_home_restaurants"),
    url(r'^ajax/get_city_list/', get_city_list, name="get_city_list"),
    url(r'^ajax/get_zone_list/', get_zone_list, name="get_zone_list"),
    url(r'^ajax/search/', search_restaurants, name="search"),
    url(r'^ajax/get_restaurant_menu/', get_restaurant_menu , name="get_restaurant_menu"),

    url(r'^restaurant/', RestaurantServerView.as_view(), name="restaurant_server"),
    url(r'^', PublicServerView.as_view(), name="public_server"),
  )