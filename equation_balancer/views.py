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
  weights = config.weight_set.all()
  return render_to_response("equation_balancer/configuration.html",
                           {'config':config, 'questions':questions, 'weights':weights},
                             context_instance=RequestContext(request))
@login_required
def new_config(request):
  name = request.POST['name']
  user = request.user
  #todo error catch for 'config already exists with that name'
  config = Configuration.objects.get_or_create(owner=user, name=name)
  return HttpResponseRedirect("/weights/")

@login_required
def save_config(request):
  config_id = request.POST['config']
  config = Configuration.objects.get(id=config_id)
  for question in Question.objects.all():
  #  try:
      new_id = 'weight-%s' % question.row
      new_value = request.POST['weight-%s' % question.row]
      if new_value == "": new_value = 0  # set to 0 if cleared
      weight, created = Weight.objects.get_or_create(question=question, config=config)
      weight.weight = new_value
      weight.save()
  #  except:
  #    pass  # question not in the form -- this probably won't happen?
  return HttpResponseRedirect("/weights/configuration/%s" % config_id)


def load_patient_data(request):
  pass

def calculate_patient_score(request):
  patient_data = request.POST['patient_data']
  weights = request.POST['weights']
  
  for question in Question.objects.all():
    pass