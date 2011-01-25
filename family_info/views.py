from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseRedirect
from smilekit.collection_tool.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from family_info.models import Visit, Family, User, RACE_ETHNICITY_CHOICES, EDUCATION_LEVEL_CHOICES
from equation_balancer.models import Configuration as equation_balancer_configuration
from collection_tool.views import question as collection_tool_question_view
import datetime, sys, pdb, simplejson as json
from django.core.urlresolvers import reverse


@login_required
def families(request, **kwargs):
    t = loader.get_template('family_info/families.html')   
    c = RequestContext(request, {
      'error_message': kwargs.get ('error_message', ''),
      'families': Family.objects.filter(active = True),
      'health_workers': User.objects.all(),
      'just_finished_visit': kwargs.get("just_finished_visit"),
    })
    return HttpResponse(t.render(c))

#**************************
#USER CRUD:
@login_required
def new_user(request, **kwargs):
    """ this displays a blank new user form"""
    varz = {}
    varz.update (kwargs)
    c = RequestContext(request,  varz)
    t = loader.get_template('family_info/add_edit_user.html')
    return HttpResponse(t.render(c))

@login_required
def back_to_new_user (request, **kwargs):
    #pdb.set_trace()
    c = RequestContext(request,{
        'error_message' :  kwargs.get('error_message', '')
    })
    t = loader.get_template('family_info/add_edit_user.html')
    return HttpResponse(t.render(c))

@login_required
def insert_user(request, **kwargs):
    """ this validates the user form and inserts the user."""
    rp = request.POST
    the_new_user = User(\
        username = request.POST['username'], \
        password= '', \
        first_name = rp['first_name'],\
        last_name =  rp['last_name']\
    )
    
    if rp['password'] == '' or  rp['password_2'] == "" or rp['password'] != rp['password_2']:
        kwargs ['error_message'] =  'Please type the new user\'s password twice.'
        return back_to_new_user (request,**kwargs )
    
    
    if len (User.objects.filter(username=rp['username'])) > 0:
        error_message = 'Sorry, %s is already in use. Please try another name.' % rp['username']
        return back_to_new_user ( request, first_name = rp['first_name'], \
            last_name = rp['last_name'], username= '', error_message = error_message)
    
    
    the_new_user.set_password(rp['password'])
        
    the_new_user.save()
    
    error_message = 'Health worker user  %s was created.' % rp['username']
    return back_to_edit_user  ( request, the_user= the_new_user, error_message = error_message)
    

@login_required
def edit_user(request, **kwargs):
    rp = request.POST
    user_id = kwargs['user_id']
    """ edit the user"""
    error_message = ''
    the_user = get_object_or_404(User, pk=user_id)
    if request.POST != {}:
    
        #password prep:
        new_password = None
        if rp.has_key ('password') and rp['password'] != '':
            if rp['password'] != rp['password_2']:
                err = 'Please type the new password twice.'
                return back_to_edit_user  ( request, the_user = the_user, error_message = err)
            
            elif " " in rp['password']:
                err  = 'Passwords cannot contain spaces.'
                return back_to_edit_user  ( request, the_user = the_user, error_message = err)
                
            else:
                new_password = rp['password']
    
        if " " in  rp['username']:
            return back_to_edit_user  ( request, the_user = the_user, error_message= 'User name cannot contain spaces.')
        
        if  rp['username'] !=  rp['username'].lower():
            return back_to_edit_user  ( request, the_user = the_user, error_message='User name cannot contain uppercase letters.')
        
        if the_user.username != rp['username'] and len (User.objects.filter(username=rp['username'])) > 0:
            err =  'Sorry, %s is already in use. Please try another name.' % rp['username']
            return back_to_edit_user  ( request, the_user = the_user, error_message = err)
    
    
        try:
          the_user.first_name = rp['first_name']
          the_user.username = rp['username']
          the_user.last_name = rp['last_name']
          if new_password != None:
            the_user.set_password (new_password)
          the_user.save()
          error_message = 'Your changes were saved.'
          
        except:
          # misc. database errors:
          return back_to_edit_user (request, the_user = the_user, error_message =  "Error: %s" % sys.exc_info()[1])
          
          
    return back_to_edit_user  ( request, the_user = the_user, error_message= error_message)

@login_required
def back_to_edit_user (request, **kwargs):
    #assert kwargs.has_key ('user_id')
    varz ={}
    varz.update(kwargs)
    c = RequestContext(request, varz)
    t = loader.get_template('family_info/add_edit_user.html')
    return HttpResponse(t.render(c))


#**************************
#FAMILY CRUD:

def default_family_form_vars():
  return {
    'r_e_choices' : RACE_ETHNICITY_CHOICES,
    'e_l_choices' : EDUCATION_LEVEL_CHOICES,
    'equation_balancer_configs': equation_balancer_configuration.objects.all()
  }

@login_required
def new_family(request, **kwargs):
    """ this displays a new family form. You can pass in kv pairs from previous attempts to fill out the form via kwargs."""
    varz = default_family_form_vars()
    varz.update (kwargs)
    c = RequestContext(request,  varz)
    t = loader.get_template('family_info/add_edit_family.html')
    return HttpResponse(t.render(c))

@login_required
def insert_family(request, **kwargs):
    """ this validates the family form and inserts the family."""
    rp = request.POST;
    
    study_id = None
    try:
      study_id = int(rp['study_id_number'])
    except ValueError:
      kwargs ['error_message'] = "Sorry, couldn't turn : \"%s\" into a valid study ID number." % rp['study_id_number']
      return new_family (request,**kwargs )
    assert study_id != None
    
    if len (Family.objects.filter(study_id_number=study_id)) > 0:
        kwargs ['error_message'] = 'Sorry, there\'s already a family with study ID number %s .' % rp['study_id_number']
        return new_family (
          request,
          **kwargs
        )
        
    
    child_year_of_birth = None
    if rp['child_year_of_birth'] != '':
      try:
        child_year_of_birth = int(rp['child_year_of_birth'])
      except ValueError:
        kwargs ['error_message'] = "Sorry, %s is not a valid year." % rp['child_year_of_birth']
        return new_family (request,**kwargs )

    
    the_config = equation_balancer_configuration.objects.get(pk = rp['config_id'])
    assert the_config != None
    
    the_new_family = Family (
      active = True,
      study_id_number= study_id,
      date_created = datetime.datetime.now(),
      date_modified = datetime.datetime.now(),
      child_year_of_birth = child_year_of_birth,
      config_id = the_config.id
    )
    
    #not collected at the moment due to HIPAA concerns
    if rp.has_key ('child_first_name'):
      the_family.child_first_name                   = rp['child_first_name']
    if rp.has_key ('child_last_name'):
      the_family.child_last_name                    = rp['child_last_name'] 
    if rp.has_key ('family_last_name'):
      the_family.family_last_name                   = rp['family_last_name']
    
    the_new_family.mother_born_in_us =                  (rp['mother_born_in_us'] == 'True')
    the_new_family.food_stamps_in_last_year =           (rp['food_stamps_in_last_year'] == 'True')
    the_new_family.race_ethnicity                     = rp['race_ethnicity']
    the_new_family.highest_level_of_parent_education  = rp['highest_level_of_parent_education']
        
    the_new_family.save()
    error_message = 'Family  "%s" was created.' % the_new_family
    
    return back_to_edit_family  ( request, family = the_new_family, error_message= error_message)
    

@login_required
def back_to_edit_family (request, **kwargs):
    assert kwargs.has_key ('family')
    varz = default_family_form_vars()
    varz.update(kwargs)
    c = RequestContext(request, varz)
    t = loader.get_template('family_info/add_edit_family.html')
    return HttpResponse(t.render(c))

@login_required
def edit_family(request, **kwargs):
    rp = request.POST
    family_id = kwargs['family_id']
    
    """ edit the family"""
    error_message = None
    
    the_family = get_object_or_404(Family, pk=family_id)
    if rp != {}:
        try:
            #make sure study_id and year of birth are valid ints:
            study_id = None
            try:
              study_id = int(rp['study_id_number'])
            except ValueError:
              return back_to_edit_family (
                request,
                family=the_family,
                error_message="Sorry, couldn't turn : \"%s\" into a valid study ID number." % rp['study_id_number']
              )
            assert study_id != None
            
            child_year_of_birth = None
            if rp['child_year_of_birth'] != '':
              try:
                child_year_of_birth = int(rp['child_year_of_birth'])
              except ValueError:
                return back_to_edit_family (
                  request,
                  family=the_family,
                  error_message="Sorry, %s is not a valid year." % rp['child_year_of_birth']
                )
                
            if the_family.study_id_number != study_id and len (Family.objects.filter(study_id_number=rp['study_id_number'])) > 0:
                error_message = 'Sorry, there\'s already a family with study ID number %s .' % rp['study_id_number']
                return back_to_edit_family (
                  request,
                  family=the_family,
                  error_message=error_message
                )
                
                return back_to_edit_user  ( request, user, error_message)
                
            
            the_config = equation_balancer_configuration.objects.get(pk = rp['config_id'])
            assert the_config != None
            
            
            the_family.mother_born_in_us                  = (rp['mother_born_in_us'] == 'True')
            the_family.food_stamps_in_last_year           = (rp['food_stamps_in_last_year'] == 'True')
            the_family.study_id_number                    = rp['study_id_number']
            the_family.study_id_number                    = study_id
            the_family.child_year_of_birth                = child_year_of_birth
            the_family.race_ethnicity                     = rp['race_ethnicity']
            the_family.highest_level_of_parent_education  = rp['highest_level_of_parent_education']
            the_family.date_modified = datetime.datetime.now()
            
            the_family.config_id = the_config.id
            
            the_family.save()
            
            error_message = 'Your changes were saved.'
        except:
            return back_to_edit_family (request,
            family=the_family,
            error_message="Error: %s" % sys.exc_info()[1]
        )
   
    return back_to_edit_family  (
        request,
        family=the_family,
        error_message=error_message
      )


#**************************
#**************************
@login_required
def start_interview(request, **kwargs):
    rp = request.POST
    my_happening_visits =     [ v for v in request.user.visit_set.all() if v.is_happening]
    #can't start an interview if i'm already interviewing someone else:
    if len (my_happening_visits) == 0:
    
        the_families = Family.objects.filter(pk__in = rp.getlist('families'))

        #assert that at least one family is selected.
        if len(the_families) == 0:
          my_args = {'error_message' : 'Please check at least one family.'}
          return families (request, **my_args)
        
        #double-check nobody else started an interview with any of these families since you arrived on the page.
        if [fam for fam in the_families if fam.in_a_visit]:
          my_args = {'error_message' : 'Sorry, one of these families is already being visited.'}
          return families (request, **my_args)

        interviewer = request.user
        new_visit = Visit(interviewer=request.user)
        new_visit.save()
        new_visit.families =  the_families
        new_visit.save();
        #else get list of families from current users's interview
        
        assert len(my_happening_visits ) < 2

      
    else:
        #the_families = my_happening_visits[0].families.all()
        # no longer allowing this:
        return HttpResponseRedirect ( reverse (families))
        
    c = RequestContext(request, {
      'families' : the_families,
      'new_visit' : new_visit
     } )
    t = loader.get_template('family_info/start_interview.html')
    return HttpResponse(t.render(c))


@login_required
def dashboard (request):
  """this page allows the user to switch between families."""
  
  c = RequestContext(request, {} )
  t = loader.get_template('family_info/dashboard.html')
  return HttpResponse(t.render(c))

    
    
@login_required
def end_interview(request, **args):
  """Attempt to store the responses posted and, on success, redirect to the list of families."""
  rp = request.POST
  answer_count = 0
  
   
  if rp.has_key('visit_id'):
    try:
      visits = [ Visit.objects.get (pk =  rp['visit_id'])]
    except ValueError: # for old visits where no id is stored:
      visits = [ v for v in request.user.visit_set.all() if v.is_happening]
    except Visit.DoesNotExist:
      visits = [] #this can occasionally happen due to selenium test teardown.
  else:
    visits = [ v for v in request.user.visit_set.all() if v.is_happening]
  
  
  if 1 == 0:
      #old way:
      if rp.has_key('force_end'):
        if rp.has_key('visit_id'):
          visits = [ Visit.objects.get (pk =  rp['visit_id'])]
      else:
        visits = [ v for v in request.user.visit_set.all() if v.is_happening]
       
       
      
  if len(visits) == 0:
    #back button by mistake after ending an interview, or hit refresh.
    #just toss them back to families page.
    return HttpResponseRedirect ( reverse (families))
  
  assert len (visits) == 1
  my_visit = visits[0]
  for fam in my_visit.families.all():
    family_id = fam.id
    if rp.has_key('state_%d' % family_id):
      fam = Family.objects.get(pk=family_id)
      fam.set_state( rp['state_%d' % family_id])
    if rp.has_key(str(family_id)):
      try:
        their_answers = json.loads(rp[str(family_id)])
      except ValueError:
        their_answers = {}
      for question_id, answer_id in their_answers.iteritems():
        my_visit.store_answer (family_id, int(question_id), int(answer_id))
        answer_count = answer_count + 1
  
  my_visit.close_now()
  my_args = {}
  assert not my_visit.is_happening
  my_args['just_finished_visit'] = my_visit
  return families (request, **my_args)
  #return HttpResponseRedirect ( reverse (families))
  
@login_required
def help_summary(request):
  t = loader.get_template('family_info/help_summary.html')
  c = RequestContext(request,{
      'all_help_items': HelpItem.objects.all()
  })
  return HttpResponse(t.render(c))
  
  

def selenium_teardown(request):
  Family.objects.filter(study_id_number = 59638).delete()
  Family.objects.filter(study_id_number = 83695).delete()
  [v.delete() for v in request.user.visit_set.all()]

  
@login_required
def selenium(request,task):
    if not request.user.is_staff:
      return HttpResponseRedirect ( reverse (families))
    
    t = loader.get_template('family_info/selenium.html')
    
    if task =='setup':
        selenium_teardown(request)
        sel_message = "proceed"
   
    if task =='teardown':
        selenium_teardown(request)
        sel_message = "success"
        
    
    c = RequestContext(request,dict(task=task, sel_message=sel_message))
    return HttpResponse(t.render(c))
  
@login_required
def summary_table(request):
  t = loader.get_template('family_info/summary_table.html')
  c = RequestContext(request,{
      'all_families':   Family.objects.all(),
      'all_display_questions': DisplayQuestion.objects.all(),
  })
  return HttpResponse(t.render(c))
  
  
  
  #(r'^kill/visit/(?P<visit_id>\d+)/$',  'family_info.views.kill_visit'),
@login_required
def kill_visit(request, visit_id):
  t = loader.get_template('family_info/kill_visit.html')
  c = RequestContext(request,{
     'visit' : Visit.objects.get(pk=visit_id)
  })
  return HttpResponse(t.render(c))

#(r'^kill/localstorage/$',  'family_info.views.kill_localstorage'),
@login_required
def kill_localstorage(request):
  t = loader.get_template('family_info/kill_localstorage.html')
  c = RequestContext(request,{ })
  return HttpResponse(t.render(c))

