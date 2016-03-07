from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from fte_admin.models import Order, ItemSelectable, ItemOrder, Photo, GlobalSetting, TextSetting, FileSetting
from fte_restaurants.admin import StackedItemInline
from fte_admin.forms import ItemSelectableForm, OrderForm, OrderAddForm,\
    ItemOrderForm
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.core.urlresolvers import reverse
from daterange_filter.filter import DateRangeFilter
from django.contrib.auth.models import Group

from django_summernote.admin import SummernoteModelAdmin

class LinkedInline(admin.options.InlineModelAdmin):
    """ 
    LinkedInline definition. It includes some Grappelli custom optimizations.
    This inline includes a link to the object created, for a better navigation.
    """
    template = "admin/edit_inline/linked.html"
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    admin_model_path = None

    def __init__(self, *args):
        super(LinkedInline, self).__init__(*args)
        if self.admin_model_path is None:
            self.admin_model_path = self.model.__name__.lower()
    
# Register your models here.    
class ItemSelectableInline(StackedItemInline):
    """ 
    Inline for ItemSelectable
    """
    model = ItemSelectable
    extra = 0
    form = ItemSelectableForm
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(ItemSelectableInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'selectable':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(selectable_type__in = request._obj_.item.selectable_types.all())  
            else:
                field.queryset = field.queryset.none()

        return field
  
class ItemOrderInline(LinkedInline):
    """ 
    Inline for ItemOrder
    """
    model = ItemOrder
    exclude = ('total_item','extras')
    extra = 0
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(ItemOrderInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'item':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(category__in = request._obj_.restaurant.categories.all())  
            else:
                field.queryset = field.queryset.none()

        return field
        
    
class ItemOrderAdmin(ModelAdmin):
    """ 
    ItemOrder ModelAdmin definition.
    """
    model = ItemOrder
    inlines = [
        ItemSelectableInline,
    ]
    form = ItemOrderForm
    
    list_display = ('id','item','total_item','get_item_category','get_item_extras','get_selectables','get_order_pk','get_order_restaurant', 'get_order_user',)
    search_fields = ['order__user__first_name','order__user__last_name','order__user__email','order__restaurant__name',]  
    list_filter = ('order__user','order__restaurant__name')
    
    def has_add_permission(self, request):
        """
        Permission override
        """
        return False
    
    def get_item_category(self, obj):
        try:
            if obj.item.category != None:
                url = reverse('admin:%s_%s_change' % (obj.item.category._meta.app_label,
                                                     (obj.item.category.__class__.__name__).lower()), 
                                                      args=(obj.item.category.pk,))
                return '<a href="'+str(url)+'">'+str(obj.item.category.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    get_item_category.allow_tags = True
    get_item_category.short_description = _("Category")
    
    def get_item_extras(self,obj):
        
        extras = obj.extras.all()
        returned_extras = []
        for extra in extras:
            returned_extras.append(extra.name)
        return ','.join(returned_extras)
    
    get_item_extras.short_description = _('Extras')
    
    def get_selectables(self,obj):
        
        selectables = obj.selectables_associated.all()
        returned_selectables = []
        for selectable in selectables:
            returned_selectables.append(str(selectable))
        return ','.join(returned_selectables)
    
    get_selectables.short_description = _('Selectables')
    
    def get_order_pk(self, obj):
        try:
            if obj.order != None:
                url = reverse('admin:%s_%s_change' % (obj.order._meta.app_label,
                                                     (obj.order.__class__.__name__).lower()), 
                                                      args=(obj.order.pk,))
                return '<a href="'+str(url)+'">'+str(obj.order.pk)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    get_order_pk.allow_tags = True
    get_order_pk.short_description = _("Order ID")
    
    def get_order_restaurant(self, obj):
        try:
            if obj.order.restaurant != None:
                url = reverse('admin:%s_%s_change' % (obj.order.restaurant._meta.app_label,
                                                     (obj.order.restaurant.__class__.__name__).lower()), 
                                                      args=(obj.order.restaurant.pk,))
                return '<a href="'+str(url)+'">'+str(obj.order.restaurant.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    get_order_restaurant.allow_tags = True
    get_order_restaurant.short_description = _("Order User")
    
    def get_order_user(self, obj):
        try:
            if obj.order.user != None:
                url = reverse('admin:%s_%s_change' % (obj.order.user._meta.app_label,
                                                     (obj.order.user.__class__.__name__).lower()), 
                                                      args=(obj.order.user.pk,))
                return '<a href="'+str(url)+'">'+str(obj.order.user.email)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    get_order_user.allow_tags = True
    get_order_user.short_description = _("Order User")
    
    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        form =  super(ItemOrderAdmin, self).get_form(request, obj, **kwargs)
        form.obj = obj
        return form
    
class OrderAdmin(ModelAdmin):
    """ 
    Order ModelAdmin definition.
    """
    model = Order
    
    list_display = ('id','delivered', 'processed','user','restaurant','timestamp','total')
    search_fields = ['user__first_name','user__last_name','user__email','restaurant__name','timestamp',]  
    list_filter = ('user','restaurant__name','delivered', 'processed',('timestamp', DateRangeFilter))
    list_max_show_all = Order.objects.all().count()
    
    form = OrderForm
    add_form = OrderAddForm
    
    inlines = [
        ItemOrderInline,
    ]
    def get_form(self, request, obj=None, **kwargs):
            defaults = {}
            if obj is None:
                defaults.update({
                    'form': self.add_form,
                })
            defaults.update(kwargs)
            request._obj_ = obj
            form =  super(OrderAdmin, self).get_form(request, obj, **defaults)
            form.obj = obj
            return form
    
    
    def response_add(self, request, obj, post_url_continue='../%s/'):
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1
        post_url_continue='../{0}/'.format(obj.id)
        return super(OrderAdmin, self).response_add(request, obj, post_url_continue)
    
    def changelist_view(self, request, extra_context=""):
        response = super(OrderAdmin, self).changelist_view(request, extra_context)
        extra_context = extra_context or {}
        
        try:
            filtered_query_set = response.context_data["cl"].queryset
                    
            total = 0
            report_restaurants = []
            for elem in filtered_query_set:
                total += elem.total
                if not elem.restaurant.name in report_restaurants:
                    report_restaurants.append(elem.restaurant.name)
                
            extra_context['report_number_orders'] = filtered_query_set.count()
            extra_context['report_restaurants'] = report_restaurants
            extra_context['report_timestamp__lte'] = request.GET.get('timestamp__lte','-')
            extra_context['report_timestamp__gte'] = request.GET.get('timestamp__gte','-') 
            extra_context['report_total'] = total
            
            url_query = "?"
            for key in request.GET:
                url_query += key + "=" + request.GET[key] + "&"
                
            extra_context['report_download_url'] = reverse('create_report') + url_query
        except:
            pass
        
        return super(OrderAdmin, self).changelist_view(request, extra_context=extra_context)
    
class PhotoAdmin(ModelAdmin):
    """ 
    Frontend Photo ModelAdmin definition.
    """
    model = Photo
    
    list_display = ('name','published')
    list_filter = ('published',)
        
class TextSettingAdmin(SummernoteModelAdmin):
    pass


admin.site.register(TextSetting,TextSettingAdmin)    
admin.site.register(Order,OrderAdmin)
admin.site.register(ItemOrder,ItemOrderAdmin)
admin.site.register(Photo,PhotoAdmin)
admin.site.unregister(Group)
admin.site.register(GlobalSetting)
admin.site.register(FileSetting)