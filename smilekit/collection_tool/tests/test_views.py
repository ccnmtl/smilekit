from django.test import TestCase
from smilekit.collection_tool.views import get_help_item


class TestGetHelpItem(TestCase):
    def test_none_found(self):
        r = get_help_item("foo")
        self.assertIsNone(r)
