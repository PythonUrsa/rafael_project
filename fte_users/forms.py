from django import forms
from django.forms.models import ModelForm, BaseInlineFormSet

from django.utils.translation import ugettext_lazy as _
from fte_users.models import FTEFrontendUser, FTERestaurantUser

class RequiredInlineFormSet(BaseInlineFormSet):
    '''
    Required Inline formset definition.
    '''
    def _construct_form(self, i, **kwargs):
        '''
        Method override. Makes mandatory at least one element.
        '''
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form
    

class FTEFrontendUserForm(ModelForm):
    '''
    Frontend user form definition.
    '''
    class Meta:
        model = FTEFrontendUser        
        fields = "__all__"

class FTERestaurantUserForm(ModelForm):
    '''
    Restaurant user form definition
    '''
    class Meta:
        model = FTERestaurantUser  
        fields = "__all__"      