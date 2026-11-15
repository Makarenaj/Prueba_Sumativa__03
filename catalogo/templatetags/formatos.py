from django import template
from catalogo.utils import formato_pesos

register = template.Library()

@register.filter
def pesos(valor):
    return formato_pesos(valor)