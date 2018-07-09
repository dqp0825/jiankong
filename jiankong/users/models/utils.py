#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf import settings
from django.utils import timezone


def date_expired_default():
    return timezone.now() + timezone.timedelta(days=365*70)

# def init_model():
#     for cls in [User, UserGroup]:
#         if getattr(cls, 'initial'):
#             cls.initial()
#
#
# def generate_fake():
#     for cls in [User, UserGroup]:
#         if getattr(cls, 'generate_fake'):
#             cls.generate_fake()
