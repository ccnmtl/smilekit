from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render_to_response
from smilekit.collection_tool.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from family_info.models import Family, User
import datetime

#TODO: rename this "families"
@login_required
def families(request):
  return render_to_response("family_info/families.html")
  
  
  
  
@login_required
def family_assessment(request):
  return render_to_response("family_info/family_assessment.html")
  
  
##THIS WILL BE REPLACED BY FAMILY CRUD:  
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
    """ this displays a blank new family form"""
    t = loader.get_template('family_info/add_edit_family.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))


#@login_required
def back_to_new_family (request,  **kwargs ):
    #pdb.set_trace()
    c = RequestContext(request,{
        'first_name' : first_name,
        'last_name' : last_name,
        'username' : username,
        'error_message' : error_message
    })
    t = loader.get_template('family_info/add_edit_user.html')
    return HttpResponse(t.render(c))


if 1 == 0:

    goat = """
     
      
       Family (study_id_number=12, family_last_name='asd', child_last_name='asd', date_created = datetime.datetime.now(), date_modified = datetime.datetime.now(), child_year_of_birth=1992)

      
      """


#@login_required
def insert_family(request, **kwargs):
    """ this validates the family form and inserts the family."""
    rp = request.POST;
    study_id_number = int( rp['study_id_number'])
    
    
    #TODO check unique study id number    
    #TODO check integer for year #
    #TODO 
    if 1 == 0:
      if len (User.objects.filter(username=rp['username'])) > 0:
          error_message = 'Sorry, %s is already in use. Please try another name.' % rp['username']
          return back_to_new_user ( request, first_name = rp['first_name'], \
              last_name = rp['last_name'], username= '', error_message = error_message)
      
    
    the_new_family = Family (
      study_id_number= study_id_number,
      family_last_name= rp['family_last_name'],
      child_last_name= rp['child_last_name'],
      date_created = datetime.datetime.now(),
      date_modified = datetime.datetime.now(),
      child_year_of_birth = int( rp['child_year_of_birth']),
    )
    
        
    new_family.save()
    error_message = 'Family   %s was created.' % family
    
    import pdb
    pdb.set_trace()
    
    
    return back_to_edit_family  ( request, the_new_family, error_message)
    

@login_required
def edit_family(request, **kwargs):
    rp = request.POST
    family_id = kwargs['family_id']
    
    """ edit the family"""
    #pdb.set_trace()
    family = get_object_or_404(Family, pk=family_id)
    if request.POST != {}:
        try:
            pass
            #if " " in  rp['username']:
            #    error_message = 'User ID cannot contain spaces.'
            #    return back_to_edit_user  ( request, user, error_message)
            #
            #if  rp['username'] !=  rp['username'].lower():
            #    error_message = 'User ID cannot contain uppercase letters.'
            #    return back_to_edit_user  ( request, user, error_message)
            #
            #if user.username != rp['username'] and len (User.objects.filter(username=rp['username'])) > 0:
            #    error_message = 'Sorry, %s is already in use. Please try another name.' % rp['username']
            #    return back_to_edit_user  ( request, user, error_message)
        
            #family.first_name = request.POST['first_name']
            #family.username = request.POST['username']
            #family.last_name = request.POST['last_name']
            family.is_active = (request.POST['is_active'] == 'True')
            family.save()
            
        except:
            return back_to_edit_user (request, user, "Error: %s" % sys.exc_info()[1])
   
    error_message = 'Your changes were saved.'
    return back_to_edit_user  ( request, user, error_message)

@login_required
def back_to_edit_family (request, **kwargs):
    c = RequestContext(request,{
        'family' :  kwargs['family'],
        'error_message' : kwargs['error_message']
    })
    t = loader.get_template('family_info/add_edit_family.html')
    return HttpResponse(t.render(c))


#**************************
#**************************

