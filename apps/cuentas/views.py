from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,TemplateView
from .forms import RegistroClienteForm
from .models import UsuarioPersonalizado

class IniciarSesionView(LoginView):
    """
    Vista de inicio de sesión personalizada. 
    Como configuramos USERNAME_FIELD = 'email', Django autenticará automáticamente 
    usando el correo electrónico.
    """
    template_name = 'cuentas/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('cuentas:dashboard')


class RegistrarClienteView(CreateView):
    """
    Vista encargada del registro público de nuevos clientes.
    """
    form_class = RegistroClienteForm
    template_name = 'cuentas/registro.html'
    success_url = reverse_lazy('cuentas:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Evaluamos si la tabla de usuarios está completamente vacía
        context['es_primer_usuario'] = not UsuarioPersonalizado.objects.exists()
        return context

class DashboardAdminView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/admin_index.html'
    login_url = 'cuentas:login'