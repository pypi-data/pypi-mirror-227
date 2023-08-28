# -*- coding:utf-8 -*-
from rest_framework import exceptions, authentication
__author__ = 'denishuang'

from .models import Appointment


class AppointAuthentication(authentication.TokenAuthentication):
    model = Appointment

    def authenticate_credentials(self, key):
        from .helper import check_appoint_token
        context = check_appoint_token(key)
        if not context:
            return None
        user, policy = super(AppointAuthentication, self).authenticate_credentials(context['ak'])
        return user, policy
