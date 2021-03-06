import hashlib
import random
import re
import datetime
from rest_framework.views import exception_handler
from django.conf import settings
from django.utils.timezone import now as datetime_now
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from .models import RegistrationProfile


class EmailActivation(object):

    days = 7
    key = None
    ACTIVATED = u"ALREADY ACTIVATED"

    SHA1_RE = re.compile('^[a-f0-9]{40}$')

    def get_days(self):
        return {'message': 'You are registered'}

    def key_expired(self, user):
        activated = RegistrationProfile.objects.get(user=user)
        date_joined = user.date_joined
        expiration_date = datetime.timedelta(days=self.days)
        if date_joined + expiration_date <= datetime_now():
            activated.activation_key = self.ACTIVATED
            activated.save()
            return True
        else:
            return False

    def create_profile(self, user):
        activation_key = self.create_activation_key(user)
        registration_profile = RegistrationProfile.objects.create(
            user=user, activation_key=activation_key)
        return registration_profile

    def create_activation_key(self, user):
        username = user.username
        salt_bytes = str(random.random()).encode('utf-8')
        salt = hashlib.sha1(salt_bytes).hexdigest()[:5]
        hash_input = (salt + username).encode('utf-8')
        activation_key = hashlib.sha1(hash_input).hexdigest()
        return activation_key

    def send_activation_email(self, user, site):
        ctx_dict = {'activation_key': user.api_registration_profile.activation_key,
                    'expiration_days': self.days,
                    'site': site}
        subject = 'ACTIVATION KEY'
        message = str(ctx_dict)
        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def activate_user(self, activation_key):
        if self.SHA1_RE.search(activation_key):
            try:
                profile = RegistrationProfile.objects.get(
                    activation_key=activation_key)
            except RegistrationProfile.DoesNotExit:
                return False
            if profile.user.is_active and not self.key_expired(profile.user):
                print(profile.user.is_active)
                return profile.user
            if not self.key_expired(profile.user):
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = RegistrationProfile.ACTIVATED
                profile.save()
                return user
        return False

    def re_activate(self, email):
        activated = RegistrationProfile.objects.get(user__email=email)
        activated.activation_key = self.create_activation_key(activated.user)
        activated.save()
        self.send_activation_email(activated.user, Site.objects.get_current())

    def create_inactive_user(self, username, email, password=None):
        user_model = get_user_model()
        if username is not None:
            new_user = user_model.objects.create_user(username, email, password)
        else:
            new_user = user_model.objects.create_user(email=email, password=password)
        new_user.is_active = False
        new_user.save()
        self.create_profile(new_user)
        site = Site.objects.get_current()
        self.send_activation_email(new_user, site)
        return new_user


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        print(exc.get_full_details(), exc.get_codes(), exc.default_detail)
        response.data['status_code'] = response.status_code
        # response.data['errors'] = exc.get_full_details()
    return response