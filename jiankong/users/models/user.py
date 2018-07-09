#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os

from collections import OrderedDict

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.shortcuts import reverse

from .utils import date_expired_default

__all__ = ['User']


class User(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', _('超级用户')),
        ('User', _('普通用户')),
        ('Group', _('组长'))
    )

    username = models.CharField(max_length=20, unique=True, verbose_name=_('用户名'))
    name = models.CharField(max_length=20, verbose_name=_('姓名'))
    role = models.CharField(choices=ROLE_CHOICES, default='User', max_length=10, blank=True, verbose_name=_('角色'))
    date_expired = models.DateTimeField(default=date_expired_default, blank=True, null=True,
                                        verbose_name=_('过期时间'))
    created_by = models.CharField(max_length=30, default='', verbose_name=_('创建者'))
    about_relation = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name="group_member", verbose_name=_('组长'))
    has_asset = models.BooleanField(default=False, verbose_name='是否拥有资产')

    @property
    def password_raw(self):
        raise AttributeError('Password raw is not a readable attribute')

    #: Use this attr to set user object password, example
    #: user = User(username='example', password_raw='password', ...)
    #: It's equal:
    #: user = User(username='example', ...)
    #: user.set_password('password')
    @password_raw.setter
    def password_raw(self, password_raw_):
        self.set_password(password_raw_)

    def get_absolute_url(self):
        return reverse('users:user-detail', args=(self.id,))

    @property
    def is_expired(self):
        if self.date_expired and self.date_expired < timezone.now():
            return True
        else:
            return False

    @property
    def is_valid(self):
        if self.is_active and not self.is_expired:
            return True
        return False

    @property
    def is_superuser(self):
        if self.role == 'Admin':
            return True
        else:
            return False

    @is_superuser.setter
    def is_superuser(self, value):
        if value is True:
            self.role = 'Admin'
        else:
            self.role = 'Group'

    @property
    def is_group_leader(self):
        if self.role == 'Group':
            return True
        else:
            return False

    @property
    def is_user(self):
        return self.role == 'User'

    @property
    def is_staff(self):
        if self.is_authenticated and self.is_valid:
            return True
        else:
            return False

    @is_staff.setter
    def is_staff(self, value):
        pass

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.username

        super(User, self).save(*args, **kwargs)

    # @property
    # def private_token(self):
    #     return self.create_private_token()

    # def create_private_token(self):
    #     from .authentication import PrivateToken
    #     try:
    #         token = PrivateToken.objects.get(user=self)
    #     except PrivateToken.DoesNotExist:
    #         token = PrivateToken.objects.create(user=self)
    #     return token.key

    # def refresh_private_token(self):
    #     from .authentication import PrivateToken
    #     PrivateToken.objects.filter(user=self).delete()
    #     return PrivateToken.objects.create(user=self)

    # def generate_reset_token(self):
    #     return signer.sign_t({'reset': self.id, 'email': self.email}, expires_in=3600)

    def to_json(self):
        return OrderedDict({
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser,
            'role': self.get_role_display(),
            'date_expired': self.date_expired.strftime('%Y-%m-%d %H:%M:%S')
        })

    # @classmethod
    # def validate_reset_token(cls, token):
    #     try:
    #         data = signer.unsign_t(token)
    #         user_id = data.get('reset', None)
    #         user = cls.objects.get(id=user_id)
    #
    #     except (signing.BadSignature, cls.DoesNotExist):
    #         user = None
    #     return user

    def reset_password(self, new_password):
        self.set_password(new_password)
        self.save()

    def delete(self):
        if self.pk == 1 or self.username == 'admin':
            return
        return super(User, self).delete()

    class Meta:
        ordering = ['username']

    # : Use this method initial user
    @classmethod
    def initial(cls):
        user = cls(username='admin',
                   name=_('Administrator'),
                   password_raw='admin',
                   role='Admin',
                   created_by=_('System'))
        user.save()

    # @classmethod
    # def generate_fake(cls, count=100):
    #     from random import seed, choice
    #     import forgery_py
    #     from django.db import IntegrityError
    #
    #     seed()
    #     for i in range(count):
    #         user = cls(username=forgery_py.internet.user_name(True),
    #                    name=forgery_py.name.full_name(),
    #                    password=make_password(forgery_py.lorem_ipsum.word()),
    #                    role=choice(dict(User.ROLE_CHOICES).keys()),
    #                    created_by=choice(cls.objects.all()).username)
    #         try:
    #             user.save()
    #         except IntegrityError:
    #             print('Duplicate Error, continue ...')
    #             continue
    #         user.save()
