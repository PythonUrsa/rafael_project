from tastypie.exceptions import Unauthorized
from tastypie.authorization import Authorization


class CustomAuthorization(Authorization):
    '''
    Authorization for FTE FrontEndUsers, they can only access
    their own data
    '''
    def read_list(self, object_list, bundle):
        return object_list.filter(email=bundle.request.user)
    
    def read_detail(self, object_list, bundle):
        return bundle.obj.pk == bundle.request.user.pk
    
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
        return bundle.obj.pk == bundle.request.user.pk
    
    def delete_list(self, object_list, bundle):
        return []
    
    def delete_detail(self, object_list, bundle):
        return bundle.obj.pk == bundle.request.user.pk