from pprint import pprint

from django.db import IntegrityError
from recurrence import Recurrence
from tests.models import EventWithNulls, EventWithNoNulls, EventWithNullAndBlank
import pytest


@pytest.mark.django_db
def test_recurs_can_be_explicitly_none_if_none_is_allowed():
    # Check we can save None correctly
    event = EventWithNulls.objects.create(recurs=None)
    assert event.recurs is None

    # Check we can deserialize None correctly
    reloaded = EventWithNulls.objects.get(pk=event.pk)
    assert reloaded.recurs is None


@pytest.mark.django_db
def test_recurs_cannot_be_explicitly_none_if_none_is_disallowed():
    with pytest.raises(IntegrityError):
        EventWithNoNulls.objects.create(recurs=None)


@pytest.mark.django_db
def test_recurs_can_be_empty_even_if_none_is_disallowed():
    event = EventWithNoNulls.objects.create(recurs=Recurrence())
    assert event.recurs == Recurrence()


@pytest.mark.django_db
def test_recurs_can_be_saved_and_retrieved_as_none_if_blank_and_null_set_to_true():
    # Can save this one, and it is returned as None
    event = EventWithNullAndBlank.objects.create()
    assert event.recurs is None
    event.refresh_from_db()
    assert event.recurs is None
    print(event.pk)

    # Can save this as well, and it is returned as None
    event = EventWithNullAndBlank.objects.create(recurs=None)
    assert event.recurs is None
    event.refresh_from_db()
    assert event.recurs is None


@pytest.mark.django_db
def test_recurs_errors_on_none_if_null_set_to_false():
    event = EventWithNoNulls.objects.create()

    # We should get an error
    pprint(event.__dict__)
    assert False
    assert event.recurs == Recurrence()

@pytest.mark.django_db
def test_recurs_can_be_saved_and_retrieved_as_none_if_null_set_to_true():
    event = EventWithNoNulls.objects.create()
    assert event.recurs == Recurrence()


@pytest.mark.django_db
def test_recurs_is_fetched_as_none_from_the_database_if_saved_as_empty_string_previously():
    event = EventWithNoNulls.objects.create(recurs=Recurrence())
    assert event.recurs == Recurrence()