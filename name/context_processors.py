from name.models import NAME_TYPE_CHOICES


def baseurl(request):
    """
    Return a BASE_URL template context for the current request
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    return {
        'BASE_URL': scheme + request.get_host(),
    }


def name_types(request):
    return {'name_types': dict(NAME_TYPE_CHOICES)}
