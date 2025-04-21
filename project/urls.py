from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from education import views


# router = routers.DefaultRouter()
# router.register(r'schools', views.SchoolViewset)
# router.register(r'classes', views.SClassViewset)
# router.register(r'students', views.StudentViewset)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('protect.urls')),
    path('', include('simpleapp.urls')),
    path('sign/', include('sign.urls')),
    path('', include('education.urls')),

]
