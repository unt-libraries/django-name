import re

from django.db.models import Q
from .models import Name
from functools import reduce


def normalize_query(query_string):
    """Splits the query string in individual keywords, removing
    unnecessary spaces and grouping quoted words together.

    Example:
    >>> normalize_query('some random words "with quotes" and spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    """
    findterms = re.compile(r'"([^"]+)"|(\S+)').findall
    normspace = re.compile(r'\s{2,}').sub

    terms = (findterms(query_string))

    return [normspace(' ', (t[0] or t[1]).strip()) for t in terms]


def compose_query(query_string):
    """Composes a Q object from the query_string.

    This will first normalize the query_sting and split the string up
    into words. Then it will iterate over the list of words creating Q
    object for each one. Last, it reduces the generated Q objects into
    a single Q object by combining them using the & operator.

    The reduce function essential performs the following operation for
    a query_string that contains 4 words,

        (((Q1 & Q2) & Q3) & Q4)

    where Q1-4 are instances of the Q object.
    """
    # Normalize the query_string which will also split the single string
    # into a list of terms.
    terms = normalize_query(query_string)

    # Create a generator that produces an instance of the Q object
    # for each term.
    qs = (Q(name__icontains=term) for term in terms)

    # Use bitwise AND to compose the objects into a single instance of Q.
    return reduce(lambda x, y: x & y, qs)


def resolve_type(q_type):
    """Resolve the Name Types passed to the request, and returns
    a list of Name Type IDs.

    The input is expected to be the raw q_type query string value passed
    in with the request.  The input is expected to be a comma delimited
    list such as, `Personal,Event,Software`.  This function will lookup
    up the ID of the Name Type based on the string and return a list
    of Name Type IDs.
    """
    if not q_type:
        return []

    q_type = q_type.split(',')

    if "Any Type" in q_type:
        return [k for k, v in Name.NAME_TYPE_CHOICES]
    else:
        # Iterate through the Name Types and create a list of Name IDs
        # using the corresponding strings values in q_type
        return [k for k, v in Name.NAME_TYPE_CHOICES if v in q_type]


# TODO: Look at reducing the number of queries.
def filter_names(request):
    """Return the set of Name objects filtered on the query
    parameters passed with the request.
    """
    q = request.GET.get('q', None)
    name_types = resolve_type(request.GET.get('q_type', None))

    # Retrieve the visible names from the database.
    names = Name.objects.visible()

    # Filter by name type if it is passed with the request.
    if name_types:
        names = names.filter(name_type__in=name_types)

    # Do further filtering if the q parameter is present.
    if q:
        # All names that fit query OR all variants that contain query
        query_filter = compose_query(q) | Q(variant__variant__icontains=q)
        names = names.filter(query_filter).distinct()

    return names
