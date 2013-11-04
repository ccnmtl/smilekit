from django.test import TestCase
from smilekit.family_info.views import default_family_form_vars


class DefaultFamilyFormVarsTest(TestCase):
    def test_basics(self):
        r = default_family_form_vars()
        self.assertEqual(r['equation_balancer_configs'].count(), 0)
