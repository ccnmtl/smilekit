from smilekit.collection_tool.models import most_frequent_item, HelpItem
from smilekit.collection_tool.models import HelpUrl, HelpBulletPoint
from smilekit.collection_tool.models import HelpDefinition
from django.test import TestCase
from .factories import TopicFactory, GoalFactory


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


class TopicTest(TestCase):
    def test_unicode(self):
        t = TopicFactory()
        self.assertEqual(str(t), "hello")

    def test_display_questions(self):
        t = TopicFactory()
        self.assertEqual(t.display_questions, [])

    def test_displayquestions_string(self):
        t = TopicFactory()
        self.assertEqual(t.displayquestions_string, "")

    def test_section(self):
        t = TopicFactory()
        self.assertIsNone(t.section)

    def test_dir(self):
        t = TopicFactory()
        self.assertTrue('dir' in t.dir)

    def test_answers(self):
        t = TopicFactory()
        self.assertEqual(t.answers, [])

    def test_scoring_info(self):
        t = TopicFactory()
        self.assertEqual(t.scoring_info, "{}")

    def test_scoring_info_object(self):
        t = TopicFactory()
        self.assertEqual(t.scoring_info_object, {})

    def test_maxmin_scoring_info(self):
        t = TopicFactory()
        self.assertEqual(t.maxmin_scoring_info, "{}")

    def test_maxmin_scoring_info_object(self):
        t = TopicFactory()
        self.assertEqual(t.maxmin_scoring_info_object, {})

    def test_question_count(self):
        t = TopicFactory()
        self.assertEqual(t.question_count, 0)

    def test_learn_more_english(self):
        t = TopicFactory()
        self.assertIsNone(t.learn_more_english)

    def test_learn_more_spanish(self):
        t = TopicFactory()
        self.assertIsNone(t.learn_more_spanish)


class GoalTest(TestCase):
    def test_dir(self):
        g = GoalFactory()
        self.assertTrue('dir' in g.dir)

    def test_help_item(self):
        g = GoalFactory()
        self.assertIsNone(g.help_item)
