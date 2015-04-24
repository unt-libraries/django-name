import re
import csv
import copy
import json
from xml.etree import ElementTree
from django.http import (HttpResponse, HttpResponseGone, HttpResponseRedirect,
                         HttpResponseNotFound)
from django.template import RequestContext
from django.shortcuts import (render_to_response, get_object_or_404, render,
                              redirect)
from django.db.models import Q, Count, Max, Min
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.conf import settings
from dateutil import rrule
from datetime import datetime
from pynaco.naco import normalizeSimplified
from name.decorators import jsonp
from name.models import (
    Name,
    Identifier,
    Location,
    NAME_TYPE_CHOICES,
    VARIANT_TYPE_CHOICES,
    NOTE_TYPE_CHOICES,
    DATE_DISPLAY_LABELS,
)

VOCAB_DOMAIN = settings.VOCAB_DOMAIN


# these next two functions were nabbed for the most part from this blog post:
# julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
#
# they are implemented in the 'search' view
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    """
    Splits the query string in individual keywords, getting rid of
    unnecessary spaces and grouping quoted words together.
    Example:

    >>> normalize_query('some random words "with quotes" and spaces')
    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    """
    return [normspace(
        ' ',
        (t[0] or t[1]).strip()
    ) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    """Returns a query, that is a combination of Q objects.

    That combination aims to search keywords within a model by testing the
    given search fields.
    """
    # Query to search for every search term
    terms = normalize_query(query_string)
    qs = (Q(name__icontains=term) for term in terms)

    return reduce(lambda x, y: x & y, qs)


def label(request, name_value):
    """Find a name by label.

    If the label matches a single name, users are redirected
    to the name_entry_detail page. Otherwise, if the label
    does not exist, or the specified label matches multiple Name
    objects, a status code 404 is returned.
    """
    if not name_value:
        return HttpResponseNotFound()

    normalized_name = normalizeSimplified(name_value)
    try:
        name = Name.objects.get(normalized_name=normalized_name)

        return HttpResponseRedirect(
            reverse('name_entry_detail', args=[name.name_id]))

    except Name.DoesNotExist:
        return HttpResponseNotFound(
            u'No matching term found - authoritative, or variant - for \"{0}\"'
            .format(name_value))

    except Name.MultipleObjectsReturned:
        return HttpResponseNotFound(
            u'There are multiple Name objects with the same name: \'{0}\'.'
            .format(normalized_name))


class AtomSiteNewsFeed(Feed):
    """Sets up atom feed"""

    feed_type = Atom1Feed
    link = "/name/feed/"
    title = "Name App"
    subtitle = "new records"

    def items(self):
        # last 5 added items
        return Name.objects.order_by('-date_created')[:20]

    def item_title(self, item):
        return item.name

    def item_location(self, item):
        """
        Returns an extra keyword arguments dictionary that is used
        with the `add_item` call of the feed generator. Add the
        'content' field of the 'Entry' item, to be used by the custom
        feed generator.
        """
        location_set = []
        for l in Location.objects.filter(belong_to_name=item):
            location_set.append(
                'georss:point', "%s %s" % (l.latitude, l.longitude)
            )
        return location_set

    def item_description(self, item):
        return "Name Type: %s" % NAME_TYPE_CHOICES[item.name_type][1]

    def item_link(self, item):
        return VOCAB_DOMAIN + 'name/' + item.name_id + '/'


def entry_detail(request, name_id):
    """Name Entry Detail View."""
    queryset = (
        Name.objects.select_related().
        prefetch_related('identifier_set__type')
    )

    name_entry = get_object_or_404(queryset, name_id=name_id)

    if name_entry.merged_with:
        return redirect(name_entry.merged_with)

    elif name_entry.is_suppressed():
        return HttpResponseNotFound()

    elif name_entry.is_deleted():
        return HttpResponseGone('The requested record has been deleted!')

    return render(request, 'name/name_detail.html', {'name': name_entry})


def export(request):
    """Exports Names as TSV file."""
    # Create a CSV response.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.tsv"'

    writer = csv.writer(response, delimiter='\t', quoting=csv.QUOTE_MINIMAL)

    # Iterate through the Active Names that are not merged with any other
    # Name records and write a row for each record.
    for n in Name.objects.filter(record_status=0).filter(merged_with=None):
        writer.writerow([
            n.get_name_type_label().lower(),
            n.name.encode('utf-8'),
            request.build_absolute_uri(n.get_absolute_url())
        ])

    return response


def opensearch(request):
    """Opensearch

    Returns Opensearch XML file.
    """

    # create XML root element
    root = ElementTree.Element('OpenSearchDescription')
    root.set('xmlns', 'http://a9.com/-/spec/opensearch/1.1/')

    # define the children to root and their parameters
    shortname = ElementTree.SubElement(root, 'ShortName')
    shortname.text = "Name App"
    description = ElementTree.SubElement(root, 'Description')
    description.text = "Search Name App Entries"

    # set icon
    image = ElementTree.SubElement(root, 'Image')
    image.set('width', '16')
    image.set('height', '16')
    image.text = request.get_host() + '/media/icons/unt_favicon.ico'

    # set search url
    url = ElementTree.SubElement(root, 'Url')
    url.set('type', 'text/html')
    url.set(
        'template',
        "{url}?q_type=Personal&q={{searchTerms}}".format(
            url=request.build_absolute_uri(reverse('name_search')))
    )

    auto_suggest = ElementTree.SubElement(root, 'Url')
    auto_suggest.set('type', 'application/x-suggestions+json')
    auto_suggest.set(
        'template',
        "{url}?q={{searchTerms}}".format(
            url=request.build_absolute_uri(reverse('name_names')))
    )

    # export the element tree to a string and send to httpresponse
    t = ElementTree.tostring(root)
    return HttpResponse(t, content_type='text/xml')


def about(request):
    """
    Renders the name about page to the user.
    """
    return render(request, 'name/about.html')


def prepare_graph_date_range():
    """
    Several functions use the same code to prepare the dates and values
    for the graphing of event data, so we can make a function for it.
    DRY 4 LYPHE

    returns list of lists
    """

    name_objects = Name.objects.all()
    # grab the dates for the bounds of the graphs
    if name_objects.count() > 0:
        dates = Name.objects.all().aggregate(
            Min("date_created"), Max('date_created'))
        system_start_date = dates['date_created__min']
        system_end_date = dates['date_created__max']

        # setup list for month call data
        daily_edit_counts = []
        # we need to first fill in the first month, because it won't
        # grab that when the for loop iterates to a new month.
        month = system_start_date.strftime('%Y-%m')
        daily_edit_counts.append([datetime.strptime(month, '%Y-%m'), 0])
        # start with a zero count and reset this as we cross a month
        for dt in rrule.rrule(
            rrule.DAILY,
            dtstart=system_start_date,
            until=system_end_date,
        ):
            # if we change months
            if month != dt.strftime('%Y-%m'):
                month = dt.strftime('%Y-%m')
                # make the year and drop in if i doenst exist
                daily_edit_counts.append(
                    [datetime.strptime(month, '%Y-%m'), 0])
        return daily_edit_counts
    else:
        raise Exception('no name objects to construct graph')


def calc_total_by_month(**kwargs):
    """
    totals for the bag / file count by month.
    Returns an ordered dict
    """

    if kwargs['created']:
        # get the daily Name totals
        daily_counts = Name.objects.extra(
            select={'day': 'date_created'}
        ).values('day').annotate(num=Count('date_created'))
    elif kwargs['edited']:
        # get the daily Name totals
        daily_counts = Name.objects.extra(
            select={'day': 'last_modified'}
        ).values('day').annotate(num=Count('last_modified'))
    # make current total events count
    current_total = 0
    month_skeleton = copy.deepcopy(prepare_graph_date_range())
    # fill in totals
    for u in month_skeleton:
        # replace existing value of zero with sum of nums in certain
        # month
        current_month_counts = [e for e in daily_counts if datetime.strftime(
            e['day'], '%Y-%m') == datetime.strftime(u[0], '%Y-%m')]

        for n in current_month_counts:
            current_total += n['num']
        u[1] = current_total
        if not kwargs['running']:
            current_total = 0
    return month_skeleton


def stats(request):
    """
    Renders the name stats page to the user
    """

    name_type_counts = {
        'personal': Name.objects.filter(name_type=0).count(),
        'organization': Name.objects.filter(name_type=1).count(),
        'event': Name.objects.filter(name_type=2).count(),
        'software': Name.objects.filter(name_type=3).count(),
    }
    name_line_graph_data = {
        'creation_running': calc_total_by_month(created=True,
                                                edited=False, running=True),
        'creation_monthly': calc_total_by_month(created=True,
                                                edited=False, running=False),
        'edited_running': calc_total_by_month(created=False,
                                              edited=True, running=True),
        'edited_monthly': calc_total_by_month(created=False,
                                              edited=True, running=False),
    }
    return render_to_response(
        'name/stats.html',
        {
            'name_line_graph_data': name_line_graph_data,
            'name_type_counts': name_type_counts,
            'total_names': Name.objects.count(),
            'total_links': Identifier.objects.count(),
        },
        context_instance=RequestContext(request)
    )


def resolve_type(request):
    """
    resolves the type of the request
    """
    q_types = []

    if 'q_type' in request.GET:
        query_named_type = request.GET['q_type']

        if ',' in query_named_type:
            query_named_type = query_named_type.split(',')
        else:
            query_named_type = [query_named_type]
        for k, v in NAME_TYPE_CHOICES:
            for q_type in query_named_type:
                if q_type == v:
                    q_types.append(NAME_TYPE_CHOICES[k][0])
    return q_types


def filter_names(q, name_types):
    """
    Return the set of filtered name objects

    q: Query string
    name_types: List of name_type ids. List of integers.
    """
    # we definitely don't want to serve up hidden/merged/deleted
    # records.
    names = Name.objects.filter(record_status=0).filter(merged_with=None)
    # we get passed a type - include that in the filter
    if name_types:
        names = names.filter(name_type__in=name_types)

    # clean and normalize the query for the filter,
    #  searching name and bio
    if q is '':
        pass
    elif q:
        # all names that fit query OR all variants that contain query
        names = names.filter(
            get_query(q, ['name']) |
            Q(variant__variant__icontains=q)
        ).distinct()

    return names


@jsonp
def get_names(request):
    """
    returns the json ajax autocomplete
    """

    # headers sent in search.json responses
    cors_headers = [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Headers', 'X-Requested-With'),
    ]
    # if the request is ajax, we want to retrieve the suggestions list
    if request.is_ajax():
        # resolve the name and type
        q = request.GET.get('q', '')
        q_types = resolve_type(request)
        # build a list of results
        results = []
        # closest 10 results, filtered by query and type
        for n in filter_names(q, q_types)[:10]:
            name_json = {'id': n.name_id, 'label(request, name_value)': n.name}
            if n.disambiguation:
                name_json['label'] += " (" + n.disambiguation + ")"
            name_json['value'] = n.name
            results.append(name_json)
    else:
        # resolve the name and type
        q = request.GET.get('q', '')
        q_types = resolve_type(request)
        results = []
        for n in filter_names(q, q_types):
            name_json = {
                'id': n.name_id,
                'type': str(NAME_TYPE_CHOICES[n.name_type][1])
            }
            if n.disambiguation:
                name_json['disambiguation'] = n.disambiguation

            name_json['name'] = n.name
            name_json['URL'] = request.build_absolute_uri(
                reverse('name_entry_detail', args=[n.name_id]))

            if n.begin:
                name_json['begin_date'] = n.begin
            if n.end:
                name_json['begin_date'] = n.end
            results.append(name_json)
    response = HttpResponse(
        content_type='application/json'
    )
    # attached CORS headers
    for hk, hv in cors_headers:
        response[hk] = hv
    json.dump(
        results,
        fp=response,
        indent=4,
        sort_keys=True,
    )
    return response


def paginate_entries(request, entries_result, num_per_page=10):
    """
    paginates a set of entries (set of model objects)
    """

    # create paginator from result set
    paginator = Paginator(entries_result, num_per_page)

    # try to resolve the current page
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        paginated_entries = paginator.page(page)

    except (EmptyPage, InvalidPage):
        paginated_entries = paginator.page(paginator.num_pages)

    # send back the paginated entries
    return paginated_entries


def landing(request):
    """
    Renders the results of a search back to the user
    """

    # Get the active Names and create a context dictionary
    # that contains the counts of each Name type.
    active_names = Name.objects.all().filter(record_status=0)

    counts = {
        'total': active_names.count(),
        'personal': active_names.filter(name_type=0).count(),
        'organization': active_names.filter(name_type=1).count(),
        'event': active_names.filter(name_type=2).count(),
        'software': active_names.filter(name_type=3).count(),
        'building': active_names.filter(name_type=4).count()
    }

    return render_to_response(
        'name/landing.html',
        {'counts': counts},
        context_instance=RequestContext(request)
    )


def map_json(request):
    """Presents the Locations and related Names serialized into JSON."""
    locations = Location.objects.all().filter(status=0)

    if request.is_ajax():
        data = serializers.serialize('json', locations,
                                     use_natural_foreign_keys=True, indent=4)
        return HttpResponse(data, content_type='application/json')
    return HttpResponseNotFound()


def map(request):
    """
    Renders the results of a search back to the user
    """
    locations = Location.objects.all().filter(status=0)

    # render the view with the dict of results
    return render_to_response(
        'name/map.html',
        {'locations': locations},
        context_instance=RequestContext(request)
    )


def search(request):
    """
    Renders the big search bar and results of a search back to the user
    """
    VALID_SORTS = {
        'name_a': 'name',
        'name_d': '-name',
        'begin_a': 'begin',
        'begin_d': '-begin',
        'end_a': 'end',
        'end_d': '-end',
    }

    DEFAULT_SORT = 'name_a'
    # resolve the name and type
    q = request.GET.get('q', '')
    q_type = resolve_type(request)
    # set up the sorting
    sort_key = request.GET.get('order', DEFAULT_SORT)
    sort = VALID_SORTS.get(sort_key, DEFAULT_SORT)
    # use get_query function from the model, searching name and bio
    if 'q' in request.GET or 'q_type' in request.GET:
        # paginate 15 per page and apply ordering
        paginated_entries = paginate_entries(
            request,
            filter_names(q, q_type).order_by(sort),
            15
        )
    else:
        # gather all records if all of the above is false
        paginated_entries = None
    # render html date display for the case of one q_type
    if len(q_type) == 1:
        date_display_begin = DATE_DISPLAY_LABELS[q_type[0]].get('begin')
        date_display_end = DATE_DISPLAY_LABELS[q_type[0]].get('end')
        q_type = DATE_DISPLAY_LABELS[q_type[0]]['type']
    # if we have more than one qtype, use more generic dates
    elif len(q_type) != 1:
        date_display_begin = 'Start Date'
        date_display_end = 'End Date'
        # rebuild q_type display
        q_type = ','.join([DATE_DISPLAY_LABELS[x]['type'] for x in q_type])
    return render_to_response(
        'name/search.html',
        {
            'date_display_begin': date_display_begin,
            'date_display_end': date_display_end,
            'q_type': q_type,
            'q': q,
            'sort': sort_key,
            'entries': paginated_entries,
        },
        context_instance=RequestContext(request)
    )


def name_json(request, name_id):
    """
    Returns result of name query in json format
    """

    # define the requested user from the passed id
    requested_user = get_object_or_404(Name, name_id=name_id)

    jsonDict = {}
    variant_list = []
    link_list = []
    note_list = []

    jsonDict['name_type'] = str(
        NAME_TYPE_CHOICES[requested_user.name_type][1]
    ).lower()

    # make list and add to json for variant
    for variant in requested_user.variant_set.all():
        variant_list.append({
            "type": VARIANT_TYPE_CHOICES[variant.variant_type][1],
            "variant": variant.variant
        })
        jsonDict['variants'] = variant_list

    # make list and add to json for identifiers (links)
    for link in requested_user.identifier_set.all():
        if link.visible:
            link_list.append({
                "label": link.type.label,
                "href": link.value
            })
        jsonDict['links'] = link_list

    # make list and add to json for notes
    for note in requested_user.note_set.all().exclude(note_type=2):
        note_list.append({
            "type": NOTE_TYPE_CHOICES[note.note_type][1],
            "note": note.note
        })
        jsonDict['note'] = note_list

    # build dictionary to serialize to json
    if requested_user.begin:
        jsonDict['begin_date'] = requested_user.begin
    if requested_user.end:
        jsonDict['end_date'] = requested_user.end
    jsonDict['authoritative_name'] = requested_user.name
    jsonDict['identifier'] = request.build_absolute_uri()[:-5]

    # dump the dict to as an HttpResponse
    response = HttpResponse(content_type='application/json')

    json.dump(
        jsonDict,
        fp=response,
        indent=4,
        sort_keys=True,
    )
    return response


def set_prefixes(elem, prefix_map):
    """
    sets prefixes for mads xml
    """

    # check if this is a tree wrapper
    if not ElementTree.iselement(elem):
        elem = elem.getroot()

    # build uri map and add to root element
    uri_map = {}
    for prefix, uri in prefix_map.items():
        uri_map[uri] = prefix
        elem.set("xmlns:" + prefix, uri)

    # fix up all elements in the tree
    memo = {}
    for elem in elem.getiterator():
        fixup_element_prefixes(elem, uri_map, memo)


def fixup_element_prefixes(elem, uri_map, memo):
    """
    fixes the prefix names for proper mads headers
    """

    def fixup(name):
        try:
            return memo[name]
        except KeyError:
            if name[0] != "{":
                return
            uri, tag = name[1:].split("}")
            if uri in uri_map:
                new_name = uri_map[uri] + ":" + tag
                memo[name] = new_name
                return new_name

    # fix element name
    name = fixup(elem.tag)
    if name:
        elem.tag = name

    # fix attribute names
    for key, value in elem.items():
        name = fixup(key)
        if name:
            elem.set(name, value)
            del elem.attrib[key]


def mads_serialize(request, name_id):
    """
    render mads xml and push to the view
    """

    NSMAP = {
        'mods': 'http://www.loc.gov/mods/v3',
        'xlink': 'http://www.w3.org/1999/xlink',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    }
    # get the user
    requested_user = Name.objects.get(name_id=name_id)
    # create XML root element
    root = ElementTree.Element('mads')
    root.set('xmlns', 'http://www.loc.gov/mads/v2')
    root.set('xsi:schemaLocation', 'http://www.loc.gov/mads/mads.xsd')
    set_prefixes(root, NSMAP)
    # define the children that should always appear
    authority = ElementTree.SubElement(root, 'authority')
    name = ElementTree.SubElement(authority, 'name')
    name_part = ElementTree.SubElement(name, 'namePart')
    # get location information
    for loc in Location.objects.filter(belong_to_name=requested_user):
        location = ElementTree.SubElement(root, 'geographic')
        location.set('point', str(loc.latitude) + ' ' + str(loc.longitude))
    # if we have variants, cycle through creating children, etc.
    if requested_user.variant_set:
        for elem in requested_user.variant_set.all():
            variant = ElementTree.SubElement(root, 'variant')
            variant.set(
                'type',
                str(VARIANT_TYPE_CHOICES[elem.variant_type][1]).lower()
            )
            variant_name = ElementTree.SubElement(variant, 'name')
            variant_name_pt = ElementTree.SubElement(variant_name, 'namePart')
            variant_name_pt.text = elem.variant

    # record info must come after variants
    record_info = ElementTree.SubElement(root, 'recordInfo')
    record_creation_date = ElementTree.SubElement(
        record_info,
        'recordCreationDate'
    )
    record_change_date = ElementTree.SubElement(
        record_info,
        'recordChangeDate'
    )
    record_identifier = ElementTree.SubElement(
        record_info,
        'recordIdentifier'
    )

    # if we have notes, cycle through creating children, etc.
    if requested_user.note_set:
        for elem in requested_user.note_set.all().exclude(note_type=2):
            note = ElementTree.SubElement(root, 'note')
            note.set(
                'type',
                str(NOTE_TYPE_CHOICES[elem.note_type][1]).lower()
            )
            note.text = elem.note

    # if we have links, cycle through creating children, etc.
    if requested_user.identifier_set:
        for elem in requested_user.identifier_set.all():
            if elem.visible:
                url = ElementTree.SubElement(root, 'url')
                url.set('displayLabel', elem.type.label)
                url.text = elem.value

    identifier = ElementTree.SubElement(root, 'identifier')
    identifier.set('type', "URL")
    identifier.text = request.build_absolute_uri()[:-9]

    # set authority type from type choices
    if requested_user.name_type == 0:
        pass
    elif requested_user.name_type == 1:
        name.set('type', 'corporate')

    # if we have a begin date, make authority child node
    if requested_user.begin:
        name_part_date = ElementTree.SubElement(name, 'namePart')
        name_part_date.set('type', 'date')
        date_string = requested_user.begin + '/open'

        # edit the date string should we encounter an end date
        if requested_user.end:
            date_string = requested_user.begin + '/' + requested_user.end
        name_part_date.text = date_string
    elif requested_user.end:
        name_part_date = ElementTree.SubElement(name, 'namePart')
        date_string = 'unknown/' + requested_user.end
        name_part_date.text = date_string

    # add the information that will always be a part of a record.
    name_part.text = requested_user.name
    record_change_date.text = requested_user.last_modified.strftime(
        '%Y-%m-%dT%H:%M:%S'
    )
    record_creation_date.text = requested_user.date_created.strftime(
        '%Y-%m-%dT%H:%M:%S'
    )
    record_identifier.text = request.build_absolute_uri()[:-9]

    mads_xml = ElementTree.tostring(root)

    return HttpResponse(mads_xml, content_type="application/xml")
