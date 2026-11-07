from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib import messages
from .models import Categoria, Maquinaria, Unidad
from .forms import CategoriaForm, MaquinariaIntegralForm

# --- Mixin de Permisos para el módulo de Inventario ---
class InventarioAdminRequiredMixin(UserPassesTestMixin):
    """Verifica que el usuario sea Administrador o Técnico (Tercero) para modificar el inventario."""
    def test_func(self):
        # Utiliza las propiedades que definiste en el UsuarioPersonalizado
        user = self.request.user
        return user.is_authenticated and (user.es_administrador or user.es_tercero)

# --- Vistas de Categorías ---
class CategoriaListaView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'inventario/categoria_lista.html'
    context_object_name = 'categorias'

class CategoriaCrearView(LoginRequiredMixin, InventarioAdminRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'inventario/categoria_form.html'
    success_url = reverse_lazy('inventario:categoria_lista')


# --- Vistas de Maquinaria / Unidad Física ---
class MaquinariaListaView(LoginRequiredMixin, ListView):
    model = Unidad
    template_name = 'inventario/maquinaria_lista.html' 
    context_object_name = 'unidades'
    
    def get_queryset(self):
        # Traemos la unidad junto con los datos de su maquinaria base
        queryset = Unidad.objects.select_related('maquinaria__categoria').all()
        
        # Capturar parámetros de la URL (GET)
        q = self.request.GET.get('q', '').strip()
        categoria_id = self.request.GET.get('categoria', '')
        estado = self.request.GET.get('estado', '')

        # Filtrar por texto (código, nombre del equipo, número de serie o marca)
        if q:
            queryset = queryset.filter(
                models.Q(maquinaria__codigo__icontains=q) |
                models.Q(maquinaria__nombre__icontains=q) |
                models.Q(numero_serie__icontains=q) |
                models.Q(maquinaria__marca__icontains=q)
            )
        
        # Filtrar por categoría
        if categoria_id:
            queryset = queryset.filter(maquinaria__categoria_id=categoria_id)
            
        # Filtrar por estado
        if estado:
            queryset = queryset.filter(estado=estado)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos las categorías y los estados disponibles al template para poblar los selectores
        context['categorias'] = Categoria.objects.all()
        context['estados'] = Unidad.ESTADOS
        # Mantener los valores actuales en el contexto para rellenar el formulario de filtros
        context['request_get'] = self.request.GET
        return context

class MaquinariaCrearView(LoginRequiredMixin, InventarioAdminRequiredMixin, CreateView):
    form_class = MaquinariaIntegralForm
    template_name = 'inventario/maquinaria_form.html'
    success_url = reverse_lazy('inventario:maquinaria_lista')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # En la creación no pasamos ninguna instancia de unidad
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'La maquinaria y unidad se registraron correctamente.')
        return super().form_valid(form)

class MaquinariaEditarView(LoginRequiredMixin, InventarioAdminRequiredMixin, UpdateView):
    model = Unidad
    form_class = MaquinariaIntegralForm
    template_name = 'inventario/maquinaria_form.html'
    success_url = reverse_lazy('inventario:maquinaria_lista')
    pk_url_kwarg = 'unidad_id' # Usaremos el ID de la unidad en la URL

    def get_object(self, queryset=None):
        return Unidad.objects.select_related('maquinaria').get(pk=self.kwargs.get(self.pk_url_kwarg))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Le pasamos la unidad al form en lugar de 'instance' (como pide nuestro form personalizado)
        kwargs.pop('instance', None)
        kwargs['unidad'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Los datos de la maquinaria se actualizaron correctamente.')
        return super().form_valid(form)

class MaquinariaDetalleView(LoginRequiredMixin, DetailView):
    model = Unidad
    template_name = 'inventario/maquinaria_detalle.html'
    context_object_name = 'unidad'
    pk_url_kwarg = 'unidad_id' # Coincide con el <int:unidad_id> de la URL

    def get_object(self, queryset=None):
        # Optimizamos trayendo la unidad, su maquinaria y la categoría en una sola consulta
        return Unidad.objects.select_related('maquinaria__categoria').get(pk=self.kwargs.get(self.pk_url_kwarg))