from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from smilekit.equation_balancer.models import Module, Question, Answer
from smilekit.equation_balancer.models import Configuration, ModuleWeight, Weight

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
  modules = Module.objects.all()
  questions = Question.objects.order_by('module', 'number')
  weights = config.weight_set.all()
  module_weights = config.moduleweight_set.all()
  return render_to_response("equation_balancer/configuration.html",
                            {'modules':modules, 'questions':questions,
                             'config':config, 'weights':weights,
                             'moduleweights':module_weights},
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
  # save module weights
  for module in Module.objects.all():
    new_value = request.POST['moduleweight-%s' % module.id]
    if new_value == "": new_value = 0 # set to 0 if cleared
    # TODO handle NaN
    weight, created = ModuleWeight.objects.get_or_create(module=module, config=config, weight=new_value)
    weight.save()
  
  # save question weights
  for question in Question.objects.all():
  #  try:
      new_value = request.POST['weight-%s' % question.number]
      if new_value == "": new_value = 0  # set to 0 if cleared
      weight, created = Weight.objects.get_or_create(question=question, config=config, weight=new_value)
      weight.save()
  #  except:
  #    pass  # question not in the form -- this probably won't happen?
  return HttpResponseRedirect("/weights/configuration/%s" % config_id)

@login_required
def load_questions(request):
  # if csv file provided, load
  if request.method == 'POST':
    try:
      fh = request.FILES['csvfile']
    except:
      return {}

    if file == '':
      # TODO: error checking (correct file type, etc.)
      return HttpResponseRedirect("/weights/")

  # delete existing data
  Question.objects.all().delete()
  Module.objects.all().delete()
  Answer.objects.all().delete()

  table = csv.reader(fh)

  headers = ""
  questions = []
  
  for question in zip(*table):
    questions.append(question)

  headers = questions.pop(0)

  # parse headers (so they can be in any order)
  for i in range(len(headers)):
    header = headers[i]
    if header.lower() == "question text": id_text = i
    elif header.lower() == "question number": id_number = i
    elif header.lower() == "answers": id_answers = i
    elif header.lower() == "numerical equivalent": id_weights = i
    elif header.lower() == "module": id_module = i
    else: print "invalid header detected: %s" % header

  for question in questions:
    (m, created) = Module.objects.get_or_create(name = question[id_module])
    m.save()
    q = Question(number = question[id_number],
                 text = question[id_text],
                 module = m)
    q.save()

    answers = question[id_answers].split(",")
    weights = question[id_weights].split(",")

    for (ans,wt) in zip(answers, weights):
      a = Answer(question = q,
                 text = ans,
                 weight = wt.strip() or 1)
      a.save()

  return HttpResponseRedirect("/admin/equation_balancer/question/")

def load_patient_data(request):
  # if csv file provided, load
  if request.method == 'POST':
    try:
      fh = request.FILES['csvfile']
    except:
      return {}

    if file == '':
      # TODO: error checking (correct file type, etc.)
      return HttpResponseRedirect("/weights/")

  table = csv.reader(fh)
  headers = table.next()

  patients = {}
  for row in table:
    patient_number = row[0]
    patient_data = {}
    for i in range(len(row)):
      if i==0: pass
      patient_data[headers[i]] = row[i]
    patients[patient_number] = patient_data

  #json = '{"total": %s}' % round(total_mol,2)
  print patients
  json = '{"data": %s}' % patients
  return HttpResponse(json, mimetype="application/javascript")


def calculate_patient_score(request):
  patient_data = request.POST['patient_data']
  weights = request.POST['weights']
  
  for question in Question.objects.all():
    pass
