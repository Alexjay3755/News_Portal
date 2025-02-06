from django.db import models
from django.core.validators import MinValueValidator


# Товар для нашей витрины
class News(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,  # названия товаров не должны повторяться
    )
    text = models.TextField()

    time_in = models.DateTimeField(auto_now_add=True)

    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news',  # все продукты в категории будут доступны через поле products
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0)],
    )

    def __str__(self):
        return f'{self.name.title()}: {self.text[:20]}'


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()

