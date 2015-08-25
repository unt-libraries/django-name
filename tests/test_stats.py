import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from name.api import stats
from name.models import Name

# Give all tests access to the database.
pytestmark = pytest.mark.django_db


class TestNameStatisticsType:

    def test_get_queryset_members_returns_none_with_empty_queryset(self):
        """Check the behaviour of get_queryset_member when no objects
        are contained in the queryset passed to NameStatisticsType.

        The generator is expected to raise a StopIteration upon
        the first call of next().
        """
        name_stats = stats.NameStatisticsType(Name.objects.created_stats())
        result = name_stats.get_queryset_members()

        with pytest.raises(StopIteration):
            next(result)

    def test_get_queryset_members_with_names_created_in_current_month(self):
        Name.objects.create(name="John Smith", name_type=Name.PERSONAL)
        name_stats = stats.NameStatisticsType(Name.objects.created_stats())
        gen = name_stats.get_queryset_members()

        expected_month = timezone.now().replace(day=1, hour=0, minute=0,
                                                second=0, microsecond=0)

        result = next(gen)
        assert result['count'] == 1
        assert result['month'] == expected_month

    def test_get_queryset_members_with_no_names_created_in_current_month(self):
        """Check that get_queryset_members generates the correct data
        when the queryset is empty but the generator has not yet raised
        a StopIteration.
        """
        now = timezone.now()
        date_created = now - relativedelta(months=5)
        current_month = now.replace(day=1, hour=0, minute=0, second=0,
                                    microsecond=0)

        name = Name.objects.create(name="Test Name", name_type=Name.PERSONAL)

        # Manual reset the date_created field so then Name was no longer
        # created in the current month.
        name.date_created = date_created
        name.save()

        name_stats = stats.NameStatisticsType(Name.objects.created_stats())
        gen = name_stats.get_queryset_members()

        # Expand the generator into a list, and get the last element.
        # That element will represent the statistics for the current month,
        # where no names were created.
        results = [n for n in gen]
        last_result = results.pop()

        assert last_result['count'] == 0
        assert last_result['month'] == current_month

    def test_calculate_with_empty_queryset(self):
        name_stats = stats.NameStatisticsType(Name.objects.created_stats())
        result = name_stats.calculate()
        assert isinstance(result, list)
        assert len(result) == 0

    def test_calculate_counts(self):
        now = datetime.now()
        date_created = now - relativedelta(months=2)

        name1 = Name.objects.create(name="John Smith", name_type=Name.PERSONAL)
        Name.objects.create(name="Jane Doe", name_type=Name.PERSONAL)

        name1.date_created = date_created
        name1.save()

        name_stats = stats.NameStatisticsType(Name.objects.created_stats())
        results = name_stats.calculate()

        assert len(results) == 3

        first_month = results.pop(0)
        assert first_month.total_to_date == 1
        assert first_month.total == 1

        second_month = results.pop(0)
        assert second_month.total_to_date == 1
        assert second_month.total == 0

        third_month = results.pop(0)
        assert third_month.total_to_date == 2
        assert third_month.total == 1


class TestNameStatisticsMonth:
    def test_available_instance_variables(self):
        name_stats_month = stats.NameStatisticsMonth()
        assert hasattr(name_stats_month, 'total')
        assert hasattr(name_stats_month, 'total_to_date')
        assert hasattr(name_stats_month, 'month')


class TestNameStatistics:
    def test_available_instance_variables(self):
        name_stats = stats.NameStatistics()
        assert hasattr(name_stats, 'created')
        assert hasattr(name_stats, 'modified')
        assert hasattr(name_stats, 'name_type_totals')

    def test_has_statistics(self, twenty_name_fixtures):
        name_stats = stats.NameStatistics()
        assert len(name_stats.created.stats) > 0
        assert len(name_stats.modified.stats) > 0
        assert len(name_stats.name_type_totals) > 0
