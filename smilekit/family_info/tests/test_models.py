from smilekit.family_info.models import friendly_score, Family, Visit
from smilekit.family_info.models import Response
from smilekit.equation_balancer.models import Configuration, Question, Answer
from smilekit.equation_balancer.models import Module
from django.contrib.auth.models import User
from django.test import TestCase


class FriendlyScoreTest(TestCase):
    def test_bailout(self):
        r = friendly_score(0, 0, 0)
        self.assertIsNone(r)

    def test_regular_case(self):
        r = friendly_score(0.0, 5.0, 10.0)
        self.assertEqual(r, 6.0)


def family_factory():
    u = User.objects.create(username="testuser")
    c = Configuration.objects.create(owner=u, name="testconfig")
    return Family.objects.create(config=c, study_id_number=1)


class FamilyTest(TestCase):
    def test_start_interview_info(self):
        f = family_factory()
        self.assertIsNotNone(f.start_interview_info)

    def test_dir(self):
        f = family_factory()
        self.assertEqual(f.dir, dir(f))

    def test_unicode(self):
        f = family_factory()
        self.assertEqual(str(f), "Family # 1")

    def test_planner_data_summary(self):
        f = family_factory()
        self.assertEqual(f.planner_data_summary, [])

    def test_all_visits(self):
        f = family_factory()
        self.assertEqual(f.all_visits, [])

    def test_in_a_visit(self):
        f = family_factory()
        self.assertFalse(f.in_a_visit)

    def test_visits_happening(self):
        f = family_factory()
        self.assertEqual(f.visits_happening, [])

    def test_has_had_an_interview(self):
        f = family_factory()
        self.assertFalse(f.has_had_an_interview)

    def test_config_locked(self):
        f = family_factory()
        self.assertFalse(f.config_locked)

    def test_interviewer(self):
        f = family_factory()
        self.assertIsNone(f.interviewer)

    def test_latest_answers(self):
        f = family_factory()
        self.assertEqual(f.latest_answers, {})

    def test_goal_info(self):
        f = family_factory()
        self.assertEqual(f.goal_info, {})

    def test_answerable_questions(self):
        f = family_factory()
        self.assertEqual(f.answerable_questions, [])

    def test_recent_visits(self):
        f = family_factory()
        self.assertEqual(f.recent_visits, [])

    def test_has_recent_visits(self):
        f = family_factory()
        self.assertFalse(f.has_recent_visits)

    def test_percent_complete_cache_key(self):
        f = family_factory()
        self.assertTrue(
            f.percent_complete_cache_key.startswith("family_percent_done_"))

    def test_percent_complete(self):
        f = family_factory()
        self.assertIsNone(f.percent_complete)

    def test_risk_score(self):
        f = family_factory()
        self.assertIsNone(f.risk_score)

    def test_set_state(self):
        f = family_factory()
        self.assertEqual(f.state, u'{}')
        f.set_state(u'{"foo": "bar"}')
        self.assertEqual(f.state, u'{"foo": "bar"}')

    def test_state(self):
        f = family_factory()
        self.assertEqual(f.state, u'{}')

    def test_evil_state(self):
        f = family_factory()
        self.assertEqual(f.evil_state, u'{}')

    def test_responses(self):
        f = family_factory()
        self.assertEqual(f.responses().count(), 0)


def visit_factory():
    i = User.objects.create(username="interviewer")
    return Visit.objects.create(interviewer=i)


class VisitTest(TestCase):
    def test_dir(self):
        v = visit_factory()
        self.assertEqual(v.dir, dir(v))

    def test_unicode(self):
        v = visit_factory()
        self.assertTrue(str(v).startswith("Visit "))

    def test_is_happening(self):
        v = visit_factory()
        self.assertTrue(v.is_happening)
        v.close_now()
        self.assertFalse(v.is_happening)


def response_factory():
    f = family_factory()
    v = visit_factory()
    m = Module.objects.create(name="module 1")
    q = Question.objects.create(module=m, number=1)
    a = Answer.objects.create(question=q, weight=0)
    return Response.objects.create(
        during_visit=v,
        family=f,
        question=q,
        answer=a,
    )


class ResponseTest(TestCase):
    def test_dir(self):
        r = response_factory()
        self.assertEqual(r.dir, dir(r))

    def test_answer_english(self):
        r = response_factory()
        self.assertEqual(r.answer_english, "")

    def test_interviewer(self):
        r = response_factory()
        self.assertEqual(r.interviewer, "")

    def test_module(self):
        r = response_factory()
        self.assertEqual(r.module, "module 1")

    def test_answer_weight(self):
        r = response_factory()
        self.assertEqual(r.answer_weight, 0)

    def id_of_question(self):
        r = response_factory()
        self.assertEqual(r.id_of_question, r.question.id)

    def id_of_answer(self):
        r = response_factory()
        self.assertEqual(r.id_of_answer, r.answer.id)

    def id_of_family(self):
        r = response_factory()
        self.assertEqual(r.id_of_family, 1)
