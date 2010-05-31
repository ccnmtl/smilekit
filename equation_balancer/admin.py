from smilekit.equation_balancer.models import Module, Question, Answer
from smilekit.equation_balancer.models import Configuration, ModuleWeight, Weight
from django.contrib import admin

admin.site.register(Module)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Configuration)
admin.site.register(ModuleWeight)
admin.site.register(Weight)
