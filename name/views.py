import csv

from django import http
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed
from django.templatetags.static import static
from django.utils.feedgenerator import Atom1Feed
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from pynaco.naco import normalizeSimplified

from .models import Name, Identifier, Location
from .utils import filter_names

VOCAB_DOMAIN = settings.VOCAB_DOMAIN


def label(request, name_value):
    """Find a name by label.

    If the label matches a single name, users are redirected
    to the name_entry_detail page. Otherwise, if the label
    does not exist, or the specified label matches multiple Name
    objects, a status code 404 is returned.
    """
    if not name_value:
        return http.HttpResponseNotFound()

    normalized_name = normalizeSimplified(name_value)
    try:
        name = Name.objects.get(normalized_name=normalized_name)

        return http.HttpResponseRedirect(
            reverse('name_entry_detail', args=[name.name_id]))

    except Name.DoesNotExist:
        return http.HttpResponseNotFound(
            u'No matching term found - authoritative, or variant - for \"{0}\"'
            .format(name_value))

    except Name.MultipleObjectsReturned:
        return http.HttpResponseNotFound(
            u'There are multiple Name objects with the same name: \'{0}\'.'
            .format(normalized_name))


class AtomSiteNewsFeed(Feed):
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
        return "Name Type: %s" % item.get_name_type_label()

    def item_link(self, item):
        return VOCAB_DOMAIN + 'name/' + item.name_id + '/'


def entry_detail(request, name_id):
    """View for the Name detail page."""
    queryset = (
        Name.objects.select_related().
        prefetch_related('identifier_set__type')
    )

    name_entry = get_object_or_404(queryset, name_id=name_id)

    if name_entry.merged_with:
        return redirect(name_entry.merged_with)

    elif name_entry.is_suppressed():
        return http.HttpResponseNotFound()

    elif name_entry.is_deleted():
        return http.HttpResponseGone('The requested record has been deleted!')

    return render(request, 'name/name_detail.html', dict(name=name_entry))


def export(request):
    """Exports Names as TSV file."""
    # Create a CSV response.
    response = http.HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.tsv"'

    writer = csv.writer(response, delimiter='\t', quoting=csv.QUOTE_MINIMAL)

    # Iterate through the visible Names that are not merged with any other
    # Name records and write a row for each record.
    for n in Name.objects.visible():
        writer.writerow([
            n.get_name_type_label().lower(),
            n.name.encode('utf-8'),
            request.build_absolute_uri(n.get_absolute_url())
        ])

    return response


def opensearch(request):
    """Renders an Opensearch XML file.

    Opensearch URL templates are composed in the view
    to more easily compose the absolute url with the
    query string.
    """
    # Query templates for the URLs.
    search_query = '{0}?q_type=Personal&q={{searchTerms}}'
    search_json_query = '{0}?q={{searchTerms}}'

    # Build the absolute URLs.
    search_url = request.build_absolute_uri(reverse('name_search'))
    search_json_url = request.build_absolute_uri(reverse('name_names'))

    # Compose the full URLs  that will be sent to the template.
    search = search_query.format(search_url)
    search_json = search_json_query.format(search_json_url)
    image = request.build_absolute_uri(static('name/img/favicon.png'))

    urls = dict(search=search, search_json=search_json, image=image)

    return render(request, 'name/opensearch.xml',
                  urls, content_type='text/xml')


def about(request):
    """View for the About page."""
    return render(request, 'name/about.html')


def stats(request):
    """View for the Stats page."""
    context = dict(
        total_names=Name.objects.count(),
        total_identifiers=Identifier.objects.count()
    )
    return render(request, 'name/stats.html', context)


def landing(request):
    """View for the Landing page."""
    counts = dict(counts=Name.objects.active_type_counts())
    return render(request, 'name/landing.html', counts)


def map(request):
    """View for the Map page."""
    return render(request, 'name/map.html')


class SearchView(generic.ListView):
    model = Name
    template_name = 'name/search.html'
    paginate_by = 15

    VALID_SORTS = {
        'name_a': 'name',
        'name_d': '-name',
        'begin_a': 'begin',
        'begin_d': '-begin',
        'end_a': 'end',
        'end_d': '-end',
    }

    DEFAULT_SORT = VALID_SORTS['name_a']

    def get_sort_method(self):
        order = self.request.GET.get('order', '')
        return self.VALID_SORTS.get(order, self.DEFAULT_SORT)

    def get_queryset(self):
        query = self.request.GET
        if query.get('q') or query.get('q_type'):
            return filter_names(self.request).order_by(self.get_sort_method())
        return Name.objects.none()


def mads_serialize(request, name_id):
    """Renders the Name serialized into the MADS XML format."""
    queryset = (
        Name.objects.select_related()
        .prefetch_related('identifier_set__type', 'note_set', 'variant_set')
    )

    context = dict(name=get_object_or_404(queryset, name_id=name_id))

    return render(request, 'name/name.mads.xml',
                  context, content_type='text/xml')
