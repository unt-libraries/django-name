import unittest

import pytest
from name.models import Name, BaseTicketing
from django.test import Client, TestCase
try: import simplejson as json
except ImportError: import json


class NameCase(TestCase):

    def setUp(self):
        Name(name='test person', name_type=0, begin='2012-01-12').save()
        Name(name='test organization', name_type=1, begin='2000-01-12').save()
        Name(name='test event', name_type=2, begin='2500-01-12').save()
        Name(name='test building', name_type=4, begin='2000-01-12').save()
        self.c = Client()
        self.routes_to_test = [
            'about/',
            'stats/',
            'map/',
            'feed/',
        ]

@pytest.mark.django_db(transaction=True)
class NameTestCase(NameCase):

    def test_response_codes(self):
        for test_route in self.routes_to_test:
            response = self.c.get('/name/%s' % test_route)
            self.assertEqual(response.status_code, 200)


@pytest.mark.django_db(transaction=True)
class NameSearchCase(NameCase):

    def test_json_returns_expected_results(self):
        response = self.c.get('/name/search.json?q_type=Personal&q=person')
        self.assertTrue(json.loads(response.content)[0]['name'] == 'test person')
        self.assertEqual(response.status_code, 200)

    def test_can_json_search_multiple_name_types(self):
        response = self.c.get('/name/search.json?q_type=Personal,Organization&q=test')
        json_results = json.loads(response.content)
        self.assertTrue(len(json_results) == 2)
        self.assertEqual(response.status_code, 200)

    def test_can_search_multiple_name_types(self):
        response = self.c.get('/name/search/?q_type=Personal,Organization&q=test')
        self.assertEqual(response.status_code, 200)

    def test_can_search(self):
        response = self.c.get('/name/search/?q_type=Personal&q=test')
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db(transaction=True)
class NameDetailCase(NameCase):
    """
    This class is inteded to check that the intended html properties are showing correctly
    """
    def test_itemprops(self):
        # people get certain itemprops
        response = self.c.get('/name/nm0000001/')
        self.assertTrue('itemprop=\"name\"' in response.content)
        self.assertTrue('itemprop=\'url\'' in response.content)
        self.assertTrue('itemprop=\"birthDate\"' in response.content)
        # buildings get others
        response = self.c.get('/name/nm0000004/')
        self.assertTrue('itemprop=\"name\"' in response.content)
        self.assertTrue('itemprop=\'url\'' in response.content)
        self.assertTrue('itemprop=\"erectedDate\"' in response.content)
        # organizations get others still
        response = self.c.get('/name/nm0000002/')
        self.assertTrue('itemprop=\"name\"' in response.content)
        self.assertTrue('itemprop=\'url\'' in response.content)
        self.assertTrue('itemprop=\"foundingDate\"' in response.content)
        # events get others still
        response = self.c.get('/name/nm0000003/')
        self.assertTrue('itemprop=\"name\"' in response.content)
        self.assertTrue('itemprop=\'url\'' in response.content)
        self.assertTrue('itemprop=\"startDate\"' in response.content)
