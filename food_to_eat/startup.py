from django.contrib.auth.models import Group, Permission

from fte_users.models import FTEFrontendUser

def setup_groups():
	FrontEndUserGroup, created = Group.objects.get_or_create(name='FTEFrontEndUsers')
	permission_set = Permission.objects.filter(content_type__app_label__icontains="fte_users"
		).exclude(content_type__model__exact="fterestaurantuser"
		).exclude(content_type__model__exact="fteuser"
		).exclude(codename="add_ftefrontenduser")

	FrontEndUserGroup.permissions.add(*permission_set)

	user_set = FTEFrontendUser.objects.filter(is_active=True)

	FrontEndUserGroup.user_set.add(*user_set)
