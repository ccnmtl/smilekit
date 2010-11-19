from django.db import models
from django.db.models.signals import post_save
import datetime
import simplejson as json
#from equation_balancer.models import *
#from equation_balancer.models import *


User          = models.get_model('auth','user')
Configuration = models.get_model('equation_balancer', 'configuration')
Question      = models.get_model('equation_balancer', 'question')
DisplayQuestion      = models.get_model('equation_balancer', 'displayquestion')
Answer        = models.get_model('equation_balancer', 'answer')


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
  
  
  class Meta:
    ordering = ('study_id_number',)
  
    
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

  @property
  def interviewer (self):
    visits_happening = [ v for v in self.visit_set.all() if v.is_happening]
    if len (visits_happening) > 0:
      return visits_happening[0].interviewer
    return None
    

  @property
  def latest_answers (self):
    """Answers to previous interviews, for the collection tool to show on repeat visits. If the family has already answered a question more than once, the most recent answer is returned."""
    result = {}
    all_visits = self.visit_set.all()
    
    #start with most recent visits: we like fresh answers better than stale answers.
    all_visits.reverse()

    for v in all_visits:
      for r in v.response_set.all():
        if r.family == self:
          q_id = r.question.id
          if not result.has_key(q_id):
            result[q_id] = r.answer.id

    return result
    
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




  
  def responses (self):
    return Response.objects.filter (family= self)
  
  
  #this is the set of weights to assign to the questions asked:
  config = models.ForeignKey(Configuration)
  
  #General-purpose metadata fields (better safe than sorry.)
  #any extra notes on the interview (1)
  notes_1 = models.TextField(null=True, blank =True,  help_text = "Notes (1)")

  #any extra notes on the interview (2)
  notes_2 = models.TextField(null=True, blank =True,  help_text = "Notes (2).")

  #any extra notes on the interview (3)
  notes_3 = models.TextField(null=True, blank =True,  help_text = "Notes (3).")
  

class Visit (models.Model):
  @property
  def dir(self):
    return dir(self)
   
  families = models.ManyToManyField(Family)
  start_timestamp = models.DateTimeField(auto_now_add=True)
  end_timestamp = models.DateTimeField(null=True, blank =True)
  interviewer = models.ForeignKey(User)
  analytics_info =  models.TextField(null=True, blank =True)
  
  
  
  #Optional extra auth, maybe:
  token =  models.TextField(null=True, blank =True)


  class Meta:
    ordering = ('start_timestamp',)
  

  @property
  def is_happening(self):
    if self.start_timestamp == None:
      return False
    if self.end_timestamp != None:
      return False
    return True
  
  def close_now(self):
    self.end_timestamp = datetime.datetime.now()
    self.save()


  def store_answer (self, family_id, question_id, answer_id):
    family = Family.objects.get(pk=family_id)
    question = Question.objects.get(pk=question_id)
    answer = Answer.objects.get(pk=answer_id)
    
    
    assert family   != None
    assert question != None
    assert answer   != None
    
    new_response = Response()
    
    new_response.during_visit  = self
    new_response.family        = family
    new_response.question      = question
    new_response.answer        = answer
    
    new_response.save()
    self.save()
    


def monkey_patch_user_current_visit(self):
    my_current_visits = [ v for v in self.visit_set.all() if v.is_happening]
    #this should NEVER happen as there is code in the visit creation code in  family_info/views.py that prevents you from opening a new visit until you close the current one.
    assert len ( my_current_visits) < 2
    if len (my_current_visits) == 1:
      return my_current_visits [0]
    return None
      
User.current_visit = monkey_patch_user_current_visit




class Response (models.Model):
  @property
  def dir(self):
    return dir(self)
    
  during_visit = models.ForeignKey (Visit)
  family = models.ForeignKey (Family)
  question = models.ForeignKey (Question) #can't be null
  answer = models.ForeignKey (Answer) #can't be null

  @property
  def date_of_response(self):
    return 'a'
    
  @property
  def question_english(self):
    #import pdb
    #pdb.set_trace()
    #return DisplayQuestion.objects.get (question = self.question)
    return self.question.displayquestion_set.all()[0].english

  @property
  def question_english(self):
    return self.question.text

  @property
  def answer_english(self):
    return self.answer.text

  @property
  def interviewer(self):
    return self.during_visit.interviewer.first_name

  @property
  def module(self):
    return self.question.module.name
    
  @property
  def module_weight(self):
    return float(self.family.config.moduleweight_set.get(module=self.question.module).weight)

  @property
  def config(self):
    return self.family.config

  @property
  def question_weight(self):
    return float(self.question.weight_set.get(config=self.config).weight)

  @property
  def answer_weight(self):
    return float(self.answer.weight)

  @property
  def score(self):
    return self.module_weight * self.question_weight * self.answer_weight
    
  @property
  def date_of_response(self):
    #return self.during_visit.start_timestamp.strftime("%a, %d %b %Y %H:%M:%S")
    return self.during_visit.start_timestamp.strftime("%a %d %H:%M")
    
  @property
  def id_of_question(self):
    return self.question.id

  @property
  def id_of_answer(self):
    return self.answer.id

  @property
  def id_of_question(self):
    return self.question.id

  @property
  def id_of_family(self):
    return self.family.study_id_number


      

  

