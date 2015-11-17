=====
Django Model History
=====

The package is designed to track changes in object models. It has the ability to roll back changes to the object and attempt to restore an object if it has been deleted.
If the change of the object were conducted script or from the console, the user field will be empty.

=====
Quick start
=====
0. Install::

    pip install django-model-history2

1. Add in INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'model_history'
    )

3. Make migrate::

    python manage.py migrate model_history

4. Add decorator model_hisotry to your Model class:

.. code-block:: python

    from model_history.decorators import model_history

    @model_history()
    class SomeModel(models.Model):
        field_one = models.CharField()
        last_modified = models.DateTimeField()


=====
Arguments for decorator model_history
=====
1. ``exclude`` - Exclude fields. Default: []::

    @model_hisotry(exclude=['last_modified'])

2. ``related`` - Track all related models. Default: False::

    @model_history(exclude=['last_modified'], related=True)

3. ``related_exclude`` - Exclude for related models. По-умолчанию []::

    @model_history(exclude=['last_modified'], related=True, related_exclude=['myapp.models.Model2'])

=====
Settings
=====
1. The settings are defined in the dictionary named ``MODEL_HISTORY_SETTINGS``::

    MODEL_HISTORY_SETTINGS = {
        'connect': [
            {'model': 'django.contrib.auth.models.User', 'exclude': ['last_login'], 'related': True, 'related_exclude': ['django.contrib.admin.models.LogEntry']}
        ]
    }
2. Models are listed in parameter ``connect`` will be put on track, with the specified parameters.
3. ``delete_action`` - Should be in the admin interface function "delete selected objects". Default: False::

    MODEL_HISTORY_SETTINGS = {
        'delete_action': True
        'connect': [
            {'model': 'django.contrib.auth.models.User', 'exclude': ['last_login'], 'related': True, 'related_exclude': ['django.contrib.admin.models.LogEntry']}
        ]
    }
4. ``delete_permission`` - Which option is the user to check for compliance with the availability of the right to delete entries from the history::

    MODEL_HISTORY_SETTINGS = {
        'delete_action': True,
        'delete_permission': 'is_superuser',
        'connect': [
            {'model': 'django.contrib.auth.models.User', 'exclude': ['last_login'], 'related': True, 'related_exclude': ['django.contrib.admin.models.LogEntry']}
        ]
    }
5. ``revert_action`` - Should be in the admin function "Revert". This function tries to make changes or cancellation recover a deleted object from the dump. Default: True::

    MODEL_HISTORY_SETTINGS = {
        'delete_action': True,
        'delete_permission': 'is_superuser',
        'revert_action': True,
        'connect': [
            {'model': 'django.contrib.auth.models.User', 'exclude': ['last_login'], 'related': True, 'related_exclude': ['django.contrib.admin.models.LogEntry']}
        ]
    }
6. ``revert_permission`` - Which option is the user to check for compliance with the availability of rights to recovery facility::

    MODEL_HISTORY_SETTINGS = {
        'delete_action': True,
        'delete_permission': 'is_superuser',
        'revert_action': True,
        'revert_permission': 'is_superuser',
        'connect': [
            {'model': 'django.contrib.auth.models.User', 'exclude': ['last_login'], 'related': True, 'related_exclude': ['django.contrib.admin.models.LogEntry']}
        ]
    }