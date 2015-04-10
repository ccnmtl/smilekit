from django.db import models
import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import smilekit.collection_tool as ct


# configurations
class Configuration(models.Model):

    """A set of weights associated with questions and groups of questions"""
    @property
    def dir(self):
        return dir(self)

    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def weights_greater_than_zero(self):
        return self.weight_set.filter(weight__gt=0)

    def questions_with_weights_greater_than_zero(self):
        return [w.question for w in self.weights_greater_than_zero()]

    @property
    def scores_for_all_questions(self):
        """A helper function used on the risk page to calculate scores."""
        return json.dumps(self.scores_for_all_questions_raw)

    @property
    def scores_for_all_questions_raw(self):
        """A helper function used on the risk page to calculate scores."""
        mins = {}
        maxs = {}
        scores = {}
        for w in self.weight_set.all():
            q = w.question
            module = q.module
            # get weight of this module for this config:
            try:
                module_weight = float(
                    self.moduleweight_set.get(
                        module=module).weight)
            except ModuleWeight.DoesNotExist:
                module_weight = 0.0
            question_weight = float(w.weight) * float(module_weight)
            qmin = q.min_answer_weight
            qmax = q.max_answer_weight
            for answer in q.answer_set.all():
                scores[answer.id] = round(
                    float(answer.weight) * question_weight,
                    3)
                mins[answer.id] = round(
                    qmin * question_weight,
                    3)
                maxs[answer.id] = round(
                    qmax * question_weight,
                    3)
        return_value = {'min': mins, 'max': maxs, 'score': scores}
        return return_value

    def display_questions(self):
        """This is the recipe for determining which display questions will
        be asked if a configuration is chosen."""

        nwq = self.questions_with_weights_greater_than_zero()
        nonzero_weight_questions = nwq
        result = []
        all_questions = []

        # order all questions, first by nav section, then by rank within that
        # section:
        for s in ct.models.AssessmentSection.objects.all():
            all_questions.extend(s.displayquestion_set.all())

        # now filter out the ones with weight zero, except if they're special.
        for display_question in all_questions:
            if display_question.display_regardless_of_weight:
                result.append(display_question)
            else:
                if display_question.question in nonzero_weight_questions:
                    result.append(display_question)

        return result

    def configuration_first_display_question(self):
        them = self.display_questions()
        return them[0]

    def url_list(self):
        """A list of URLs to visit for each configuration. This will be
        used for navigation."""
        from smilekit.collection_tool.views import intro as intro_view
        from smilekit.collection_tool.views import question as question_view
        from smilekit.collection_tool.views import section as section_view
        from smilekit.collection_tool.views import risk as risk_view

        language_codes = ['en', 'es']
        result = []
        nwq = self.questions_with_weights_greater_than_zero()
        nonzero_weight_questions = nwq
        result.append(language_url_dict(language_codes, intro_view))
        for s in ct.models.AssessmentSection.objects.all():
            result.append(
                language_url_dict(
                    language_codes,
                    section_view,
                    'section_id',
                    s.id))
            for dq in s.displayquestion_set.all():
                if dq.display_regardless_of_weight:
                    result.append(
                        language_url_dict(
                            language_codes,
                            question_view,
                            'displayquestion_id',
                            dq.id))
                else:
                    if dq.question in nonzero_weight_questions:
                        result.append(
                            language_url_dict(
                                language_codes,
                                question_view,
                                'displayquestion_id',
                                dq.id))
        result.append(language_url_dict(language_codes, risk_view))
        return result


def language_url_dict(
        language_codes, view, item_label=None, item_id=None):
    """ a common pattern: returns something that looks like :
    {   'en': '/collection_tool/section/2/language/en/',
        'es': '/collection_tool/section/2/language/es/'  }
    """
    result = {}
    for lc in language_codes:
        if item_label:
            result[lc] = reverse(
                view,
                kwargs={item_label: item_id,
                        'language_code': lc})
        else:
            result[lc] = reverse(view, kwargs={'language_code': lc})
    return result


class Module(models.Model):

    """ A set of questions that can be weighted as a group for a given
    configuration."""

    @property
    def dir(self):
        return dir(self)

    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=30, unique=True)


class ModuleWeight(models.Model):
    """The relative importance of a module's questions for a
    particular configuration"""

    @property
    def dir(self):
        return dir(self)

    config = models.ForeignKey(Configuration)
    module = models.ForeignKey(Module)
    unique_together = (("config", "module"),)

    def __unicode__(self):
        return "%s: %s" % (self.module.name, self.weight)

    weight = models.DecimalField(decimal_places=3, max_digits=10)


class Question(models.Model):

    @property
    def dir(self):
        return dir(self)

    def __unicode__(self):
        return "%s: %s" % (self.number, self.text)

    TYPE_CHOICES = (
        (u'T', u'Text Input'),
        (u'M', u'Multiple Choice'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    module = models.ForeignKey(Module)
    number = models.IntegerField()
    text = models.CharField(max_length=500)

    @property
    def all_answer_weights(self):
        return [a.weight for a in self.answer_set.all()]

    @property
    def max_answer_weight(self):
        return float(max(self.all_answer_weights))

    @property
    def min_answer_weight(self):
        return float(min(self.all_answer_weights))

    @property
    def show_planner(self):
        return (
            self.text.lower(
            ) in ["number risky exposures",
                  "fluoride rinse exposures",
                  "children's daily toothbrushing"]
        )

    class Meta:
        ordering = ['number']

    # empty for a fill-in-the-blank question; list of choices otherwise
    # examples:
    # {'yes':1, 'no':-1}  # yes is a good thing e.g. brushing teeth
    # {'yes':-1, 'no':1}  # no is a good thing e.g. eating candy
    # {'always':2, 'sometimes':1, 'never':-1}  # same idea


class Weight(models.Model):

    """The relative importance of a question in a given configuration"""
    @property
    def dir(self):
        return dir(self)

    config = models.ForeignKey(Configuration)
    question = models.ForeignKey(Question)
    unique_together = (("config", "question"),)

    def __unicode__(self):
        return "%s: %s" % (self.question.number, self.weight)

    weight = models.DecimalField(decimal_places=3, max_digits=10)


class Answer(models.Model):

    @property
    def dir(self):
        return dir(self)

    def __unicode__(self):
        return "%s: %s (%s)" % (self.question.text, self.text, self.weight)

    question = models.ForeignKey(Question)
    text = models.CharField(max_length=500)

    # this weight is the researcher's estimated risk of answers for
    # each question: a lower weight denotes a low risk, a high rate
    # denotes a high risk.  Note that these weights DO NOT change from
    # config to config.
    weight = models.DecimalField(decimal_places=3, max_digits=10)

    # Note: ordering is done via the display questions.
