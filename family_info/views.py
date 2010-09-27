from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render_to_response
from smilekit.collection_tool.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from family_info.models import Family, User, RACE_ETHNICITY_CHOICES, EDUCATION_LEVEL_CHOICES
import datetime, sys, pdb

@login_required
def families(request):
  return render_to_response("family_info/families.html")
  
@login_required
def family_assessment(request):
  return render_to_response("family_info/family_assessment.html")
  
#TODO delete this:
##THIS has been rendered obsolete BY edit_family:  
@login_required
def family_information(request):
  return render_to_response("family_info/family_information.html")
  

@login_required
def sync(request):
  return render_to_response("family_info/sync.html")
  


##THIS WILL BE REPLACED BY USER CRUD:
@login_required
def health_worker_information(request):
  return render_to_response("family_info/health_worker_information.html")
  


#**************************
#USER CRUD:
@login_required
def new_user(request, **kwargs):
    """ this displays a blank new user form"""
    t = loader.get_template('family_info/add_edit_user.html')
    c = RequestContext(request, {})
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
        password= password, \
        first_name = rp['first_name'],\
        last_name =  rp['last_name']\
    )
    
    if len (User.objects.filter(username=rp['username'])) > 0:
        error_message = 'Sorry, %s is already in use. Please try another name.' % rp['username']
        return back_to_new_user ( request, first_name = rp['first_name'], \
            last_name = rp['last_name'], username= '', error_message = error_message)
        
    the_new_user.save()
    error_message = 'Health worker user  %s was created.' % rp['username']
    
    if rp.get('destination', '') == 'new':
        return back_to_new_user ( request, error_message = error_message)
    else:
        return back_to_edit_user  ( request, ag, new_user, error_message)
    

@login_required
def edit_user(request, **kwargs):
    rp = request.POST
    user_id = kwargs['user_id']
    
    """ edit the user"""
    #pdb.set_trace()
    user = get_object_or_404(User, pk=user_id)
    if request.POST != {}:
        try:
            if " " in  rp['username']:
                error_message = 'User ID cannot contain spaces.'
                return back_to_edit_user  ( request, user, error_message)
            
            if  rp['username'] !=  rp['username'].lower():
                error_message = 'User ID cannot contain uppercase letters.'
                return back_to_edit_user  ( request, user, error_message)
            
            if user.username != rp['username'] and len (User.objects.filter(username=rp['username'])) > 0:
                error_message = 'Sorry, %s is already in use. Please try another name.' % rp['username']
                return back_to_edit_user  ( request, user, error_message)
        
            user.first_name = request.POST['first_name']
            user.username = request.POST['username']
            user.last_name = request.POST['last_name']
            user.is_active = (request.POST['is_active'] == 'True')
            user.save()
            
        except:
            return back_to_edit_user (request, user, "Error: %s" % sys.exc_info()[1])
   
    error_message = 'Your changes were saved.'
    return back_to_edit_user  ( request, user, error_message)


@login_required
def back_to_edit_user (request, **kwargs):
    #pdb.set_trace()
    c = RequestContext(request,{
        'error_message' :  kwargs.get('error_message', ''),
        'user_id' :  kwargs.get('user_id', '')
    })
    t = loader.get_template('family_info/add_edit_user.html')
    return HttpResponse(t.render(c))




#**************************
#FAMILY CRUD:
#@login_required
def new_family(request, **kwargs):
    """ this displays a new family form. You can pass in kv pairs from previous attempts to fill out the form via kwargs."""
    
    varz = {
        'r_e_choices' : RACE_ETHNICITY_CHOICES,
        'e_l_choices' : EDUCATION_LEVEL_CHOICES
    }
    varz.update (kwargs)
    c = RequestContext(request,  varz)
    t = loader.get_template('family_info/add_edit_family.html')
    return HttpResponse(t.render(c))



#@login_required
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
    
    
    #TODO once this is working, reduce the amount of duplicate valiation code.
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
    
    
    the_new_family = Family (
      active = True,
      study_id_number= study_id,
      date_created = datetime.datetime.now(),
      date_modified = datetime.datetime.now(),
      child_year_of_birth = int( rp['child_year_of_birth']),
      config_id = 8 #TODO: get this from the form.
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
    
    varz = {
      'r_e_choices' : RACE_ETHNICITY_CHOICES,
      'e_l_choices' : EDUCATION_LEVEL_CHOICES
    }
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
        
            the_family.active =                   (rp['active'] == 'True')
            the_family.mother_born_in_us =        (rp['mother_born_in_us'] == 'True')
            the_family.food_stamps_in_last_year = (rp['food_stamps_in_last_year'] == 'True')
            
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

