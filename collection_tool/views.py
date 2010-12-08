from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render_to_response
from smilekit.collection_tool.models import *
from smilekit.family_info.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader
import random
from datetime import datetime, timedelta


def risk(request, language_code):
  """ Show risk score."""
  if language_code not in ['en', 'es']:
    raise Http404
  t = loader.get_template('collection_tool/risk.html')
      
  c = RequestContext(request,{
      'language_code': language_code,
      'all_topics': Topic.objects.all(),
      'all_families': Family.objects.all(),
  })
  return HttpResponse(t.render(c))


def topics(request, language_code):
  if language_code not in ['en', 'es']:
    raise Http404
  t = loader.get_template('collection_tool/topics.html')
      
  c = RequestContext(request,{
      'language_code': language_code,
      'all_topics': Topic.objects.all(),
      'all_families': Family.objects.all(),
  })
  return HttpResponse(t.render(c))

def topic(request, topic_id, language_code ):
  """Show the topic title and description, goal title and
description. Get here by clicking 'Learn' on the goals page."""

  if language_code not in ['en', 'es']:
    raise Http404
  t = loader.get_template('collection_tool/topic.html')
      
  c = RequestContext(request,{
      'language_code': language_code,
      'topic': get_object_or_404(Topic, pk=topic_id)
  })
  return HttpResponse(t.render(c))    
  
def goals(request, language_code):
  """Displays goals we've already made progress on. AKA Plan History."""
  if language_code not in ['en', 'es']:
    raise Http404
  t = loader.get_template('collection_tool/goals.html')
  c = RequestContext(request,{
      'all_goals': Goal.objects.all()
  })
  return HttpResponse(t.render(c))


def goal(request, goal_id, language_code):
  """Goal form: shown when you pick a goal by clicking 'Plan' in the Topics page..."""
  if language_code not in ['en', 'es']:
    raise Http404
  t = loader.get_template('collection_tool/goal.html')
      
  c = RequestContext(request,{
      'language_code': language_code,
      'goal': get_object_or_404(Goal, pk=goal_id)
  })
  return HttpResponse(t.render(c))    



def get_planner_items():
  # look up question ids for planner
  starttime = datetime(1984,1,1,6)
  planner_times = [(starttime + timedelta(minutes=30) * i).strftime("%I:%M%p")
           for i in range(36)]
  planner_items = PlannerItem.objects.all().order_by('type', 'label')
  
  return {
    'planner_times':planner_times,
    'planner_items':planner_items,
  }

# planner/goal/(?P<goal_id>\d+)/language/(?P<language_code>\w+)
def goal_planner(request, goal_id, language_code):
  """Goal planner form."""
  
  stuff = {
      'language_code': language_code,
      'goal': get_object_or_404(Goal, pk=goal_id)
  }
  print stuff
  stuff.update (get_planner_items());
  print stuff
  
  if language_code not in ['en', 'es']:
    raise Http404
  t = loader.get_template('collection_tool/goal_planner.html')
      
  c = RequestContext(request, stuff)
  return HttpResponse(t.render(c))    




##########################
##########################




def section(request, section_id, language_code):
  section = get_object_or_404(AssessmentSection, pk=section_id)
  if language_code not in ['en', 'es']:
    raise Http404
    
  t = loader.get_template('collection_tool/sectionindex.html')
  c = RequestContext(request,{
      'section': section,
      'language_code': language_code,
      'all_sections': AssessmentSection.objects.all()
  })
  return HttpResponse(t.render(c))
  
def section(request, section_id, language_code):
  section = get_object_or_404(AssessmentSection, pk=section_id)
  
  if language_code not in ['en', 'es']:
    raise Http404
    
  t = loader.get_template('collection_tool/sectionindex.html')
  c = RequestContext(request,{
      'section': section,
      'language_code': language_code,
      'all_sections': AssessmentSection.objects.all()
  })
  return HttpResponse(t.render(c))
  
def video (request, video_filename):
  """Show a video."""
  t = loader.get_template('collection_tool/video.html')
  c = RequestContext(request,{
      'video_filename' : video_filename
  })
  return HttpResponse(t.render(c))

def question(request, displayquestion_id, language_code):
  """ Look up a DisplayQuestion object and display it in the data collection tool. Note that question_id refers to a displayquestion object, not a question object."""
  
  displayquestion = get_object_or_404(DisplayQuestion, pk=displayquestion_id)
  if language_code not in ['en', 'es']:
    raise Http404
  wording = displayquestion.wording(language_code)
  
  answers = []
  
  if displayquestion.display_answers:
    for d in displayquestion.display_answers:
      answers.append ( {
                        'stock_answer' : False,
                        'wording': d.wording(language_code),
                        'image': d.image,
                        'id': d.answer.id
                        } )
                        
  else:
    for a in displayquestion.question.answer_set.all():
      answers.append ( {
                    'stock_answer' : True,
                    'text': a.text,
                    'id': a.id
                      })

  # look up question ids for planner
  planner_times = []
  planner_items = []

  risky_exposures_question = Question.objects.get(text="number risky exposures")
  risky_answers = {}

  fluoride_question = Question.objects.get(text="Fluoride rinse exposures")
  fluoride_answers = {}

  brushing_question = Question.objects.get(text="Children's daily toothbrushing")
  brushing_answers = {}

  if displayquestion.question in [risky_exposures_question, brushing_question, fluoride_question]:
    starttime = datetime(1984,1,1,6)
    planner_times = [(starttime + timedelta(minutes=30) * i).strftime("%I:%M%p")
             for i in range(36)]
    planner_items = PlannerItem.objects.all().order_by('type', 'label')
    
    for answer in Answer.objects.filter(question=risky_exposures_question):
      risky_answers[answer.text] = answer.id

    for answer in Answer.objects.filter(question=brushing_question):
      brushing_answers[answer.text] = answer.id
      
    for answer in Answer.objects.filter(question=fluoride_question):
      fluoride_answers[answer.text] = answer.id

  t = loader.get_template('collection_tool/question.html')
  c = RequestContext(request,{
      'displayquestion': displayquestion,
      'wording' : wording,
      'answers': answers,
      'language_code': language_code,
      'all_sections': AssessmentSection.objects.all(),
      'planner_times':planner_times,
      'planner_items':planner_items,
      
      'widget_question_ids':[risky_exposures_question.id, brushing_question.id, fluoride_question.id],
      'risky_question_id':risky_exposures_question.id,
      'risky_answers_keys':[str(key) for key in risky_answers.keys()],
      'risky_answers_values':risky_answers.values(),
      'fluoride_question_id':fluoride_question.id,
      'fluoride_answers_keys':[str(key) for key in fluoride_answers.keys()],
      'fluoride_answers_values':fluoride_answers.values(),
      'brushing_question_id':brushing_question.id,
      'brushing_answers_keys':[str(key) for key in brushing_answers.keys()],
      'brushing_answers_values':brushing_answers.values()
  })
  return HttpResponse(t.render(c))



def widget_test(request):
  starttime = datetime(1984,1,1,7)
  times = [(starttime + timedelta(minutes=30) * i).strftime("%I:%M%p")
           for i in range(34)]
  items = PlannerItem.objects.all().order_by('type')
  return render_to_response("collection_tool/widget_test.html", {"times":times, "items":items})



def manifest(request):
  """ This is the list of files that Smilekit needs to save locally on the ipad, so that researchers can access them offline while interviewing.
  The url is:
  /collection_tool/manifest.cache
  Relevant research:
  https://developer.mozilla.org/en/Offline_resources_in_Firefox
  http://docs.djangoproject.com/en/dev/ref/request-response/
  http://stackoverflow.com/questions/1715568/how-to-properly-invalidate-an-html5-cache-manifest-for-online-offline-web-apps
  http://www.webreference.com/authoring/languages/html/HTML5-Application-Caching/
  """
  paths_to_question_images = [d.image.url for d in DisplayQuestion.objects.all() if has_image(d.image)]
  
  paths_to_answer_images = [d.image.url for d in DisplayAnswer.objects.all() if has_image(d.image)]
  
  nav_section_ids = [p.id for p in AssessmentSection.objects.all()]
  
  planner_labels = [i.label for i in PlannerItem.objects.all()]

  response = HttpResponse(mimetype='text/cache-manifest')
  t = loader.get_template('collection_tool/manifest')
  c = RequestContext(request,{
    'paths_to_question_images' :  paths_to_question_images,
    'paths_to_answer_images' :    paths_to_answer_images,
    'nav_section_ids' :           nav_section_ids,
    'planner_labels' :            planner_labels,
    'goals' :                     Goal.objects.all(),
    # this was breaking on questions that weren't part of the nav:
    # 'question_ids':              [d.id for d in DisplayQuestion.objects.all()],
    'question_ids':               all_display_question_ids_in_order(),
    'randomnumber' :              random.randint(0, 9999999999)
  })
  response.write(t.render(c))
  return response
  
  
