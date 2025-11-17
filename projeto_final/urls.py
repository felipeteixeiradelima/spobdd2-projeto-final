from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),       # homepage, campanhas públicas
    path('', include('accounts.urls')),  # login, cadastro
]
