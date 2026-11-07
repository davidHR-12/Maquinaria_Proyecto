import re
from django.core.exceptions import ValidationError

ESPACIOS_CEDULA = [' ', '\t', '\n', '\r', '\xa0']

def validar_cedula(valor):
    """
    Valida que la cédula tenga 11 dígitos y cumpla con el algoritmo 
    oficial de la Junta Central Electoral de la República Dominicana.
    """
    digitos = re.sub(r'\D', '', valor or '')
    if len(digitos) != 11:
        raise ValidationError('La cédula debe tener exactamente 11 dígitos.')
    if len(set(digitos)) == 1:
        raise ValidationError('Ingresa un número de cédula válido.')

    suma = 0
    for digito, peso in zip(digitos[:10], (1, 2) * 5):
        producto = int(digito) * peso
        suma += producto - 9 if producto > 9 else producto
    
    if (10 - suma % 10) % 10 != int(digitos[10]):
        raise ValidationError('El número de cédula no es válido. Revísalo e inténtalo de nuevo.')

    return f'{digitos[:3]}-{digitos[3:10]}-{digitos[10]}'