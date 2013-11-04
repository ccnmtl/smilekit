from django.http import HttpResponse, Http404
from .models import (
    HelpUrl, Topic, Goal, PlannerItem, AssessmentSection, DisplayQuestion,
    DisplayAnswer, has_image)
from smilekit.family_info.models import Family
from smilekit.equation_balancer.models import Answer, Question, Configuration
from django.contrib.flatpages.models import FlatPage
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
import random
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required


def get_help_item(url_string):
    """ fetch a help item for a particular URL"""
    help_item = None
    try:
        help_item = HelpUrl.objects.filter(
            url__contains=url_string)[0].help_item
    except:
        pass
    return help_item


@login_required()
def intro(request, language_code):
    """ Intro (default first ) page of the collection tool."""
    if language_code not in ['en', 'es']:
        raise Http404

    t = loader.get_template('collection_tool/intro.html')
    c = RequestContext(request, {
        'language_code': language_code,
        'help_item': get_help_item('/intro/')
    })
    return HttpResponse(t.render(c))


@login_required()
def risk(request, language_code):
    """ Show risk score."""
    if language_code not in ['en', 'es']:
        raise Http404
    t = loader.get_template('collection_tool/risk.html')
    c = RequestContext(request, {
        'language_code': language_code,
        'help_item': get_help_item('/risk/'),
        'all_topics': Topic.objects.all(),
        'all_configs': Configuration.objects.all(),
        'all_families': Family.objects.all(),
    })
    return HttpResponse(t.render(c))


@login_required()
def topics(request, language_code):
    if language_code not in ['en', 'es']:
        raise Http404
    t = loader.get_template('collection_tool/topics.html')

    # collate all the flat pages referred to by the topics so we can easily
    # put them into divs:
    topic_urls = [
        the_topic.learn_more_english['url']
        for the_topic in Topic.objects.all() if the_topic.learn_more_english]
    topic_urls.extend(
        [the_topic.learn_more_spanish['url']
         for the_topic in Topic.objects.all() if the_topic.learn_more_spanish])
    flat_pages_we_need = FlatPage.objects.filter(url__in=topic_urls)

    # print dir (FlatPage)
    c = RequestContext(request, {
        'language_code': language_code,
        'all_topics': Topic.objects.all(),
        'flat_pages_we_need': flat_pages_we_need,
        'help_item': get_help_item('/topics/'),
    })
    return HttpResponse(t.render(c))


@login_required()
def goals(request, language_code):
    """Displays goals we've already made progress on. AKA Plan History."""
    if language_code not in ['en', 'es']:
        raise Http404
    t = loader.get_template('collection_tool/goals.html')
    c = RequestContext(request, {
        'language_code': language_code,
        'all_goals': Goal.objects.all(),
        'help_item': get_help_item('/goals/'),
    })
    return HttpResponse(t.render(c))


@login_required()
def goal(request, goal_id, language_code):
    """Goal form: shown when you pick a goal by clicking 'Plan' in the
    Topics page..."""
    if language_code not in ['en', 'es']:
        raise Http404
    t = loader.get_template('collection_tool/goal.html')

    c = RequestContext(request, {
        'language_code': language_code,
        'goal': get_object_or_404(Goal, pk=goal_id)
    })
    return HttpResponse(t.render(c))


def get_planner_items():
    # look up question ids for planner
    starttime = datetime(1984, 1, 1, 6)
    planner_times = [
        (starttime + timedelta(minutes=30) * i).strftime("%I:%M%p")
        for i in range(36)]

    # OK, now drinks come before foods.
    #planner_items = PlannerItem.objects.all().order_by('type', 'label')

    planner_items = list(PlannerItem.objects.all())
    planner_items.sort(key=lambda p_i: p_i.label)
    planner_items.sort(key=lambda p_i: p_i.new_ordering)

    return {
        'planner_times': planner_times,
        'planner_items': planner_items,
    }


@login_required()
def goal_planner(request, goal_id, language_code):
    """Goal planner form."""

    stuff = {
        'language_code': language_code,
        'goal': get_object_or_404(Goal, pk=goal_id)
    }

    stuff.update(get_planner_items())

    if language_code not in ['en', 'es']:
        raise Http404
    t = loader.get_template('collection_tool/goal_planner.html')

    c = RequestContext(request, stuff)
    return HttpResponse(t.render(c))


@login_required()
def section(request, section_id, language_code):
    section = get_object_or_404(AssessmentSection, pk=section_id)

    if language_code not in ['en', 'es']:
        raise Http404

    t = loader.get_template('collection_tool/sectionindex.html')
    c = RequestContext(request, {
        'section': section,
        'language_code': language_code,
        'all_sections': AssessmentSection.objects.all()
    })
    return HttpResponse(t.render(c))


@login_required()
def question(request, displayquestion_id, language_code):
    """ Look up a DisplayQuestion object and display it in the data
    collection tool. Note that question_id refers to a displayquestion
    object, not a question object."""

    displayquestion = get_object_or_404(DisplayQuestion, pk=displayquestion_id)
    if language_code not in ['en', 'es']:
        raise Http404
    wording = displayquestion.wording(language_code)

    answers = []

    if displayquestion.display_answers:
        for d in displayquestion.display_answers:
            answers.append({
                'stock_answer': False,
                'wording': d.wording(language_code),
                'image': d.image,
                'id': d.answer.id
            })

    else:
        for a in displayquestion.question.answer_set.all():
            answers.append({
                'stock_answer': True,
                'text': a.text,
                'id': a.id
            })

    # look up question ids for planner
    planner_question = False

    risky_exposures_question = Question.objects.get(
        text="number risky exposures")
    risky_answers = {}

    fluoride_question = Question.objects.get(text="Fluoride rinse exposures")
    fluoride_answers = {}

    brushing_question = Question.objects.get(
        text="Children's daily toothbrushing")
    brushing_answers = {}

    if displayquestion.show_planner:
        planner_question = True

        for answer in Answer.objects.filter(question=risky_exposures_question):
            risky_answers[answer.text] = answer.id

        for answer in Answer.objects.filter(question=brushing_question):
            brushing_answers[answer.text] = answer.id

        for answer in Answer.objects.filter(question=fluoride_question):
            fluoride_answers[answer.text] = answer.id

    t = loader.get_template('collection_tool/question.html')
    c = RequestContext(request, {
        'displayquestion': displayquestion,
        'wording': wording,
        'answers': answers,
        'language_code': language_code,
        'all_sections': AssessmentSection.objects.all(),
        'planner_question': planner_question,  # is this a planner question?
        'planner_items': get_planner_items()['planner_items'],
        'planner_times': get_planner_items()['planner_times'],
        # TODO to just check the boolean planner_question and remove this
        # variable
        'widget_question_ids':
        [risky_exposures_question.id,
         brushing_question.id,
         fluoride_question.id],


        'risky_question_id': risky_exposures_question.id,
        # these are the TEXT of the answers
        'risky_answers_keys': [str(key) for key in risky_answers.keys()],
        # these are the IDS of the answers
        'risky_answers_values': risky_answers.values(),

        'brushing_question_id': brushing_question.id,
        'brushing_answers_keys': [str(key) for key in brushing_answers.keys()],
        'brushing_answers_values': brushing_answers.values(),

        'fluoride_question_id': fluoride_question.id,
        'fluoride_answers_keys': [str(key) for key in fluoride_answers.keys()],
        'fluoride_answers_values': fluoride_answers.values(),

    })
    return HttpResponse(t.render(c))


def manifest(request):
    """ This is the list of files that Smilekit needs to save locally
    on the ipad, so that researchers can access them offline while
    interviewing.  The url is:

    /collection_tool/manifest.cache
    Relevant research:
    https://developer.mozilla.org/en/Offline_resources_in_Firefox
    http://docs.djangoproject.com/en/dev/ref/request-response/
    http://stackoverflow.com/questions/1715568/
         how-to-properly-invalidate-an-html5-cache
         -manifest-for-online-offline-web-apps
    http://www.webreference.com/authoring/languages/
         html/HTML5-Application-Caching/
    """
    paths_to_question_images = [
        d.image.url for d in DisplayQuestion.objects.all(
        ) if has_image(
            d.image)]

    paths_to_answer_images = [
        d.image.url for d in DisplayAnswer.objects.all(
        ) if has_image(
            d.image)]

    nav_section_ids = [p.id for p in AssessmentSection.objects.all()]

    question_ids = [dq.id for dq in DisplayQuestion.objects.all()]

    planner_labels = [i.label for i in PlannerItem.objects.all()]

    response = HttpResponse(mimetype='text/cache-manifest')
    #response = HttpResponse()

    t = loader.get_template('collection_tool/manifest')
    c = RequestContext(request, {
        'language_codes': ['en', 'es'],
        'paths_to_question_images': paths_to_question_images,
        'paths_to_answer_images': paths_to_answer_images,
        'nav_section_ids': nav_section_ids,
        'planner_labels': planner_labels,
        'goals': Goal.objects.all(),
        'question_ids': question_ids,
        'randomnumber': random.randint(0, 9999999999)
    })
    response.write(t.render(c))
    return response
