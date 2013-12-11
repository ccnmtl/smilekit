from smilekit.family_info.models import friendly_score
from django.test import TestCase
from .factories import FamilyFactory, VisitFactory, ResponseFactory


class FriendlyScoreTest(TestCase):
    def test_bailout(self):
        r = friendly_score(0, 0, 0)
        self.assertIsNone(r)

    def test_regular_case(self):
        r = friendly_score(0.0, 5.0, 10.0)
        self.assertEqual(r, 6.0)


class FamilyTest(TestCase):
    def test_start_interview_info(self):
        f = FamilyFactory()
        self.assertIsNotNone(f.start_interview_info)

    def test_dir(self):
        f = FamilyFactory()
        self.assertEqual(f.dir, dir(f))

    def test_unicode(self):
        f = FamilyFactory()
        self.assertEqual(str(f), "Family # 1")

    def test_planner_data_summary(self):
        f = FamilyFactory()
        self.assertEqual(f.planner_data_summary, [])

    def test_all_visits(self):
        f = FamilyFactory()
        self.assertEqual(f.all_visits, [])

    def test_in_a_visit(self):
        f = FamilyFactory()
        self.assertFalse(f.in_a_visit)

    def test_visits_happening(self):
        f = FamilyFactory()
        self.assertEqual(f.visits_happening, [])

    def test_has_had_an_interview(self):
        f = FamilyFactory()
        self.assertFalse(f.has_had_an_interview)

    def test_config_locked(self):
        f = FamilyFactory()
        self.assertFalse(f.config_locked)

    def test_interviewer(self):
        f = FamilyFactory()
        self.assertIsNone(f.interviewer)

    def test_latest_answers(self):
        f = FamilyFactory()
        self.assertEqual(f.latest_answers, {})

    def test_goal_info(self):
        f = FamilyFactory()
        self.assertEqual(f.goal_info, {})

    def test_answerable_questions(self):
        f = FamilyFactory()
        self.assertEqual(f.answerable_questions, [])

    def test_recent_visits(self):
        f = FamilyFactory()
        self.assertEqual(f.recent_visits, [])

    def test_has_recent_visits(self):
        f = FamilyFactory()
        self.assertFalse(f.has_recent_visits)

    def test_percent_complete_cache_key(self):
        f = FamilyFactory()
        self.assertTrue(
            f.percent_complete_cache_key.startswith("family_percent_done_"))

    def test_percent_complete(self):
        f = FamilyFactory()
        self.assertIsNone(f.percent_complete)

    def test_risk_score(self):
        f = FamilyFactory()
        self.assertIsNone(f.risk_score)

    def test_set_state(self):
        f = FamilyFactory()
        self.assertEqual(f.state, u'{}')
        f.set_state(u'{"foo": "bar"}')
        self.assertEqual(f.state, u'{"foo": "bar"}')

    def test_state(self):
        f = FamilyFactory()
        self.assertEqual(f.state, u'{}')

    def test_evil_state(self):
        f = FamilyFactory()
        self.assertEqual(f.evil_state, u'{}')

    def test_responses(self):
        f = FamilyFactory()
        self.assertEqual(f.responses().count(), 0)


class VisitTest(TestCase):
    def test_dir(self):
        v = VisitFactory()
        self.assertEqual(v.dir, dir(v))

    def test_unicode(self):
        v = VisitFactory()
        self.assertTrue(str(v).startswith("Visit "))

    def test_is_happening(self):
        v = VisitFactory()
        self.assertTrue(v.is_happening)
        v.close_now()
        self.assertFalse(v.is_happening)


class ResponseTest(TestCase):
    def test_dir(self):
        r = ResponseFactory()
        self.assertEqual(r.dir, dir(r))

    def test_answer_english(self):
        r = ResponseFactory()
        self.assertEqual(r.answer_english, "")

    def test_interviewer(self):
        r = ResponseFactory()
        self.assertEqual(r.interviewer, "")

    def test_module(self):
        r = ResponseFactory()
        self.assertEqual(r.module, "module 1")

    def test_answer_weight(self):
        r = ResponseFactory()
        self.assertEqual(r.answer_weight, 0)

    def test_id_of_question(self):
        r = ResponseFactory()
        self.assertEqual(r.id_of_question, r.question.id)

    def test_id_of_answer(self):
        r = ResponseFactory()
        self.assertEqual(r.id_of_answer, r.answer.id)

    def test_id_of_family(self):
        r = ResponseFactory()
        self.assertEqual(r.id_of_family, 1)
