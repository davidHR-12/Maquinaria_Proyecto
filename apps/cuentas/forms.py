from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado, PerfilCliente
from .validators import validar_cedula

class RegistroClienteForm(UserCreationForm):
    """
    Formulario de registro para nuevos clientes que captura correo, 
    teléfono, nombre, apellido, cédula y contraseña.
    """
    first_name = forms.CharField(
        label='Nombre',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'})
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nombre@correo.com'})
    )
    telefono = forms.CharField(
        label='Teléfono',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(809) 000-0000'})
    )
    cedula = forms.CharField(
        label='Cédula de identidad',
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000-0000000-0'})
    )

    class Meta(UserCreationForm.Meta):
        model = UsuarioPersonalizado
        fields = ('first_name', 'last_name', 'email', 'telefono')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        # Validamos usando la función oficial dominicana
        return validar_cedula(cedula)

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Comprobamos si es el primer usuario registrado en todo el sistema
        if not UsuarioPersonalizado.objects.exists():
            user.rol = 'Administrador'
            user.is_staff = True
            user.is_superuser = True
        else:
            user.rol = 'Cliente'
            
        if commit:
            user.save()
            # Solo creamos el PerfilCliente si es un usuario común (Cliente)
            if user.rol == 'Cliente':
                PerfilCliente.objects.create(
                    usuario=user,
                    cedula=self.cleaned_data.get('cedula')
                )
        return user