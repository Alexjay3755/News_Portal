from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
   # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
   # подключались к главному приложению с префиксом products/.
    path('sign/', include('simpleapp.urls')),
    path('accounts/', include('allauth.urls')),

    path('', include('protect.urls')),
    path('', include('simpleapp.urls')),
    path('', include('sign.urls')),
    path('appointments/', include(('appointment.urls', 'appointments'), namespace='appointments')),
]