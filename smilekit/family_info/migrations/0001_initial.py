# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('equation_balancer', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, help_text=b'Uncheck to mostly-delete this family')),
                ('study_id_number', models.IntegerField(unique=True)),
                ('family_last_name', models.CharField(max_length=64, null=True, blank=True)),
                ('child_last_name', models.CharField(max_length=64, null=True, blank=True)),
                ('child_first_name', models.CharField(max_length=64, null=True, blank=True)),
                ('child_year_of_birth', models.IntegerField(null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('mother_born_in_us', models.NullBooleanField(help_text=b'Was the mother born in the United States?')),
                ('food_stamps_in_last_year', models.NullBooleanField(help_text=b'Has the family used food stamps in the past year?')),
                ('highest_level_of_parent_education', models.CharField(default=b'nd', help_text=b"Highest level of parents' education", max_length=2, choices=[(b'nd', b'No data'), (b'lt', b'Did not complete high school'), (b'hi', b'Earned a a high-school degree.'), (b'co', b'More than a high-school degree.')])),
                ('race_ethnicity', models.CharField(default=b'nd', max_length=2, choices=[(b'nd', b'No data'), (b'aa', b'African-American'), (b'ca', b'Caucasian'), (b'la', b'Hispanic'), (b'as', b'Asian'), (b'na', b'Native-American'), (b'ot', b'Other')])),
                ('interview_state', models.TextField(default=b'{}', blank=True)),
                ('notes_1', models.TextField(help_text=b'Notes (1)', null=True, blank=True)),
                ('notes_2', models.TextField(help_text=b'Notes (2).', null=True, blank=True)),
                ('notes_3', models.TextField(help_text=b'Notes (3).', null=True, blank=True)),
                ('config', models.ForeignKey(to='equation_balancer.Configuration')),
            ],
            options={
                'ordering': ('study_id_number',),
                'verbose_name_plural': 'Families',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ForeignKey(to='equation_balancer.Answer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_timestamp', models.DateTimeField(auto_now_add=True)),
                ('end_timestamp', models.DateTimeField(help_text=b'If necessary, you can force this interview to end by setting the date / time to today and now. Results collected during the interview may be lost.', null=True, blank=True)),
                ('analytics_info', models.TextField(null=True, blank=True)),
                ('token', models.TextField(null=True, blank=True)),
                ('families', models.ManyToManyField(to='family_info.Family')),
                ('interviewer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('start_timestamp',),
                'get_latest_by': 'end_timestamp',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='response',
            name='during_visit',
            field=models.ForeignKey(to='family_info.Visit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='response',
            name='family',
            field=models.ForeignKey(to='family_info.Family'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='response',
            name='question',
            field=models.ForeignKey(to='equation_balancer.Question'),
            preserve_default=True,
        ),
    ]
