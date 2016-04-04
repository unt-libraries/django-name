from ..models import Name
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class NameStatisticsMonth(object):
    """A simple datatype to represent Name statistics for a
    single month.
    """

    def __init__(self, **kwargs):
        self.total = kwargs.get('total', 0)
        self.total_to_date = kwargs.get('total_to_date', 0)
        self.month = kwargs.get('month', None)


class NameStatisticsType(object):
    """Statistics class for calculating the number
    of Name objects in the database using a DateTime field.

    Accepts a list of dictionaries in the form of
        [{ count: <num>, month: <datetime object> }, ...]

    This will calculate:
        1. The overall total of of Name objects according to the
           the Iterable passed in.
        2. Starting from the first Name created, this will create
           a new NameStatisticsMonth object for each month up to
           the current month according to the system time.
    """

    def __init__(self, raw_stats):
        self.running_total = 0
        self.raw_stats = raw_stats
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
        for u in self.process_raw_stats():
            stats_month = NameStatisticsMonth(
                total=u.get('count'), month=u.get('month'))

            # Update the running total and use that value to
            # set the NameStatisticsMonth total_to_date property.
            self.running_total += u.get('count', 0)
            stats_month.total_to_date = self.running_total

            self.stats.append(stats_month)
        return self.stats

    def process_raw_stats(self):
        """Produces a generator which yields each element in the list
        in order.

        The list used to initialize this object is expected to
        only contain elements for each month where a name was created
        or modified (based on the list). If there is a month when a
        Name was not created, this method will instead create an element
        with `count` set to 0 for said month and yield it.
        """
        # Return early if the list is empty.
        if not len(self.raw_stats) > 0:
            return

        # Use the month in the first element of the list
        # as the starting month.
        current = self.raw_stats[0].get('month')

        # Create a datetime object for the first day of the current
        # month according to the system time.
        end = timezone.now().replace(day=1, hour=0, minute=0, second=0,
                                     microsecond=0)

        # Set up the delta to increment the `current` date in the generator.
        delta = relativedelta(months=1)

        while current <= end:
            # Get the first element of the list, if it exists.
            elem = self.raw_stats[0] if len(self.raw_stats) else False

            # Yield the first list element if the element
            # exists and if it's member month is equal to `current`.
            if elem and elem.get('month') == current:
                yield self.raw_stats.pop(0)
            else:
                yield dict(count=0, month=current)
            current += delta


class NameStatistics(object):
    """Container class for all statistics gathered on
    Name objects.
    """

    def __init__(self):
        self.created = NameStatisticsType(Name.objects.created_stats())
        self.modified = NameStatisticsType(Name.objects.modified_stats())
        self.name_type_totals = Name.objects.active_type_counts()
        self.calculate()

    def calculate(self):
        self.created.calculate()
        self.modified.calculate()
