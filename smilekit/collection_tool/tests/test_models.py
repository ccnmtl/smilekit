from smilekit.collection_tool.models import most_frequent_item, HelpItem
from smilekit.collection_tool.models import HelpUrl, HelpBulletPoint
from smilekit.collection_tool.models import HelpDefinition
from django.test import TestCase


class TestMostFrequentItem(TestCase):
    def test_bailout(self):
        r = most_frequent_item([])
        self.assertIsNone(r)

    def test_populated(self):
        alist = [1, 1, 1, 2, 2, 3]
        r = most_frequent_item(alist)
        self.assertEqual(r, 1)

    def test_single(self):
        alist = [1]
        r = most_frequent_item(alist)
        self.assertEqual(r, 1)


class TestHelpItem(TestCase):
    def test_unicode(self):
        h = HelpItem.objects.create()
        self.assertEqual(str(h), "(no title)")
        h.english_title = "foo"
        h.save()
        self.assertEqual(str(h), "foo")

    def test_dir(self):
        h = HelpItem.objects.create()
        self.assertEqual(h.dir, dir(h))


def helpurl_factory():
    hi = HelpItem.objects.create()
    return HelpUrl(help_item=hi)


class TestHelpUrl(TestCase):
    def test_unicode(self):
        h = helpurl_factory()
        h.url = "foo"
        h.save()
        self.assertEqual(str(h), "foo")

    def test_dir(self):
        h = helpurl_factory()
        self.assertEqual(h.dir, dir(h))


def helpbulletpoint_factory():
    hi = HelpItem.objects.create()
    return HelpBulletPoint(help_item=hi, ordering_rank=1)


class HelpBulletPointTest(TestCase):
    def test_dir(self):
        hbp = helpbulletpoint_factory()
        self.assertEqual(hbp.dir, dir(hbp))


def helpdefinition_factory():
    hi = HelpItem.objects.create()
    return HelpDefinition(help_item=hi, ordering_rank=1)


class HelpDefinitionTest(TestCase):
    def test_dir(self):
        hd = helpdefinition_factory()
        self.assertEqual(hd.dir, dir(hd))
