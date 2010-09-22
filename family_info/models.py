from django.db import models
from django.db.models.signals import post_save
#from equation_balancer.models import *


User          = models.get_model('auth','user')
assert User != None

Configuration = models.get_model('equation_balancer', 'configuration')
assert Configuration != None

RACE_ETHNICITY_CHOICES = (
  ('aa', 'African-American'),
  ('ca', 'Caucasian'),
  ('la', 'Hispanic'),
  ('as', 'Asian'),
  ('na', 'Native-American'),
  ('ot', 'Other'),
)

EDUCATION_LEVEL_CHOICES = (
  ('lt', 'Did not complete high school'),
  ('hi', 'Earned a a high-school degree.'),
  ('co', 'More than a high-school degree.'),
)


    
class Family(models.Model):
  @property
  def dir(self):
    return dir(self)
    
  def __unicode__(self):
    return "Family %d" + self.study_id_number
    
  #study id (used as link. cannot be null.)
  study_id_number = models.IntegerField(unique=True)
  family_last_name = models.CharField(max_length=64, null = True, blank = True)
  child_last_name = models.CharField(max_length=64, null = True, blank = True)
  child_first_name = models.CharField(max_length=64, null = True, blank = True)
  date_created =  models.DateTimeField(auto_now=True)
  date_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
  
  
  #demographic info:
  mother_born_in_us = models.BooleanField( help_text = "Was the mother born in the United States?", null=True, blank = True)
  food_stamps_in_last_year = models.BooleanField( help_text = "Has the family used food stamps in the past year?" , null=True, blank = True)
  highest_level_of_parent_education = models.CharField( max_length=2, choices=EDUCATION_LEVEL_CHOICES,  help_text = "Highest level of parents' education" , null=True, blank = True)
  race_ethnicity = models.CharField(max_length=2, choices=RACE_ETHNICITY_CHOICES, null=True, blank = True)  # 
  
  #this is the set of weights to assign to the questions asked:
  config = models.ForeignKey(Configuration)
  

  notes = models.TextField(null=True, blank =True,  help_text = "Notes.")
  

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
    



  
