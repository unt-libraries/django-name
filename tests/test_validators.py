import pytest
from name.models import validate_merged_with, Name
from django.core.exceptions import ValidationError


@pytest.fixture
def merge_candidates(db):
    """Fixture setup to for testing merged validators."""
    primary = Name.objects.create(name='Primary', name_type=0)
    secondary = Name.objects.create(name='Secondary', name_type=0)
    return (primary, secondary)


@pytest.mark.django_db
def test_validate_merged_with_passes(merge_candidates):
    primary, secondary = merge_candidates
    # We will not assert here because failure will raise
    # an exception and cause a failure. Passing validation
    # returns nothing and the test passes.
    validate_merged_with(primary.id)


@pytest.mark.django_db
def test_validate_merged_with_fails(merge_candidates):
    """Tests validate_merged_with_fails.

    This should fail when attempting to circularly merge Names.
    Example: Name1 -> Name2, Name2 -> Name1.
    """
    primary, secondary = merge_candidates

    secondary.merged_with = primary
    primary.merged_with = secondary

    secondary.save()
    primary.save()

    with pytest.raises(ValidationError):
        validate_merged_with(primary.id)
