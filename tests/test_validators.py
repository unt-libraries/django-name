import pytest
from name.validators import validate_merged_with
from name.models import Name
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_validate_merged_with_passes_without_merged_with():
    name = Name.objects.create(name='John Smith', name_type=0)
    validate_merged_with(name)


@pytest.mark.django_db
def test_validate_merged_with_fails_with_unsaved_name():
    name = Name.objects.create(name='John Smith', name_type=0)
    not_saved = Name(id=13, name='John Doe', name_type=0)

    name.merged_with = not_saved

    with pytest.raises(ValidationError):
        validate_merged_with(name)


@pytest.mark.django_db
def test_validate_merged_with_passes():
    john = Name.objects.create(name='John Smith', name_type=0)
    jane = Name.objects.create(name='Jane Doe', name_type=0)

    jane.merged_with = john

    validate_merged_with(jane)


@pytest.mark.django_db
def test_validate_merged_with_fails():
    """Checks that validate_merged_with fails.

    This should fail when attempting to circularly merge Names.
    Example: Name1 -> Name2, Name2 -> Name1.
    """
    john = Name.objects.create(name='John Smith', name_type=0)
    jane = Name.objects.create(name='Jane Doe', name_type=0)

    jane.merged_with = john
    john.merged_with = jane

    jane.save()

    with pytest.raises(ValidationError):
        validate_merged_with(john)


@pytest.mark.django_db
def test_validate_merged_with_fails_when_name_merges_with_itself():
    """Check that validate_merged_with fails when we try to merge
    a name into itself.
    """
    name = Name.objects.create(name='John Smith', name_type=0)

    name.merged_with = name
    name.save()

    with pytest.raises(ValidationError):
        validate_merged_with(name)


@pytest.mark.django_db
def test_validate_merged_with_when_name_changed_merged_with_to_new_name():
    """Check that validation does not alter when a name has a
    merged_with model, but is then changed to another name instance.
    """
    john = Name.objects.create(name='John Smith', name_type=0)
    jane = Name.objects.create(name='Jane Doe', name_type=0)
    ben = Name.objects.create(name='Ben Willis', name_type=0)

    john.merged_with = jane
    john.save()

    validate_merged_with(john)

    john.merged_with = ben
    john.save()

    validate_merged_with(john)


@pytest.mark.django_db
def test_validate_merged_with_when_name_changed_merged_with_to_invalid_name():
    """Check that validation if a valid merged_with related model is
    changed to an invalid related model.
    """
    john = Name.objects.create(name='John Smith', name_type=0)
    jane = Name.objects.create(name='Jane Doe', name_type=0)
    ben = Name(id=31, name='Ben Willis', name_type=0)

    john.merged_with = jane
    john.save()

    validate_merged_with(john)

    john.merged_with = ben

    with pytest.raises(ValidationError):
        validate_merged_with(john)


@pytest.mark.django_db
def test_validate_merged_with_fails_with_more_than_two_names():
    """Checks that a merge loop constisting of more than two name
    also fails validation.
    """
    john = Name.objects.create(name='John Smith', name_type=0)
    jane = Name.objects.create(name='Jane Doe', name_type=0)
    ben = Name.objects.create(name='Ben Willis', name_type=0)

    jane.merged_with = john
    jane.save()

    ben.merged_with = jane
    ben.save()

    john.merged_with = ben
    john.save()

    with pytest.raises(ValidationError):
        validate_merged_with(john)
