from django import forms
from django.forms.models import ModelForm
from fte_admin.models import ItemSelectable, Order, ItemOrder
from fte_restaurants.models import Extra
   

class ItemSelectableForm(ModelForm):
    '''
    ItemSelectable Form base definition.
    '''
    class Meta:
        model = ItemSelectable
        fields = "__all__"
        
class OrderForm(forms.ModelForm):
    '''
    Order complete Form base definition.
    '''
    class Meta:
        model = Order
        fields = '__all__'
        
    def __init__(self,*args,**kwargs):
        super(OrderForm,self).__init__(*args,**kwargs)
        
class OrderAddForm(forms.ModelForm):
    '''
    Order base form definition.
    '''
    class Meta:
        model = Order
        fields = ('user','restaurant')

class ItemOrderForm(forms.ModelForm):
    '''
    ItemOrder Form base definition.
    '''
    class Meta:
        model = ItemOrder
        fields = '__all__'
        
    def __init__(self,*args,**kwargs):
        super(ItemOrderForm,self).__init__(*args,**kwargs)
        ids = []
        for extra_type in self.obj.item.extra_types.all():
            ids.append(extra_type.id)
        self.fields['extras'].queryset = Extra.objects.filter(extra_type_id__in=ids)