import logging

from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate,login,logout
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
import logging, json

from .models import FTEUser, FTEFrontendUser, FTERestaurantUser
from fte_admin.models import GlobalSetting, FileSetting

logger = logging.getLogger(__name__)

@csrf_exempt
def customer_login(request):
    print("Requesting Login: ", request.body)
    credentials = json.loads(request.body.decode("utf-8"))
    email = credentials['email']
    password = credentials['password']
    print(credentials)
    user = authenticate(email=email, password=password)

    if user is None:
        print("uno")    
        return HttpResponseNotAllowed("Error de User y/o Password", status=401)

    if user is not None:
        if user.is_active:
            try:
                #Check if its a FrontEnd User
                fe_user = FTEFrontendUser.objects.get(id=user.id)
            except ObjectDoesNotExist:
                logger.warning("customer_login: El Usuario no esta habilitado para loguearse")
                return HttpResponse("El Usuario no esta habilitado para loguearse", status=401)
            login(request, user)
            return HttpResponse(json.dumps({
                'name': user.first_name,
                'lastname': user.last_name,
                'email': user.email,
                'id': user.id,
            }))
        else:
            return HttpResponseNotAllowed("El usuario esta inhabilitado", status=401)
    else:
        print("dos")    
        return HttpResponse("Error de User y/o Password", status=401)

@csrf_exempt
def restaurant_login(request):
    print("Requesting Login: ", request.body)
    credentials = json.loads(request.body.decode("utf-8"))
    email = credentials['email']
    password = credentials['password']
    print(credentials)
    user = authenticate(email=email, password=password)

    if user is None:
        print("uno")    
        return HttpResponseNotAllowed("Error de User y/o Password", status=401)

    if user is not None:
        if user.is_active:
            try:
                #Check if its a FrontEnd User
                fe_user = FTERestaurantUser.objects.get(id=user.id)
            except ObjectDoesNotExist:
                logger.warning("restaurant_login: El Usuario no esta habilitado para loguearse")
                return HttpResponse("El Usuario no esta habilitado para loguearse", status=401)
            login(request, user)
            return HttpResponse(json.dumps({
                'name': user.first_name,
                'lastname': user.last_name,
                'email': user.email,
                'id': user.id,
            }))
        else:
            return HttpResponseNotAllowed("El usuario esta inhabilitado", status=401)
    else:
        print("dos")    
        return HttpResponse("Error de User y/o Password", status=401)


def user_logout(request):
    logout(request)
    return HttpResponse("Logged out!")


def send_confirmation_key(request):
    info = json.loads(request.body.decode("utf-8"))
    email = info['email']
    try:
        fe_user = FTEFrontendUser.objects.get(email=email)
    except ObjectDoesNotExist:
        print (ObjectDoesNotExist.message)
        return HttpResponse("Email no existe", status=401)
    if not fe_user.confirmed_emails:
        if not fe_user.unconfirmed_emails:
            fe_user.add_unconfirmed_email(email);
        try:
            plaintext_file = FileSetting.objects.get(key='EMAIL_TEMPLATE_TEXT').value.file
            plaintext_file.open()
            plaintext = plaintext_file.read()
            plaintext = Template(plaintext.decode("UTF-8"))
            plaintext_file.close()

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
            logger.error("send_confirmation_key: Error enviando mail: " + e)
    return HttpResponse(confirmation_link, status=200)

def confirm_email(request, email, key):
    try:
        fe_user = FTEFrontendUser.objects.get(email=email)
    except ObjectDoesNotExist:
        return HttpResponse("Email no existe", status=401)
    try:
        fe_user.confirm_email(key)
    except ObjectDoesNotExist:
        logger.warning("confirm_email: Clave de confirmacion incorrecta")
        return HttpResponse("Clave de confirmacion incorrecta", status=401)
    
    return HttpResponse("El mail ha sido confirmado con exito", status=200)

def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, uidb64=uidb64, token=token,
        post_reset_redirect=reverse("public_server"),
        template_name='password_reset_confirm.html')

def reset(request):
    return password_reset(request,
        email_template_name='reset_password_mail.html',
        template_name='password_reset_form.html',
        post_reset_redirect=reverse("public_server"))
