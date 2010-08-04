from django.db import models
from django.db.models.signals import post_save

LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('es', 'Spanish'),
)

#User = models.get_model('auth','user')

Question = models.get_model('equation_balancer', 'question')
Answer = models.get_model('equation_balancer', 'answer')
  
class DisplayQuestion(models.Model):
  """associates questions with translations, images, help topics, etc."""
  part_of_score =  models.CharField(max_length=1, null=False)
  question = models.ForeignKey(Question, null=True, blank=True)
  #topic = models.ForeignKey(Topic, blank=True, null=True)
  image = models.ImageField(upload_to='question_images',blank=True,null=True)
  
  @models.permalink
  def get_absolute_url(self):
    return ('smilekit.views.question', [str(self.id), 'en'])

  
  @property
  def display_answers (self):
    return DisplayAnswer.objects.filter(answer__in= self.question.answer_set.all())

  
  @property
  def answers(self):
      return self.question.answer_set.all()
  
  
  @property
  def next(self):
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
  # order -- how to display within question
  
  
  
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
    
  
class AnswerTranslation(models.Model):
  """ a question wording in a particular language"""
  answer = models.ForeignKey(DisplayAnswer)
  language = models.CharField(max_length=2,  choices=LANGUAGE_CHOICES, null=False)
  text =  models.TextField(null=True, blank =True)
  
  ordering_string =  models.TextField(null=True, blank =True)

  class Meta:
    ordering = ['ordering_string']
  
  
  #@property
  #def orderfunction(self):
  #  return answer.text#

  #def __unicode__(self):
  #  return self.orderfunction  


def post_save_ordering_string_update(sender, **kwargs):
  #print "OK updating."
  answer_translation = kwargs['instance']
  #import pdb
  #pdb.set_trace()
  answer_translation.ordering_string = answer_translation.answer.question_text()
  
  #person = person_name.person
  #if person.ordering_string != unicode(person)[0:254]:
  #    person.ordering_string = unicode(person)[0:254]
  #    super(Person, person).save()

post_save.connect(post_save_ordering_string_update, sender=AnswerTranslation)


    
    
    
if 1 == 0:
  class Topic(models.Model):
    #a help topic
    
    def __unicode__(self): return self.name  
    name = models.CharField(max_length=30, unique=True)
    help_text = models.TextField(null=True, blank =True)
    # order?
    # associated text? -- i.e. landing page?
