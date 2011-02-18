from django.db import models

User = models.get_model('auth','user')


# configurations
class Configuration(models.Model):
  """A set of weights associated with questions and groups of questions"""
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


class Module(models.Model):
  """ A set of questions that can be weighted as a group for a given configuration."""
  @property
  def dir(self):
    return dir(self)
    
  def __unicode__(self): return self.name  
  name = models.CharField(max_length=30, unique=True)
      

class ModuleWeight(models.Model):
  """The relative importance of a module's questions for a particular configuration"""
  @property
  def dir(self):
    return dir(self)
    
  config = models.ForeignKey(Configuration)
  module = models.ForeignKey(Module)
  unique_together = (("config", "module"),)

  def __unicode__(self): return "%s: %s" % (self.module.name, self.weight)

  weight = models.DecimalField(decimal_places=3, max_digits=10)
  

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
  
  @property
  def all_answer_weights(self):
    return [a.weight for a in self.answer_set.all()]
  
  @property
  def max_answer_weight (self):
    return float(max (self.all_answer_weights))
    
  @property
  def min_answer_weight (self):
    return float(min (self.all_answer_weights))
  
  @property
  def show_planner (self):
    return self.text.lower() in ["number risky exposures", "fluoride rinse exposures", "children's daily toothbrushing"]
  
  class Meta:
    ordering = ['number']

  # empty for a fill-in-the-blank question; list of choices otherwise
  # examples:
  #  {'yes':1, 'no':-1}  # yes is a good thing e.g. brushing teeth
  #  {'yes':-1, 'no':1}  # no is a good thing e.g. eating candy
  #  {'always':2, 'sometimes':1, 'never':-1}  # same idea

class Weight(models.Model):
  """The relative importance of a question in a given configuration"""
  @property
  def dir(self):
    return dir(self)
    
  config = models.ForeignKey(Configuration)
  question = models.ForeignKey(Question)
  unique_together = (("config", "question"),)

  def __unicode__(self): return "%s: %s" % (self.question.number, self.weight)

  weight = models.DecimalField(decimal_places=3, max_digits=10)

class Answer(models.Model):
  @property
  def dir(self):
    return dir(self)
    
  def __unicode__(self): return "%s: %s (%s)" % (self.question.text, self.text, self.weight)

  question = models.ForeignKey(Question)
  text = models.CharField(max_length=500)

  # this weight is the researcher's estimated risk of answers for each question:
  # a lower weight denotes a low risk, a high rate denotes a high risk.
  # Note that these weights DO NOT change from config to config.
  weight = models.DecimalField(decimal_places=3, max_digits=10)
  
  #Note: ordering is done via the display questions.
  

