from django.db import models

#User = models.get_model('auth','user')
Question = models.get_model('equation_balancer', 'question')
Answer = models.get_model('equation_balancer', 'answer')

class Topic(models.Model):
  def __unicode__(self): return self.name  
  name = models.CharField(max_length=30, unique=True)
  # order?
  # associated text? -- i.e. landing page?

class DisplayQuestion(models.Model):
  question = models.ForeignKey(Question)
  topic = models.ForeignKey(Topic)
  # order? -- would control display within topic
  imagelink = models.CharField(max_length=100, null=True)  # URL to associated image, if any
  
class Translation(models.Model):
  question = models.ForeignKey(DisplayQuestion)
  language = models.CharField(max_length=3)  # code for language (i.e. "EN", "ES")
  text = models.CharField(max_length=30)
  
class DisplayAnswer(models.Model):
  answer = models.ForeignKey(Answer)  # better to link to DB answer or DisplayQuestion?
  imagelink = models.CharField(max_length=100, null=True)  # URL to associated image, if any
  # order -- how to display within question
  
class AnswerTranslation(models.Model):
  answer = models.ForeignKey(DisplayAnswer)
  language = models.CharField(max_length=3)  # code for language (i.e. "EN", "ES")
  text = models.CharField(max_length=30)