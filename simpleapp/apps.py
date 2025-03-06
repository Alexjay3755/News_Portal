from django.apps import AppConfig


class SimpleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simpleapp'


    # # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import simpleapp.signals
