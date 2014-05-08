from smilekit.collection_tool.models import (
    HelpDefinition, HelpBulletPoint, HelpUrl, HelpItem,
    Goal, Topic, Resource, AssessmentSection, Translation,
    DisplayQuestion, AnswerTranslation, DisplayAnswer,
    PlannerItem)
from django.contrib import admin


class TinyMceAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/media/js/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/media/js/simple_tinymce.js',
        )


class HelpDefinitionInline(admin.TabularInline):
    model = HelpDefinition
    extra = 2


class HelpBulletPointInline(admin.TabularInline):
    model = HelpBulletPoint
    verbose_name = 'Bullet Point'
    verbose_name_plural = 'Bullet Points'
    extra = 2


class HelpUrlInline(admin.TabularInline):
    model = HelpUrl
    verbose_name = 'Associated URL for this help item'
    verbose_name_plural = 'Associated URLs for this help item'
    extra = 2


class HelpItemAdmin(TinyMceAdmin):
    inlines = [HelpUrlInline, HelpBulletPointInline, HelpDefinitionInline]
    verbose_name = 'Help Item'
    verbose_name_plural = 'Help Items'

admin.site.register(HelpItem, HelpItemAdmin)


class GoalInline(admin.TabularInline):
    model = Goal


class TopicAdmin(TinyMceAdmin):
    inlines = [GoalInline]
    list_display = ('id', '__unicode__', 'displayquestions_string',)

admin.site.register(Topic, TopicAdmin)
admin.site.register(Resource)
admin.site.register(AssessmentSection)


class TranslationInline(admin.TabularInline):
    model = Translation
    fields = ['language', 'text']
    verbose_name = 'Question wording'
    verbose_name_plural = 'Question wordings'
    extra = 2


class DisplayQuestionAdmin(TinyMceAdmin):
    search_fields = ['question__text', ]
    list_display = ('question', '__unicode__')
    fields = ['question', 'display_regardless_of_weight',
              'ordering_rank', 'nav_section', 'image',
              'topics', 'resources', ]
    inlines = [TranslationInline]
    verbose_name = 'Display Question'
    verbose_name_plural = 'Display Questions'


admin.site.register(DisplayQuestion, DisplayQuestionAdmin)


class AnswerTranslationInline(admin.TabularInline):
    model = AnswerTranslation
    fields = ['language', 'text']
    extra = 2
    verbose_name = 'Answer wording'
    verbose_name_plural = 'Answer wordings'


class DisplayAnswerAdmin(TinyMceAdmin):
    list_display = ('question_text', 'answer_text')
    fields = ['answer', 'image', ]
    inlines = [AnswerTranslationInline]
    verbose_name = 'Display Answer'
    verbose_name_plural = 'Display Answers'

admin.site.register(DisplayAnswer, DisplayAnswerAdmin)
admin.site.register(PlannerItem)
