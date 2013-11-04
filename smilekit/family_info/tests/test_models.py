from smilekit.family_info.models import friendly_score
from django.test import TestCase


class FriendlyScoreTest(TestCase):
    def test_bailout(self):
        r = friendly_score(0, 0, 0)
        self.assertIsNone(r)

    def test_regular_case(self):
        r = friendly_score(0.0, 5.0, 10.0)
        self.assertEqual(r, 6.0)
