from django.contrib import admin
from fte_users.models import FTEUser, FTERestaurantUser, FTEFrontendUser,\
    DeliveryAddress, RNC
from custom_user.admin import EmailUserAdmin
from django.utils.translation import ugettext_lazy as _
from fte_restaurants.admin import StackedItemInline
from fte_users.forms import RequiredInlineFormSet
from django.core.urlresolvers import reverse

class FTEUserAdmin(EmailUserAdmin):
    '''
    Basic user Admin definition.
    '''
    list_display = ('email','is_staff','is_superuser')
    list_filter = ('is_staff','is_superuser',)
    search_fields = ['first_name','last_name','email']
    
    model = FTEUser
    actions_on_top = False
    actions_on_bottom = True
    
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name','last_name',
                           'telephone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','first_name','last_name',
                       'telephone')}
        ),
    )
    
class RNCInline(StackedItemInline):
    '''
    RNC Inline admin definition.
    '''
    model = RNC
    extra = 0
    
class DeliveryAddressInline(StackedItemInline):
    '''
    Delivery address admin definition.
    '''
    model = DeliveryAddress
    extra = 0
    min_num = 1
    formset = RequiredInlineFormSet
    
class FTEFrontendUserAdmin(FTEUserAdmin):
    '''
    Frontend user Admin definition.
    '''
    model = FTEFrontendUser
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name','last_name','date_of_birth',
                           'telephone','gender','photo')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','first_name','last_name',
                       'telephone','date_of_birth','gender')}
        ),
    )
    
    inlines = [
        DeliveryAddressInline, RNCInline,
    ]
    
    list_display = ('first_name','last_name','email','telephone','gender')
    list_display_links = ('first_name', 'last_name', 'email')
    search_fields = ['first_name','last_name','email','gender']
    list_filter = ('is_staff','is_superuser','gender',)
    
class FTERestaurantUserAdmin(FTEUserAdmin):
    '''
    Restaurant user Admin definition.
    '''
    model = FTERestaurantUser
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name','last_name',
                           'telephone','restaurant_associated')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('first_name','last_name','email','restaurant_name','telephone')
    list_display_links = ('first_name', 'last_name', 'email')
    search_fields = ['first_name','last_name','email',]
    list_filter = ('is_staff','is_superuser',)
    
    
    def restaurant_name(self, obj):
        try:
            if obj.restaurant_associated != None:
                url = reverse('admin:%s_%s_change' % (obj.restaurant_associated._meta.app_label,
                                                     (obj.restaurant_associated.__class__.__name__).lower()), 
                                                      args=(obj.restaurant_associated.pk,))
                return '<a href="'+str(url)+'">'+str(obj.restaurant_associated.name)+'</a>'  
            else:
                return '-'
        except:
            return '-'
    restaurant_name.allow_tags = True
    restaurant_name.short_description = _("Restaurant")

# Register your models here.
admin.site.register(FTEUser, FTEUserAdmin)
admin.site.register(FTEFrontendUser, FTEFrontendUserAdmin)
admin.site.register(FTERestaurantUser, FTERestaurantUserAdmin)
#admin.site.unregister(Group)