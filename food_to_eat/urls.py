from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from food_to_eat import settings
from django.contrib.admin.views.decorators import staff_member_required
from fte_admin.views import ReportCSVGenerate
from fte_admin import urls as admin_url
from fte_users import urls as users_url
from fte_restaurants import urls as public_url

from tastypie.api import Api
from fte_restaurants.resources import RestaurantResource, ZoneResource, CityResource, FoodTypeResource, CategoryResource, \
ItemResource, ScheduleResource, ExtraResource, ExtraTypeResource, SelectableResource, SelectableTypeResource, TelephoneResource, \
PaymentMethodResource
from fte_admin.resources import GlobalSettingResource, PhotoResource, OrderResource, ItemOrderResource, TextSettingResource
from fte_users.resources import CreateFrontEndUserResource, FrontEndUserResource, RNCResource, DeliveryAddressResource
from food_to_eat.startup import setup_groups

v1_api = Api(api_name='v1')
v1_api.register(RestaurantResource())
v1_api.register(ZoneResource())
v1_api.register(CityResource())
v1_api.register(FoodTypeResource())
v1_api.register(CategoryResource())
v1_api.register(ItemResource())
v1_api.register(GlobalSettingResource())
v1_api.register(PhotoResource())
v1_api.register(ScheduleResource())
v1_api.register(ExtraTypeResource())
v1_api.register(ExtraResource())
v1_api.register(SelectableResource())
v1_api.register(SelectableTypeResource())
v1_api.register(FrontEndUserResource())
v1_api.register(RNCResource())
v1_api.register(DeliveryAddressResource())
v1_api.register(OrderResource())
v1_api.register(ItemOrderResource())
v1_api.register(TelephoneResource())
v1_api.register(TextSettingResource())
v1_api.register(PaymentMethodResource())
v1_api.register(CreateFrontEndUserResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'food_to_eat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root':settings.MEDIA_ROOT }),
    url(r'^admin-app/', include(admin_url)),
    url(r'^user/', include(users_url)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    (r'^summernote/', include('django_summernote.urls')),
    (r'^api/', include(v1_api.urls)),
    url(r'^create_report/', staff_member_required(ReportCSVGenerate), name="create_report"),
    url(r'^', include(public_url)),
)

setup_groups()