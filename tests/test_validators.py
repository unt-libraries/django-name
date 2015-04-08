import pytest
from name.models import validate_merged_with, Name
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_validate_merged_with_fails_with_unknown_id():
    with pytest.raises(ValidationError):
        validate_merged_with(1)


@pytest.mark.django_db
def test_validate_merged_with_passes():
    primary = Name.objects.create(name='Primary', name_type=0)
    secondary = Name.objects.create(name='Secondary', name_type=0)

    secondary.merged_with = primary
    secondary.save()

    validate_merged_with(secondary.id)


@pytest.mark.django_db
def test_validate_merged_with_fails():
    """Checks that validate_merged_with fails.

    This should fail when attempting to circularly merge Names.
    Example: Name1 -> Name2, Name2 -> Name1.
    """
    primary = Name.objects.create(name='Primary', name_type=0)
    secondary = Name.objects.create(name='Secondary', name_type=0)

    secondary.merged_with = primary
    primary.merged_with = secondary

    secondary.save()
    primary.save()

    with pytest.raises(ValidationError):
        validate_merged_with(primary.id)


@pytest.mark.django_db
def test_validate_merged_with_fails_when_name_merges_with_itself():
    """Check that validate_merged_with fails when we try to merge
    a name into itself.
    """
    name = Name.objects.create(name='Primary', name_type=0)

    name.merged_with = name
    name.save()

    with pytest.raises(ValidationError):
        validate_merged_with(name.id)


@pytest.mark.django_db
def test_validate_merged_with_fails_with_more_than_two_names():
    """Checks that a merge loop constisting of more than two name
    also fails validation.
    """
    primary = Name.objects.create(name='Primary', name_type=0)
    second = Name.objects.create(name='Second', name_type=0)
    third = Name.objects.create(name='Third', name_type=0)

    second.merged_with = primary
    second.save()

    third.merged_with = second
    third.save()

    primary.merged_with = third
    primary.save()

    with pytest.raises(ValidationError):
        validate_merged_with(primary.id)
