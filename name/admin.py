from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from name.models import (
    Name,
    Variant,
    Note,
    Identifier,
    Identifier_Type,
    Location
)


# we need this custom filter for the boolean sidebar merged_with toggle
class IsMergedWithFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('merged status')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'merged_with'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the coded
        value for the option that will appear in the URL query. The second
        element is the human-readable name for the option that will appear
        in the right sidebar.
        """

        return (
            ('Yes', _('Currently merged')),
            ('No', _('Not merged')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        # Compare the requested value (either 'Yes' or 'No')
        # to decide how to filter the queryset.
        if self.value() == 'Yes':
            # the merged_with foreign key will be None if not merged
            return queryset.exclude(merged_with=None)
        if self.value() == 'No':
            return queryset.filter(merged_with=None)


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0


class MergedWithInline(admin.TabularInline):

    # we dont want to add any records to this inline, just show merged
    def has_add_permission(self, request):
        return False

    model = Name
    verbose_name_plural = 'names that are merged with this record'
    verbose_name = 'names merged with this record'
    readonly_fields = ('name',)
    fields = ('name',)
    extra = 0
    can_delete = False


class IdentifierInline(admin.TabularInline):
    model = Identifier
    extra = 0


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0


class Identifier_TypeAdmin(admin.ModelAdmin):
    model = Identifier_Type
    extra = 0


class LocationInline(admin.StackedInline):
    model = Location
    extra = 0


class NameAdmin(admin.ModelAdmin):

    # what to display/order of Names list /admin/name/name
    list_display = [
        'name',
        'name_id',
        'disambiguation',
        'begin',
        'end',
        'record_status',
        'has_geocode',
    ]

    # list of fields that the search queries
    search_fields = [
        'name',
        'biography',
        'variant__variant',
        'disambiguation',
    ]

    raw_id_fields = [
        'merged_with'
    ]

    # right-side filter toggle
    list_filter = [
        'record_status',
        'name_type',
        IsMergedWithFilter,
    ]

    # non-editable
    readonly_fields = [
        'name_id',
        'normalized_name',
    ]

    # FK inline fields
    inlines = [
        MergedWithInline,
        VariantInline,
        IdentifierInline,
        NoteInline,
        LocationInline,
    ]
    no_merged_inlines = [
        VariantInline,
        IdentifierInline,
        NoteInline,
        LocationInline,
    ]

    # these functions decide which set of inlines should be displayed
    def get_inline_instances(self, request, obj=None):
        inline_instances = []

        inlines = self.no_merged_inlines
        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_add_permission(request) or
                        inline.has_change_permission(request) or
                        inline.has_delete_permission(request)):
                    continue
                if not inline.has_add_permission(request):
                    inline.max_num = 0
            inline_instances.append(inline)
        return inline_instances

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)

    # edit page fieldset / order
    fieldsets = [
        (None, {
            'fields': [
                'name_id',
            ]
        }),
        ('Basic Info', {
            'fields': [
                'name',
                'normalized_name',
                'name_type',
                'biography',
                'begin',
                'end',
                'disambiguation',
            ]
        }),
        ('Misc Options', {
            'fields': [
                'record_status',
                'merged_with',
            ]
        }),
    ]

admin.site.register(Name, NameAdmin)
admin.site.register(Identifier_Type, Identifier_TypeAdmin)
