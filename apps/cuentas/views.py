from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistroClienteForm

class IniciarSesionView(LoginView):
    """
    Vista de inicio de sesión personalizada. 
    Como configuramos USERNAME_FIELD = 'email', Django autenticará automáticamente 
    usando el correo electrónico.
    """
    template_name = 'cuentas/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # Redirige a la página principal o al panel según prefieras
        return reverse_lazy('inicio')


class RegistrarClienteView(CreateView):
    """
    Vista encargada del registro público de nuevos clientes.
    """
    form_class = RegistroClienteForm
    template_name = 'cuentas/registro.html'
    success_url = reverse_lazy('login')