from datetime import datetime
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.dispatch import receiver
from django.template import Template, Context

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from sorl.thumbnail import get_thumbnail
from .models import GlobalSetting, Photo, Order, ItemOrder, ItemSelectable, TextSetting, FileSetting
from .signals import new_order
from .authorization import CustomAuthorization
from fte_users.models import FTEUser, FTEFrontendUser, DeliveryAddress, RNC
from fte_restaurants.models import Restaurant, Item, Selectable, Extra, PaymentMethod
from fte_restaurants.exceptions import CustomBadRequest

logger = logging.getLogger(__name__)

class TextSettingResource(ModelResource):

	class Meta:
		queryset = TextSetting.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'text_setting'
		allowed_methods = ['get']
		filtering = {
			'key': ALL,
		}
		always_return_data = True


class GlobalSettingResource(ModelResource):

	class Meta:
		queryset = GlobalSetting.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'setting'
		allowed_methods = ['get']
		filtering = {
			'key': ALL,
		}
		always_return_data = True


class PhotoResource(ModelResource):

	class Meta:
		queryset = Photo.objects.filter(published=True)
		serializer = Serializer(formats=['json'])
		resource_name = 'photo'
		allowed_methods = ['get']
		filtering = {
			'name': ALL,
		}
		always_return_data = True


class OrderResource(ModelResource):
	restaurant = fields.ForeignKey('fte_restaurants.resources.RestaurantResource', 'restaurant', full=True)
	user = fields.ForeignKey('fte_users.resources.FrontEndUserResource', 'user', full=True)
	delivery_address = fields.ForeignKey('fte_users.resources.DeliveryAddressResource',
			'delivery_address', full=True, null=True)
	rnc = fields.ForeignKey('fte_users.resources.RNCResource', 'rnc', null=True, full=True)
	payment_method = fields.ForeignKey('fte_restaurants.resources.PaymentMethodResource',
			'payment_method',full=True)

	class Meta:
		queryset = Order.objects.all().order_by('-id')
		serializer = Serializer(formats=['json'])
		resource_name = 'order'
		allowed_methods = ['get', 'post', 'patch']
		filtering = {
			'name': ALL,
			'timestamp': ['range', 'gt', 'gte', 'lt', 'lte'],
			'user': ALL_WITH_RELATIONS,
			'restaurant': ALL_WITH_RELATIONS,
		}
		always_return_data = True
		authentication = SessionAuthentication()
		authorization = CustomAuthorization()

	def obj_create(self, bundle, **kwargs):
		user = bundle.data['user'].split("/")
		user = user[len(user) - 2]
		try:
			bundle.obj.user = FTEFrontendUser.objects.get(pk=user)
			if not bundle.obj.user.is_confirmed:
				logger.warning("Orden con mail sin confirmar del FTEFrontendUser " + user)
				raise CustomBadRequest(
					code="unconfirmed_email",
					message=("Es necesario activar su cuenta para procesar la orden."))
		except FTEUser.DoesNotExist:
			logger.error("Orden con usuario inexistente")
			raise CustomBadRequest(
					code="does_not_exist",
					message="That user does not exist.")

		restaurant = bundle.data['restaurant'].split("/")
		restaurant = restaurant[len(restaurant) - 2]
		try:
			bundle.obj.restaurant = Restaurant.objects.get(pk=restaurant)
			schedule = bundle.obj.restaurant.schedules.all()[0]
			now = datetime.now().time()
			if schedule.start_time <= schedule.finish_time:
				if (not (schedule.start_time <= now <= schedule.finish_time)):
					logger.warning("Orden en restaurante cerrado del FTEFrontendUser " + user)
					raise CustomBadRequest(
						code="closed",
						message="Lo sentimos, el restaurante se encuentra cerrado y no acepta ordenes.")
			else:
				if not (schedule.start_time <= now or now <= schedule.finish_time):
					logger.warning("Orden en restaurante cerrado del FTEFrontendUser " + user)
					raise CustomBadRequest(
						code="closed",
						message="Lo sentimos, el restaurante se encuentra cerrado y no acepta ordenes.")

		except ObjectDoesNotExist:
			logger.error("Orden en restaurante inexistente")
			raise CustomBadRequest(
					code="does_not_exist",
					message="That restaurant does not exist.")

		bundle.obj.order_type = bundle.data['order_type']
		if (bundle.data['order_type'] == "DELIVERY"):
			delivery_address = bundle.data['delivery_address'].split("/")
			delivery_address = delivery_address[len(delivery_address) - 2]
			try:
				bundle.obj.delivery_address = DeliveryAddress.objects.get(pk=delivery_address)
			except ObjectDoesNotExist:
				logger.error("Orden con direccion inexistente del FTEFrontendUser " + user)
				raise CustomBadRequest(
						code="does_not_exist",
						message="That address does not exist.")
			if bundle.obj.delivery_address.frontend_user.email != bundle.obj.user.email:
				logger.warning("Orden con direccion de otro usuario del FTEFrontendUser " + user)
				raise CustomBadRequest(
						code="does_not_belong",
						message="That address does not belong to the user.")
			if bundle.obj.delivery_address.delivery_zone not in bundle.obj.restaurant.zones.all():
				logger.info("Orden con direccion fuera de la zona de delivery del FTEFrontendUser " + user)
				raise CustomBadRequest(
						code="does_not_belong",
						message="Esta direccion no esta dentro de las zonas de envio, por favor seleccione otra.")

		bundle.obj.additional_info = bundle.data['additional_info']
		bundle.obj.change = bundle.data['change']

		rnc = bundle.data['rnc']
		if rnc != '':
			rnc = rnc['id']
			try:
				bundle.obj.rnc = RNC.objects.get(pk=rnc)
			except ObjectDoesNotExist:
				logger.error("Orden con RNC inexistente del FTEFrontendUser " + user)
				raise CustomBadRequest(
						code="does_not_exist",
						message="That RNC does not exist.")
		if (bundle.obj.rnc != None and 
					bundle.obj.rnc.frontend_user.email != bundle.obj.user.email):
			logger.warning("Orden con RNC de otro usuario del FTEFrontendUser " + user)
			raise CustomBadRequest(
					code="does_not_belong",
					message="That RNC does not belong to the user.")

		payment_method = bundle.data['payment_method'].split("/")
		payment_method = payment_method[len(payment_method) - 2]
		try:
			bundle.obj.payment_method = PaymentMethod.objects.get(pk=payment_method)
		except ObjectDoesNotExist:
			logger.error("Orden con metodo de pago inexistente del FTEFrontendUser " + user)
			raise CustomBadRequest(
					code="does_not_exist",
					message="That payment method does not exist.")

		try:
			bundle.obj.save()
		except Exception as e:
			logger.error("Problema al guardar una orden. Error: " + e)
			raise CustomBadRequest(
					code="unknown",
					message="Could not save the order.")

		for item in bundle.data['items']:
			try:
				resource_item = Item.objects.get(pk=item['item']['id'])
				if (resource_item.category.restaurant.id != int(restaurant)):
					try:
						bundle.obj.delete()
					except Exception as e:
						logger.error("Problema al borrar la orden. Error: " + e)
					logger.warning("Orden con item de restaurante equivocado del FTEFrontendUser " + user)
					raise CustomBadRequest(
						code="does_not_belong",
						message="That item does not belong to the restaurant.")
			except ObjectDoesNotExist:
				logger.error("Orden con item inexistente del FTEFrontendUser " + user)
				try:
					bundle.obj.delete()
				except Exception as e:
					logger.error("Problema al borrar la orden. Error: " + e)
				raise CustomBadRequest(
						code="does_not_exist",
						message="That item does not exist.")
			it = ItemOrder(order=bundle.obj, item=resource_item, quantity=item['quantity'],
							extra_info=item['extra_info'], total_item=item['total_item'])
			it.save()
			if (item['selectables_associated']):
				for selectable in item['selectables_associated']:
					try:
						select = Selectable.objects.get(pk=selectable['id'])
						if resource_item not in select.selectable_type.item_set.all():
							logger.warning(
								"Orden con seleccionable que no pertenece al item seleccionado del FTEFrontendUser " 
								+ user)
							try:
								bundle.obj.delete()
							except Exception as e:
								logger.error("Problema al borrar la orden. Error: " + e)
							raise CustomBadRequest(
									code="does_not_belong",
									message="That selectable does not belong to the item.")
					except ObjectDoesNotExist:
						logger.error("Orden con selectable inexistente del FTEFrontendUser " + user)
						try:
							bundle.obj.delete()
						except Exception as e:
							logger.error("Problema al borrar la orden. Error: " + e)
						raise CustomBadRequest(
							code="does_not_exist",
							message="That selectable does not exist.")
					it_sel = ItemSelectable(item_order=it, selectable=select)
					it_sel.save()
			if (item['extras']):
				for extra_type in item['extras']:
					for extra in extra_type['types']:
						if extra['selected']:
							try:
								ex = Extra.objects.get(pk=extra['id'])
								if resource_item not in select.selectable_type.item_set.all():
									logger.warning("Orden con extra que no pertenece al item seleccionado del FTEFrontendUser "
										 + user)
									try:
										bundle.obj.delete()
									except Exception as e:
										logger.error("Problema al borrar la orden. Error: " + e)
									raise CustomBadRequest(
										code="does_not_belong",
										message="That selectable does not belong to the item.")
							except ObjectDoesNotExist:
								logger.error("Orden con extra inexistente del FTEFrontendUser " + user)
								try:
									bundle.obj.delete()
								except Exception as e:
									logger.error("Problema al borrar la orden. Error: " + e)
								raise CustomBadRequest(
									code="does_not_exist",
									message="That item does not exist.")
							it.extras.add(ex)
			it.save()

		new_order.send(sender=self.__class__, order=bundle.obj)

		return bundle


class ItemOrderResource(ModelResource):
	order = fields.ForeignKey('fte_admin.resources.OrderResource', 'order', full=True)
	item = fields.ForeignKey('fte_restaurants.resources.ItemResource', 'item', full=True)
	selectables_associated = fields.ManyToManyField(
						'fte_restaurants.resources.SelectableResource',
						'selectables_associated', full=True)
	extras = fields.ManyToManyField('fte_restaurants.resources.ExtraResource', 'extras', full=True)

	class Meta:
		queryset = ItemOrder.objects.all()
		serializer = Serializer(formats=['json'])
		resource_name = 'order_item'
		allowed_methods = ['get', 'post']
		filtering = {
			'name': ALL,
			'order': ALL_WITH_RELATIONS,
		}
		always_return_data = True


@receiver(new_order)
def new_order_handler(sender, **kwargs):
	order = kwargs['order']
	email = order.user.email
	# Se crea la entrada del log para la nueva orden creada.
	logger.info("Nueva orden creada por " + email +
				" en " + order.restaurant.name + 
				". Numero de orden: " + order.order_number)

	# Enviar mail de confirmacion al dueño de la orden
	try:
		plaintext_file = FileSetting.objects.get(key='ORDER_TEMPLATE_TEXT').value.file
		plaintext_file.open()
		plaintext = plaintext_file.read()
		plaintext = Template(plaintext.decode("UTF-8"))
		plaintext_file.close()

		html_file = FileSetting.objects.get(key='ORDER_TEMPLATE_HTML').value.file
		html_file.open()
		html = html_file.read()
		html = Template(html.decode("UTF-8"))
		html_file.close()
		
		context = Context({"restaurant": order.restaurant.name, "order_num": order.order_number})

		subject = 'DeliveryRD - Confirmacion de orden'
		from_email = GlobalSetting.objects.get(key='DEFAULT_FROM_EMAIL').value
		text_content = plaintext.render(context)
		html_content = html.render(context)
		msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
		msg.attach_alternative(html_content, "text/html")
		msg.send(fail_silently=False)
	except Exception as e:
		logger.error("new_order_handler: Problema al enviar mail. Error: " + e)