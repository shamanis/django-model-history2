=====
Dajngo Model Hisotry
=====

Пакет предназначен для отслеживания изменений объектов моделей.

=====
Быстрый старт
=====
0. Устанавливаем пакет::

    pip install django-model-history

1. Добавляем его в INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'model_history'
    )

3. Выполняем миграцию::

    python manage.py migrate model_history

4. Добавляем декоратор model_hisotry к классу Вашей модели:

::

    from model_history.decorators import model_history

    @model_history()
    class SomeModel(models.Model):
        field_one = models.CharField()
        last_modified = models.DateTimeField()
