from smilekit.family_info.models import Family, Visit
from smilekit.family_info.models import Response
from smilekit.equation_balancer.models import Configuration, Question, Answer
from smilekit.equation_balancer.models import Module
from django.contrib.auth.models import User

import factory


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: "user%d" % n)


class InterviewerFactory(UserFactory):
    username = "interviewer"


class ConfigurationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Configuration
    owner = factory.SubFactory(UserFactory)
    name = "testconfig"


class FamilyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Family
    config = factory.SubFactory(ConfigurationFactory)
    study_id_number = 1


class VisitFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Visit
    interviewer = factory.SubFactory(InterviewerFactory)


class ModuleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Module
    name = "module 1"


class QuestionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Question
    module = factory.SubFactory(ModuleFactory)
    number = 1


class AnswerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Answer
    question = factory.SubFactory(QuestionFactory)
    weight = 0


class ResponseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Response
    family = factory.SubFactory(FamilyFactory)
    during_visit = factory.SubFactory(VisitFactory)
    question = factory.SubFactory(QuestionFactory)
    answer = factory.SubFactory(AnswerFactory,
                                question=factory.SelfAttribute('..question'))
