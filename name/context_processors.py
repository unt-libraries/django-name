from name.models import NAME_TYPE_CHOICES


def name_types(request):
    return {'name_types': dict(NAME_TYPE_CHOICES)}
