from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core import serializers


class History(models.Model):
    created_date = models.DateTimeField(_('created date'), default=timezone.now)
    user = models.CharField(_('user'), max_length=255, blank=True, null=True)
    model = models.CharField(_('model'), max_length=255)
    object = models.CharField(_('object'), max_length=255)

    TYPE_CREATE = 0
    TYPE_UPDATE = 1
    TYPE_DELETE = 2
    TYPES = (
        (TYPE_CREATE, _('Create')),
        (TYPE_UPDATE, _('Update')),
        (TYPE_DELETE, _('Delete'))
    )
    type = models.PositiveSmallIntegerField(_('type'), choices=TYPES)

    STATUS_NEW = 0
    STATUS_REVERTED = 1
    STATUSES = (
        (STATUS_NEW, _('New')),
        (STATUS_REVERTED, _('Revert'))
    )
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUSES, default=STATUS_NEW)
    field = models.CharField(_('field'), max_length=255, blank=True, null=True)
    old_value = models.TextField(_('old value'), blank=True, null=True)
    new_value = models.TextField(_('new value'), blank=True, null=True)
    dump = models.TextField(_('object dump'), blank=True, null=True)

    class Meta:
        verbose_name = _('model\'s history')
        verbose_name_plural = _('history of models')
        ordering = ['-created_date']

    def __str__(self):
        return self.object

    def clean(self):
        validation_errors = {}
        if self.type == self.TYPE_UPDATE and not self.field:
            validation_errors['field'] = ValidationError(_('Field `field` ca not be null if `status` TYPE_UPDATE'))

        if validation_errors:
            raise ValidationError(validation_errors)

    @classmethod
    def add(cls, model, object, type, **kwargs):
        from .utils import get_request

        try:
            _model = '%s.%s' % (model.__module__, model.__name__)
        except AttributeError:
            _model = model.__name__
        finally:
            model = _model

        request = get_request()
        if request:
            if request.user.is_authenticated():
                kwargs.update({
                    'user': request.user.pk
                })
        h = cls(model=model, object=object.pk, **kwargs)
        h.type = type
        h.save()
        return h

    def get_object(self):
        from .utils import get_model_class

        model = get_model_class(self.model)
        try:
            _object = model.objects.get(pk=self.object)
        except model.DoesNotExist:
            return None

        return _object

    def revert(self):
        if self.type == self.TYPE_DELETE:
            return self.restore()
        elif self.type == self.TYPE_UPDATE:
            _object = self.get_object()
            object_field = getattr(_object, self.field)
            if object_field == self.new_value:
                setattr(_object, self.field, self.old_value)
                _object.save()
                self.status = self.STATUS_REVERTED
                self.save()
                return True
        return False

    def restore(self):
        if self.dump:
            for obj in serializers.deserialize("json", self.dump):
                obj.save()
                self.status = self.STATUS_REVERTED
                self.save()
                return True
        return False


