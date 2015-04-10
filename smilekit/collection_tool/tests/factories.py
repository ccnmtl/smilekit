import factory
from smilekit.collection_tool.models import (
    Topic, Goal, AssessmentSection, Resource, PlannerItem,
    DisplayQuestion,
)


class TopicFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Topic
    english_title = "hello"
    spanish_title = "hola"
    english_description = "english description"
    spanish_description = "spanish description"
    ordering_rank = 1


class GoalFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Goal
    english_title = "english title"
    spanish_title = "spanish title"
    english_description = "english description"
    spanish_description = "spanish description"
    topic = factory.SubFactory(TopicFactory)
    ordering_rank = 1


class AssessmentSectionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AssessmentSection
    title = "assessmentsection"
    english_title = "english title"
    spanish_title = "spanish title"
    english_description = "english description"
    spanish_description = "spanish description"
    ordering_rank = 1


class ResourceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Resource
    name = "resource"
    url = "/resource/"
    resource_type = ""
    ordering_rank = 1


class PlannerItemFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PlannerItem
    type = "A"
    label = "planner item"
    spanish_label = "spanish planner item"
    risk_level = 1


class DisplayQuestionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = DisplayQuestion
    ordering_rank = 1
