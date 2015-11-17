from django.core import serializers

from .models import History


def check_update_fields(sender, instance, **kwargs):
    if instance.pk:
        exclude = getattr(instance, 'exclude', None)
        try:
            orig = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return

        for field in instance._meta.fields:
            orig_value = getattr(orig, field.name)
            new_value = getattr(instance, field.name)
            if orig_value != new_value:
                if not exclude or (exclude and field.name not in exclude):
                    if not hasattr(instance, 'update_fields'):
                        setattr(instance, 'update_fields', [])
                        instance.update_fields.append(field.name)
                        setattr(instance, '_orig_%s' % field.name, orig_value)


def create_history(sender, instance, created, **kwargs):
    if not created:
        if hasattr(instance, 'update_fields'):
            for field in instance.update_fields:
                old_value = getattr(instance, '_orig_%s' % field)
                new_value = getattr(instance, '%s' % field)
                History.add(sender, instance, History.TYPE_UPDATE,
                            field=field, old_value=old_value, new_value=new_value)
    else:
        dump = serializers.serialize("json", [instance])
        History.add(sender, instance, History.TYPE_CREATE, dump=dump)



def dump_object(sender, instance, **kwargs):
    dump = serializers.serialize("json", [instance])
    History.add(sender, instance, History.TYPE_DELETE, dump=dump)
