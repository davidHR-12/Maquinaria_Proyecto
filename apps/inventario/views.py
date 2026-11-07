from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Categoria, Maquinaria
from .forms import CategoriaForm, MaquinariaForm

# --- Vistas de Categorías ---
class CategoriaListaView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'inventario/categoria_lista.html'
    context_object_name = 'categorias'


class CategoriaCrearView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'inventario/categoria_form.html'
    success_url = reverse_lazy('inventario:categoria_lista')


# --- Vistas de Maquinaria ---
class MaquinariaListaView(LoginRequiredMixin, ListView):
    model = Maquinaria
    template_name = 'inventario/maquinaria_lista.html'
    context_object_name = 'maquinarias'


class MaquinariaCrearView(LoginRequiredMixin, CreateView):
    model = Maquinaria
    form_class = MaquinariaForm
    template_name = 'inventario/maquinaria_form.html'
    success_url = reverse_lazy('inventario:maquinaria_lista')