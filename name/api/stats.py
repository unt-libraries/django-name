from ..models import Name
from datetime import datetime
from dateutil.relativedelta import relativedelta


class NameStatisticsMonth(object):
    """A simple datatype to represent Name statistics for a
    single month.
    """
    def __init__(self, **kwargs):
        self.total = kwargs.get('total', 0)
        self.total_to_date = kwargs.get('total_to_date', 0)
        self.month = kwargs.get('month', None)

    def __repr__(self):
        return '<{name} {0}, {1}>'.format(
            str(self.month), self.total, name=self.__class__.__name__)


class NameStatisticsType(object):
    """Statistics class for calculating a the number
    of Name objects in the database using a DateTime field.

    Accepts an Iterable of dictionaries in the form of
        [{ count: <num>, month: <datetime object> }, ...]

    This will calculate:
        1. The overall total of of Name objects according to the
           the Iterable passed in.j
        2. Starting from the first Name created, this will create
           a new NameStatisticsMonth object for each month up to
           the current month according to the system time.
    """
    def __init__(self, queryset):
        self.running_total = 0
        self.queryset = queryset
        self.start = queryset.first().get('month')
        self.stats = []

    def calculate(self):
        """Calculate the running total of the Name objects
        and total and total_to_date for each month since the
        first Name was created.
        """
        # Reset stats and running total to ensure they are not
        # mutated unintentionally if the method is executed successively.
        self.stats = []
        self.running_total = 0

        # Create a NameStatisticsMonth object for each month since the
        # first Name was created.
        for u in self.get_queryset_members():
            stats_month = NameStatisticsMonth(
                total=u.get('count'), month=u.get('month'))

            # Update the running total and use that value to
            # set the NameStatisticsMonth total_to_date property.
            self.running_total += u.get('count', 0)
            stats_month.total_to_date = self.running_total

            self.stats.append(stats_month)
        return self.stats

    def get_queryset_members(self):
        """Produces a generator which yields each element in the queryset
        in order.

        The queryset used to initialize this object is expected to
        only contain elements for each month where a name was created
        or modified (based ont the queryset). If there is a month when a
        Name was not created, this method will instead create an element
        with `count` set to 0 for said month and yield it instead.
        """
        # Convert the queryset to a list so that we can mutate
        # it with the pop() method.
        queryset = list(self.queryset)

        # Create a datetime object for the first day of the current
        # month according to the system time.
        now = datetime.now()
        end = datetime(now.year, now.month, 1)

        current = self.start
        # Set up the delta to increment the `current` date in the generator.
        delta = relativedelta(months=1)

        while current <= end:
            elem = queryset[0]
            # Compare the element's datetime to the `current` datetime
            if elem.get('month') == current:
                yield queryset.pop(0)
            else:
                yield dict(count=0, month=current)
            current += delta


class NameStatistics(object):
    """Container class to for all statistics gathered on
    Name objects.
    """
    def __init__(self):
        self.created = NameStatisticsType(Name.objects.created_stats())
        self.modified = NameStatisticsType(Name.objects.modified_stats())

    def calculate(self):
        self.created.calculate()
        self.modified.calculate()
