import csv

from django import http
from django.views import generic
from django.core.urlresolvers import reverse
from django.templatetags.static import static
from django.shortcuts import get_object_or_404, render, redirect
from pynaco.naco import normalizeSimplified

from .models import Name, Identifier
from .utils import filter_names


def label(request, name_value):
    """Find a name by label.

    If the label matches a single name, users are redirected
    to the name detail page. Otherwise, if the label
    does not exist, or the specified label matches multiple Name
    objects, a status code 404 is returned.
    """
    if not name_value:
        return http.HttpResponseNotFound()

    normalized_name = normalizeSimplified(name_value)
    try:
        name = Name.objects.get(normalized_name=normalized_name)

        return http.HttpResponseRedirect(
            reverse('name:detail', args=[name.name_id]))

    except Name.DoesNotExist:
        return http.HttpResponseNotFound(
            'No matching term found - authoritative or variant - for "{0}"'
            .format(name_value))

    except Name.MultipleObjectsReturned:
        return http.HttpResponseNotFound(
            'There are multiple Name objects with the same name: "{0}".'
            .format(normalized_name))


def detail(request, name_id):
    """View for the Name detail page."""
    queryset = (
        Name.objects.select_related().
        prefetch_related('identifier_set__type')
    )

    name_entry = get_object_or_404(queryset, name_id=name_id)

    if name_entry.merged_with:
        return redirect(name_entry.merged_with)

    elif name_entry.is_suppressed():
        return http.HttpResponseNotFound(
            'The requested record could not be found.')

    elif name_entry.is_deleted():
        return http.HttpResponseGone('The requested record has been deleted!')

    return render(request, 'name/name_detail.html', dict(name=name_entry))


def export(request):
    """Exports Names to a TSV file."""
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
    search_url = request.build_absolute_uri(reverse('name:search'))
    search_json_url = request.build_absolute_uri(reverse('name:search-json'))

    # Compose the full URLs that will be sent to the template.
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
        total_names=Name.objects.visible().count(),
        total_identifiers=Identifier.objects.count()
    )
    return render(request, 'name/stats.html', context)


def landing(request):
    """View for the Landing page."""
    counts = dict(counts=Name.objects.active_type_counts())
    return render(request, 'name/landing.html', counts)


def locations(request):
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
