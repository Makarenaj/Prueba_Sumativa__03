from django.db import models


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