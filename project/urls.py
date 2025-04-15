from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('protect.urls')),
    path('', include('simpleapp.urls')),
    path('sign/', include('sign.urls')),
    # path('', include('basic.urls'))

]