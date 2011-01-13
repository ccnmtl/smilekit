from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from collection_tool.models import Goal


import datetime
import simplejson as json

#from collection_tool.urls import urlpatterns
#

def friendly_score (min_score, actual_score, max_score):
    """ One possible version of a weighted score: 1 is good, 10 is a lot of risk:"""
    range_of_possible_scores = max_score - min_score
    if range_of_possible_scores == 0:
      return None

    adjusted_score = actual_score - min_score
    result =    1.0 + round ( 9.0 * adjusted_score /  range_of_possible_scores )
    if 1 == 0:
      print "User's actual score is %f" % actual_score
      print "Worst possible score is %f " % max_score 
      print "Best possible score is  %f " %  min_score 
      print "Adjusted score  %f " %  adjusted_score 
      print "Friendly score is  %f" % result
    return result;
 
   
User          = models.get_model('auth','user')
Configuration = models.get_model('equation_balancer', 'configuration')
Question      = models.get_model('equation_balancer', 'question')
Answer        = models.get_model('equation_balancer', 'answer')
ModuleWeight  = models.get_model('equation_balancer', 'modueleweight')

DisplayQuestion      = models.get_model('collection_tool', 'displayquestion')


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
  def start_interview_info(self):
    all_questions = [dq.id for dq in self.config.display_questions()]
    #first_dq_id = self.config.first_display_question().id
    
    #from collection_tool.views import question as question_view
    
    url_list = self.config.url_list()
    first_url = url_list[0]
    #first_url = reverse(question_view, kwargs={'displayquestion_id': first_dq_id, 'language_code':'en'})
    
    
    tmp = {
      "first_question_url" : first_url,
      "family_id" : self.id,
      "family_study_id_number" : self.study_id_number,
      "previous_visit_questions" : self.latest_answers,
      "all_questions" : all_questions,
      "url_list" : url_list
    }
    # double-escape: this is printed into a string in the template, (unescape 1)
    # which string is passed to the browser's native JSON parser. (unescape 2)
    return_value =  json.dumps(tmp).replace ('\\', '\\\\');
    return return_value;
  
  @property
  def dir(self):
    return dir(self)
    
  def __unicode__(self):
    return "Family # %d" % self.study_id_number
  
  class Meta:
    ordering = ('study_id_number',)
    verbose_name_plural = "Families"
    
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
  
  @property
  def all_visits(self):
    return [v for v in self.visit_set.all() ]
  
  @property
  def in_a_visit(self):
    return len (self.visits_happening) > 0
  
  @property
  def visits_happening (self):
    return [ v for v in self.all_visits  if v.is_happening]
  
  @property
  def has_had_an_interview(self):
    return len (self.all_visits) > 0
    
  @property
  def config_locked(self):
    """ should we allow this family's configuration to change? Not if they've already had an interview."""
    return not self.has_had_an_interview
  
  @property
  def interviewer (self):
    if len (self.visits_happening) > 0:
      return self.visits_happening[0].interviewer
    return None
    
  @property
  def latest_answers (self):
    """Answers to previous interviews, for the collection tool to show on repeat visits. If the family has already answered a question more than once, the most recent answer is returned."""
    result = {}
    
    #start with most recent visits: we like fresh answers better than stale answers.
    all_visits = self.visit_set.all().reverse()
    
    #MEMENTOTE OMNES IN SAECULA SAECULORUM: THIS DOES NOT WORK.
    #all_visits.reverse()

    for v in all_visits:
      for r in v.response_set.all():
        if r.family == self:
          q_id = r.question.id
          if not result.has_key(q_id):
            result[q_id] = r.answer.id

    return result
   
   
    
  @property
  def goal_info (self):
    """A summary of goal info"""
    try:
      data = json.loads(self.interview_state)['goals_data']
    except:
      return {}
    
    #separate goal data from score data:
    temp_array = []
    for k, value in data.iteritems():
      try:
        the_id = int(k.split('_')[0])
        field_key = k.split('_')[1]
        if field_key in ['name','resp','stps','when']:
          the_goal = Goal.objects.get (pk = the_id)
          temp_array.append ((the_goal, field_key, value))
      except:
        pass
    
    if len(temp_array) == 0:
      return {}
    
    #ok, we do have goal data.
    result = {}
    for the_goal, field_key, val in temp_array:
      if not result.has_key(the_goal.id):
        result [the_goal.id] = {'goal': the_goal}
      result [the_goal.id][field_key] = val
      
    return result
    
  @property
  def percent_complete (self):
    """What percentage of the available questions has this family answered?"""
    if self.config.weight_set.all().count() == 0:
      return None
    return 100.0 * float(len(self.latest_answers)) / float(self.config.weight_set.all().count())

  @property
  def risk_score (self):
    """For each answer in a configuration, compute the best and worst possible scores based on all the answer data available. Then return out an easy-to-compare "friendly" score on a scale of 1 to 10. (1 is good, 10 is bad.)"""
    config = self.config
    min_score, actual_score, max_score = 0,0,0
    for answer in Answer.objects.filter (pk__in=self.latest_answers.values()):
      question = answer.question
      module = question.module
      #print answer
      try:
        overall_weight = float(config.moduleweight_set.get(module=module).weight)
      except ModuleWeight.DoesNotExist:
        overall_weight = 0.0
      #question_weight:
      try:
        question_weight = float(config.weight_set.get(question = question).weight)
      except:
        question_weight = 0.0
      #score:
      actual_score += float(answer.weight) *  question_weight * overall_weight
      #min and max scores:
      min_score += question.min_answer_weight * question_weight * overall_weight
      max_score += question.max_answer_weight * question_weight * overall_weight
      
      
    if min_score == max_score:
      return None
    
    return round(friendly_score ( min_score, actual_score, max_score))

  #any extra interview state aside from basic questions and answers:
  interview_state = models.TextField(blank=True, default = '{}')
  
    
  def set_state (self, obj):
    """ takes json"""
    fact_obj = json.loads (self.interview_state)
    fact_obj.update(json.loads(obj))
    self.interview_state = json.dumps(fact_obj)
    self.save()

  @property
  def state (self):
    """outputs a json string"""
    try:
      return  self.interview_state
    except:
      return json.dumps({'error': 'Error loading interview state info.'})

  @property
  def evil_state(self):
    """outputs an extra replaced json string"""
    return self.state.replace ('\\', '\\\\');
  
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
  end_timestamp = models.DateTimeField(null=True, blank =True, help_text = "If necessary, you can force this interview to end by setting the date / time to today and now. Results collected during the interview may be lost.")
  interviewer = models.ForeignKey(User)
  analytics_info =  models.TextField(null=True, blank =True)
  
  #Optional extra auth, maybe:
  token =  models.TextField(null=True, blank =True)

  
  class Meta:
    ordering = ('start_timestamp',)

  def __unicode__(self):
    return "Visit %s" % self.pk

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
  def question_english(self):
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


      

  

