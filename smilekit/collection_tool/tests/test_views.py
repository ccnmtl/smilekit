from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from smilekit.collection_tool.views import (
    get_help_item, intro, risk, topics, goals, manifest, goal,
    goal_planner, section, question
)
from smilekit.family_info.tests.factories import UserFactory
from smilekit.equation_balancer.tests.factories import QuestionFactory
from .factories import (
    GoalFactory, AssessmentSectionFactory, DisplayQuestionFactory
)


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


class TestGoal(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_invalid_language(self):
        request = self.factory.get('/collection_tool/goal/00/language/nl/')
        request.user = UserFactory()
        with self.assertRaises(Http404):
            goal(request, 0, 'nl')

    def test_goal(self):
        g = GoalFactory()
        request = self.factory.get(
            '/collection_tool/goal/%d/language/en/' % g.pk)
        request.user = UserFactory()
        response = goal(request, g.pk, 'en')
        self.assertEqual(response.status_code, 200)


class TestGoalPlanner(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_invalid_language(self):
        request = self.factory.get(
            '/collection_tool/planner/goal/00/language/nl/')
        request.user = UserFactory()
        with self.assertRaises(Http404):
            goal_planner(request, 0, 'nl')

    def test_goal_planner(self):
        g = GoalFactory()
        request = self.factory.get(
            '/collection_tool/planner/goal/%d/language/en/' % g.pk)
        request.user = UserFactory()
        response = goal_planner(request, g.pk, 'en')
        self.assertEqual(response.status_code, 200)


class TestSection(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_invalid_language(self):
        request = self.factory.get(
            '/collection_tool/section/00/language/nl/')
        request.user = UserFactory()
        with self.assertRaises(Http404):
            section(request, 0, 'nl')

    def test_section(self):
        s = AssessmentSectionFactory()
        request = self.factory.get(
            '/collection_tool/section/%d/language/en/' % s.pk)
        request.user = UserFactory()
        response = section(request, s.pk, 'en')
        self.assertEqual(response.status_code, 200)


class TestQuestion(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_invalid_language(self):
        request = self.factory.get(
            '/collection_tool/question/00/language/nl/')
        request.user = UserFactory()
        with self.assertRaises(Http404):
            question(request, 0, 'nl')

    def test_section(self):
        QuestionFactory(text="number risky exposures")
        QuestionFactory(text="Fluoride rinse exposures")
        QuestionFactory(text="Children's daily toothbrushing")
        q = DisplayQuestionFactory(question=QuestionFactory())
        request = self.factory.get(
            '/collection_tool/question/%d/language/en/' % q.pk)
        request.user = UserFactory()
        response = question(request, q.pk, 'en')
        self.assertEqual(response.status_code, 200)


class TestManifest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_manifest(self):
        request = self.factory.get('/collection_tool/manifest.cache')
        request.user = AnonymousUser()
        response = manifest(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header('content-type'))
        self.assertEqual(response['content-type'], 'text/cache-manifest')
