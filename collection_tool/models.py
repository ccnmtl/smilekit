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
  """associates questions with images, help topics, etc."""
  part_of_score =  models.CharField(max_length=1, null=False)
  question = models.ForeignKey(Question, null=True, blank=True)
  #topic = models.ForeignKey(Topic, blank=True, null=True)
  image = models.ImageField(upload_to='question_images',blank=True,null=True)
  # order? -- would control display within topic
  #add a method for englishtranslation()
  #add a method for spanishtranslation()

  def __unicode__(self):
    #import pdb
    #pdb.set_trace()
    if self.translation_set.all():
      return self.translation_set.all()[0].text


class Translation(models.Model):
  """ a question wording in a particular language"""
  question = models.ForeignKey(DisplayQuestion)
  language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null=False)  # code for language (i.e. "EN", "ES")
  text =  models.TextField(null=True, blank =True)
  
class DisplayAnswer(models.Model):
  """associates answers with images, help topics, etc."""

  answer = models.ForeignKey(Answer)  # better to link to DB answer or DisplayQuestion?
  image = models.ImageField(upload_to='answer_images',blank=True,null=True)
  # order -- how to display within question
  
  #add a method for englishtranslation()
  #add a method for spanishtranslation()
  def question_text (self):
    return self.answer.question.text
  
  def answer_text (self):
    return self.answer.text  
    
  
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
