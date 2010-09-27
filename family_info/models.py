from django.db import models
from django.db.models.signals import post_save
#from equation_balancer.models import *


User          = models.get_model('auth','user')
assert User != None

Configuration = models.get_model('equation_balancer', 'configuration')
assert Configuration != None
#TODO: add 'no data' option to these and make them mandatory. Make "no data" the default.

RACE_ETHNICITY_CHOICES = (
  ('nd', 'No data'),
  ('aa', 'African-American'),
  ('ca', 'Caucasian'),
  ('la', 'Hispanic'),
  ('as', 'Asian'),
  ('na', 'Native-American'),
  ('ot', 'Other'),
)

EDUCATION_LEVEL_CHOICES = (
  ('nd', 'No data'),
  ('lt', 'Did not complete high school'),
  ('hi', 'Earned a a high-school degree.'),
  ('co', 'More than a high-school degree.'),
)

    
class Family(models.Model):
  active = models.BooleanField( help_text = "Uncheck to mostly-delete this family" , default = True)
  
  @property
  def dir(self):
    return dir(self)
    
  def __unicode__(self):
    return "Family # %d" % self.study_id_number
    
  #study id (used as link. cannot be null.)
  study_id_number =         models.IntegerField(unique=True)
  family_last_name =        models.CharField(max_length=64, null = True, blank = True)
  child_last_name =         models.CharField(max_length=64, null = True, blank = True)
  child_first_name =        models.CharField(max_length=64, null = True, blank = True)
  child_year_of_birth =     models.IntegerField(null = True, blank = True)
  date_created =            models.DateTimeField(auto_now=True)
  date_modified =           models.DateTimeField(auto_now=True, auto_now_add=True)
  
  #demographic info:
  mother_born_in_us = models.BooleanField( help_text = "Was the mother born in the United States?", null=True, blank = True)
  food_stamps_in_last_year = models.BooleanField( help_text = "Has the family used food stamps in the past year?" , null=True, blank = True)
  highest_level_of_parent_education = models.CharField(
    max_length=2,
    choices=EDUCATION_LEVEL_CHOICES, 
    help_text = "Highest level of parents' education" , 
    default = 'nd'
  )
  race_ethnicity = models.CharField(
    max_length=2,
    choices=RACE_ETHNICITY_CHOICES,
    default = 'nd'
  )
    
  #any extra interview state aside from basic questions and answers:
  interview_state = models.TextField(blank=True, default = '{}')

  def set_interview_state (self, obj):
      if self.interview_state == "":
          self.interview_state = '{}'
      fact_obj = json.loads (self.interview_state)
      fact_obj.update(json.loads(obj))
      self.interview_state = json.dumps(fact_obj)
      self.save()

  def get_interview_state (self, keys):
      key_list = json.loads(keys)
      if self.interview_state != "":
          return dict([(key, json.loads(self.interview_state).get(key, '')) for key in key_list])
      return dict([(f, '') for f in key_list])

  def interview_state (self):
      try:
          return  simplejson.loads(self.interview_state)
      except:
          return {'error': 'Error loading interview state info.'}

  
  
  #this is the set of weights to assign to the questions asked:
  config = models.ForeignKey(Configuration)
  
  #General-purpose metadata fields (better safe than sorry.)
  #any extra notes on the interview (1)
  notes_1 = models.TextField(null=True, blank =True,  help_text = "Notes (1)")

  #any extra notes on the interview (2)
  notes_2 = models.TextField(null=True, blank =True,  help_text = "Notes (2).")

  #any extra notes on the interview (3)
  notes_3 = models.TextField(null=True, blank =True,  help_text = "Notes (3).")
  

#note: "interviewers" are just standard-issue django users.
class Interview (models.Model):
  @property
  def dir(self):
    return dir(self)
    
  family = models.ForeignKey('family') #can't be blank.
  interviewer = models.ForeignKey(User)
  start_timestamp = models.DateTimeField()
  end_timestamp = models.DateTimeField()
  
  notes = models.TextField(null=True, blank =True,  help_text = "Notes.")

  def __unicode__(self):
    return "Interview with family %d " + self.family.study_id_number
    



  
