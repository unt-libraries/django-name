from rest_framework import serializers
from .. import models


class IdentifierSerializer(serializers.ModelSerializer):
    label = serializers.StringRelatedField(source='type')
    href = serializers.CharField(source='value')

    class Meta:
        model = models.Identifier
        fields = ('label', 'href')


class NoteSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = models.Note
        fields = ('note', 'type')

    def get_type(self, obj):
        return obj.get_note_type_label().lower()


class VariantSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = models.Variant
        fields = ('variant', 'type')

    def get_type(self, obj):
        return obj.get_variant_type_label().lower()


class NameSerializer(serializers.ModelSerializer):
    authoritative_name = serializers.CharField(source='name')
    begin_date = serializers.CharField(source='begin')
    name_type = serializers.SerializerMethodField()
    end_date = serializers.CharField(source='end')
    links = IdentifierSerializer(many=True, source='identifier_set')
    notes = NoteSerializer(many=True, source='note_set')
    variants = VariantSerializer(many=True, source='variant_set')
    identifier = serializers.HyperlinkedIdentityField(
        view_name='name_entry_detail', lookup_field='name_id')

    class Meta:
        model = models.Name
        fields = (
            'authoritative_name',
            'name_type',
            'begin_date',
            'end_date',
            'identifier',
            'links',
            'notes',
            'variants',
        )

    def get_name_type(self, obj):
        return obj.get_name_type_label().lower()


class NameSearchSerializer(serializers.ModelSerializer):
    begin_date = serializers.CharField(source='begin')
    type = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    URL = serializers.HyperlinkedIdentityField(
        view_name='name_entry_detail', lookup_field='name_id')

    class Meta:
        model = models.Name
        fields = (
            'id',
            'name',
            'label',
            'type',
            'begin_date',
            'disambiguation',
            'URL'
        )

    def get_type(self, obj):
        return obj.get_name_type_label().lower()

    def get_label(self, obj):
        if obj.disambiguation:
            return u'{0} ({1})'.format(obj.name, obj.disambiguation)
        return obj.name


class LocationSerializer(serializers.ModelSerializer):
    belong_to_name = NameSerializer()

    class Meta:
        model = models.Location


class NameStatisticsMonthSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    total_to_date = serializers.IntegerField()
    month = serializers.DateTimeField()


class NameStatisticsTypeSerializer(serializers.Serializer):
    running_total = serializers.IntegerField()
    stats = NameStatisticsMonthSerializer(many=True)


class NameStatisticsSerializer(serializers.Serializer):
    created = NameStatisticsTypeSerializer()
    modified = NameStatisticsTypeSerializer()
