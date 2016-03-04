from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from food_to_eat import settings
from .views import customer_login, restaurant_login, user_logout, send_confirmation_key, confirm_email, \
	reset, reset_confirm



urlpatterns = patterns('fte_restaurants.views',
    url(r'^api/customer_login/', customer_login, name="customer_login"),
    url(r'^api/restaurant_login/', restaurant_login, name="restaurant_login"),
    url(r'^api/send_confirmation_key/', send_confirmation_key, name="send_confirmation_key"),
    url(r'^api/confirm_email/(?P<email>[a-z,A-Z,0-9,@,.,\-,\_]+)/(?P<key>[a-z,A-Z,0-9,]+)/', confirm_email, name="confirm_email"),
    url(r'^api/user_logout/', user_logout, name="user_logout"),
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', reset_confirm, name='reset_confirm'),
    url(r'^reset/', reset, name='reset'),
  )