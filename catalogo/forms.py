import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Reserva


def validar_rut(valor):
    rut = valor.replace('.', '').replace('-', '').upper().strip()
    if not re.fullmatch(r'\d{7,8}[0-9K]', rut):
        raise ValidationError('Formato de RUT inválido. Ejemplo: 12.345.678-5')
    cuerpo, dv = rut[:-1], rut[-1]
    suma, mult = 0, 2
    for digito in reversed(cuerpo):
        suma += int(digito) * mult
        mult = 2 if mult == 7 else mult + 1
    resto = 11 - (suma % 11)
    esperado = '0' if resto == 11 else 'K' if resto == 10 else str(resto)
    if dv != esperado:
        raise ValidationError('El dígito verificador del RUT es incorrecto.')
    return f"{int(cuerpo):,}".replace(",", ".") + "-" + dv


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre', 'correo', 'rut', 'cantidad']

    def __init__(self, *args, comic=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.comic = comic  # el modelo usa el cómic para validar stock

    def clean_rut(self):
        return validar_rut(self.cleaned_data['rut'])