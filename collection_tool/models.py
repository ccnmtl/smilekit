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



class HelpItem(models.Model):
  english_objective = models.CharField(max_length=1024, null = True, blank = True)
  spanish_objective = models.CharField(max_length=1024, null = True, blank = True)
  english_title = models.CharField(max_length=1024, null = True, blank = True)
  spanish_title = models.CharField(max_length=1024, null = True, blank = True)
  
  english_script = models.TextField(null=True, blank =True,  help_text = "Basic script to follow")
  english_script_instructions = models.TextField(null=True, blank =True,  help_text = "More details about this subject")
  
  spanish_script = models.TextField(null=True, blank =True ,  help_text = "Basic script to follow")
  spanish_script_instructions = models.TextField(null=True, blank =True, help_text = "More details about this question")
  
  
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
  
  english_description = models.TextField(null=True, blank =True)
  spanish_description = models.TextField(null=True, blank =True)
  
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
  
  english_description = models.TextField(null=True, blank =True)
  spanish_description = models.TextField(null=True, blank =True)
  
  topic = models.ForeignKey(Topic)
  
  show_in_planner = models.BooleanField( help_text = "i.e. does picking this goal mean the next button takes you to the planner JS game?")
  
  ordering_rank = models.IntegerField()
  class Meta:
    ordering = ('ordering_rank',)

  @property
  def dir(self):
    return dir(self)
##################END HELP AND TOPICS#######


        
class AssessmentSection(models.Model):
  """nav section that each question belongs to."""
  title =  models.TextField(null=True, blank =True)

  english_title = models.CharField(max_length=1024, null = True, blank = True)
  spanish_title = models.CharField(max_length=1024, null = True, blank = True)

  ordering_rank = models.IntegerField()
    
  class Meta:
    ordering = ('ordering_rank',)

  
  @property
  def dir(self):
    return dir(self)
    
  def __unicode__(self):
    return self.title

  
  def display_question_ids(self):
    """ used for ordering"""
    return [q.id for q in self.displayquestion_set.all()] 
  

#TODO: refactor this to take into account a configuration.
#TODO: use caching for this.
def all_display_question_ids_in_order():
  result = []
  #order all questions, first by nav section, then by rank within that section:
  sections = [a for a in AssessmentSection.objects.all()]
  for a in [s.display_question_ids() for s in sections]:
    result.extend (a)
  return result
    

def has_image(image_field_file):
  try:
    if image_field_file.url != "":
      return True
    else:
      return False
  except:
    return False
  return False


class Resource(models.Model):
  """just a wrapper for a URL (e.g. video, internal or external link)"""
  
  name = models.CharField(max_length=500)
  url = models.CharField(max_length=500)
  resource_type =  models.CharField(max_length=64, help_text = "Ignore this for now.")
  
  ordering_rank = models.IntegerField(help_text = "Ignore this for now.")
  class Meta:
    ordering = ('ordering_rank',)
    
  @property
  def dir(self):
    return dir(self)

  def __unicode__(self):
    return self.name

  
class DisplayQuestion(models.Model):
  """associates questions with translations, images, help topics, etc."""

  display_regardless_of_weight =  models.BooleanField( help_text = "Check this to display this question (and store answers to it) for all configurations, regardless of the weight assigned to it.", default = False)

  question = models.ForeignKey(Question, null=True, blank=True)
  nav_section = models.ForeignKey(AssessmentSection, null=True, blank=True)
  
  topics = models.ManyToManyField(Topic, help_text =  "One or more topics this question is associated with.", null=True, blank=True)

  resources = models.ManyToManyField(Resource, help_text =  "Links to other pages that are relevant to this question.", null=True, blank=True)


  image = models.ImageField(upload_to='question_images',blank=True,null=True)
  
  ordering_rank = models.IntegerField(help_text = "Use this to determine the order in which the questions are asked within each nav section.")
  class Meta:
    ordering = ('ordering_rank',)

  def get_absolute_url(self):
    return '/collection_tool/question/%d/language/en/' % self.id

  @property
  def question_type(self):
    return self.question.type
  
  #this violates DRY but I'm fine with that for now.
  @property
  def help_item(self):
    try:
      return HelpUrl.objects.filter (url__contains = 'question/%d' % self.id )[0]
    except:
      #print "exception thrown"
      return None
    #print "no exception thrown"
    return None
    
  @property
  def has_question_picture(self):
    return has_image(self.image)
    
  @property
  def has_answer_pictures(self):
    #import pdb
    #pdb.set_trace()
    if len (self.display_answers) == 0:
      return False
    
    if len( [a.image for a in self.display_answers if has_image(a.image)]) == 0:
      return False  
      
    return True
    

  #http://kodos.ccnmtl.columbia.edu:7112/collection_tool/question/2/language/en/

  @property
  def no_pictures(self):
    return self.has_question_picture is False and self.has_answer_pictures is False
    
    
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
    """ return the next question in order by nav section, then rank."""
    all_numbers = all_display_question_ids_in_order()
    
    
    if self.id not in all_numbers:
      return None
    
    next_index = all_numbers.index(self.id) + 1
    
    if next_index == len(all_numbers):
      return None
    
    try:
      return DisplayQuestion.objects.get(id=all_numbers[next_index])
    except:
      return None

  @property
  def prev(self):
    """ return the previous question in order by nav section, then rank."""
    all_numbers = all_display_question_ids_in_order()
    #
    #import pdb
    #pdb.set_trace()
    #
    # if this question hasn't been assigned a section, i can't assign it an order
    # in the collection tool, so just return none.
    if self.id not in all_numbers:
      return None
    
    prev_index = all_numbers.index(self.id) - 1
    
    
    if prev_index == -1:
      return None
    try:
      return DisplayQuestion.objects.get(id=all_numbers[prev_index])
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
  """ an answer wording in a particular language."""
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


  
  
  
# planner widget items

class PlannerItem(models.Model):
  def __unicode__(self):
    return "%s: %s" % (self.type, self.label)

  TYPE_CHOICES = ( ('A', 'Fluoride'), ('B', 'Foods'), ('C', 'Drinks'))
  type = models.CharField(max_length=1, choices=TYPE_CHOICES)
  label = models.TextField()
  #image = models.ImageField(upload_to='answer_images',blank=True,null=True)