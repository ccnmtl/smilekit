import factory
from smilekit.collection_tool.models import Topic


class TopicFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Topic
    english_title = "hello"
    spanish_title = "hola"
    english_description = "english description"
    spanish_description = "spanish description"
    ordering_rank = 1
