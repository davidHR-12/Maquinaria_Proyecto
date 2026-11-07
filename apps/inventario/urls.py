from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Categorías
    path('categorias/', views.CategoriaListaView.as_view(), name='categoria_lista'),
    path('categorias/nuevo/', views.CategoriaCrearView.as_view(), name='categoria_crear'),
    
    # Maquinarias
    path('maquinarias/', views.MaquinariaListaView.as_view(), name='maquinaria_lista'),
    path('maquinarias/nuevo/', views.MaquinariaCrearView.as_view(), name='maquinaria_crear'),
]