from .utils import connect_signals, connect_signals_to_related


def model_history(exclude=[], **options):
    if not isinstance(exclude, list) and not isinstance(exclude, tuple):
        raise TypeError('Argument `exclude` must be list or tuple')

    def decorator(cls):
        connect_signals(cls, exclude=exclude)

        related = options.get('related', False)
        related_exclude = options.get('related_exclude', [])
        if related:
            connect_signals_to_related(cls, exclude=related_exclude)

        return cls
    return decorator
