# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equation_balancer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=2, choices=[(b'en', b'English'), (b'es', b'Spanish')])),
                ('text', models.TextField(null=True, blank=True)),
                ('ordering_string', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['ordering_string'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssessmentSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('english_title', models.CharField(max_length=1024, null=True, blank=True)),
                ('spanish_title', models.CharField(max_length=1024, null=True, blank=True)),
                ('english_description', models.CharField(help_text=b'a few English sentences that will appear at the top of this index page.', max_length=1024, null=True, blank=True)),
                ('spanish_description', models.CharField(help_text=b'a few Spanish sentences that will appear at the top of this index page.', max_length=1024, null=True, blank=True)),
                ('ordering_rank', models.IntegerField()),
            ],
            options={
                'ordering': ('ordering_rank',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DisplayAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'answer_images', blank=True)),
                ('ordering_rank', models.IntegerField()),
                ('answer', models.ForeignKey(to='equation_balancer.Answer')),
            ],
            options={
                'ordering': ('ordering_rank',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DisplayQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_regardless_of_weight', models.BooleanField(default=False, help_text=b'Check this to display this question (and store answers to it) for all configurations, regardless of the weight assigned to it.')),
                ('image', models.ImageField(null=True, upload_to=b'question_images', blank=True)),
                ('ordering_rank', models.IntegerField(help_text=b'Use this to determine the order in which the questions are asked within each nav section.')),
                ('nav_section', models.ForeignKey(blank=True, to='collection_tool.AssessmentSection', null=True)),
                ('question', models.ForeignKey(blank=True, to='equation_balancer.Question', null=True)),
            ],
            options={
                'ordering': ('ordering_rank',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english_title', models.CharField(max_length=1024, null=True, blank=True)),
                ('spanish_title', models.CharField(max_length=1024, null=True, blank=True)),
                ('english_description', models.TextField(null=True, blank=True)),
                ('spanish_description', models.TextField(null=True, blank=True)),
                ('show_in_planner', models.BooleanField(default=False, help_text=b'i.e. does picking this goal mean the next button takes you to the planner JS game?')),
                ('ordering_rank', models.IntegerField()),
            ],
            options={
                'ordering': ('ordering_rank',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HelpBulletPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english_text', models.TextField(null=True, blank=True)),
                ('spanish_text', models.TextField(null=True, blank=True)),
                ('ordering_rank', models.IntegerField()),
            ],
            options={
                'ordering': ('ordering_rank',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HelpDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english_title', models.CharField(max_length=1024, null=True, blank=True)),
                ('english_body', models.TextField(null=True, blank=True)),
                ('spanish_title', models.CharField(max_length=1024, null=True, blank=True)),
                ('spanish_body', models.TextField(null=True, blank=True)),
                ('ordering_rank', models.IntegerField()),
            ],
            options={
                'ordering': ('ordering_rank',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HelpItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english_objective', models.CharField(max_length=1024, null=True, blank=True)),
                ('spanish_objective', models.CharField(max_length=1024, null=True, blank=True)),
                ('english_title', models.CharField(max_length=1024, null=True, blank=True)),
                ('spanish_title', models.CharField(max_length=1024, null=True, blank=True)),
                ('english_script', models.TextField(help_text=b'Basic script to follow', null=True, blank=True)),
                ('english_script_instructions', models.TextField(help_text=b'More details about this subject', null=True, verbose_name=b'English - More Details', blank=True)),
                ('spanish_script', models.TextField(help_text=b'Basic script to follow', null=True, blank=True)),
                ('spanish_script_instructions', models.TextField(help_text=b'More details about this question', null=True, verbose_name=b'Spanish - More Details', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HelpUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(help_text=b'Include leading and trailing slashes, please.', max_length=1024, null=True, blank=True)),
                ('help_item', models.ForeignKey(to='collection_tool.HelpItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlannerItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=1, choices=[(b'A', b'Fluoride'), (b'B', b'Foods'), (b'C', b'Drinks')])),
                ('label', models.TextField()),
                ('spanish_label', models.TextField()),
                ('risk_level', models.IntegerField()),
            ],
            options={
                'ordering': ('type', 'label'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=500)),
                ('resource_type', models.CharField(help_text=b"type 'video' here if this is a video; otherwise just leave blank.", max_length=64)),
                ('ordering_rank', models.IntegerField(help_text=b'Ignore this for now.')),
            ],
            options={
                'ordering': ('ordering_rank',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english_title', models.CharField(max_length=1024, null=True, blank=True)),
                ('spanish_title', models.CharField(max_length=1024, null=True, blank=True)),
                ('english_description', models.TextField(null=True, blank=True)),
                ('spanish_description', models.TextField(null=True, blank=True)),
                ('ordering_rank', models.IntegerField()),
            ],
            options={
                'ordering': ('ordering_rank',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=2, choices=[(b'en', b'English'), (b'es', b'Spanish')])),
                ('text', models.TextField(null=True, blank=True)),
                ('question', models.ForeignKey(to='collection_tool.DisplayQuestion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='helpdefinition',
            name='help_item',
            field=models.ForeignKey(to='collection_tool.HelpItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='helpbulletpoint',
            name='help_item',
            field=models.ForeignKey(to='collection_tool.HelpItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goal',
            name='topic',
            field=models.ForeignKey(to='collection_tool.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='displayquestion',
            name='resources',
            field=models.ManyToManyField(help_text=b'Links to other pages that are relevant to this question.', to='collection_tool.Resource', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='displayquestion',
            name='topics',
            field=models.ManyToManyField(help_text=b'One or more topics this question is associated with.', to='collection_tool.Topic', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answertranslation',
            name='answer',
            field=models.ForeignKey(to='collection_tool.DisplayAnswer'),
            preserve_default=True,
        ),
    ]
