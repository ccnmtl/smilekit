from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render_to_response
from smilekit.collection_tool.models import *
from smilekit.family_info.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader
import random
from datetime import datetime, timedelta


#(r'topics/language/(?P<language_code>\w+)$', 'collection_tool.views.topics'), 
def topics(request, language_code):
  if language_code not in ['en', 'es']:
    raise Http404
  t = loader.get_template('collection_tool/topics.html')
  
  if 1 == 0:  
    all_scores = {}
    for ttopic in Topic.objects.all():
      new_score_infoes  = {}
      for conf in  Configuration.objects.all():
        new_score_infoes  [ttopic] = ttopic.scoring_info(conf)
      all_scores[ttopic] = new_score_infoes
      
  c = RequestContext(request,{
      'language_code': language_code,
      'all_topics': Topic.objects.all(),
      'all_families': Family.objects.all(),
      #'all_configs': Configuration.objects.all(),
      #'all_scores' : all_scores
  })
  return HttpResponse(t.render(c))    
  
#(r'goals/language/(?P<language_code>\w+)$', 'collection_tool.views.goals'), 
def goals(request, language_code):
  if language_code not in ['en', 'es']:
    raise Http404
  t = loader.get_template('collection_tool/goals.html')
  c = RequestContext(request,{
      'language_code': language_code,
      'all_goals': Goal.objects.all()
  })
  return HttpResponse(t.render(c))

#(r'help_summary$', 'collection_tool.views.help_summary'), 
def help_summary(request):
  section = get_object_or_404(AssessmentSection, pk=section_id)
  t = loader.get_template('collection_tool/help_summary.html')
  c = RequestContext(request,{
      'all_display_questions': DisplayQuestion.objects.all()
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
  """ Look up a DisplayQuestion object and display it in the data collection tool. Note that question_id refers to a displayquestion object, not a question object; some displayquestions are not associated with any question."""
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

  planner_times = []
  planner_items = []
  if displayquestion.question.number == 24:
    starttime = datetime(1984,1,1,6)
    planner_times = [(starttime + timedelta(minutes=30) * i).strftime("%I:%M%p")
             for i in range(36)]
    planner_items = PlannerItem.objects.all().order_by('type', 'label')

  t = loader.get_template('collection_tool/question.html')
  c = RequestContext(request,{
      'displayquestion': displayquestion,
      'wording' : wording,
      'answers': answers,
      'language_code': language_code,
      'all_sections': AssessmentSection.objects.all(),
      'planner_times':planner_times,
      'planner_items':planner_items
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
    # this was breaking on questions that weren't part of the nav:
    # 'question_ids':              [d.id for d in DisplayQuestion.objects.all()],
    'question_ids':               all_display_question_ids_in_order(),
    'randomnumber' :              random.randint(0, 9999999999)
  })
  response.write(t.render(c))
  return response
  
  
