import factory
from smilekit.family_info.tests.factories import UserFactory
from smilekit.equation_balancer.models import (
    Configuration, Module, Question)


class ConfigurationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Configuration
    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: "configuration %d" % n)


class ModuleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Module
    name = factory.Sequence(lambda n: "module %d" % n)


class QuestionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Question
    module = factory.SubFactory(ModuleFactory)
    number = factory.Sequence(lambda n: n)
    text = "some question text"
