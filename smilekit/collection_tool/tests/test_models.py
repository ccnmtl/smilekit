from smilekit.collection_tool.models import most_frequent_item
from django.test import TestCase


class TestMostFrequentItem(TestCase):
    def test_bailout(self):
        r = most_frequent_item([])
        self.assertIsNone(r)
