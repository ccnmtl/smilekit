from django.db import models
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
import simplejson as json
from smilekit.equation_balancer.models import (
    ModuleWeight, Question, Answer, Configuration)
from django.contrib.flatpages.models import FlatPage


LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('es', 'Spanish'),
)

# HELP AND TOPICS####


class HelpItem(models.Model):
    english_objective = models.CharField(
        max_length=1024,
        null=True,
        blank=True)
    spanish_objective = models.CharField(
        max_length=1024,
        null=True,
        blank=True)
    english_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True)
    spanish_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True)

    english_script = models.TextField(
        null=True,
        blank=True,
        help_text="Basic script to follow")
    english_script_instructions = models.TextField(
        null=True,
        blank=True,
        verbose_name="English - More Details",
        help_text="More details about this subject")

    spanish_script = models.TextField(
        null=True,
        blank=True,
        help_text="Basic script to follow")
    spanish_script_instructions = models.TextField(
        null=True,
        blank=True,
        verbose_name="Spanish - More Details",
        help_text="More details about this question")

    def __unicode__(self):
        if self.english_title:
            return self.english_title
        return "(no title)"

    @property
    def dir(self):
        # print self
        return dir(self)


class HelpUrl(models.Model):

    """Associates a help item with an arbitrary URL."""
    url = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        help_text="Include leading and trailing slashes, please.")
    help_item = models.ForeignKey(HelpItem)

    def __unicode__(self):
        return self.url

    @property
    def dir(self):
        return dir(self)


class HelpBulletPoint(models.Model):
    """Displayed as a bullet-point list, these give a summary / what
    to watch for each page."""
    english_text = models.TextField(null=True, blank=True)
    spanish_text = models.TextField(null=True, blank=True)
    help_item = models.ForeignKey(HelpItem)

    ordering_rank = models.IntegerField()

    class Meta:
        ordering = ('ordering_rank',)

    @property
    def dir(self):
        return dir(self)


class HelpDefinition(models.Model):

    """Definitions."""
    english_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True)
    english_body = models.TextField(null=True, blank=True)
    spanish_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True)
    spanish_body = models.TextField(null=True, blank=True)
    help_item = models.ForeignKey(HelpItem)

    ordering_rank = models.IntegerField()

    class Meta:
        ordering = ('ordering_rank',)

    @property
    def dir(self):
        return dir(self)


def most_frequent_item(alist):
    frequencies = [(a, alist.count(a)) for a in set(alist)]
    if frequencies:
        return sorted(frequencies, key=lambda x: -x[1])[0][0]
    return None


def dquestions_for_config_and_topic(config, topic):
        # don't count the planner questions for now:
    topic_dquestions = [
        dq.id for dq in topic.display_questions if dq.nav_section is not None]
    config_dquestions = [
        dq.id for dq in config.display_questions(
        ) if dq.nav_section is not None]
    return [a for a in topic_dquestions if a in config_dquestions]


class Topic(models.Model):

    """an aspect of the patient's health that can be improved"""

    def __unicode__(self):
        return self.english_title

    english_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True)
    spanish_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True)

    english_description = models.TextField(null=True, blank=True)
    spanish_description = models.TextField(null=True, blank=True)

    ordering_rank = models.IntegerField()

    class Meta:
        ordering = ('ordering_rank',)

    @property
    def displayquestions_string(self):
        return (
            ";".join(["%d: %s" % (t.id, t.english)
                     for t in self.display_questions])
        )

    @property
    def display_questions(self):
        return [dq for dq in self.displayquestion_set.all() if dq.nav_section]

    @property
    def section(self):
        sections = [dq.nav_section for dq in self.display_questions]
        if sections:
            return most_frequent_item(sections)
        return None

    @property
    def dir(self):
        return dir(self)

    @property
    def answers(self):
        """used for scoring the topic"""
        dquestions = self.displayquestion_set.all()
        all_answers = []
        for dq in dquestions:
            all_answers.extend(dq.question.answer_set.all())
        all_answers.sort()
        return all_answers

    @property
    def scoring_info(self):
        return json.dumps(self.scoring_info_object)

    @property
    def scoring_info_object(self):
        return (
            dict([(config.id, self.config_scoring_info(config))
                  for config in Configuration.objects.all()])
        )

    # self is a topic.
    def config_scoring_info(self, config):
        result = {}
        overall_weight = 0
        old_weighting_system = False

        # Changing the weighting system for topics, per action item #72345
        if old_weighting_system:
            try:
                overall_weight = config.moduleweight_set.get(
                    module=self).weight
            except ModuleWeight.DoesNotExist:
                pass
            except ModuleWeight.MultipleObjectsReturned:
                # Only one weight per module please.  This should be
                # enforced by the equation balancer. See bug 72244.  I
                # want this to fail loudly and immediately.
                raise

            for the_answer in self.answers:
                try:
                    question_weight = config.weight_set.get(
                        question=the_answer.question).weight
                except:
                    question_weight = 0
                result[the_answer.id] = float(
                    the_answer.weight *
                    question_weight *
                    overall_weight)

        else:  # new weighting system ignores question and config weights.
            for the_answer in self.answers:
                result[the_answer.id] = float(the_answer.weight)

        result['question_count'] = len(
            dquestions_for_config_and_topic(config, self))
        return result

    @property
    def maxmin_scoring_info(self):
        """format is: {  config.id : { "max" : { answer.id : max,
           answer.id: max ... }, "min" : {answer.id : min , ... }, ...}, ... }
        """

        return json.dumps(self.maxmin_scoring_info_object)

    @property
    def maxmin_scoring_info_object(self):
        """ For all configurations and all answers, show the best and
        worst possible scores."""
        return (
            dict([(config.id, self.config_maxmin_scores(config))
                  for config in Configuration.objects.all()])
        )

    def config_maxmin_scores(self, config):
        """for each answer in a configuration, show the best and worst
        possible scores."""
        # Changing the weighting system for topics, per action item #72345
        old_weighting_system = False
        mins = {}
        maxs = {}

        if old_weighting_system:
            try:
                overall_weight = float(
                    config.moduleweight_set.get(module=self).weight)
            except ModuleWeight.DoesNotExist:
                overall_weight = 0.0
            for dq in self.displayquestion_set.all():
                try:
                    question_weight = float(
                        config.weight_set.get(
                            question=dq.question).weight)
                except:
                    question_weight = 0.0
                for answer in dq.question.answer_set.all():
                    mins[answer.id] = dq.question.min_answer_weight * \
                        question_weight * overall_weight
                    maxs[answer.id] = dq.question.max_answer_weight * \
                        question_weight * overall_weight
        else:  # new weighting system ignores question and config weights.
            for dq in self.displayquestion_set.all():
                for answer in dq.question.answer_set.all():
                    mins[answer.id] = dq.question.min_answer_weight
                    maxs[answer.id] = dq.question.max_answer_weight

        return_value = {'min': mins, 'max': maxs}

        if sum(mins.values()) == sum(maxs.values()):
            return_value['irrelevant'] = 'true'
            # special case: for this topic and this config, no matter
            # how many questions you answer, you can't obtain a score
            # due to the weights assigned the questions.
        else:
            return_value['irrelevant'] = 'false'

        return return_value

    @property
    def question_count(self):
        return len(self.displayquestion_set.all())

    @property
    def learn_more_english(self):
        learn_more_list = [
            dq.learn_more for dq in self.displayquestion_set.all(
            ) if dq.learn_more is not None]
        if learn_more_list:
            return learn_more_list[0]
        return None

    @property
    def learn_more_spanish(self):
        learn_more_list = [
            dq.learn_more_spanish for dq in self.displayquestion_set.all(
            ) if dq.learn_more_spanish is not None]
        if learn_more_list:
            return learn_more_list[0]
        return None


class Goal (models.Model):

    """ one concrete step in the direction of a topic"""

    english_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True)
    spanish_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True)

    english_description = models.TextField(null=True, blank=True)
    spanish_description = models.TextField(null=True, blank=True)

    topic = models.ForeignKey(Topic)

    show_in_planner = models.BooleanField(
        default=False,
        help_text=("i.e. does picking this goal mean the next "
                   "button takes you to the planner JS game?"))

    ordering_rank = models.IntegerField()

    class Meta:
        ordering = ('ordering_rank',)

    @property
    def dir(self):
        return dir(self)

    @property
    def help_item(self):
        try:
            help_url = HelpUrl.objects.filter(
                url__contains='goal/%d/' %
                self.id)[0].help_item
            return help_url
        except:
            return None
        return None


# END HELP AND TOPICS#######


class AssessmentSection(models.Model):

    """nav section that each question belongs to."""
    title = models.TextField(null=True, blank=True)

    english_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True)
    spanish_title = models.CharField(
        max_length=1024,
        null=True,
        blank=True)

    english_description = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        help_text=("a few English sentences that will appear at "
                   "the top of this index page."))
    spanish_description = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        help_text=("a few Spanish sentences that will appear "
                   "at the top of this index page."))

    ordering_rank = models.IntegerField()

    class Meta:
        ordering = ('ordering_rank',)

    @property
    def dir(self):
        return dir(self)

    def __unicode__(self):
        return self.title

    @property
    def help_item(self):
        try:
            return (
                HelpUrl.objects.filter(
                    url__contains='section/%d/' %
                    self.id)[0].help_item
            )
        except:
            return None
        return None


def configuration_display_questions(self):
    """This is the recipe for determining which display questions will
    be asked if a configuration is chosen."""

    nonzero_weight_questions = self.questions_with_weights_greater_than_zero()
    result = []
    all_questions = []

    # order all questions, first by nav section, then by rank within that
    # section:
    for s in AssessmentSection.objects.all():
        all_questions.extend(s.displayquestion_set.all())

    # now filter out the ones with weight zero, except if they're special.
    for display_question in all_questions:
        if display_question.display_regardless_of_weight:
            result.append(display_question)
        else:
            if display_question.question in nonzero_weight_questions:
                result.append(display_question)

    return result

# Duck-tape this method into the configuration model;
# although the method belongs that model,
# the code itself has more to do with display questions than with
# equation balancing, so it belongs here.


def configuration_first_display_question(self):
    them = self.display_questions()
    return them[0]


Configuration.display_questions = configuration_display_questions
Configuration.first_display_question = configuration_first_display_question


def language_url_dict(
        language_codes, view, item_label=None, item_id=None):
    """ a common pattern: returns something that looks like :
    {   'en': '/collection_tool/section/2/language/en/',
        'es': '/collection_tool/section/2/language/es/'  }
    """
    from django.core.urlresolvers import reverse
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


def configuration_url_list(self):
    """A list of URLs to visit for each configuration. This will be
    used for navigation."""
    from .views import intro as intro_view
    from .views import question as question_view
    from .views import section as section_view
    from .views import risk as risk_view

    language_codes = ['en', 'es']
    result = []
    nonzero_weight_questions = self.questions_with_weights_greater_than_zero()
    result.append(language_url_dict(language_codes, intro_view))
    for s in AssessmentSection.objects.all():
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

Configuration.url_list = configuration_url_list


def has_image(image_field_file):
    try:
        if image_field_file.url != "":
            return True
        else:
            return False
    except:
        return False
    return False


class Resource(models.Model):

    """just a wrapper for a URL (e.g. video, internal or external link)"""
    name = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    resource_type = models.CharField(
        max_length=64,
        help_text=("type 'video' here if this is a video; "
                   "otherwise just leave blank."))
    ordering_rank = models.IntegerField(help_text="Ignore this for now.")

    class Meta:
        ordering = ('ordering_rank',)

    @property
    def flat_page(self):
        try:
            return FlatPage.objects.get(url=self.url)
        except:
            return None

    @property
    def dir(self):
        return dir(self)

    @property
    def summary(self):
        resource_type = self.resource_type
        url = self.url
        my_flat_page = get_object_or_404(FlatPage, url=url)
        return {
            'url': my_flat_page.url,
            'resource_type': resource_type,
            'title': my_flat_page.title,
            'content': my_flat_page.content,
            'id': my_flat_page.id
        }

    def other_language_version(self, language_code):
        language_code_in_parentheses = '(%s)' % language_code
        candidates = Resource.objects.filter(
            name__contains=self.name
        ).filter(
            name__contains=language_code_in_parentheses)
        if candidates:
            return candidates[0]
        return self

    @property
    def spanish_version(self):
        return self.other_language_version('es')

    @property
    def english_version(self):
        return self.other_language_version('en')

    def __unicode__(self):
        return self.name


class DisplayQuestion(models.Model):

    """associates questions with translations, images, help topics, etc."""

    display_regardless_of_weight = models.BooleanField(
        help_text=("Check this to display this question (and store "
                   "answers to it) for all configurations, regardless "
                   "of the weight assigned to it."),
        default=False)

    question = models.ForeignKey(Question, null=True, blank=True)
    nav_section = models.ForeignKey(AssessmentSection, null=True, blank=True)

    topics = models.ManyToManyField(
        Topic,
        help_text="One or more topics this question is associated with.",
        null=True,
        blank=True)

    resources = models.ManyToManyField(
        Resource,
        help_text="Links to other pages that are relevant to this question.",
        null=True,
        blank=True)

    image = models.ImageField(
        upload_to='question_images',
        blank=True,
        null=True)

    ordering_rank = models.IntegerField(
        help_text=("Use this to determine the order in which the "
                   "questions are asked within each nav section."))

    class Meta:
        ordering = ('ordering_rank',)

    def get_absolute_url(self):
        return '/collection_tool/question/%d/language/en' % self.id

    @property
    def show_planner(self):
        return self.question.show_planner

    # not actually used:
    @property
    def question_type(self):
        return self.question.type

    # this violates DRY but guess what? I'm fine with that.
    @property
    def help_item(self):
        try:
            return (
                HelpUrl.objects.filter(
                    url__contains='question/%d/' %
                    self.id)[0].help_item
            )
        except:
            return None
        return None

    @property
    def has_question_picture(self):
        return has_image(self.image)

    @property
    def has_answer_pictures(self):
        if len(self.display_answers) == 0:
            return False

        if len([a.image for a in self.display_answers
                if has_image(a.image)]) == 0:
            return False

        return True

    @property
    def no_pictures(self):
        return (
            self.has_question_picture is False
            and self.has_answer_pictures is False
        )

    @property
    def display_answers(self):
        return (
            DisplayAnswer.objects.filter(
                answer__in=self.question.answer_set.all())
        )

    @property
    def answers(self):
        return self.question.answer_set.all()

    @property
    def weight_info(self):
        my_module = self.question.module
        results = []
        for qw in self.question.weight_set.all():
            module_weight = [
                mw.weight for mw in qw.config.moduleweight_set.all(
                ) if mw.module == my_module][0]
            results.append(
                (qw.config.id, qw.config.name, float(qw.weight),
                 float(module_weight),
                 float(qw.weight * module_weight)
                 ))
        return results

    @property
    def dir(self):
        return dir(self)

    @property
    def english(self):
        try:
            return Translation.objects.get(question=self, language='en').text
        except:
            return None

    @property
    def spanish(self):
        try:
            return Translation.objects.get(question=self, language='es').text
        except:
            return None

    def wording(self, preferred_language_code):
        """attempts to provide a wording in preferred language;
        otherwise return a language in an arbitrary language;
        otherwise returns a fixed string."""

        try:
            return (
                Translation.objects.get(
                    question=self,
                    language=preferred_language_code).text
            )
        except:
            pass

        try:
            return self.translation_set.all()[0].text
        except:
            pass
        return (
            "Sorry, no wordings provided in either language. "
            "Enter wordings at /admin/collection_tool/"
            "displayquestion/%d/" % self.id
        )

    @property
    def resource(self):
        """the content of some flat pages also need to be accessible
        from the question page in the collection tool. here's a simple
        way of doing this:"""
        if not self.resources.all():
            return None
        return self.resources.all()[0]

    # TODO: make this obsolete. Shoud use either of the functions below this
    # one.
    @property
    def learn_more(self):
        if self.resource:
            return self.resource.summary
        return None

    @property
    def learn_more_english(self):
        if self.resource:
            return self.resource.summary
        return None

    @property
    def learn_more_spanish(self):
        if self.resource:
            if self.resource.spanish_version:
                return self.resource.spanish_version.summary
            else:
                return self.resource.summary
        else:
            return None

    def __unicode__(self):
        """ Just the English."""
        try:
            return self.english
        except:
            return None


class Translation(models.Model):

    """ a question wording in a particular language"""
    question = models.ForeignKey(DisplayQuestion)
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        null=False)  # code for language (i.e. "EN", "ES")
    text = models.TextField(null=True, blank=True)


class DisplayAnswer(models.Model):

    """associates answers with images, help topics, etc."""

    # TODO: this isn't right: this should be a one-to-one mapping. there
    # should only be one display answer per answer. this shouln't be a foreign
    # key.
    # better to link to DB answer or DisplayQuestion?
    answer = models.ForeignKey(Answer)

    image = models.ImageField(upload_to='answer_images', blank=True, null=True)

    ordering_rank = models.IntegerField()

    class Meta:
        ordering = ('ordering_rank',)

    def question_text(self):
        return self.answer.question.text

    def answer_text(self):
        return self.answer.text

    @property
    def english(self):
        try:
            return (
                AnswerTranslation.objects.get(answer=self, language='en').text
            )
        except:
            return None

    @property
    def spanish(self):
        try:
            return (
                AnswerTranslation.objects.get(answer=self, language='es').text
            )
        except:
            return None

    def wording(self, preferred_language_code):
        """attempts to provide a wording in preferred language;
        otherwise falls back on the other language; otherwise returns
        a fixed string."""
        try:
            return (
                AnswerTranslation.objects.get(
                    answer=self,
                    language=preferred_language_code).text
            )
        except:
            pass

        try:
            return self.answer_translation_set.all()[0].text
        except:
            pass

        return (
            "Sorry, no wordings provided in either language. "
            "Enter wordings at /admin/collection_tool/displayanswer"
            "/%d/" % self.id
        )

    @property
    def dir(self):
        return dir(self)


class AnswerTranslation(models.Model):

    """ an answer wording in a particular language."""
    answer = models.ForeignKey(DisplayAnswer)
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        null=False)
    text = models.TextField(null=True, blank=True)
    ordering_string = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['ordering_string']

    @property
    def dir(self):
        return dir(self)


def post_save_ordering_string_update(sender, **kwargs):
    answer_translation = kwargs['instance']
    answer_translation.ordering_string = (
        answer_translation.answer.question_text())


post_save.connect(post_save_ordering_string_update, sender=AnswerTranslation)


class PlannerItem(models.Model):

    def __unicode__(self):
        return "%s: %s" % (self.get_type_display(), self.label)

    TYPE_CHOICES = (('A', 'Fluoride'), ('B', 'Foods'), ('C', 'Drinks'))
    SPANISH_TYPES = (('A', 'Fluoruro'), ('B', 'Alimentos'), ('C', 'Bebidas'))
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def get_spanish_type(self):
        return (
            [label[1]
                for label in self.SPANISH_TYPES if label[0] == self.type][0]
        )

    label = models.TextField()
    spanish_label = models.TextField()

    risk_level = models.IntegerField()

    # Image is just assumed to be "slugified_label.jpg"

    # reordering for Jess:
    ordering_map = {
        'A': 0,  # fluoride first
        'C': 1,  # then drinks
        'B': 2    # and then food
    }

    @property
    def new_ordering(self):
        return self.ordering_map[self.type]

    class Meta:
        ordering = ('type', 'label')
