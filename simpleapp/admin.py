from django.contrib import admin
from .models import Post, Author, Category, Comment, PostCategory



# напишем уже знакомую нам функцию обнуления товара на складе
def nullfy_rating(modeladmin, request,
                    queryset):  # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)


nullfy_rating.short_description = 'Обнулить рейтинг'  # описание для более понятного представления в админ панеле задаётся, как будто это объект


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title','type_post', 'text', 'time_in', 'rating')  # оставляем только имя и цену товара
    list_filter = ('title', 'category__name', 'type_post', 'rating')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'category__name')  # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_rating]  # добавляем действия в список

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostCategory)

