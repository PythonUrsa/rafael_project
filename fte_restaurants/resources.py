import re
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authentication import SessionAuthentication, Authentication
from tastypie.authorization import Authorization, DjangoAuthorization
from sorl.thumbnail import get_thumbnail
from .models import Restaurant, City, Zone, PaymentMethod, FoodType, Item, Category, Schedule, \
	Telephone, SelectableType, Selectable, Extra, ExtraType
from .exceptions import CustomBadRequest
from fte_admin.models import GlobalSetting, Order, ItemOrder, ItemSelectable
from fte_users.models import FTEFrontendUser, DeliveryAddress, RNC


logger = logging.getLogger(__name__)


class FoodTypeResource(ModelResource):

	class Meta:
		queryset = FoodType.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'food_type'
		allowed_methods = ['get']
		filtering = {
			'name': ALL,
		}
		always_return_data = True


class CityResource(ModelResource):

	class Meta:
		queryset = City.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'city'
		allowed_methods = ['get']
		filtering = {
			'name': ALL,
		}
		always_return_data = True


class ZoneResource(ModelResource):
	city = fields.ForeignKey('fte_restaurants.resources.CityResource', 'city')

	class Meta:
		queryset = Zone.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'zone'
		allowed_methods = ['get']
		filtering = {
			'name': ALL,
			'city': ALL_WITH_RELATIONS,
		}
		always_return_data = True

class RestaurantResource(ModelResource):
	zones = fields.ManyToManyField('fte_restaurants.resources.ZoneResource', 'zones')
	main_food_type = fields.ForeignKey(FoodTypeResource, 'main_food_type')
	secondary_food_type = fields.ForeignKey(FoodTypeResource, 'secondary_food_type')
	user = fields.OneToOneField('fte_users.resources.RestaurantUserResource', 'user', null=True)
	payment_methods = fields.ManyToManyField('fte_restaurants.resources.PaymentMethodResource', 'payment_methods',
											full=True)

	
	def dehydrate(self, bundle):
		bundle.data['thumb_logo'] = get_thumbnail(bundle.obj.logo, "84x84", quality=99, crop="center").url
		bundle.data['thumb_logo_detail'] = get_thumbnail(bundle.obj.logo, "172x172", quality=99, crop="center").url
		bundle.data['thumb_photo'] = get_thumbnail(bundle.obj.photo, "220x165", quality=99, crop="center").url
		bundle.data['main_food'] = bundle.obj.main_food_type.name
		bundle.data['second_food'] = bundle.obj.secondary_food_type.name
		try:
			bundle.data['user'] = bundle.obj.user
		except ObjectDoesNotExist as e:
			bundle.data['user'] = '';
		return bundle


	def apply_filters(self, request, applicable_filters):
		base_object_list = super(RestaurantResource, self).apply_filters(request, applicable_filters)
		city_id = request.GET.get('city', None)

		filters = {}
		try:
			if city_id:
				city = City.objects.get(id=city_id)
				zones = city.delivery_zones.all()
				filters.update(dict(zones__in=zones))
			'''
			else:
				main_city_id = GlobalSetting.objects.get(key="MAIN_CITY")
				city = City.objects.get(id=main_city_id.value)
				zones = city.delivery_zones.all()
				filters.update(dict(zones__in=zones))
			'''		
		except ObjectDoesNotExist:
			logger.warning("City not Found")

		
		preference = request.GET.get('preference', None)

		if not (preference == '' or preference==None):
			qset = (
					Q(name__icontains=preference) |
					Q(main_food_type__name__icontains=preference) |
					Q(secondary_food_type__name__icontains=preference)
				    )

			base_object_list = base_object_list.filter(qset)

		est_time = request.GET.get('est_time', None)

		if not (est_time == '' or est_time==None):
			qset = (
					Q(delivery_time__lte=est_time)
				    )

			base_object_list = base_object_list.filter(qset)

		ord_min = request.GET.get('ord_min', None)

		if not (ord_min == '' or ord_min==None):
			qset = (
					Q(order_minimum__lte=ord_min)
				    )

			base_object_list = base_object_list.filter(qset)


		return base_object_list.filter(**filters).distinct()		

	def obj_update(self, bundle, **kwargs):
		try:
			restaurant = Restaurant.objects.get(pk=bundle.obj.id)
		except Restaurant.DoesNotExist:
			logger.warning("That restaurant does not exist.")
			raise CustomBadRequest(
				code="does_not_exist",
				message="That restaurant does not exist.")
		if ('address') in bundle.data:
			restaurant.address = bundle.data['address']
			try:
				restaurant.save()
			except Exception as e:
				logger.error("RestaurantResource.obj_update: " + e)
		if ('location') in bundle.data:
			restaurant.location = bundle.data['location']
			try:
				restaurant.save()
			except Exception as e:
				logger.error("RestaurantResource.obj_update: " + e)
		if ('payment_methods') in bundle.data:
			payment_method_ids = []
			for method in bundle.data['payment_methods']:
				expr = re.search('\/api\/v1\/payment\/(?P<payment_id>\d+)\/', str(method))
				payment_method_ids.append(expr.group('payment_id'))
			payment_methods = PaymentMethod.objects.filter(id__in=payment_method_ids)
			restaurant.payment_methods.clear()
			restaurant.payment_methods.add(*payment_methods)
			try:
				restaurant.save()
			except Exception as e:
				logger.error("RestaurantResource.obj_update: " + e)
		else:
			return super(RestaurantResource, self).obj_update(bundle, **kwargs)


	class Meta:
		queryset = Restaurant.objects.filter(enabled=True)
		serializer = Serializer(formats=['json'])
		resource_name = 'restaurant'
		allowed_methods = ['get', 'patch']
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'zones': ALL_WITH_RELATIONS,
			'featured': ALL,
		}
		ordering = {
			'name',
		}
		always_return_data = True
		authentication = Authentication()
		authorization = Authorization()

class CategoryResource(ModelResource):
	restaurant = fields.ForeignKey('fte_restaurants.resources.RestaurantResource', 'restaurant')

	class Meta:
		queryset = Category.objects.filter().order_by('position')
		serializer = Serializer(formats=['json'])
		resource_name = 'category'
		allowed_methods = ['get', 'post', 'put']
		filtering = {
			'name': ALL,
			'restaurant': ALL_WITH_RELATIONS,
			'enabled': ALL,
		}
		ordering = {
			'position',
		}
		always_return_data = True
		authentication = Authentication()
		authorization = Authorization()


class SelectableTypeResource(ModelResource):
	category = fields.ForeignKey('fte_restaurants.resources.CategoryResource', 'category')

	class Meta:
		queryset = SelectableType.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'selectable_type'
		allowed_methods = ['get', 'post', 'patch', 'delete']
		filtering = {
			'name': ALL,
			'category': ALL_WITH_RELATIONS,
		}
		ordering = {
			'name',
		}
		always_return_data = True
		authentication = Authentication()
		authorization = Authorization()

class SelectableResource(ModelResource):
	selectable_type = fields.ForeignKey('fte_restaurants.resources.SelectableTypeResource', 'selectable_type')
	
	class Meta:
		queryset = Selectable.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'selectable'
		allowed_methods = ['get', 'post', 'patch', 'delete']
		filtering = {
			'name': ALL,
			'selectable_type': ALL_WITH_RELATIONS,
		}
		ordering = {
			'name',
		}
		always_return_data = True
		authentication = Authentication()
		authorization = Authorization()

class ExtraTypeResource(ModelResource):
	restaurant = fields.ForeignKey('fte_restaurants.resources.RestaurantResource', 'restaurant')

	class Meta:
		queryset = ExtraType.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'extra_type'
		allowed_methods = ['get', 'post', 'patch', 'delete']
		filtering = {
			'name': ALL,
			'restaurant': ALL_WITH_RELATIONS,
		}
		ordering = {
			'name',
		}
		always_return_data = True
		authentication = Authentication()
		authorization = Authorization()

class ExtraResource(ModelResource):
	extra_type = fields.ForeignKey('fte_restaurants.resources.ExtraTypeResource', 'extra_type')

	class Meta:
		queryset = Extra.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'extra'
		allowed_methods = ['get', 'post', 'patch', 'delete']
		filtering = {
			'name': ALL,
			'extra_type': ALL_WITH_RELATIONS,
		}
		ordering = {
			'name',
		}
		always_return_data = True
		authentication = Authentication()
		authorization = Authorization()

class ItemResource(ModelResource):
	category = fields.ForeignKey('fte_restaurants.resources.CategoryResource', 'category', full=True)
	selectable_types = fields.ManyToManyField('fte_restaurants.resources.SelectableTypeResource', 'selectable_types', full=True)
	extra_types = fields.ManyToManyField('fte_restaurants.resources.ExtraTypeResource', 'extra_types', full=True)

	class Meta:
		queryset = Item.objects.filter()
		serializer = Serializer(formats=['json'])
		resource_name = 'item'
		allowed_methods = ['get', 'post', 'patch']
		filtering = {
			'name': ALL,
			'category': ALL_WITH_RELATIONS,
			'enabled': ALL,
			'deleted': ALL
		}
		ordering = {
			'name',
		}
		always_return_data = True
		authentication = Authentication()
		authorization = Authorization()


class ScheduleResource(ModelResource):
	restaurant = fields.ForeignKey('fte_restaurants.resources.RestaurantResource', 'restaurant')
	class Meta:
		queryset = Schedule.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'schedule'
		allowed_methods = ['get', 'post', 'patch', 'delete']
		filtering = {
			'restaurant': ALL_WITH_RELATIONS,
		}
		always_return_data = True
		authentication = Authentication()
		authorization = Authorization()

class TelephoneResource(ModelResource):
	restaurant = fields.ForeignKey('fte_restaurants.resources.RestaurantResource', 'restaurant')
	class Meta:
		queryset = Telephone.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'telephone'
		allowed_methods = ['get', 'patch', 'post', 'delete']
		filtering = {
			'restaurant': ALL_WITH_RELATIONS,
		}
		always_return_data = True
		authentication = Authentication()
		authorization = Authorization()


class PaymentMethodResource(ModelResource):

	class Meta:
		queryset = PaymentMethod.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'payment'
		allowed_methods = ['get']
		filtering = {
			'name': ALL,
		}
		always_return_data = True

