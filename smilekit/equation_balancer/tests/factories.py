import factory
from smilekit.equation_balancer.models import (
    Module, Question)


class ModuleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Module
    name = factory.Sequence(lambda n: "module %d" % n)


class QuestionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Question
    module = factory.SubFactory(ModuleFactory)
    number = factory.Sequence(lambda n: n)
    text = "some question text"
