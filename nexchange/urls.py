"""nexchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import django.contrib.auth.views as auth_views
import core.views
from core.models import Currency, Profile, Order
from core.forms import LoginForm

admin.site.register(Currency)
admin.site.register(Profile)
admin.site.register(Order)



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', core.views.main, name='main'),
    url(r'^order/$',  core.views.index_order, name='core.order'),
    url(r'^order/add/$', core.views.add_order),

    url(r'^profile/add$', core.views.user_registration, name='core.user_registration'),
    url(r'^profile/resendSMS/$',  core.views.resend_sms, name='core.resend_sms'),
    url(r'^profile/verifyPhone/$',  core.views.verify_phone, name='core.verify_phone'),    
    url(r'^profile/(?P<slug>[-\+\w\d]+)/$', core.views.UserUpdateView.as_view(), name='core.user_profile'),
    
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'core/user_login.html', 'authentication_form': LoginForm}, name='accounts.login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='accounts.logout'),       
    # asking for passwd reset
    url(r'^accounts/password/reset/$', auth_views.password_reset, {'post_reset_redirect' : '/accounts/password/reset/done/'}, name="accounts.password_reset"),
    # passwd reset e-mail sent
    url(r'^accounts/password/reset/done/$', auth_views.password_reset_done),
    # paswd reset url with sent via e-mail
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'post_reset_redirect' : '/accounts/password/done/'}, name='accounts.password_reset_confirm'),
    # after saved the new passwd
    url(r'^accounts/password/done/$', auth_views.password_reset_complete),
    
]
