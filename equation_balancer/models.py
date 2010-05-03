from django.db import models

User = models.get_model('auth','user')

class Question(models.Model):
  def __unicode__(self): return "%s: %s" % (self.row, self.text)

  TYPE_CHOICES = (
    (u'T', u'Text Input'),
    (u'M', u'Multiple Choice'),
  )
  type = models.CharField(max_length=2, choices=TYPE_CHOICES)
  module = models.CharField(max_length=30)

  row = models.CharField(max_length=30, primary_key=True)  # question # on spreadsheet
  text = models.CharField(max_length=500)

  #order = models.IntegerField()  # the order it displays within the module
  #ordering = ['order']

  # empty for a fill-in-the-blank question; list of choices otherwise
  # examples:
  #  {'yes':1, 'no':-1}  # yes is a good thing e.g. brushing teeth
  #  {'yes':-1, 'no':1}  # no is a good thing e.g. eating candy
  #  {'always':2, 'sometimes':1, 'never':-1}  # same idea
  answers = models.TextField(blank=True)


  
#class Answer(models.Model):
#  def __unicode__(self): return "%s: %s" % (question.name, text)

#  question = models.ForeignKey(Question)
#  text = models.CharField(max_length=500)

#  order = models.IntegerField()  # the order it displays within the question
#  ordering = ['order']
#  class Meta:
#    order_with_respect_to = 'question'



# configurations
class Configuration(models.Model):
  owner = models.ForeignKey(User)
  name = models.CharField(max_length=100)

  def __unicode__(self): return self.name

  #high_risk = models.IntegerField()
  #medium_risk = models.IntegerField()
  #low_risk = models.IntegerField()
  
class Weight(models.Model):
  config = models.ForeignKey(Configuration)
  question = models.ForeignKey(Question)
  unique_together = (("config", "question"),)

  def __unicode__(self): return "%s: %s" % (self.question.row, self.weight)

  weight = models.DecimalField(decimal_places=3, max_digits=10)
