# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# #
#
# from __future__ import unicode_literals
#
# from django.db import models
#
# from django.utils.translation import ugettext_lazy as _
#
# __all__ = ['UserGroup']
#
#
# class UserGroup(models.Model):
#     name = models.CharField(max_length=128, verbose_name=_('Name'))
#     comment = models.TextField(blank=True, verbose_name=_('Comment'))
#     date_created = models.DateTimeField(auto_now_add=True, null=True,
#                                         verbose_name=_('Date created'))
#     created_by = models.CharField(max_length=100)
#
#     def __unicode__(self):
#         return self.name
#     __str__ = __unicode__
#
#
