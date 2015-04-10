from django.test import TestCase, RequestFactory
from smilekit.collection_tool.views import (
    get_help_item, intro, risk, topics, goals)
from smilekit.family_info.tests.factories import UserFactory
from django.contrib.auth.models import AnonymousUser
from django.http import Http404


class TestGetHelpItem(TestCase):
    def test_none_found(self):
        r = get_help_item("foo")
        self.assertIsNone(r)


class TestIntro(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get('/collection_tool/intro/language/en/')
        request.user = AnonymousUser()
        response = intro(request)
        self.assertEqual(response.status_code, 302)

    def test_invalid_language(self):
        request = self.factory.get('/collection_tool/intro/language/nl/')
        request.user = UserFactory()
        with self.assertRaises(Http404):
            intro(request, 'nl')

    def test_valid_languages(self):
        request = self.factory.get('/collection_tool/intro/language/en/')
        request.user = UserFactory()
        response = intro(request, 'en')
        self.assertEqual(response.status_code, 200)
        response = intro(request, 'es')
        self.assertEqual(response.status_code, 200)


class TestRisk(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get('/collection_tool/risk/language/en/')
        request.user = AnonymousUser()
        response = risk(request)
        self.assertEqual(response.status_code, 302)

    def test_invalid_language(self):
        request = self.factory.get('/collection_tool/risk/language/nl/')
        request.user = UserFactory()
        with self.assertRaises(Http404):
            risk(request, 'nl')

    def test_valid_languages(self):
        request = self.factory.get('/collection_tool/risk/language/en/')
        request.user = UserFactory()
        response = risk(request, 'en')
        self.assertEqual(response.status_code, 200)
        response = risk(request, 'es')
        self.assertEqual(response.status_code, 200)


class TestTopics(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get('/collection_tool/topics/language/en/')
        request.user = AnonymousUser()
        response = topics(request)
        self.assertEqual(response.status_code, 302)

    def test_invalid_language(self):
        request = self.factory.get('/collection_tool/topics/language/nl/')
        request.user = UserFactory()
        with self.assertRaises(Http404):
            topics(request, 'nl')

    def test_valid_languages(self):
        request = self.factory.get('/collection_tool/topics/language/en/')
        request.user = UserFactory()
        response = topics(request, 'en')
        self.assertEqual(response.status_code, 200)
        response = topics(request, 'es')
        self.assertEqual(response.status_code, 200)


class TestGoals(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get('/collection_tool/goals/language/en/')
        request.user = AnonymousUser()
        response = goals(request)
        self.assertEqual(response.status_code, 302)

    def test_invalid_language(self):
        request = self.factory.get('/collection_tool/goals/language/nl/')
        request.user = UserFactory()
        with self.assertRaises(Http404):
            goals(request, 'nl')

    def test_valid_languages(self):
        request = self.factory.get('/collection_tool/goals/language/en/')
        request.user = UserFactory()
        response = goals(request, 'en')
        self.assertEqual(response.status_code, 200)
        response = goals(request, 'es')
        self.assertEqual(response.status_code, 200)
