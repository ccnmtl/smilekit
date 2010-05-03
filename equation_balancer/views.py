from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from smilekit.equation_balancer.models import Configuration, Question, Weight

import csv
import simplejson as json

@login_required
def index(request):
  user = request.user
  configs = user.configuration_set.all()
  return render_to_response("equation_balancer/index.html",
                             {'configs':configs},
                             context_instance=RequestContext(request))



# TODO admin only
# def loadcsv(request, csvfile):
#   load questions from CSV

@login_required
def view_config(request, config_id):
  config = Configuration.objects.get(id=config_id)
  questions = Question.objects.all()
  return render_to_response("equation_balancer/configuration.html",
                           {'config':config, 'questions':questions},
                             context_instance=RequestContext(request))
@login_required
def new_config(request):
  name = request.POST['name']
  user = request.user
  #todo error catch for 'config already exists with that name'
  config = Configuration.objects.get_or_create(owner=user, name=name)
  print config
  return HttpResponseRedirect("weights/")
