from name.models import Name


def name_types(request):
    return {'name_types': dict(Name.NAME_TYPE_CHOICES)}
