# ~*~ coding: utf-8 ~*~

from __future__ import unicode_literals

from urllib import parse

# from django import forms
# from django.contrib import auth
# from django.contrib.auth.backends import ModelBackend
# from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import reverse, redirect
from django.utils.decorators import method_decorator
# from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
# from django.views.decorators.http import require_POST
# from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView, View
# from django.conf import settings

# from common.utils import get_object_or_none, crypt
# from requests import Response
# from record.utils import save_record

# from ..models import User
# from ..hands import write_login_log_async
from .. import forms


__all__ = ['doorLogin', 'UserLoginView']  #, 'UserLogoutView', 'UserForgotPasswordSendmailSuccessView',
           # 'UserResetPasswordView', 'UserResetPasswordSuccessView',
           # 'UserFirstLoginView']


def crypt(source,key):
    from itertools import cycle
    result = ''
    temp = cycle(key)
    for ch in source:
        result = result + chr(ord(ch) ^ ord(next(temp)))
    return result


def doorLogin(request, token):
    if request.method == 'GET':
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # print('000000000000000000000' + token)
        token = parse.unquote(token)
        # print(token)
        sec = crypt(token, "12345678")
        user = authenticate(username=sec.split('&')[0], password=sec.split('&')[1])

        if user is not None:
            auth_login(request, user)
            # save_record('登录', '系统', request.user)
            return redirect("/index/")
            # res = JsonResponse({"errcode": 1, "url": "/website/index/", "msg": "登陆成功"})
            # res.__setitem__('Access-Control-Allow-Origin', '*')
            # return res
        else:
            return JsonResponse({"errcode": 0, "msg": "用户或密码错误"})


@method_decorator(sensitive_post_parameters(), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = forms.UserLoginForm
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect(self.get_success_url())
        return super(UserLoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        # login_ip = self.request.META.get('REMOTE_ADDR', '')
        # user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        # write_login_log_async.delay(self.request.user.username,
        #                             self.request.user.name,
        #                             login_type='W', login_ip=login_ip,
        #                             user_agent=user_agent)
        # save_record('登录', '系统', self.request.user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        # if self.request.user.is_first_login:
        #     return reverse('users:user-first-login')

        return self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, reverse('index')))


# class UserForgotPasswordView(TemplateView):
#     template_name = 'users/forgot_password.html'
#
#     def post(self, request):
#         email = request.POST.get('email')
#         user = get_object_or_none(User, email=email)
#         if not user:
#             return self.get(request, errors=_('Email address invalid, '
#                                               'please input again'))
#         else:
#             send_reset_password_mail(user)
#             return HttpResponseRedirect(
#                 reverse('users:forgot-password-sendmail-success'))
#
#
# class UserForgotPasswordSendmailSuccessView(TemplateView):
#     template_name = 'flash_message_standalone.html'
#
#     def get_context_data(self, **kwargs):
#         context = {
#             'title': _('Send reset password message'),
#             'messages': _('Send reset password mail success, '
#                           'login your mail box and follow it '),
#             'redirect_url': reverse('users:login'),
#         }
#         kwargs.update(context)
#         return super(UserForgotPasswordSendmailSuccessView, self)\
#             .get_context_data(**kwargs)
#
#
# class UserResetPasswordSuccessView(TemplateView):
#     template_name = 'flash_message_standalone.html'
#
#     def get_context_data(self, **kwargs):
#         context = {
#             'title': _('Reset password success'),
#             'messages': _('Reset password success, return to login page'),
#             'redirect_url': reverse('users:login'),
#             'auto_redirect': True,
#         }
#         kwargs.update(context)
#         return super(UserResetPasswordSuccessView, self)\
#             .get_context_data(**kwargs)
#
#
# class UserResetPasswordView(TemplateView):
#     template_name = 'users/reset_password.html'
#
#     def get(self, request, *args, **kwargs):
#         token = request.GET.get('token')
#         user = User.validate_reset_token(token)
#
#         if not user:
#             kwargs.update({'errors': _('Token invalid or expired')})
#         return super(UserResetPasswordView, self).get(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         password = request.POST.get('password')
#         password_confirm = request.POST.get('password-confirm')
#         token = request.GET.get('token')
#
#         if password != password_confirm:
#             return self.get(request, errors=_('Password not same'))
#
#         user = User.validate_reset_token(token)
#         if not user:
#             return self.get(request, errors=_('Token invalid or expired'))
#
#         user.reset_password(password)
#         return HttpResponseRedirect(reverse('users:reset-password-success'))
#
#
# class UserFirstLoginView(LoginRequiredMixin, SessionWizardView):
#     template_name = 'users/first_login.html'
#     form_list = [forms.UserProfileForm, forms.UserPublicKeyForm]
#     file_storage = default_storage
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated():  # and not request.user.is_first_login
#             return redirect(reverse('index'))
#         return super(UserFirstLoginView, self).dispatch(request, *args, **kwargs)
#
#     def done(self, form_list, **kwargs):
#         user = self.request.user
#         for form in form_list:
#             for field in form:
#                 if field.value():
#                     setattr(user, field.name, field.value())
#                 if field.name == 'enable_otp':
#                     user.enable_otp = field.value()
#         # user.is_first_login = False
#         # user.is_public_key_valid = True
#         user.save()
#         context = {
#             'user_guide_url': settings.CONFIG.USER_GUIDE_URL
#         }
#         return render(self.request, 'users/first_login_done.html', context)
#
#     def get_context_data(self, **kwargs):
#         context = super(UserFirstLoginView, self).get_context_data(**kwargs)
#         context.update({'app': _('Users'), 'action': _('First login')})
#         return context
#
#     def get_form_initial(self, step):
#         user = self.request.user
#         if step == '0':
#             return {
#                 'username': user.username or '',
#                 'name': user.name or user.username,
#                 'email': user.email or '',
#                 'wechat': user.wechat or '',
#                 'phone': user.phone or ''
#             }
#         return super(UserFirstLoginView, self).get_form_initial(step)
#
#     def get_form(self, step=None, data=None, files=None):
#         form = super(UserFirstLoginView, self).get_form(step, data, files)
#
#         form.instance = self.request.user
#         return form
