import importlib
import inspect
from django.conf import settings
from django.db.models.signals import pre_save, post_save, pre_delete

from .signals import check_update_fields, create_history, dump_object


def get_model_class(model_string):
    """
    Get Model Class from string.
    :param model_string: String by ModelClass
    :return: ModelClass
    """
    module_name = model_string.split(".")[:-1]
    module_name = ".".join(module_name)
    model_name = model_string.split(".")[-1:]
    model_name = ".".join(model_name)

    module = importlib.import_module(module_name)
    model = getattr(module, model_name)
    return model


def get_related_models(model):
    """
    Get all related models by model
    :param model: Model
    :return: list of Models
    """
    related_models = [rel.model for rel in model._meta.get_all_related_objects()]
    return related_models


def get_related_exclude(exclude):
    """
    Get list of exclude related models
    :param exclude: list of string
    :return: list of models
    """
    model_exclude = []
    for model_string in exclude:
        model = get_model_class(model_string)
        model_exclude.append(model)
    return model_exclude


def connect_signals(model, **kwargs):
    """
    Connected signals to Model
    :param model: Model
    :param kwargs: `exclude` - exclude fields
    :return: None
    """
    pre_save.connect(check_update_fields, model)
    post_save.connect(create_history, model)
    pre_delete.connect(dump_object, model)
    exclude = kwargs.get('exclude', [])
    if exclude:
        setattr(model, 'exclude', exclude)


def connect_signals_to_related(model, exclude=[]):
    """
    Connect signal to related models
    :param model: Model
    :return: None
    """
    related_models = get_related_models(model)
    related_exclude = get_related_exclude(exclude)
    for related_model in related_models:
        if not related_exclude or (related_exclude and related_model not in related_exclude):
            print(related_model)
            connect_signals(related_model)


def get_request():
    """
    Get request
    :return: request or None
    """
    frame = None
    try:
        for f in inspect.stack()[1:]:
            frame = f[0]
            code = frame.f_code
            if code.co_varnames and code.co_varnames[0] == 'request':
                return frame.f_locals['request']
    finally:
        del frame