from django.contrib.admin.filters import SimpleListFilter
from fte_restaurants.models import FoodType

class MainFoodFilter(SimpleListFilter):
    """ 
    Main food type filter for Restaurant Admin.
    """
    
    title = 'Main Food Type'
    parameter_name = 'main_food_type'

    def lookups(self, request, model_admin):
        foodtypes = set([c for c in FoodType.objects.all()])
        return [(c.name, c.name) for c in foodtypes]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(main_food_type__name__exact=self.value())
        else:
            return queryset
        
class SecondaryFoodFilter(SimpleListFilter):
    """ 
    Secondary food type filter for Restaurant Admin
    """
    title = 'Secondary Food Type'
    parameter_name = 'secondary_food_type'

    def lookups(self, request, model_admin):
        foodtypes = set([c for c in FoodType.objects.all()])
        return [(c.name, c.name) for c in foodtypes]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(secondary_food_type__name__exact=self.value())
        else:
            return queryset