import logging

from django.db import models
from django.contrib.auth.models import Group
from django.dispatch import receiver
from custom_user.models import EmailUserManager, AbstractEmailUser
from django.db.models.fields.files import ImageField
from django.db.models.fields import IntegerField
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Template, Context
from django.apps.config import AppConfig

from simple_email_confirmation import SimpleEmailConfirmationUserMixin

from fte_admin.models import GlobalSetting, FileSetting


logger = logging.getLogger(__name__)


GENDERS = (
    ('M', 'Male'),
    ('F', 'Female')
    )

class UsersAppConfig(AppConfig):
    name = 'fte_users'
    verbose_name = "Food to Eat - Users"

# Create your models here.
class FTEUser(SimpleEmailConfirmationUserMixin, AbstractEmailUser):
    '''
    Custom EmailUser implementation.
    '''
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=30)
    
    objects = EmailUserManager()
    REQUIRED_FIELDS = ['first_name','last_name','telephone']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"
    
    def __unicode__(self):
        return self.email
        
    # Methods
    def get_full_name(self):
        """
        Retorna el nombre completo del usuario.
        """ 
        return self.first_name + ' - ' + self.last_name

    def get_short_name(self):
        """
        Retorna el nickname del usuario.
        """ 
        return self.email
    
    
class FTEFrontendUser(FTEUser):
    '''
    Frontend user implementation.
    '''
    
    photo = ImageField(upload_to='images',verbose_name=('User Photo'), null=True, blank=True,
                        help_text="366x366 px")
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices = GENDERS)
    
    
    class Meta:
        verbose_name = 'Frontend User'
        verbose_name_plural = "Frontend Users"




    def __str__(self):
        return self.email
    
class FTERestaurantUser(FTEUser):
    '''
    Restaurant user implementation.
    '''
    
    restaurant_associated = models.OneToOneField('fte_restaurants.Restaurant',help_text=('Restaurant associated.'),
                                      related_name="user", blank = True, null = True, unique = True)
    

    class Meta:
        verbose_name = 'Restaurant User'
        verbose_name_plural = "Restaurant Users"
    
    def __str__(self):
        return self.email    
    
class RNC(models.Model):
    '''
    FrontendUser's RNC Number model definition.
    '''
    rnc_number = models.IntegerField()
    description = models.CharField(max_length=255, verbose_name = ("Short description"))
    frontend_user = models.ForeignKey('FTEFrontendUser',help_text=('User.'),
                                      related_name="user_rnc")
    main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.main:
            try:
                temp = RNC.objects.get(main=True, frontend_user=self.frontend_user)
                if self != temp:
                    temp.main = False
                    temp.save()
            except RNC.DoesNotExist:
                pass
        super(RNC, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'RNC Number'
        verbose_name_plural = "RNC Numbers"
    
    def __unicode__(self):
        return self.rnc_number
    
class DeliveryAddress(models.Model):
    '''
    FrontendUser's Delivery Address model definition.
    '''
    
    street_name = models.CharField(max_length=255)
    street_number = models.CharField(max_length=50)
    city = models.ForeignKey('fte_restaurants.City', related_name="city_user_addresses")
    delivery_zone = models.ForeignKey('fte_restaurants.Zone', related_name="zone_user_addresses")
    associated_name = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    frontend_user = models.ForeignKey('FTEFrontendUser',help_text=('User.'),
                                      related_name="user_delivery_addresses")
    main = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Delivery Address'
        verbose_name_plural = "Delivery Addresses"

    def save(self, *args, **kwargs):
        if self.main:
            try:
                temp = DeliveryAddress.objects.get(main=True, frontend_user=self.frontend_user)
                if self != temp:
                    temp.main = False
                    temp.save()
            except DeliveryAddress.DoesNotExist:
                pass
        super(DeliveryAddress, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return (self.street_name + ' ' + self.street_number + ', ' + self.delivery_zone.name + ', ' +
                self.city.name + '.')



@receiver(post_save, sender=FTEFrontendUser)
def user_post_save(sender, instance, created, **kwargs):
    
    if created:
        # Add user to the frontend users group
        try:
            group = Group.objects.get(name="FTEFrontEndUsers")
            instance.groups.add(group)
        except Exception as e:
            logger.error("user_post_save: " + e)

    # Send user the verification email
    email = instance.email
    try:
        fe_user = FTEFrontendUser.objects.get(email=email)
    except ObjectDoesNotExist:
        print (ObjectDoesNotExist.message)
        raise ObjectDoesNotExist
    if not fe_user.confirmed_emails:
        if not fe_user.unconfirmed_emails:
            fe_user.add_unconfirmed_email(email);
        try:
            # plaintext   = get_template(GlobalSetting.objects.get(key='EMAIL_TEMPLATE_TEXT').value)
            plaintext_file = FileSetting.objects.get(key='EMAIL_TEMPLATE_TEXT').value.file
            plaintext_file.open()
            plaintext = plaintext_file.read()
            plaintext = Template(plaintext.decode("UTF-8"))
            plaintext_file.close()

            # html        = get_template(GlobalSetting.objects.get(key='EMAIL_TEMPLATE_HTML').value)
            html_file = FileSetting.objects.get(key='EMAIL_TEMPLATE_HTML').value.file
            html_file.open()
            html = html_file.read()
            html = Template(html.decode("UTF-8"))
            html_file.close()
            confirmation_url = GlobalSetting.objects.get(key='EMAIL_CONFIRMATION_URL').value
            confirmation_link = (confirmation_url +
                                fe_user.email + '/' +
                                fe_user.confirmation_key + '/')
            context = Context({"email": fe_user.email, "confirmation_link": confirmation_link})

            subject = 'DeliveryRD - Confirmacion de email'
            from_email = GlobalSetting.objects.get(key='DEFAULT_FROM_EMAIL').value
            text_content = plaintext.render(context)
            html_content = html.render(context)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
        except Exception as e:
            logger.error("user_post_save: Error enviando mail. Error: " + e)

