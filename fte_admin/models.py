from __future__ import division
from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.files import ImageField
from django.apps.config import AppConfig


ORDER_TYPE = (
                ('DELIVERY', 'Delivery'),
                ('PICKUP', 'Pick up'),
             )

class AdministrationConfig(AppConfig):
    name = 'fte_admin'
    verbose_name = _("Food to Eat - Administration")


# Create your models here.
class Order(models.Model):
    '''
    Order model definition. It specifies it's user and restaurant
    '''
    user = models.ForeignKey('fte_users.FTEFrontendUser', help_text=_("User who made the order."),
                                  related_name="user_orders")
    restaurant = models.ForeignKey('fte_restaurants.Restaurant', help_text=_("Restaurant associated to the order."),
                                  related_name="restaurant_orders")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name = _("Date added"))
    delivered = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    change = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.ForeignKey('fte_restaurants.PaymentMethod', related_name="method_orders")
    additional_info = models.TextField(verbose_name = _("Additional information"), blank=True, null=True)
    delivery_address = models.ForeignKey('fte_users.DeliveryAddress', help_text=_("Address for the order to be delivered."),
                                    related_name="address_orders", blank=True, null=True)
    rnc = models.ForeignKey('fte_users.RNC', related_name="rnc_orders", null=True, blank=True)
    order_number = models.TextField(verbose_name=_("Number that identifies the order"))
    order_type = models.CharField(max_length=16, choices=ORDER_TYPE, default='DELIVERY')

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _("Orders")
    
    def __str__(self):
        return str(self.id) + " - " + self.user.email  + " - " + self.restaurant.name
    
    def get_order_total (self):
        total = 0
        if self.items_related.exists():
            for item_order in self.items_related.all():
                total += item_order.total_item
        total += self.restaurant.delivery_cost;
        itbis = GlobalSetting.objects.get(key="ITBIS")
        itbis = total * Decimal(int(itbis.value) / 100)
        tip = GlobalSetting.objects.get(key="LEGAL_TIP")
        tip = total * Decimal(int(tip.value) / 100)
        return total + tip + itbis
        
    
    def save(self, *args, **kwargs):
        self.total = self.get_order_total()
        if (self.order_number == ''):
            restaurant_id = self.restaurant.id.__str__()
            restaurant_id = restaurant_id.zfill(3);
            order_num = self.restaurant.restaurant_orders.count().__str__()
            self.order_number = restaurant_id + '-' + order_num.zfill(6)
        super(Order, self).save(*args, **kwargs)
        
    

class ItemOrder (models.Model):
    '''
    Item - Order relation definition. 
    '''
    order = models.ForeignKey('Order', related_name = "items_related")
    item = models.ForeignKey('fte_restaurants.Item', related_name = "orders_related" )
    extras = models.ManyToManyField('fte_restaurants.Extra', blank=True, null=True)
    selectables_associated = models.ManyToManyField('fte_restaurants.Selectable', through = 'ItemSelectable', blank = True, null = True)
    
    quantity = models.PositiveIntegerField(help_text = _("Item's quantity"))
    extra_info = models.TextField(verbose_name = _("Additional information"), blank=True, null=True)
    total_item = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = _("Order's Item")
        verbose_name_plural = _("Order's Items")
        
    def __str__(self):
        return str(self.order.id) + ' - ' + self.item.name + ': ' + str(self.quantity)
    
    def get_price(self):
        '''
        Method that gets the total price, with extras and selectables included
        '''
        total = self.item.price
        
        if self.extras.exists():
            for extra in self.extras.all():
                total += extra.price
        
        if self.selectables_associated.exists():
            for selectable in self.selectables_associated.all():
                total += selectable.price
            
        total = total * self.quantity
        return total
        
    
    def save(self, *args, **kwargs):
        # Save many to many relations first
        self.total_item = 0
        super(ItemOrder, self).save(*args, **kwargs)
        # Get total item price
        self.total_item = self.get_price()
        # Save it
        super(ItemOrder, self).save(*args, **kwargs)
        # Request order update
        self.order.save()
    
class ItemSelectable(models.Model):
    '''
    Item - Selectable relation definition.
    '''
    item_order = models.ForeignKey('ItemOrder')
    selectable = models.ForeignKey('fte_restaurants.Selectable')
    
    class Meta:
        verbose_name = _('Item - Selectable')
        verbose_name_plural = _("Items - Selectables")
        
    def __str__(self):
        return str(self.id) + ' - ' + self.item_order.item.name + ' - ' + self.selectable.name
    
    def save(self, *args, **kwargs):
        super(ItemSelectable, self).save(*args, **kwargs)
        self.item_order.save()
    
    
class Photo(models.Model):
    '''
    Frontend Photo model definition.
    '''
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    image = ImageField(upload_to='main_photos',verbose_name=('Front Picture'), help_text="1290x345 px")
    description = models.CharField(max_length=200, verbose_name=_('Description'),blank=True,null=True)    
    published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Front Photo')
        verbose_name_plural = _("Front Photos")
    
class GlobalSetting(models.Model):
    """
        GLOBAL SETTINGS USED:

        MAIN_CITY: ID of Main City
        ITBIS: Tax value
        LEGAL_TIP: Legal tip
        EMAIL_CONFIRMATION_URL: Base url that calls the confirm_email view
        DEFAULT_FROM_EMAIL: Default email to be used as sender

        
    """


    key = models.CharField(unique=True, max_length=255)
    value = models.CharField(max_length=255)
    #objects = GlobalSettingsManager()

    def __str__(self):
        return self.key

class TextSetting(models.Model):
    """
        TEXT SETTINGS USED:

        TERMS:      Terminos de uso del sitio
        POLITICS:   Politicas y condiciones
        ABOUT_US:   "Sobre nosotros"
        CONTACT:    Informacion de contacto
        EMPLOYMENT: Informacion de empleo
    """
    key = models.CharField(unique=True, max_length=255)
    value = models.TextField()

    def __str__(self):
        return self.key

class FileSetting(models.Model):
    """
        FILE SETTINGS USED:

        EMAIL_TEMPLATE_HTML: HTML template for the user email
                             confirmation email
        EMAIL_TEMPLATE_TEXT: Plaintext template for the user
                             email confirmation email
        ORDER_TEMPLATE_HTML: HTML template for the order confirmation
                             email that is sent to the user.
        ORDER_TEMPLATE_TEXT: Plaintext template for the order confirmation
                             email that is sent to the user.
    """
    key = models.CharField(unique=True, max_length=255)
    value = models.FileField(upload_to='files', verbose_name=('File'))

    def __str__(self):
        return self.key