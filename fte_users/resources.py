import logging

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.validators import validate_email

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import (Authentication, BasicAuthentication, ApiKeyAuthentication,
									SessionAuthentication, MultiAuthentication)
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from tastypie.serializers import Serializer

from .models import FTEUser, FTEFrontendUser, RNC, DeliveryAddress, FTERestaurantUser
from .authorization import CustomAuthorization
from fte_restaurants.exceptions import CustomBadRequest
from sorl.thumbnail import get_thumbnail


logger = logging.getLogger(__name__)

##### Mixin For Image Upload #######

class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)

            return data

        return super(MultipartResource, self).deserialize(request, data, format)

#########


class FrontEndUserResource(MultipartResource, ModelResource):
	#user = fields.ForeignKey('core.api.UserResource', 'user', full=True)
	photo = fields.FileField(attribute='photo', null=True, blank=True)

	class Meta:
		queryset = FTEFrontendUser.objects.all()
		excludes = ['is_superuser','is_staff', 'password']
		resource_name = 'auth/user'
		always_return_data = True
		allowed_methods = ['get', 'post', 'delete', 'patch']
		filtering = {
			'id': ALL,
		}
		serializer = Serializer(formats=['json'])
		authentication = SessionAuthentication()
		authorization = CustomAuthorization()

	def obj_create(self, bundle, **kwargs):
		try:
			if (type(bundle.data['photo']) is not str):
				user = FTEFrontendUser.objects.get(pk=bundle.data['id'])
				user.photo = bundle.data['photo']
				user.save()
		except Exception as e:
			logger.error("FrontEndUserResource.obj_create: " + e)


	def obj_update(self, bundle, **kwargs):

		if ('password') in bundle.data:
			raw_password = bundle.data.pop('password')
			if len(raw_password) < 6:
				raise CustomBadRequest(
					code="minlength_exception",
					message="La contraseña debe tener al menos 6 caractéres.")

			user = FTEFrontendUser.objects.get(email=bundle.data["email"])
			user.password = make_password(raw_password)

			user.save()
		else:
			try:
				user = FTEFrontendUser.objects.get(email=bundle.obj.email)
			except FTEUser.DoesNotExist:
				raise CustomBadRequest(
					code="does_not_exist",
					message="That user does not exist.")

			email = bundle.data["email"]
			try:
				validate_email(email)
			except ValidationError as e:
				logger.warning("FrontEndUserResource.obj_update: Email invalido: "
					+ e)
				raise CustomBadRequest(
						code="invalid_email",
						message="Provided email is not valid.")
			try:
				if FTEUser.objects.filter(email=email) and (email != user.email):
					raise CustomBadRequest(
						code="duplicate_exception",
						message="That email is already used.")
			except FTEUser.DoesNotExist:
				pass

			try:
				int(bundle.data['telephone'])
			except ValueError:
				raise CustomBadRequest(
						code="not_a_number",
						message="El telefono debe ser un número de 10 digitos.")

			if (not len(bundle.data['telephone']) == 10):
				raise CustomBadRequest(
					code="not_a_number",
					message="El telefono debe ser un número de 10 digitos.")

			if email != user.email:
				user.add_unconfirmed_email(email)
				old_email = user.email
				user.email = bundle.data["email"]
				user.remove_email(old_email)
				
			user.first_name = bundle.data["first_name"]
			user.last_name = bundle.data["last_name"]
			user.gender = bundle.data["gender"]
			user.telephone = bundle.data["telephone"]
			user.date_of_birth = bundle.data["date_of_birth"]

			try:
				user.save()
			except Exception as e:
				logger.error("FrontEndUserResource.obj_update: " + e)

	def dehydrate(self, bundle):
		bundle.data['is_confirmed'] = FTEFrontendUser.objects.get(pk=bundle.data['id']).is_confirmed
		try:
			bundle.data['user_picture'] = get_thumbnail(bundle.obj.photo, "366x366", quality=99, crop="center").url
		except Exception as e:
			logger.error("FrontEndUserResource.dehydrate: " + e)
		return bundle

class CreateFrontEndUserResource(MultipartResource, ModelResource):
	photo = fields.FileField(attribute='photo', null=True, blank=True)

	class Meta:
		queryset = FTEFrontendUser.objects.all()
		excludes = ['is_superuser','is_staff', 'password']
		resource_name = 'create_user'
		always_return_data = True
		allowed_methods = ['post']
		filtering = {
			'id': ALL,
		}
		serializer = Serializer(formats=['json'])
		authentication = Authentication()
		authorization = Authorization()


	def obj_create(self, bundle, **kwargs):
		REQUIRED_FIELDS = ("email", "first_name", "last_name",
							"password", "date_of_birth", "gender",
							"telephone")
		for field in REQUIRED_FIELDS:
			if field not in bundle.data:
				logger.warning("CreateFrontEndUserResource.obj_create: Intento crear usuario sin campo obligatorio: "
					+ field)
				raise CustomBadRequest(
					code="missing_key",
					message="El campo {missing_key} es obligatorio."
							.format(missing_key=field))
		email = bundle.data["email"]
		try:
			validate_email(email)
		except ValidationError as e:
			logger.warning("CreateFrontEndUserResource.obj_create: Email invalido: "
					+ e)
			raise CustomBadRequest(
					code="invalid_email",
					message="El email elegido no es valido.")
		try:
			if FTEUser.objects.filter(email=email):
				logger.warning("CreateFrontEndUserResource.obj_create: Email ya utilizado")
				raise CustomBadRequest(
					code="duplicate_exception",
					message="El email elegido ya esta en uso, por favor elija otro.")
		except FTEUser.DoesNotExist:
			pass
		try:
			int(bundle.data['telephone'])
		except ValueError:
			logger.warning("CreateFrontEndUserResource.obj_create: Telefono no es un numero")
			raise CustomBadRequest(
					code="not_a_number",
					message="El telefono debe ser un número de 10 digitos.")

		if (not len(bundle.data['telephone']) == 10):
			logger.warning("CreateFrontEndUserResource.obj_create: Telefono no tiene 10 digitos")
			raise CustomBadRequest(
				code="not_a_number",
				message="El telefono debe ser un número de 10 digitos.")

		raw_password = bundle.data['password']

		if len(raw_password) < 6:
			logger.warning("CreateFrontEndUserResource.obj_create: Password invalida, menos de 6 caracteres")
			raise CustomBadRequest(
					code="minlength_exception",
					message="La contraseña debe tener al menos 6 caractéres.")
		kwargs["password"] = make_password(raw_password)

		return super(CreateFrontEndUserResource, self).obj_create(bundle, **kwargs)

	def dehydrate(self, bundle):
		bundle.data['is_confirmed'] = FTEFrontendUser.objects.get(email=bundle.data['email']).is_confirmed
		try:
			bundle.data['user_picture'] = get_thumbnail(bundle.obj.photo, "366x366", quality=99, crop="center").url
		except Exception as e:
			logger.error("CreateFrontEndUserResource.dehydrate: PhotoError: " + e)
		return bundle




class UserResource(ModelResource):
	# We need to store raw password in a virtual field because hydrate method
	# is called multiple times depending on if it's a POST/PUT/PATCH request
	raw_password = fields.CharField(attribute=None, readonly=True, null=True,
									blank=True)

	class Meta:
		# For authentication, allow both basic and api key so that the key
		# can be grabbed, if needed.
		authentication = MultiAuthentication(
			BasicAuthentication(),
			ApiKeyAuthentication())
		authorization = DjangoAuthorization()

		# Because this can be updated nested under the UserProfile, it needed
		# 'put'. No idea why, since patch is supposed to be able to handle
		# partial updates.
		allowed_methods = ['get', 'patch', 'put', ]
		always_return_data = True
		queryset = FTEUser.objects.all().select_related("api_key")
		excludes = ['is_active', 'is_staff', 'is_superuser', 'date_joined',
					'last_login']
 
	def authorized_read_list(self, object_list, bundle):
		return object_list.filter(id=bundle.request.user.id).select_related()

	def hydrate(self, bundle):
		if "raw_password" in bundle.data:
			# Pop out raw_password and validate it
			# This will prevent re-validation because hydrate is called
			# multiple times
			# https://github.com/toastdriven/django-tastypie/issues/603
			# "Cannot resolve keyword 'raw_password' into field." won't occur
		 
			raw_password = bundle.data.pop["raw_password"]
	 
			bundle.data["password"] = make_password(raw_password)
	 
		return bundle
	 
	def dehydrate(self, bundle):
		bundle.data['key'] = bundle.obj.api_key.key
 
		try:
			# Don't return `raw_password` in response.
			del bundle.data["raw_password"]
		except KeyError:
			pass
		 
		return bundle 


class RestaurantUserResource(ModelResource):
	#user = fields.ForeignKey('core.api.UserResource', 'user', full=True)

	class Meta:
		queryset = FTERestaurantUser.objects.all()
		excludes = ['is_superuser','is_staff', 'password']
		resource_name = 'auth/restaurant_user'
		always_return_data = True
		allowed_methods = ['get']
		filtering = {
			'id': ALL,
		}
		serializer = Serializer(formats=['json'])
		authentication = SessionAuthentication()
		authorization = Authorization()


class RNCResource(ModelResource):
	frontend_user = fields.ForeignKey('fte_users.resources.FrontEndUserResource', 'frontend_user', full=True)

	class Meta:
		queryset = RNC.objects.all()
		resource_name = 'user/rnc'
		always_return_data = True
		allowed_methods = ['get', 'post', 'put','delete', 'patch']
		#detail_allowed_methods = ['delete']
		#list_allowed_methods = ['delete']
		filtering = {
			'main': ALL,
			'frontend_user': ALL_WITH_RELATIONS,
		}
		serializer = Serializer(formats=['json'])
		authentication = SessionAuthentication()
		authorization = DjangoAuthorization()

	def obj_create(self, bundle, **kwargs):
		try:
			int(bundle.data['rnc_number'])
		except ValueError:
			logger.warning("RNCResource.obj_create: RNC no es un numero")
			raise CustomBadRequest(
					code="not_a_number",
					message="El RNC debe ser un número de 9 digitos.")

		if (not len(bundle.data['rnc_number']) == 9):
			logger.warning("RNCResource.obj_create: RNC no tiene 9 digitos")
			raise CustomBadRequest(
				code="not_a_number",
				message="El RNC debe ser un número de 9 digitos.")

		return super(RNCResource, self).obj_create(bundle, **kwargs)

	def obj_update(self, bundle, **kwargs):
		if 'rnc_number' in bundle.data:
			try:
				int(bundle.data['rnc_number'])
			except ValueError:
				logger.warning("RNCResource.obj_update: RNC no es un numero")
				raise CustomBadRequest(
						code="not_a_number",
						message="El RNC debe ser un número de máximo 9 digitos.")

			if (len(bundle.data['rnc_number']) > 9):
				logger.warning("RNCResource.obj_update: RNC no tiene 9 digitos")
				raise CustomBadRequest(
					code="not_a_number",
					message="El RNC debe ser un número de máximo 9 digitos.")

		return super(RNCResource, self).obj_update(bundle, **kwargs)


class DeliveryAddressResource(ModelResource):
	frontend_user = fields.ForeignKey('fte_users.resources.FrontEndUserResource', 'frontend_user', full=True)
	city = fields.ForeignKey('fte_restaurants.resources.CityResource', 'city', full=True)
	delivery_zone = fields.ForeignKey('fte_restaurants.resources.ZoneResource', 'delivery_zone', full=True)

	class Meta:
		queryset = DeliveryAddress.objects.all().order_by('-main')
		resource_name = 'user/address'
		always_return_data = True
		allowed_methods = ['get', 'post', 'delete', 'patch']
		filtering = {
			'address': ALL,
			'main': ALL,
			'frontend_user': ALL_WITH_RELATIONS,
		}
		serializer = Serializer(formats=['json'])
		authentication = SessionAuthentication()
		authorization = DjangoAuthorization()
