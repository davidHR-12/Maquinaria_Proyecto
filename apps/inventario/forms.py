from django import forms
from .models import Categoria, Maquinaria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Grúas, Excavadoras, etc.'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Breve descripción de la categoría'}),
        }


class MaquinariaForm(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = [
            'categoria', 'codigo', 'nombre', 'marca', 'modelo',
            'costo_adquisicion', 'tarifa_diaria', 'tarifa_semanal',
            'tarifa_mensual', 'deposito_garantia', 'activo'
        ]
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. GRU-001'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre descriptivo del equipo'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Caterpillar, Komatsu'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 320D'}),
            'costo_adquisicion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tarifa_diaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tarifa_semanal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tarifa_mensual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'deposito_garantia': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }