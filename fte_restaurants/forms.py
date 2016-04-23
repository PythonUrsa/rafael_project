from django import forms
from fte_restaurants.models import Restaurant, Zone,\
    PaymentMethod, Item, ExtraType

class RestaurantForm(forms.ModelForm):
    """ 
    Restaurant's base form definition.
    """
    payment_methods = forms.ModelMultipleChoiceField(queryset=PaymentMethod.objects.all() , widget=forms.CheckboxSelectMultiple(),required=True)
    zones = forms.ModelMultipleChoiceField(queryset=Zone.objects.all() , widget=forms.CheckboxSelectMultiple(),required=True)
    
    class Meta:
        model = Restaurant
        fields = '__all__'
        
    def __init__(self,*args,**kwargs):
        super(RestaurantForm,self).__init__(*args,**kwargs)
        
        # Disable featured option if user is a restaurant user
        if not self.user.is_superuser:
            self.fields['featured'].widget.attrs['disabled'] = 'True' 
        
        
class ItemForm(forms.ModelForm):
    """ 
    Item's complete form definition
    """
    class Meta:
        model = Item
        fields = '__all__'
        
    def __init__(self,*args,**kwargs):
        super(ItemForm,self).__init__(*args,**kwargs)
        self.fields['selectable_types'].queryset = self.obj.category.selectable_types.all()
        self.fields['extra_types'].queryset = self.obj.category.restaurant.extra_types.all() | ExtraType.objects.filter(restaurant__isnull = True)
        
class ItemAddForm(forms.ModelForm):
    """ 
    Item's base form definition.
    """
    class Meta:
        model = Item
        fields = ('category','name','price')
        
    