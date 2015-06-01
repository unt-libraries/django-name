"""Serializers for the Name App Models.

This module leverages the Django Rest Framework's Serializer
components to build JSON representations of the models defined
in this app.

These JSON representations are designed to be backwards compatible
with the API documented in previous versions.

For documentation regarding the Django Rest Framework Serializers go
to http://www.django-rest-framework.org/api-guide/serializers/
"""

from rest_framework import serializers
from .. import models


class IdentifierSerializer(serializers.ModelSerializer):
    """Serializer for the Identifier Model.

    The following fields have been renamed for backwards compatibility
    with previous versions of the API.
        label -> identifier.type
        href -> identifier.value
    """
    label = serializers.StringRelatedField(source='type')
    href = serializers.CharField(source='value')

    class Meta:
        model = models.Identifier
        fields = ('label', 'href')


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for the Note Model."""
    type = serializers.SerializerMethodField()

    class Meta:
        model = models.Note
        fields = ('note', 'type')

    def get_type(self, obj):
        """Sets the type field.

        Returns the Note Type label, instead of the Note Type ID, which
        is the default behavior.
        """
        return obj.get_note_type_label().lower()


class VariantSerializer(serializers.ModelSerializer):
    """Serializer for the Variant Model."""
    type = serializers.SerializerMethodField()

    class Meta:
        model = models.Variant
        fields = ('variant', 'type')

    def get_type(self, obj):
        """Sets the type field.

        Returns the Variant Type label, instead of the Variant Type ID,
        which is the default behavior.
        """
        return obj.get_variant_type_label().lower()


class NameSerializer(serializers.ModelSerializer):
    """Serializer for the Name Model.

    This serializes the the Name model to include detailed information
    about the object, including the related Variants, Notes, and
    Identifiers.

    The following fields have been renamed for backwards compatibility
    with previous versions of the API.
        authoritative_name -> name.name
        begin_date -> name.begin
        end_date -> name.end

    The identifier field is the absolute url to the name detail
    page for the model instance.
    """
    authoritative_name = serializers.CharField(source='name')
    begin_date = serializers.CharField(source='begin')
    name_type = serializers.SerializerMethodField()
    end_date = serializers.CharField(source='end')
    links = IdentifierSerializer(many=True, source='identifier_set')
    notes = NoteSerializer(many=True, source='note_set')
    variants = VariantSerializer(many=True, source='variant_set')
    identifier = serializers.HyperlinkedIdentityField(
        view_name='name:detail', lookup_field='name_id')

    class Meta:
        model = models.Name
        fields = ('authoritative_name', 'name_type', 'begin_date', 'end_date',
                  'identifier', 'links', 'notes', 'variants',)

    def get_name_type(self, obj):
        """Sets the name_type field.

        Returns the Name Type label, instead of the Name Type ID, which
        is the default behavior.
        """
        return obj.get_name_type_label().lower()


class NameSearchSerializer(serializers.ModelSerializer):
    """Name Model Serializer for the Name search/autocompletion
    endpoint.

    The following fields have been renamed for backwards compatibility
    with previous versions of the API.
        begin_date -> name.begin
        type -> name.get_name_type_label()
        label -> Formats name.name and name.disambiguation.

    The URL field is the absolute url to the name detail page for
    the model instance.
    """
    begin_date = serializers.CharField(source='begin')
    type = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    URL = serializers.HyperlinkedIdentityField(
        view_name='name:detail', lookup_field='name_id')

    class Meta:
        model = models.Name
        fields = ('id', 'name', 'label', 'type', 'begin_date',
                  'disambiguation', 'URL')

    def get_type(self, obj):
        """Sets the type field.

        Returns the Name Type label, instead of the Name Type ID, which
        is the default behavior.
        """
        return obj.get_name_type_label().lower()

    def get_label(self, obj):
        """Sets the label field.

        Returns a string in the form of
            "<name.name> (<name.disambiguation>)"
        """
        if obj.disambiguation:
            return u'{0} ({1})'.format(obj.name, obj.disambiguation)
        return obj.name


class LocationSerializer(serializers.ModelSerializer):
    """Serailizer for the Locations Model.

    This includes the related Name via the belong_to_name field. The
    belong_to_name field uses the NameSerializer to nest the related
    Name model.
    """
    belong_to_name = NameSerializer()

    class Meta:
        model = models.Location


class NameStatisticsMonthSerializer(serializers.Serializer):
    """Serializer for the NameStatisticsMonth object."""
    total = serializers.IntegerField()
    total_to_date = serializers.IntegerField()
    month = serializers.DateTimeField()


class NameStatisticsTypeSerializer(serializers.Serializer):
    """Serializer for the NameStatisticsType object.

    This serializer utilizes the NameStatisticsTypeMonth to serialize
    the NameStatisticsMonth instances that the object instance contains.
    """
    running_total = serializers.IntegerField()
    stats = NameStatisticsMonthSerializer(many=True)


class NameStatisticsSerializer(serializers.Serializer):
    """Serializer for the NameStatistics object.

    This serializer utilizes the NameStatisticsTypeSerializer to
    serialize the NameStatisticsType instances that the object instance
    contains.
    """
    created = NameStatisticsTypeSerializer()
    modified = NameStatisticsTypeSerializer()
    name_type_totals = serializers.DictField()
