import uuid
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.db.models import F


class Editorial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Editoriales'

    def __str__(self):
        return self.nombre


class Comic(models.Model):
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE, related_name='comics')
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    portada = models.ImageField(upload_to='portadas/')
    precio = models.PositiveIntegerField(help_text='Precio en pesos chilenos')
    tomo = models.PositiveIntegerField(default=1)
    tapa_dura = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cómic'
        verbose_name_plural = 'Cómics'

    def __str__(self):
        return f"{self.titulo} (Tomo {self.tomo})"

class Reserva(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='reservas')
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    rut = models.CharField(max_length=12)
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    fecha = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=10, unique=True, editable=False, blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def total(self):
        return self.comic.precio * self.cantidad

    def clean(self):
        # Control de stock (sirve para el sitio y para el admin)
        if self.comic_id and self.cantidad and self._state.adding:
            if self.cantidad > self.comic.stock:
                raise ValidationError({
                    'cantidad': f'Solo hay {self.comic.stock} ejemplar(es) disponible(s).'
                })

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.codigo:
                self.codigo = uuid.uuid4().hex[:8].upper()
            with transaction.atomic():
                Comic.objects.filter(pk=self.comic_id).update(stock=F('stock') - self.cantidad)
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
