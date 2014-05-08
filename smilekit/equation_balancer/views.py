from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from smilekit.equation_balancer.models import Module, Question, Answer
from smilekit.equation_balancer.models import (
    Configuration, ModuleWeight, Weight)

import csv
import simplejson as json

from decimal import Decimal


@login_required
def index(request):
    configs = Configuration.objects.all()
    return render_to_response("equation_balancer/index.html",
                              {'configs': configs},
                              context_instance=RequestContext(request))


@login_required
def view_config(request, config_id):
    config = Configuration.objects.get(id=config_id)
    modules = Module.objects.all()
    questions = Question.objects.order_by('module', 'number')
    weights = config.weight_set.all()
    module_weights = config.moduleweight_set.all()
    return render_to_response("equation_balancer/configuration.html",
                              {'modules': modules, 'questions': questions,
                               'config': config, 'weights': weights,
                               'moduleweights': module_weights},
                              context_instance=RequestContext(request))


@login_required
def new_config(request):
    name = request.POST['name']
    user = request.user
    # todo error catch for 'config already exists with that name'
    Configuration.objects.get_or_create(owner=user, name=name)
    return HttpResponseRedirect("/weights/")


@login_required
def delete_config(request, config_id):
    #config_id = request.POST['config']
    try:
        Configuration.objects.get(id=config_id).delete()
    except:
        pass
    return HttpResponseRedirect("/weights/")


@login_required
def export_config(request, config_id):
    config = Configuration.objects.get(id=config_id)

    response = HttpResponse(mimetype='text/csv')
    response[
        'Content-Disposition'] = 'attachment; filename="%s.csv"' % config.name
    writer = csv.writer(response)

    # write headers
    headers = ['id', 'weight']
    writer.writerow(headers)

    # write module weights
    moduleweights = config.moduleweight_set.order_by("module")
    for wt in moduleweights:
        row = ["Module %s" % wt.module.name, wt.weight]
        writer.writerow(row)

    # write question weights
    weights = config.weight_set.order_by("question")
    for wt in weights:
        row = ["Question %s" % wt.question.number, wt.weight]
        writer.writerow(row)

    return response


@login_required
def import_config(request):
    # if csv file provided, load
    if request.method == 'POST':

        if 'csvfile' not in request.FILES:
            return HttpResponseRedirect("/weights/")

        fh = request.FILES['csvfile']

        # config name is the filename
        config_name = ("%s" % fh)[:-4]
        # anyone can edit any configuration, regardless of ownership,
        # so we don't want to allow the creation of multiple configs
        # with the same name and different owners.  thus we do the
        # try/except block instead of the get_or_create.  config =
        # Configuration.objects.get_or_create(name=config_name,
        # owner=request.user)
        try:
            config = Configuration.objects.get(name=config_name)
        except:  # MultipleObjectsReturned or no config that matches query
            (config, created) = Configuration.objects.get_or_create(
                name=config_name, owner=request.user)

        # TODO: error checking (correct file type, etc.)
        table = csv.reader(fh)

        table.next()

        for row in table:
            # print "processing %s" % row
            id = row[0]
            weight = row[1]

            if id.startswith("Module "):
                modulename = id[7:]
                module = Module.objects.get(name=modulename)
                try:
                    wt = ModuleWeight.objects.get(config=config, module=module)
                    wt.weight = weight
                except:
                    wt = ModuleWeight.objects.create(
                        config=config,
                        module=module,
                        weight=weight)
                wt.save()

            else:
                question_number = id[9:]
                question = Question.objects.get(number=question_number)
                try:
                    wt = Weight.objects.get(config=config, question=question)
                    wt.weight = weight
                except:
                    wt = Weight.objects.create(
                        config=config,
                        question=question,
                        weight=weight)
                wt.save()

    return HttpResponseRedirect("/weights/")


@login_required
def save_config(request):
    config_id = request.POST['config']

    ajax_submitted = False
    try:
        ajax_submitted = request.POST['ajax']
    except:
        pass

    config = Configuration.objects.get(id=config_id)
    # save module weights
    for module in Module.objects.all():
        new_value = request.POST['moduleweight-%s' % module.id]
        if new_value == "":
            new_value = 0  # set to 0 if cleared
        # TODO handle NaN
        the_new_weight, created = ModuleWeight.objects.get_or_create(
            module=module, config=config, weight=new_value)
        if created:
            # delete all existing weights for this module and config, leaving
            # only the new one. Otherwise, mayhem ensues.
            old_weights = [
                mw for mw in ModuleWeight.objects.filter(
                    module=module,
                    config=config) if mw != the_new_weight]
            for ow in old_weights:
                ow.delete()
        the_new_weight.save()

    # save question weights
    for question in Question.objects.all():
    #  try:
        new_value = request.POST['weight-%s' % question.number]
        if new_value == "":
            new_value = 0  # set to 0 if cleared
        try:
            weight = Weight.objects.get(question=question, config=config)
            weight.weight = new_value
        except:
            weight, created = Weight.objects.get_or_create(
                question=question, config=config, weight=new_value)
        weight.save()
    #  except:
    # pass  # question not in the form -- this probably won't happen?
    if ajax_submitted:
        return HttpResponse("")
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

    process_questions(questions, headers)

    return HttpResponseRedirect("/admin/equation_balancer/question/")


def process_questions(questions, headers):
    # parse headers (so they can be in any order)
    for i in range(len(headers)):
        header = headers[i]
        if header.lower().strip() == "question text":
            id_text = i
        elif header.lower().strip() == "question number":
            id_number = i
        elif header.lower().strip() == "answers":
            id_answers = i
        elif header.lower().strip() == "numerical equivalent":
            id_weights = i
        elif header.lower().strip() == "module":
            id_module = i
        # else: print "invalid header detected: %s" % header

    for question in questions:
        process_question(question, id_module, id_number,
                         id_text, id_answers, id_weights)


def process_question(question, id_module, id_number,
                     id_text, id_answers, id_weights):
        (m, created) = Module.objects.get_or_create(name=question[id_module])
        m.save()
        q = Question(number=question[id_number],
                     text=question[id_text].strip(),
                     module=m)
        q.save()

        answers = question[id_answers].split(",")
        weights = question[id_weights].split(",")

        for (ans, wt) in zip(answers, weights):
            a = Answer(question=q,
                       text=ans.lower().strip(),
                       weight=wt.strip() or 1)
            a.save()


def write_csv_tmp_file(fh):
    destination = open('temp.csv', 'wb')
    for chunk in fh.chunks():
        destination.write(chunk)
    destination.close()


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

    # save to disk and re-open to fix line ending bug
    write_csv_tmp_file(fh)

    # for debugging row by row:
    patient_number_min = None
    patient_number_max = None

    destination = open('temp.csv', 'rU')

    table = csv.reader(destination)
    headers = table.next()

    # get current set of weights from webpage (not database, in case they have
    # modified but not saved yet)
    weights = question_weights(request)
    moduleweights = module_weights(request)
    patients, scores, order = process_table(
        table, moduleweights, weights,
        patient_number_min, patient_number_max, headers)

    result = {}
    result['data'] = patients
    result['scores'] = scores
    result['order'] = order
    return HttpResponse(json.dumps(result), mimetype="application/javascript")


def process_table(table, moduleweights, weights,
                  patient_number_min, patient_number_max, headers):
    patients = {}
    scores = {}
    order = []
    i = 0
    for row in table:
        if i < 4:
            i += 1
            continue
        patient_number = row[0]
        order.append(patient_number)
        if patient_number_min and int(patient_number) < patient_number_min:
            # print "skipping because smaller than %d " % patient_number_min
            continue
        if patient_number_max and int(patient_number) > patient_number_max:
            # print "skipping because greater than %d " % patient_number_max
            continue

        patient_data = {}
        for i in range(len(row)):
            if i == 0:
                continue
            try:
                patient_data[int(headers[i])] = row[i]
            except ValueError:
                pass
        #patients[patient_number]["answers"] = patient_data
        patients[patient_number] = patient_data
        patient_score = calculate_score(moduleweights, weights, patient_data)
        scores[patient_number] = patient_score
    return patients, scores, order


def question_weights(request):
    weights = {}
    for question in Question.objects.all():
        weights[question.number] = Decimal(
            request.POST['weight-%s' %
                         question.number])
    return weights


def module_weights(request):
    moduleweights = {}
    for module in Module.objects.all():
        moduleweights[module.id] = Decimal(
            request.POST['moduleweight-%s' %
                         module.id])
    return moduleweights


def recalculate(request):
    # unpack patient answers
    answers = {}
    weights = {}
    moduleweights = {}

    for variable in request.POST:
        if variable.startswith("patient-"):
            (prefix, patient_number, question_number) = variable.split("-", 2)
            answer = request.POST[variable]
            try:
                answers[int(patient_number)][int(question_number)] = answer
            except KeyError:
                # most likely: invalid literal for int() with base 10: 'No
                # Cavity 22'
                pass

        elif variable.startswith("weight-"):
            (prefix, question_number) = variable.split("-", 1)
            weight = request.POST[variable]
            weights[int(question_number)] = weight
        elif variable.startswith("moduleweight-"):
            (prefix, module_id) = variable.split("-", 1)
            moduleweight = request.POST[variable]
            moduleweights[int(module_id)] = moduleweight

    scores = {}

    for patient in answers:
        scores[patient] = calculate_score(
            moduleweights,
            weights,
            answers[patient])

    return HttpResponse(json.dumps(scores), mimetype="application/javascript")


def calculate_patient_score(request):
    patient = request.POST['patient']
    moduleweights = {}
    weights = {}
    answers = {}

    for module in Module.objects.all():
        moduleweights[module.id] = request.POST['moduleweight-%s' % module.id]

    for question in Question.objects.all():
        weights[question.number] = request.POST['weight-%s' % question.number]
        answers[question.number] = request.POST[
            'patient-%s-answer-%s' % (patient, question.number)]

    scores = calculate_score(moduleweights, weights, answers)
    json = '{"data": %s}' % scores
    return HttpResponse(json, mimetype="application/javascript")


def calculate_score(moduleweights, weights, answers):
    scores = {}
    totalscore = 0
    for module in Module.objects.all():
        # print "Starting with module %s" + module
        modulescore = 0
        moduleweight = float(moduleweights[module.id])
        for question in module.question_set.all():
            weight = float(weights[question.number])
            answer = answers[question.number]
            try:
                db_answer = question.answer_set.get(
                    text=answer.lower().strip())
                answer_wt = float(db_answer.weight)
            except:
                try:
                    answer_wt = float("%s" % answer)
                except ValueError:
                    answer_wt = 0

            scores['question-%s' %
                   question.number] = "%d" % (weight * answer_wt)
            modulescore += weight * answer_wt
        scores['module-%s' % module.id] = "%d" % (moduleweight * modulescore)
        totalscore += moduleweight * modulescore
    scores['total'] = "%d" % totalscore
    return scores
