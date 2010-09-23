from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render_to_response
from smilekit.collection_tool.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
import random

#def index(request):
#    return render_to_response("collection_tool/index.html")


#def temp_html(request):
#    return render_to_response("collection_tool/temp_html.html")


@login_required
def login(request):
  return render_to_response("family_info/login.html")

@login_required
def participants(request):
  return render_to_response("family_info/participants.html")
  
@login_required
def family_assessment(request):
  return render_to_response("family_info/family_assessment.html")
  
@login_required
def family_information(request):
  return render_to_response("family_info/family_information.html")
  
@login_required
def health_worker_information(request):
  return render_to_response("family_info/health_worker_information.html")
  
@login_required
def sync(request):
  return render_to_response("family_info/sync.html")
  


    
if 1 == 0:
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
        

      #      (r'video/(?P<video_path>\w+)/$', 'collection_tool.views.video'), 

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
        
        t = loader.get_template('collection_tool/question.html')
        c = RequestContext(request,{
            'displayquestion': displayquestion,
            'wording' : wording,
            'answers': answers,
            'language_code': language_code,
            'all_sections': AssessmentSection.objects.all()
        })
        return HttpResponse(t.render(c))
          

      def interview_management_login(request):
        return render_to_response("collection_tool/interview_management_login.html")
      def interview_management_participants(request):
        return render_to_response("collection_tool/interview_management_participants.html")
      def interview_management_family_assessment(request):
        return render_to_response("collection_tool/interview_management_family_assessment.html")
      def interview_management_family_information(request):
        return render_to_response("collection_tool/interview_management_family_information.html")
      def interview_management_health_worker_information(request):
        return render_to_response("collection_tool/interview_management_health_worker_information.html")
      def interview_management_sync(request):
        return render_to_response("collection_tool/interview_management_sync.html")
        

        



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


      def online_check(request):
        return HttpResponse(random.randint(0, 9999999999))


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
        
        #import pdb
        #pdb.set_trace()
        
        
        paths_to_question_images = [d.image.url for d in DisplayQuestion.objects.all() if has_image(d.image)]
        
        paths_to_answer_images = [d.image.url for d in DisplayAnswer.objects.all() if has_image(d.image)]
        
        nav_section_ids = [p.id for p in AssessmentSection.objects.all()]

        #THIS WORKS:::::
        
        response = HttpResponse(mimetype='text/cache-manifest')
        t = loader.get_template('collection_tool/manifest')
        c = RequestContext(request,{
          'paths_to_question_images' :  paths_to_question_images,
          'paths_to_answer_images' :    paths_to_answer_images,
          'nav_section_ids' :           nav_section_ids,
          # this was breaking on questions that weren't part of the nav:
          # 'question_ids':              [d.id for d in DisplayQuestion.objects.all()],
          'question_ids':               all_display_question_ids_in_order(),
          'randomnumber' :              random.randint(0, 9999999999)

          
        })
        response.write(t.render(c))
        return response
        
          

if 1 == 0:

  def manifest(request):
    return HttpResponseNotFound()  
  
