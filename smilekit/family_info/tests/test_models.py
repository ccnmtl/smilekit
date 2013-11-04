from smilekit.family_info.models import friendly_score
from django.test import TestCase


class FriendlyScoreTest(TestCase):
    def test_bailout(self):
        r = friendly_score(0, 0, 0)
        self.assertIsNone(r)
