from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from food_to_eat import settings
from .views import get_home_photos
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = patterns('fte_admin.views',
    url(r'^ajax/get_home_photos/', get_home_photos, name="get_home_photos"),
    
   )