from django.db import models
from location_field.models.plain import PlainLocationField
from django.utils.translation import ugettext_lazy as _
from django.apps.config import AppConfig

class RestaurantAppConfig(AppConfig):
    name = 'fte_restaurants'
    verbose_name = _("Food to Eat - Restaurants")

class City (models.Model):

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _("City")
    
    def get_city_data(self):
        return {'id': self.id, 'name': self.name}


    def __str__(self):
        return self.name

class Zone (models.Model):
    """ 
    Delivery Zones supported model definition.
    """
    name = models.CharField(max_length=255, verbose_name=_("Delivery Zone"))
    city = models.ForeignKey('City', related_name="delivery_zones")

    class Meta:
        verbose_name = _('Delivery Zone')
        verbose_name_plural = _("Delivery Zones")
        unique_together = ("name","city")
    
    def get_zone_data(self):

        return {'id': self.id, 'name': self.name}


    def __str__(self):
        return self.name
    
class PaymentMethod (models.Model):
    '''
    Payment Method model definition.
    '''
    PAYMENT_CHOICES = (
        ("cash", "Efectivo"),
        ("mastercard", "MasterCard"),
        ("visa", "Visa"),
        ("american_express", "American Express"),
        ("paypal", "Paypal"),
    )

    name = models.CharField(max_length=255, choices=PAYMENT_CHOICES, verbose_name=_("Payment Method"))
    
    class Meta:
        verbose_name = _('Payment Method')
        verbose_name_plural = _("Payment Methods")
    
    def __str__(self):
        return self.name
    
class FoodType(models.Model):
    '''
    Food Type model definition.
    '''
    name = models.CharField(max_length=255, verbose_name=_("Food type"))    
    
    class Meta:
        verbose_name = _('Food Type')
        verbose_name_plural = _("Food Types")
    
    def __str__(self):
        return self.name
    
# Create your models here.
class Restaurant(models.Model):
    '''
    Restaurant model definition.
    '''
    # General info
    name = models.CharField(max_length=255, verbose_name=_("Restaurant name"))
    description = models.TextField(null = True, blank = True)
    email = models.EmailField()
    featured = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='images/restaurant',verbose_name=('Restaurant Photo'),
                                help_text="220x185 px")
    logo = models.ImageField(upload_to='images/restaurant',verbose_name=('Restaurant Logo'),
                                help_text="82x82 px")
    enabled = models.BooleanField(default=True)
    # Address & Location
    address = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=[address], zoom=7) 
    
    # Restaurant info
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.IntegerField(help_text=_("Estimated delivery time in minutes"))
    order_minimum = models.IntegerField(help_text=_("Minimum quantity to order"))
    payment_methods = models.ManyToManyField('PaymentMethod')
    zones = models.ManyToManyField('Zone')
    main_food_type = models.ForeignKey('FoodType',verbose_name=_("Main food type."),
                                  related_name="related_main_food") 
    secondary_food_type = models.ForeignKey('FoodType',verbose_name=_("Secondary food type."),
                                  related_name="related_secondary_food",) 
    
    
    def get_featured_data(self):

        dict = {'id': self.id , 
                'name': self.name, 
                'logo': self.logo.url,
                }

        return dict

    def get_schedule(self):

        schedule = self.schedules.all()[0]

        return str(schedule.start_time) + "-" + str(schedule.finish_time)

    def get_search_data(self, detail=False):
        
        dict = {'id': self.id , 
                'name': self.name, 
                'picture': self.photo.url,
                'logo': self.logo.url,
                'main_food_type': self.main_food_type.name,
                'secondary_food_type': self.secondary_food_type.name,
                'address': self.address,
                'delivery_time': self.delivery_time,
                'order_minimum': self.order_minimum,
                }

        if detail:
            dict['location'] = self.location
            dict['schedule'] = self.get_schedule()


        return dict

    def get_menu(self):

        menu_dict = {}
        for category in self.categories.all():
            if category.name not in menu_dict:    
                menu_dict[category.name] = []
            menu_dict[category.name].append({'id': category.id})
            for item in category.items.filter(enabled=True):
                menu_dict[category.name].append({'name': item.name,'id': item.id, 'price': str(item.price),'description': item.description})
            
        return menu_dict

    class Meta:
        verbose_name = _('Restaurant')
        verbose_name_plural = _("Restaurants")
    
    def __str__(self):
        return self.name
    
class Telephone(models.Model):
    '''
    Restaurant's Telephone model definition.
    '''
    restaurant = models.ForeignKey('Restaurant',help_text=_("Restaurant's Telephone."),
                                  related_name="telephones")
    number = models.CharField(max_length=30)
    description = models.TextField(null = True, blank = True)
    
    class Meta:
        verbose_name = _('Telephone')
        verbose_name_plural = _("Telephones")
    
    def __str__(self):
        return self.number
    
         
class Schedule (models.Model):
    '''
    Restaurant's schedule model definition.
    '''
    restaurant = models.ForeignKey('Restaurant',help_text=_("Restaurant's Schedule."),
                                  related_name="schedules")
    start_time = models.TimeField()
    finish_time = models.TimeField()
    
    class Meta:
        verbose_name = _("Restaurant's Schedule")
        verbose_name_plural = _("Restaurant's Schedules")
    
    def __str__(self):
        return str(self.start_time) + " - " + str(self.finish_time)

    
class Category (models.Model):
    '''
    Restaurant's Category model definition. Each Item of the menu belongs to a restaurant's category.
    All restaurant's categories conform the restaurant's menu.
    '''
    
    restaurant = models.ForeignKey('Restaurant',help_text=_("Restaurant's Category."),
                                  related_name="categories")
    name = models.CharField(max_length=255)
    description = models.TextField(null = True, blank = True)
    enabled = models.BooleanField(default=False)
    position = models.IntegerField(default=0);
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _("Categories")
    
    def save(self, *args, **kwargs):
        try:
            temp = Category.objects.filter(restaurant=self.restaurant, position=self.position)
            if len(temp) > 0:
                if self.pk is None:
                        count = Category.objects.filter(restaurant=self.restaurant).count()
                        for category in temp:
                            category.position = count;
                            category.save()
                else:
                    old = Category.objects.get(pk=self.pk)
                    for category in temp:
                            category.position = category.position + 1;
                            category.save()
        except Category.DoesNotExist:
            pass

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.restaurant.name + " - " +  self.name
    
class Item (models.Model):
    '''
    Restaurant's Item model definition.
    '''
    category = models.ForeignKey('Category',help_text=_("Restaurant's Category."),
                                  related_name="items")
    name = models.CharField(max_length=255)
    description = models.TextField(null = True, blank = True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    enabled = models.BooleanField(default=False)
    selectable_types = models.ManyToManyField('SelectableType', null=True, blank=True)
    extra_types = models.ManyToManyField('ExtraType', null=True, blank=True)
    deleted = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('Menu Item')
        verbose_name_plural = _("Menu items")
    
    def __str__(self):
        return self.category.name + " - " + self.name
    
class SelectableType(models.Model):
    '''
    Restaurant's Selectable Type model definition.
    '''
    category = models.ForeignKey('Category', related_name = "selectable_types")
    name = models.CharField(max_length=255)
    description = models.TextField(null = True, blank = True)
    
    class Meta:
        verbose_name = _('Selectable Type')
        verbose_name_plural = _("Selectable Types")
    
    def __str__(self):
        return self.name
    
class Selectable(models.Model):
    '''
    Selectable model definition.
    '''
    selectable_type = models.ForeignKey('SelectableType', help_text=_("Selectable type."),
                                  related_name="selectables")
    name = models.CharField(max_length=255)
    description = models.TextField(null = True, blank = True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = _('Selectable')
        verbose_name_plural = _("Selectables")
    
    def __str__(self):
        return self.selectable_type.name + " - " + self.name


class ExtraType(models.Model):
    '''
    Restaurant's Selectable Type model definition.
    '''
    restaurant = models.ForeignKey('Restaurant', related_name = "extra_types")
    name = models.CharField(max_length=255)
    description = models.TextField(null = True, blank = True)
    
    class Meta:
        verbose_name = _('Extra Type')
        verbose_name_plural = _("Extra Types")
    
    def __str__(self):
        return self.name


class Extra(models.Model):
    '''
    Restaurant's Extra model definition.
    '''
    extra_type = models.ForeignKey('ExtraType', help_text=_("Extra type."),
                                  related_name="extras")
    name = models.CharField(max_length=255)
    description = models.TextField(null = True, blank = True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = _('Extra')
        verbose_name_plural = _("Extras")
    
    def __str__(self):
        return self.name
    

    

    
    
    
    