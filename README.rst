=====
Dajngo Model Hisotry
=====

Пакет предназначен для отслеживания изменений объектов моделей. Имеет возможность делать откат изменений объекта и попытку восстановить объект, если он был удален.
Если изменение объекта были проведены скриптом или из консоли, то поле user будет пустым.

=====
Быстрый старт
=====
0. Устанавливаем пакет::

    pip install django-model-history2

1. Добавляем его в INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'model_history'
    )

3. Выполняем миграцию::

    python manage.py migrate model_history

4. Добавляем декоратор model_hisotry к классу Вашей модели:

.. code-block:: python

    from model_history.decorators import model_history

    @model_history()
    class SomeModel(models.Model):
        field_one = models.CharField()
        last_modified = models.DateTimeField()


=====
Параметры декоратора model_history
=====
1. ``exclude`` - Принимет список названий полей, которын не нужно отслеживать. По-умолчани []::

    @model_hisotry(exclude=['last_modified'])

2. ``related`` - Отслеживать все модели, которы ссылаются на текущую. По-умолчанию False::

    @model_history(exclude=['last_modified'], related=True)

3. ``related_exclude`` - Список, связанных моделей, которые надо исключить из отслеживания. По-умолчанию []::

    @model_history(exclude=['last_modified'], related=True, related_exclude=['myapp.models.Model2'])

=====
Настройки в settings.py
=====
1. Настройки определяются в словаре с именем ``MODEL_HISTORY_SETTINGS``::

    MODEL_HISTORY_SETTINGS = {
        'connect': [
            {'model': 'django.contrib.auth.models.User', 'exclude': ['last_login'], 'related': True, 'related_exclude': ['django.contrib.admin.models.LogEntry']}
        ]
    }
2. Модели, перечисленные в параметре ``connect`` будут поставлены на отслеживание, с указанными параметрами
3. ``delete_action`` - Должна ли в админке быть функция "удалить выбранные объекты". По-умолчанию False::

    MODEL_HISTORY_SETTINGS = {
        'delete_action': True
        'connect': [
            {'model': 'django.contrib.auth.models.User', 'exclude': ['last_login'], 'related': True, 'related_exclude': ['django.contrib.admin.models.LogEntry']}
        ]
    }
4. ``delete_permission`` - Какой параметр у пользователя праверять на соответствие наличия прав на удаление записей из истории::

    MODEL_HISTORY_SETTINGS = {
        'delete_action': True,
        'delete_permission': 'is_superuser',
        'connect': [
            {'model': 'django.contrib.auth.models.User', 'exclude': ['last_login'], 'related': True, 'related_exclude': ['django.contrib.admin.models.LogEntry']}
        ]
    }
5. ``revert_action`` - Должна ли быть в админке функция "восстановить объект". Эта функция пытается сделать отсену изменений либо восстановить удаленный объект из дампа. По-умолчанию True::

    MODEL_HISTORY_SETTINGS = {
        'delete_action': True,
        'delete_permission': 'is_superuser',
        'revert_action': True,
        'connect': [
            {'model': 'django.contrib.auth.models.User', 'exclude': ['last_login'], 'related': True, 'related_exclude': ['django.contrib.admin.models.LogEntry']}
        ]
    }
6. ``revert_permission`` - Какой параметр у пользователя праверять на соответствие наличия прав на восстановление объекта::

    MODEL_HISTORY_SETTINGS = {
        'delete_action': True,
        'delete_permission': 'is_superuser',
        'revert_action': True,
        'revert_permission': 'is_superuser',
        'connect': [
            {'model': 'django.contrib.auth.models.User', 'exclude': ['last_login'], 'related': True, 'related_exclude': ['django.contrib.admin.models.LogEntry']}
        ]
    }