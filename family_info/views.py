from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render_to_response
from smilekit.collection_tool.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from family_info.models import Visit, Family, User, RACE_ETHNICITY_CHOICES, EDUCATION_LEVEL_CHOICES
from equation_balancer.models import Configuration as equation_balancer_configuration
from collection_tool.views import question as collection_tool_question_view
import datetime, sys, pdb, simplejson as json

@login_required
def families(request, **kwargs):
    t = loader.get_template('family_info/families.html')
   
    c = RequestContext(request, {
      'error_message': kwargs.get ('error_message', ''),
      'families': Family.objects.filter(active = True),
      'health_workers': User.objects.all()
    })
    
    #pdb.set_trace()
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
    rp = request.POST;
    
    the_new_user = User(\
        username = request.POST['username'], \
        password= 'testing', \
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
                kwargs['error_message'] = 'Please type the new password twice.'
                return back_to_edit_user  ( request, **kwargs)
            
            elif " " in rp['password']:
                kwargs['error_message'] = 'Passwords cannot contain spaces.'
                return back_to_edit_user  ( request, **kwargs)
                
            else:
                new_password = rp['password']
    
        try:
            if " " in  rp['username']:
                kwargs['error_message'] = 'User name cannot contain spaces.'
                return back_to_edit_user  ( request, **kwargs)
            
            if  rp['username'] !=  rp['username'].lower():
                kwargs['error_message'] = 'User name cannot contain uppercase letters.'
                return back_to_edit_user  ( request, **kwargs)
            
            if the_user.username != rp['username'] and len (User.objects.filter(username=rp['username'])) > 0:
                kwargs['error_message'] = 'Sorry, %s is already in use. Please try another name.' % rp['username']
                return back_to_edit_user  ( request, **kwargs)
        
        
        
            the_user.first_name = rp['first_name']
            the_user.username = rp['username']
            the_user.last_name = rp['last_name']
            the_user.is_active = (rp['is_active'] == 'True')
            if new_password != None:
              the_user.set_password (new_password)
            the_user.save()
            error_message = 'Your changes were saved.'
            
        except:
            return back_to_edit_user (request, the_user = the_user, error_message =  "Error: %s" % sys.exc_info()[1])
    return back_to_edit_user  ( request, the_user = the_user, error_message= error_message)

@login_required
def back_to_edit_user (request, **kwargs):
    assert kwargs.has_key ('the_user')
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
      child_year_of_birth = int( rp['child_year_of_birth']),
      config_id = the_config.id
    )
    
    #not collected at the moment due to HIPAA concerns
    if rp.has_key ('child_first_name'):
      the_family.child_first_name                   = rp['child_first_name']
    if rp.has_key ('child_last_name'):
      the_family.child_last_name                    = rp['child_last_name'] 
    if rp.has_key ('family_last_name'):
      the_family.family_last_name                   = rp['family_last_name']
    
    the_new_family.mother_born_in_us =        (rp['mother_born_in_us'] == 'True')
    the_new_family.food_stamps_in_last_year = (rp['food_stamps_in_last_year'] == 'True')
    the_new_family.study_id_number                    = rp['study_id_number']
    the_new_family.study_id_number                    = study_id
    the_new_family.child_year_of_birth                = int(rp['child_year_of_birth'])
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
        
            the_family.active                             = (rp['active'] == 'True')
            the_family.mother_born_in_us                  = (rp['mother_born_in_us'] == 'True')
            the_family.food_stamps_in_last_year           = (rp['food_stamps_in_last_year'] == 'True')
            the_family.study_id_number                    = rp['study_id_number']
            the_family.study_id_number                    = study_id
            the_family.child_year_of_birth                = child_year_of_birth
            the_family.race_ethnicity                     = rp['race_ethnicity']
            the_family.highest_level_of_parent_education  = rp['highest_level_of_parent_education']
            the_family.date_modified = datetime.datetime.now(),
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
    #pdb.set_trace()
    rp = request.POST
    happening_visits =     [ v for v in request.user.visit_set.all() if v.is_happening]
    
    
    
    if len (happening_visits) == 0:
    
        #if there is no interview currently:
        the_families = Family.objects.filter(pk__in = rp.getlist('families'))
        interviewer = request.user
        new_visit = Visit(interviewer=request.user)
        new_visit.save()
        new_visit.families =  the_families
        new_visit.save();
        #else get list of families from current users's interview
        
        assert len(happening_visits ) < 2

        #assert that at least one family is selected.
        if len(the_families) == 0:
          my_args = {'error_message' : 'Please check at least one family.'}
          return families (request, **my_args)
        
       

        
    else:
        the_families = happening_visits[0].families.all()


    
    
    c = RequestContext(request, { 'families' : the_families } )
    t = loader.get_template('family_info/start_interview.html')
    return HttpResponse(t.render(c))


@login_required
def dashboard (request):
  """show the list of families page  -- this is just meant to be downloaded."""
    
  c = RequestContext(request, {} )
  t = loader.get_template('family_info/dashboard.html')
  return HttpResponse(t.render(c))


#TODO remove. as unneeded.
@login_required
def delete_interview(request, **kwargs):
    #this is only called when someone cancels an interview before starting it.
    
    #assert an interview has no responses associated with it
    
    #delete interview
    
    #redirect to the general families page with a confirm message.
    
    pass

      
#TODO misspelled!! interivew!!
@login_required
def wrap_up_interivew(request, **args):
    """ Show a list of responses for each family, and construct a form that will submit to end_interview_and_go_back_online:"""
    c = RequestContext(request,  {})
    t = loader.get_template('family_info/end_interview.html')
    return HttpResponse(t.render(c))
    
    
    
    
@login_required
def end_interview(request, **args):
  """Attempt to store the responses posted and, on success, redirect to the list of families."""
  rp = request.POST
  
  visits = [ v for v in request.user.visit_set.all() if v.is_happening]
  if len(visits) == 0:
    #probably just hit the back button by mistake.
    return families(request)
  
  assert len (visits) == 1
  my_visit = visits[0]
      
  for fam in my_visit.families.all():
  ## instead, json parse the value for that family and iteritem on that:
    family_id = fam.id
    try:
      their_answers = json.loads(rp[str(family_id)])
    except ValueError:
      their_answers = {}
      
    for question_id, answer_id in their_answers.iteritems():
        my_visit.store_answer (family_id, int(question_id), int(answer_id))
        
  ## END ITERATE OVER FAMILIES...
  #close the visit
  my_visit.close_now()   
  assert not my_visit.is_happening
  return families(request)
