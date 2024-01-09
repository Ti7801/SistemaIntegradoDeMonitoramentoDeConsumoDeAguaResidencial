from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('loginAdministrador/', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls')),
    path('', include('InterfaceWeb.urls'))
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
