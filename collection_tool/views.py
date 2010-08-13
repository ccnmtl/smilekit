from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from smilekit.collection_tool.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader

#def index(request):
#    return render_to_response("collection_tool/index.html")


#def temp_html(request):
#    return render_to_response("collection_tool/temp_html.html")
    

def question(request, displayquestion_id, language_code):
  """ Look up a DisplayQuestion object and display it in the data collection tool. Note that question_id refers to a displayquestion object, not a question object; some displayquestions are not associated with any question."""
  #print displayquestion_id
  #print language_code
  #print DisplayQuestion.objects.get(id=displayquestion_id)
  #if language_
  
  displayquestion = get_object_or_404(DisplayQuestion, pk=displayquestion_id)
  
  if language_code not in ['en', 'es']:
    raise Http404
  
  wording = None
  if language_code == 'en':
    wording = displayquestion.english
  if language_code == 'es':
    wording = displayquestion.spanish
  
  #import pdb
  #pdb.set_trace()
  
  #if wording == None:
  #  raise Http404
  #  #TODO: use backup wording in the other language if only one is available.
  
  
  #TODO: how the hell do we store attach answers to display_questions that have a null question?
  wording = displayquestion.wording(language_code)
  
  
  answer_wordings = [d.wording(language_code) for d in displayquestion.display_answers]
  
  #return render_to_response("collection_tool/question.html")
  t = loader.get_template('collection_tool/question.html')
  c = RequestContext(request,{
      'displayquestion': displayquestion,
      'wording' : wording,
      'answer_wordings': answer_wordings,
      'language_code': language_code
      #'answers': None
  })
  return HttpResponse(t.render(c))
    

def html_sandbox(request):
  return render_to_response("collection_tool/html_sandbox.html")

# for testing:
def available_offline(request):
  t = loader.get_template('collection_tool/message.html')
  c = RequestContext(request,{
      'message': "This page should be available offline."
  })
  return HttpResponse(t.render(c))

def not_available_offline(request):
  t = loader.get_template('collection_tool/message.html')
  #print "NOT AVAILABLE OFFLINE"
  c = RequestContext(request,{
      'message': "This page should NOT be available offline."
  })
  return HttpResponse(t.render(c))


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
  response = HttpResponse(mimetype='text/cache-manifest')
  t = loader.get_template('collection_tool/manifest')
  c = RequestContext(request,{
    'question_ids': [d.id for d in DisplayQuestion.objects.all()]
  })
  response.write(t.render(c))
  return response
