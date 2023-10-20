from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
        )
        subject = "Welcome To Our API Car Dealer"
        message = "We are glad to have in our website"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,)


def update_profile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.username = profile.username
        user.email = profile.email
        user.save()

def delete_user(sender, instance, *args, **kwargs):
    try:
        profile = instance
        user = profile.user
        user.delete()
    except:
        pass






@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
   
    subject = "Welcome To Our API Car Dealer, please use the token to confirm for reseting the password"
    send_mail(
        subject,
        reset_password_token.key,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email],
        fail_silently=False,)


post_delete.connect(delete_user, sender=Profile)    
post_save.connect(update_profile, sender=Profile)
post_save.connect(create_profile, User)