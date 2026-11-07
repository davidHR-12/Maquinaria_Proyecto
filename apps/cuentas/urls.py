from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import IniciarSesionView, RegistrarClienteView


app_name = "cuentas"

urlpatterns = [
    path('login/', IniciarSesionView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    path('registro/', RegistrarClienteView.as_view(), name='registro'),
]