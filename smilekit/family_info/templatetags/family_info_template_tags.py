from django import template
from djangohelpers.templatetags import TemplateTagNode

from smilekit.family_info.models import Family, Response
from smilekit.collection_tool.models import DisplayQuestion


register = template.Library()


class GetAnswer(TemplateTagNode):
    noun_for = {
        'of_family': 'family_id',
        'to_question': 'display_question_id'
    }

    def __init__(self, varname, display_question_id, family_id):
        TemplateTagNode.__init__(
            self, varname,
            display_question_id=display_question_id, family_id=family_id)

    def execute_query(self, display_question_id, family_id):
        f = Family.objects.get(pk=family_id)
        q = DisplayQuestion.objects.get(pk=display_question_id).question
        responses = Response.objects.filter(family=f, question=q)
        if responses.count() == 0:
            return None
        return list(responses)[-1]
register.tag('get_answer', GetAnswer.process_tag)


def get_goal_info(family, goal_number):
    try:
        return family.goal_info.values()[goal_number]
    except:
        return {}


class GetGoalInfo1(TemplateTagNode):
    noun_for = {'of_family': 'family_id'}

    def __init__(self, varname, family_id):
        TemplateTagNode.__init__(self, varname, family_id=family_id)

    def execute_query(self,  family_id):
        f = Family.objects.get(pk=family_id)
        return get_goal_info(f, 0)
register.tag('get_goal_info_1', GetGoalInfo1.process_tag)


class GetGoalInfo2(TemplateTagNode):
    noun_for = {'of_family': 'family_id'}

    def __init__(self, varname, family_id):
        TemplateTagNode.__init__(self, varname, family_id=family_id)

    def execute_query(self,  family_id):
        f = Family.objects.get(pk=family_id)
        return get_goal_info(f, 1)
register.tag('get_goal_info_2', GetGoalInfo2.process_tag)


class GetGoalInfo3(TemplateTagNode):
    noun_for = {'of_family': 'family_id'}

    def __init__(self, varname, family_id):
        TemplateTagNode.__init__(self, varname, family_id=family_id)

    def execute_query(self, family_id):
        f = Family.objects.get(pk=family_id)
        return get_goal_info(f, 2)
register.tag('get_goal_info_3', GetGoalInfo3.process_tag)
