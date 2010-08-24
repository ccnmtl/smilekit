from django.db import models
from django.db.models.signals import post_save

LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('es', 'Spanish'),
)

#User = models.get_model('auth','user')

Question = models.get_model('equation_balancer', 'question')
Answer = models.get_model('equation_balancer', 'answer')

##################HELP AND TOPICS####
""" 
collection_tool_goal           
collection_tool_helpbulletpoint
collection_tool_helpdefinition 
collection_tool_helpitem       
collection_tool_helpurl        
collection_tool_topic          
collection_tool_translation    

drop table collection_tool_goal            ;
drop table collection_tool_helpbulletpoint ;
drop table collection_tool_helpdefinition  ;
drop table collection_tool_helpurl         ;
drop table collection_tool_helpitem        ;
drop table collection_tool_topic           ;


"""


class HelpItem(models.Model):


  english_objective = models.CharField(max_length=1024, null = True, blank = True)
  spanish_objective = models.CharField(max_length=1024, null = True, blank = True)
  english_title = models.CharField(max_length=1024, null = True, blank = True)
  spanish_title = models.CharField(max_length=1024, null = True, blank = True)
  english_script_instructions = models.TextField(null=True, blank =True)
  english_script = models.TextField(null=True, blank =True)
  spanish_script_instructions = models.TextField(null=True, blank =True)
  spanish_script = models.TextField(null=True, blank =True)
  
  
  def __unicode__(self):
    if self.english_title:
      return self.english_title
    return "(no title)"
    
  @property
  def dir(self):
    print self
    return dir(self)


class HelpUrl(models.Model):
  """Associates a help item with an arbitrary URL."""
  url = models.CharField(max_length=1024, null = True, blank = True)
  help_item = models.ForeignKey(HelpItem)
  def __unicode__(self): return self.url
    
  @property
  def dir(self):
      return dir(self)

class HelpBulletPoint(models.Model):
  """Displayed as a bullet-point list, these give a summary / what to watch for each page."""
  english_text =  models.TextField(null=True, blank =True)
  spanish_text =  models.TextField(null=True, blank =True)
  help_item = models.ForeignKey(HelpItem)

  ordering_rank = models.IntegerField()
  class Meta:
    ordering = ('ordering_rank',)
    
  @property
  def dir(self):
    return dir(self)


class HelpDefinition(models.Model):
  """Definitions."""
  english_title = models.CharField(max_length=1024, null = True, blank = True)
  english_body = models.TextField(null=True, blank =True)
  spanish_title = models.CharField(max_length=1024, null = True, blank = True)
  spanish_body = models.TextField(null=True, blank =True)
  help_item = models.ForeignKey(HelpItem)
  
  ordering_rank = models.IntegerField()
  class Meta:
    ordering = ('ordering_rank',)
    
  @property
  def dir(self):
    return dir(self)
    
class Topic(models.Model):    
  """an aspect of the patient's health that can be improved"""
  def __unicode__(self): return self.english_title  
  english_title  = models.CharField(max_length=1024, null = True, blank = True)
  spanish_title  = models.CharField(max_length=1024, null = True, blank = True)
  
  ordering_rank = models.IntegerField()
  class Meta:
    ordering = ('ordering_rank',)
    
  @property
  def dir(self):
    return dir(self)
  
class Goal (models.Model):
  """ one concrete step in the direction of a topic"""
  english_title  = models.CharField(max_length=1024, null = True, blank = True)
  spanish_title  = models.CharField(max_length=1024, null = True, blank = True)
  topic = models.ForeignKey(Topic)
  #is this associated with the planner JS game?
  show_in_planner = models.BooleanField()
  
  ordering_rank = models.IntegerField()
  class Meta:
    ordering = ('ordering_rank',)

  @property
  def dir(self):
    return dir(self)
##################END HELP AND TOPICS#######


        
  name =  models.CharField(max_length=256, null=False)
  description  = models.CharField(max_length=1024, null = True, blank = True)
  
class AssessmentSection(models.Model):
  """nav section that each question belongs to."""
  title =  models.TextField(null=True, blank =True)
  ordering_rank = models.IntegerField()
  class Meta:
    ordering = ('ordering_rank',)

  
  def __unicode__(self):
    return self.title

  #TODO:     """additionally, you may want to think about how force the system to differentiate between multiple choice questions that allow multiple answer selections (example: what are some of your favorite foods?) and ones that require a single answers (example: what is your child's main source of drinking water? bottled, tap, both)"""
  # This implies a json object stored in a field, itself in a question that has a text value."
  #TODO: How would we score these???
  
    
  
  
class DisplayQuestion(models.Model):
  """associates questions with translations, images, help topics, etc."""
      
  STOCK_ANSWER_CHOICES = (
      ('yesno', 'Yes / No'),
      ('number_of_times', 'None / Once / Twice / More than Twice'),
      ('relative_frequency', 'Never / Sometimes / Often / Always'),
      ('agree_disagree', 'Agree / Unsure / Disagree'),
  )

  stock_answers = models.CharField(max_length=30, choices=STOCK_ANSWER_CHOICES, blank =True, null=True) 
  part_of_score =  models.BooleanField()
  question = models.ForeignKey(Question, null=True, blank=True)
  nav_section = models.ForeignKey(AssessmentSection, null=True, blank=True)
  topic = models.ForeignKey(Topic, null=True, blank=True)
  image = models.ImageField(upload_to='question_images',blank=True,null=True)
  
  
  if 1 == 1:
    #@models.permalink
    def get_absolute_url(self):
      #import pdb
      #pdb.set_trace()
      
      #return ('smilekit.collection_tool.views.question', [str(self.id), 'en'])
      print '/collection_tool/question/%d/language/en/' % self.id
      return '/collection_tool/question/%d/language/en/' % self.id



  @property
  def question_type(self):
    return self.question.type
  
  
  #this violates DRY but I'm fine with that for now.
  @property
  def help_item(self):
    #import pdb
    #pdb.set_trace()
    try:
      #print HelpUrl.objects.filter (url__contains = 'question/%d' % self.id )[0]
      return HelpUrl.objects.filter (url__contains = 'question/%d' % self.id )[0]
    except:
      #print "exception thrown"
      return None
    #print "no exception thrown"
    return None
    
    
  @property
  def display_answers (self):
    return DisplayAnswer.objects.filter(answer__in= self.question.answer_set.all())

  
  @property
  def answers(self):
    return self.question.answer_set.all()
  
  @property
  def dir(self):
    return dir(self)
  
  

  @property
  def next(self):
    """ return the next DISPLAYQUESTION in order by id"""
    all_numbers = [q.id for q in DisplayQuestion.objects.all()]
    all_numbers.sort()
    my_number = self.id
    next_index = all_numbers.index(my_number) + 1
    if next_index == len(all_numbers):
      return None
    
    #import pdb
    #pdb.set_trace()
    
    try:
      return DisplayQuestion.objects.get(id=all_numbers[next_index])
    except:
      return None
      
      
    if 1 == 0:
              """ This returns the next QUESTION in order"""
              all_numbers = [q.number for q in Question.objects.all()]
              my_number = self.question.number
              next_index = all_numbers.index(my_number) + 1
              try:
                next_question = Question.objects.get(number=all_numbers[next_index])
                return next_question.displayquestion_set.all()[0]
              except:
                return None
  
  
  @property
  def prev(self):
    """ return the previous DISPLAYQUESTION in order by id, please."""
    all_numbers = [q.id for q in DisplayQuestion.objects.all()]
    all_numbers.sort()
    my_number = self.id
    prev_index = all_numbers.index(my_number) - 1
    if prev_index == -1:
      return None
    try:
      #import pdb
      #pdb.set_trace()
      return DisplayQuestion.objects.get(id=all_numbers[prev_index])
    except:
      return None
    
    if 1 == 0:
          """ This returns the previous QUESTION in order"""
          all_numbers = [q.number for q in Question.objects.all()]
          my_number = self.question.number
          prev_index = all_numbers.index(my_number) - 1
          try:
            prev_question = Question.objects.get(number=all_numbers[prev_index])
            return prev_question.displayquestion_set.all()[0]
          except:
            return None
      


  @property
  def english(self):
    try:
      return Translation.objects.get(question=self, language='en').text
    except:
      return None

  @property
  def spanish(self):
    try:
      return Translation.objects.get(question=self, language='es').text
    except:
      return None

  
  def wording(self, preferred_language_code):
    """attempts to provide a wording in preferred language; otherwise return a language in an arbitrary language; otherwise returns a fixed string."""
    try:
      return Translation.objects.get(question=self, language=preferred_language_code).text
    except:
      pass
    
    
    try:
      return self.translation_set.all()[0].text
    except:
      pass    
    
    return "Sorry, no wordings provided in either language. Enter wordings at /admin/collection_tool/displayquestion/%d/" % self.id
  
  
  def __unicode__(self):
    """ Just the English."""
    try:
      return self.english
    except:   
      return None

class Translation(models.Model):
  """ a question wording in a particular language"""
  question = models.ForeignKey(DisplayQuestion)
  language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null=False)  # code for language (i.e. "EN", "ES")
  text =  models.TextField(null=True, blank =True)
  
class DisplayAnswer(models.Model):
  """associates answers with images, help topics, etc."""

  #TODO: this isn't right: this should be a one-to-one mapping. there should only be one display answer per answer. this shouln't be a foreign key.
  answer = models.ForeignKey(Answer)  # better to link to DB answer or DisplayQuestion?
  
  image = models.ImageField(upload_to='answer_images',blank=True,null=True)
  
  ordering_rank = models.IntegerField()
  class Meta:
    ordering = ('ordering_rank',)
  
  
  def question_text (self):
    return self.answer.question.text
  
  def answer_text (self):
    return self.answer.text  
    
  @property
  def english(self):
    try:
      return AnswerTranslation.objects.get(answer=self, language='en').text
    except:
      return None

  @property
  def spanish(self):
    try:
      return AnswerTranslation.objects.get(answer=self, language='es').text
    except:
      return None
  
  
  def wording(self, preferred_language_code):
    """attempts to provide a wording in preferred language; otherwise falls back on the other language; otherwise returns a fixed string."""
    try:
      return AnswerTranslation.objects.get(answer=self, language=preferred_language_code).text
    except:
      pass
    
    
    try:
      return self.answer_translation_set.all()[0].text
    except:
      pass    
    
    return "Sorry, no wordings provided in either language. Enter wordings at /admin/collection_tool/displayanswer/%d/" % self.id
  
  @property
  def dir(self):
    return dir(self)
  
class AnswerTranslation(models.Model):
  """ a question wording in a particular language"""
  answer = models.ForeignKey(DisplayAnswer)
  language = models.CharField(max_length=2,  choices=LANGUAGE_CHOICES, null=False)
  text =  models.TextField(null=True, blank =True)
  
  ordering_string =  models.TextField(null=True, blank =True)

  class Meta:
    ordering = ['ordering_string']


  @property
  def dir(self):
    return dir(self)
    
    
def post_save_ordering_string_update(sender, **kwargs):
  answer_translation = kwargs['instance']
  answer_translation.ordering_string = answer_translation.answer.question_text()
  


post_save.connect(post_save_ordering_string_update, sender=AnswerTranslation)


  
