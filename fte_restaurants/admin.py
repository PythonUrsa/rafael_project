from django.contrib import admin
from fte_restaurants.models import Telephone, Schedule, Category, Restaurant,\
    Zone, FoodType, Item, SelectableType, Selectable, ExtraType, Extra, PaymentMethod, City
from django.contrib.admin.options import ModelAdmin
from fte_restaurants.forms import RestaurantForm, ItemForm, ItemAddForm
from django.utils.translation import ugettext_lazy as _
from fte_restaurants.filters import MainFoodFilter, SecondaryFoodFilter
from django.core.urlresolvers import reverse

class StackedItemInline(admin.StackedInline):
    """ 
    StackedItemInline definition. It includes some Grappelli custom optimizations.
    """
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

class TelephoneInline(StackedItemInline):
    """ 
    Inline for DeliveryAddress model.
    """
    model = Telephone
    extra = 0

class ScheduleInline(StackedItemInline):
    """ 
    Inline for Schedule model.
    """
    model = Schedule
    extra = 0
    
class CategoryInline(StackedItemInline):
    """ 
    Inline for Category model.
    """
    model = Category
    extra = 0
    
class SelectableInline(StackedItemInline):
    """ 
    Inline for Selectable model
    """
    model = Selectable
    extra = 0

class SelectableTypeInline(StackedItemInline):
    """ 
    Inline for SelectableType model
    """
    model = SelectableType
    extra = 0

#####################################
### ADMIN ###########################
#####################################
    
class RestaurantAdmin(ModelAdmin):
    """ 
    Restaurant ModelAdmin definition.
    """
    model = Restaurant
    form = RestaurantForm
    inlines = [
        TelephoneInline,ScheduleInline,CategoryInline
    ]
    
    list_display = ('name','email','user','featured','main_food_type','secondary_food_type','address',
                    'delivery_cost','delivery_time','order_minimum','get_payment_methods','get_zones')
    search_fields = ['name','email','user__email','featured','main_food_type__name','secondary_food_type__name','address',
                    'delivery_cost','delivery_time','order_minimum', 'payment_methods__name','zones__name']  
    list_filter = ('payment_methods__name','zones__name',MainFoodFilter,SecondaryFoodFilter)

    def get_payment_methods(self,obj):
        methods = obj.payment_methods.all()
        returned_methods = []
        for method in methods:
            returned_methods.append(str(method))
        return ','.join(returned_methods)
    
    get_payment_methods.short_description = _('Accepted Payment Methods')
    
    def get_zones(self,obj):
        zones = obj.zones.all()
        returned_zones = []
        for zone in zones:
            returned_zones.append(zone.name)
        return ','.join(returned_zones)
    
    get_zones.short_description = _('Delivery Zones')
    
    def get_form(self, request, *args, **kwargs): 
        form = super(RestaurantAdmin, self).get_form(request, *args, **kwargs)
        form.user = request.user
        return form
    
class SelectableTypeAdmin(ModelAdmin):
    """ 
    Restaurant's Selectable Types ModelAdmin definition.
    """
    model = SelectableType
    inlines = [
        SelectableInline
    ]
    
    list_display = ('id','name','category','restaurant_name')
    list_display_links = ('id','name')
    search_fields = ['name','category__name']  
    list_filter = ('category','category__restaurant__name')

    def restaurant_name(self, obj):
        try:
            if obj.category.restaurant != None:
                url = reverse('admin:%s_%s_change' % (obj.category.restaurant._meta.app_label,
                                                     (obj.category.restaurant.__class__.__name__).lower()), 
                                                      args=(obj.category.restaurant.pk,))
                return '<a href="'+str(url)+'">'+str(obj.category.restaurant.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    restaurant_name.allow_tags = True
    restaurant_name.short_description = _("Restaurant")
    
class ItemAdmin(ModelAdmin):
    """ 
    Item ModelAdmin definition.
    """
    model = Item

    form = ItemForm
    add_form = ItemAddForm
    
    list_display = ('id','name','category','restaurant_name','price',
                    'enabled','deleted','get_selectable_types','get_item_extras')
    search_fields = ['name','category__name','price','description']  
    list_filter = ('enabled','category','category__restaurant__name')
    
    def get_selectable_types(self,obj):
        selectables = obj.selectable_types.all()
        returned_selectables = []
        for selectable in selectables:
            returned_selectables.append(str(selectable))
        return ','.join(returned_selectables)
    
    get_selectable_types.short_description = _('Selectable Types')
    
    def get_item_extras(self,obj):
        
        extras = obj.extra_types.all()
        returned_extras = []
        for extra in extras:
            returned_extras.append(extra.name)
        return ','.join(returned_extras)
    
    get_item_extras.short_description = _('Eligible Extras')
    
    def restaurant_name(self, obj):
        try:
            if obj.category.restaurant != None:
                url = reverse('admin:%s_%s_change' % (obj.category.restaurant._meta.app_label,
                                                     (obj.category.restaurant.__class__.__name__).lower()), 
                                                      args=(obj.category.restaurant.pk,))
                return '<a href="'+str(url)+'">'+str(obj.category.restaurant.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    restaurant_name.allow_tags = True
    restaurant_name.short_description = _("Restaurant")
    
    def get_form(self, request, obj=None, **kwargs):
            defaults = {}
            if obj is None:
                defaults.update({
                    'form': self.add_form,
                })
            defaults.update(kwargs)
            form =  super(ItemAdmin, self).get_form(request, obj, **defaults)
            form.obj = obj
            return form
    
    def response_add(self, request, obj, post_url_continue='../%s/'):
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1
        post_url_continue='../{0}/'.format(obj.id)
        return super(ItemAdmin, self).response_add(request, obj, post_url_continue)
    
class ZoneAdmin(ModelAdmin):
    """ 
    Delivery Zone ModelAdmin definition.
    """
    model = Zone

    search_fields = ['name']  

class CityAdmin(ModelAdmin):
    """ 
    City ModelAdmin definition.
    """
    model = Zone

    search_fields = ['name']  



class CategoryAdmin(ModelAdmin):
    """ 
    Restaurant's Categories ModelAdmin definition.
    """
    model = Category
    
    list_display = ('id','name','restaurant_name','description')
    list_display_links = ('id','name')
    search_fields = ['name','restaurant__name','description']  
    list_filter = ('restaurant',)
    
    inlines = [
               SelectableTypeInline,
               ]
    
    def restaurant_name(self, obj):
        try:
            if obj.restaurant != None:
                url = reverse('admin:%s_%s_change' % (obj.restaurant._meta.app_label,
                                                     (obj.restaurant.__class__.__name__).lower()), 
                                                      args=(obj.restaurant.pk,))
                return '<a href="'+str(url)+'">'+str(obj.restaurant.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    restaurant_name.allow_tags = True
    restaurant_name.short_description = _("Restaurant")

class FoodTypeAdmin(ModelAdmin):
    """ 
    Restaurant's Food Type ModelAdmin definition.
    """
    model = FoodType
    search_fields = ['name']
     


class TelephoneAdmin(ModelAdmin):
    """ 
    Restaurant's Telephone ModelAdmin definition.
    """
    model = Telephone
    
    list_display = ('id','number','restaurant_name','description')
    search_fields = ['number','restaurant__name','description']  
    list_filter = ('restaurant',)
    
    def restaurant_name(self, obj):
        try:
            if obj.restaurant != None:
                url = reverse('admin:%s_%s_change' % (obj.restaurant._meta.app_label,
                                                     (obj.restaurant.__class__.__name__).lower()), 
                                                      args=(obj.restaurant.pk,))
                return '<a href="'+str(url)+'">'+str(obj.restaurant.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    restaurant_name.allow_tags = True
    restaurant_name.short_description = _("Restaurant")

class ScheduleAdmin(ModelAdmin):
    """ 
    Restaurant's Schedules ModelAdmin definition.
    """
    model = Schedule
    
    list_display = ('id','start_time','finish_time','restaurant_name')
    search_fields = ['restaurant__name']  
    list_filter = ('start_time','finish_time','restaurant__name')

    def restaurant_name(self, obj):
        try:
            if obj.restaurant != None:
                url = reverse('admin:%s_%s_change' % (obj.restaurant._meta.app_label,
                                                     (obj.restaurant.__class__.__name__).lower()), 
                                                      args=(obj.restaurant.pk,))
                return '<a href="'+str(url)+'">'+str(obj.restaurant.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    restaurant_name.allow_tags = True
    restaurant_name.short_description = _("Restaurant")

class SelectableAdmin(ModelAdmin):
    """ 
    Restaurant's Selectables ModelAdmin definition.
    """
    model = Selectable
    
    list_display = ('id','name','description','price','selectable_type','category_name','restaurant_name')
    search_fields = ['name','description','selectable_type__name','selectable_type__category__name',
                     'selectable_type__category__restaurant__name']  
    list_filter = ('selectable_type','selectable_type__category','selectable_type__category__restaurant',)

    def category_name(self, obj):
        try:
            if obj.selectable_type.category != None:
                url = reverse('admin:%s_%s_change' % (obj.selectable_type.category._meta.app_label,
                                                     (obj.selectable_type.category.__class__.__name__).lower()), 
                                                      args=(obj.selectable_type.category.pk,))
                return '<a href="'+str(url)+'">'+str(obj.selectable_type.category.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    category_name.allow_tags = True
    category_name.short_description = _("Category")

    def restaurant_name(self, obj):
        try:
            if obj.selectable_type.category.restaurant != None:
                url = reverse('admin:%s_%s_change' % (obj.selectable_type.category.restaurant._meta.app_label,
                                                     (obj.selectable_type.category.restaurant.__class__.__name__).lower()), 
                                                      args=(obj.selectable_type.category.restaurant.pk,))
                return '<a href="'+str(url)+'">'+str(obj.selectable_type.category.restaurant.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    restaurant_name.allow_tags = True
    restaurant_name.short_description = _("Restaurant")

class ExtraTypeAdmin(ModelAdmin):
    """ 
    Restaurant's ExtraTypes ModelAdmin definition.
    """
    model = ExtraType
    
    list_display = ('id','name','restaurant_name')
    search_fields = ['name','restaurant__name']  
    list_filter = ('restaurant',)

    def restaurant_name(self, obj):
        try:
            if obj.restaurant != None:
                url = reverse('admin:%s_%s_change' % (obj.restaurant._meta.app_label,
                                                     (obj.restaurant.__class__.__name__).lower()), 
                                                      args=(obj.restaurant.pk,))
                return '<a href="'+str(url)+'">'+str(obj.restaurant.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    restaurant_name.allow_tags = True
    restaurant_name.short_description = _("Restaurant")

class ExtraAdmin(ModelAdmin):
    """ 
    Restaurant's Extras ModelAdmin definition.
    """
    model = Extra
    
    list_display = ('id','name','price','extra_type','restaurant_name')
    search_fields = ['name','description','extra_type__name', 'extra_type__restaurant__name']  
    list_filter = ('extra_type','extra_type__restaurant',)

    def restaurant_name(self, obj):
        try:
            if obj.extra_type.restaurant != None:
                url = reverse('admin:%s_%s_change' % (obj.extra_type.restaurant._meta.app_label,
                                                     (obj.extra_type.restaurant.__class__.__name__).lower()), 
                                                      args=(obj.extra_type.restaurant.pk,))
                return '<a href="'+str(url)+'">'+str(obj.extra_type.restaurant.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    restaurant_name.allow_tags = True
    restaurant_name.short_description = _("Restaurant")
    
admin.site.register(Zone,ZoneAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(FoodType, FoodTypeAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Telephone, TelephoneAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SelectableType,SelectableTypeAdmin)
admin.site.register(Selectable, SelectableAdmin)
admin.site.register(ExtraType, ExtraTypeAdmin)
admin.site.register(Extra, ExtraAdmin)
admin.site.register(PaymentMethod)