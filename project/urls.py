from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('protect.urls')),
    path('', include('simpleapp.urls')),
    path('sign/', include('sign.urls')),
    path('appointments/', include(('appointment.urls', 'appointments'), namespace='appointments')),

]