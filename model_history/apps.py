from django.apps import AppConfig
from django.conf import settings

from .utils import get_model_class, connect_signals, connect_signals_to_related

MODEL_HISTORY_SETTINGS = getattr(settings, 'MODEL_HISTORY_SETTINGS', {})


class ModelHistoryConfig(AppConfig):
    name = 'model_history'
    verbose_name = 'Model History'

    def ready(self):
        connect_models = MODEL_HISTORY_SETTINGS.get('connect', [])
        if connect_models:
            for connect in connect_models:
                model_string = connect.get('model')
                model = get_model_class(model_string)
                exclude = connect.get('exclude', [])
                connect_signals(model, exclude=exclude)

                related = connect.get('related', False)
                related_exclude = connect.get('related_exclude', [])
                if related:
                    connect_signals_to_related(model, exclude=related_exclude)

