from smilekit.equation_balancer.models import Module, Question, Answer
from smilekit.equation_balancer.models import (
    Configuration, ModuleWeight, Weight)
from django.contrib import admin


class TinyMceAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/site_media/js/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/site_media/js/simple_tinymce.js',
        )


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(TinyMceAdmin):
    inlines = [AnswerInline]
    verbose_name = 'Equation Balancer Question'
    verbose_name_plural = 'Equation Balancer Questions'

admin.site.register(Module)
admin.site.register(Configuration)
admin.site.register(ModuleWeight)
admin.site.register(Weight)
admin.site.register(Question, QuestionAdmin)
