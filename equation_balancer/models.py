from django.db import models

User = models.get_model('auth','user')

class Module(models.Model):
  @property
  def dir(self):
    return dir(self)
    
  def __unicode__(self): return self.name  
  name = models.CharField(max_length=30, unique=True)

  

class Question(models.Model):
  @property
  def dir(self):
    return dir(self)
    
  def __unicode__(self): return "%s: %s" % (self.number, self.text)

  TYPE_CHOICES = (
    (u'T', u'Text Input'),
    (u'M', u'Multiple Choice'),
  )
  type = models.CharField(max_length=2, choices=TYPE_CHOICES)
  module = models.ForeignKey(Module)

  number = models.IntegerField()
  text = models.CharField(max_length=500)
  
  
  class Meta:
    ordering = ['number']

  # empty for a fill-in-the-blank question; list of choices otherwise
  # examples:
  #  {'yes':1, 'no':-1}  # yes is a good thing e.g. brushing teeth
  #  {'yes':-1, 'no':1}  # no is a good thing e.g. eating candy
  #  {'always':2, 'sometimes':1, 'never':-1}  # same idea

class Answer(models.Model):
  @property
  def dir(self):
    return dir(self)
    
  def __unicode__(self): return "%s: %s (%s)" % (self.question.text, self.text, self.weight)

  question = models.ForeignKey(Question)
  text = models.CharField(max_length=500)

  # this weight defines relative values of answers for each question
  weight = models.DecimalField(decimal_places=3, max_digits=10)

  #order = models.IntegerField()  # the order it displays within the question
  class Meta:
    pass
    #ordering = ['question.number']
    #ordering = ['']
    #order_with_respect_to = 'question'



  @property
  def good(self):
    """ This is used at the end of the interview,
    to determine which areas of dental health are of particular concern for a given family.
    This is arbitrary, but pretty darn effective.
    """
    all_weights = [a.weight for a in self.question.answer_set.all()]
    
    #one idea:
    average_weight = float(sum(all_weights)) / len(all_weights)
    
    #another idea: this yields 6 out of 21 good answers.
    #average_weight = (float(max(all_weights)) - float (min (all_weights))) / 2
    
    #note: low weights good, high weights bad.
    return ( float(self.weight) < average_weight )

    #>>> from equation_balancer import models
    #>>> from family_info.models import *
    #>>> from collection_tool.models import *


# configurations
class Configuration(models.Model):
  @property
  def dir(self):
    return dir(self)
    
  owner = models.ForeignKey(User)
  name = models.CharField(max_length=100)

  def __unicode__(self): return self.name

  def weights_greater_than_zero(self):
    return self.weight_set.filter(weight__gt=0)
  
  def questions_with_weights_greater_than_zero(self):
    return [w.question for w in self.weights_greater_than_zero()]
  
  #high_risk = models.IntegerField()
  #medium_risk = models.IntegerField()
  #low_risk = models.IntegerField()

class ModuleWeight(models.Model):
  @property
  def dir(self):
    return dir(self)
    
  config = models.ForeignKey(Configuration)
  module = models.ForeignKey(Module)
  unique_together = (("config", "module"),)

  def __unicode__(self): return "%s: %s" % (self.module.name, self.weight)

  weight = models.DecimalField(decimal_places=3, max_digits=10)

  
class Weight(models.Model):
  @property
  def dir(self):
    return dir(self)
    
  config = models.ForeignKey(Configuration)
  question = models.ForeignKey(Question)
  unique_together = (("config", "question"),)

  def __unicode__(self): return "%s: %s" % (self.question.number, self.weight)

  weight = models.DecimalField(decimal_places=3, max_digits=10)

