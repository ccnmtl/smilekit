from django.http import HttpResponse
from django.shortcuts import render_to_response

#def index(request):
#    return render_to_response("collection_tool/index.html")


#def temp_html(request):
#    return render_to_response("collection_tool/temp_html.html")
    

def question(request, question_id, language_code):
    return render_to_response("collection_tool/question.html")
    
