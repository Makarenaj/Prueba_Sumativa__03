from django.shortcuts import render
from .models import Comic, Editorial


def catalogo(request):
    comics = Comic.objects.filter(disponible=True).select_related('editorial')
    return render(request, 'catalogo/catalogo.html', {'comics': comics})