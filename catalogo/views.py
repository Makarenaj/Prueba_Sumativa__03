from django.shortcuts import render
from .models import Comic, Editorial


def catalogo(request):
    comics = Comic.objects.filter(disponible=True).select_related('editorial')
    q = request.GET.get('q', '').strip()
    editorial_id = request.GET.get('editorial', '')

    if q:
        comics = comics.filter(titulo__icontains=q)
    if editorial_id:
        comics = comics.filter(editorial_id=editorial_id)

    return render(request, 'catalogo/catalogo.html', {
        'comics': comics,
        'editoriales': Editorial.objects.all(),
        'q': q,
        'editorial_id': editorial_id,
    })