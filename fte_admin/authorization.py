from django.db.models import Q

from tastypie.exceptions import Unauthorized
from tastypie.authorization import Authorization


class CustomAuthorization(Authorization):
    '''
    Authorization for Orders, they can only be accessed
    by the owner and the restaurant
    '''
    def read_list(self, object_list, bundle):
        query = Q(user=bundle.request.user) | Q(restaurant__user=bundle.request.user)
        return object_list.filter(query)
    
    def read_detail(self, object_list, bundle):
        return ((bundle.obj.user.email == bundle.request.user.__str__()) or 
            (bundle.obj.restaurant.user.email == bundle.request.user.__str__()))
    
    def create_list(self, object_list, bundle):
        return object_list
    
    def create_detail(self, object_list, bundle):
        return bundle.obj.id == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed
    
    def update_detail(self, object_list, bundle):
        return ((bundle.obj.user.email == bundle.request.user.__str__()) or 
            (bundle.obj.restaurant.user.email == bundle.request.user.__str__()))
        # return bundle.obj.pk == bundle.request.user.pk
    
    def delete_list(self, object_list, bundle):
        return []
    
    def delete_detail(self, object_list, bundle):
        return bundle.obj.pk == bundle.request.user.pk