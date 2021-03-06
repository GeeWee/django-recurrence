import pdb
import traceback

from django.db.models import fields
from django.utils.six import string_types
import recurrence
from recurrence import forms
from recurrence.compat import Creator

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [
        "^recurrence\.fields\.RecurrenceField",
    ])
except ImportError:
    pass


# Do not use SubfieldBase meta class because is removed in Django 1.10

class RecurrenceField(fields.Field):
    """Field that stores a `recurrence.base.Recurrence` to the database."""

    def __init__(self, include_dtstart=True, **kwargs):
        self.include_dtstart = include_dtstart
        super(RecurrenceField, self).__init__(**kwargs)

    def get_internal_type(self):
        return 'TextField'

    def to_python(self, value):
        print('topython', value)
        traceback.print_stack()
        if value is None or isinstance(value, recurrence.Recurrence):
            return value
        value = super(RecurrenceField, self).to_python(value) or u''
        return recurrence.deserialize(value, self.include_dtstart)

    def from_db_value(self, value, *args, **kwargs):
        print('fromdbvalue', value)
        if value == '':
            # Backwards compatible fix, for when we used to save empty recurrences as empty strings and not null
            return None
        return self.to_python(value)

    def get_prep_value(self, value):
        print('getprepval', value)
        if not isinstance(value, string_types):
            value = recurrence.serialize(value)
        return value

    def contribute_to_class(self, cls, *args, **kwargs):
        super(RecurrenceField, self).contribute_to_class(cls, *args, **kwargs)
        setattr(cls, self.name, Creator(self))

    def value_to_string(self, obj):
        return self.get_prep_value(self.value_from_object(obj))

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.RecurrenceField,
            'widget': forms.RecurrenceWidget,
        }
        defaults.update(kwargs)
        return super(RecurrenceField, self).formfield(**defaults)
