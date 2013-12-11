from django.test import TestCase
from django.test.client import Client
from smilekit.family_info.views import default_family_form_vars
from .factories import UserFactory


class DefaultFamilyFormVarsTest(TestCase):
    def test_basics(self):
        r = default_family_form_vars()
        self.assertEqual(r['equation_balancer_configs'].count(), 0)


class LoggedInViewsTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = UserFactory()
        self.u.set_password("test")
        self.u.save()
        self.c.login(username=self.u.username, password="test")

    def test_families(self):
        r = self.c.get("/family_info/families/")
        self.assertEqual(r.status_code, 200)
