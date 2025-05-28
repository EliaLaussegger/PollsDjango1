from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from profiles.models import Profile


@receiver(user_logged_in)
def verify_user_on_social_login(request, user, **kwargs):
    try:
        profile = user.profile 
        if user.socialaccount_set.exists():
            profile.is_verified = True
            profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=user, is_verified=True)