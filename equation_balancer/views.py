from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from smilekit.equation_balancer.models import Module, Question, Answer
from smilekit.equation_balancer.models import Configuration, ModuleWeight, Weight

import csv
import simplejson as json

from decimal import *

@login_required
def index(request):
  user = request.user
  configs = user.configuration_set.all()
  return render_to_response("equation_balancer/index.html",
                             {'configs':configs},
                             context_instance=RequestContext(request))



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
    if header.lower().strip() == "question text": id_text = i
    elif header.lower().strip() == "question number": id_number = i
    elif header.lower().strip() == "answers": id_answers = i
    elif header.lower().strip() == "numerical equivalent": id_weights = i
    elif header.lower().strip() == "module": id_module = i
    #else: print "invalid header detected: %s" % header

  for question in questions:
    (m, created) = Module.objects.get_or_create(name = question[id_module])
    m.save()
    q = Question(number = question[id_number],
                 text = question[id_text].strip(),
                 module = m)
    q.save()

    answers = question[id_answers].split(",")
    weights = question[id_weights].split(",")

    for (ans,wt) in zip(answers, weights):
      a = Answer(question = q,
                 text = ans.lower().strip(),
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
  
  # get current set of weights from webpage (not database, in case they have modified but not saved yet)
  weights = {}
  for question in Question.objects.all():
    weights[question.number] = Decimal(request.POST['weight-%s' % question.number])

  moduleweights = {}
  for module in Module.objects.all():
    moduleweights[module.id] = Decimal(request.POST['moduleweight-%s' % module.id])
    
  patients = {}
  scores = {}
  for row in table:
    patient_number = row[0]
    patient_data = {}
    for i in range(len(row)):
      if i==0: pass
      patient_data[int(headers[i])] = row[i]
    #patients[patient_number]["answers"] = patient_data
    patients[patient_number] = patient_data
    patient_score = calculate_score(moduleweights, weights, patient_data)
    scores[patient_number] = patient_score
    #patients[patient_number]["score"] = 

  result = {}
  result['data'] = patients
  result['scores'] = scores
  test = json.dumps(result)
  return HttpResponse(json.dumps(result), mimetype="application/javascript")


def calculate_patient_score(request):
  patient = request.POST['patient']
  moduleweights = {}
  weights = {}
  
  for module in Module.objects.all():
    moduleweights[module.id] = request.POST['moduleweight-%s' % module.id]
    
  for question in Question.objects.all():
    weights[question.number] = request.POST['weight-%s' % question.number]
    answers[question.number] = request.POST['patient-%s-answer-%s' % (patient, question.number)]
    
  scores = calculate_score(moduleweights, weights, answers)
  json = '{"data": %s}' % scores
  return HttpResponse(json, mimetype="application/javascript")    
  
def calculate_score(moduleweights, weights, answers):
  scores = {}
  totalscore = 0
  
  for module in Module.objects.all():
    modulescore = 0
    moduleweight = moduleweights[module.id]
    for question in module.question_set.all():
      weight = weights[question.number]
      answer = answers[question.number]
      
      #print "calculating score for answer %s" % answer
      #print question.answer_set.all()
      try:
        db_answer = question.answer_set.get(text = answer.lower().strip())
        answer_wt = db_answer.weight
        #print "using weight %s" % answer_wt
      except:
        #print "no weight found for %s of the choices in %s.. zeroing answer" % (answer, question.answer_set.all()) 
        answer_wt = 0

      scores['question-%s' % question.number] = "%d" % (weight * answer_wt)
      modulescore += weight * answer_wt
    scores['module-%s' % module.id] = "%d" % (moduleweight * modulescore)
    totalscore += moduleweight * modulescore

  scores['total'] = "%d" % totalscore
  return scores