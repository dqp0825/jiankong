from __future__ import absolute_import

from django.conf.urls import url

from .. import views

app_name = 'users'

urlpatterns = [
    # Login view
    url(r'^doorlogin/([^/:]+)/$', views.login.doorLogin, name='doorlogin'),
    url(r'^login$', views.UserLoginView.as_view(), name='login'),
    # url(r'^logout$', views.UserLogoutView.as_view(), name='logout'),
    # url(r'^password/forgot$', views.UserForgotPasswordView.as_view(),
    #     name='forgot-password'),
    # url(r'^password/forgot/sendmail-success$',
    #     views.UserForgotPasswordSendmailSuccessView.as_view(),
    #     name='forgot-password-sendmail-success'),
    # url(r'^password/reset$', views.UserResetPasswordView.as_view(),
    #     name='reset-password'),
    # url(r'^password/reset/success$',
    #     views.UserResetPasswordSuccessView.as_view(),
    #     name='reset-password-success'),
]
