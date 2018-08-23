#! python3

# DJANGO VERSION 2.1

#building first django app 

'''
What is Django? 

Django's primary goal is to create complex data driven websites. It is essentially a set of modules
built around creating web applications. It is a python framework for web development. 

'''
#this is a tutorial for a poll app
'''
What will this program do? 

This tutorial is for the creation of a basic poll application. 

It has two parts: 

1. A public site that lets people view polls and vote in them

2. An admin site that lets you add change and delete polls

'''

# in mysite folder, type 'python manage.py runserver'
#this will open Djanogo development server. This is a lightweight web server
#It is only to be used for development, it is not for use as a web server. 

#by default: the development server is set to the internal ip: '8000'
# to change server's port: run command 'python manage.py runserver ####'

# to listen on all public IP's 'python manage.py runserver 0:8000'
#0 is a shortcut for 0.0.0.0 


# 1.1 Creating a project

# 1.2 the development server

# 1.3 creating the polls app

# 1.4 write your first view

# when to use include() you sohuld always use include() when you include other URL patterns. admin.site.urls is the only exception to this. 

# this wires an index view into the URLconf. to verify if it is working, run: 

# python3 manage.py runserver



# 1.5 


#part 2 
#2.1 Database setup

# Python and django use SQLite as their default database. 

# run 'python manage.py migrate' on manage.py to create tables in the database that these will make use of

# settings.py includes: 
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
# ]
# these are all the apps which come with django and will be migrated. To keep them from being migrated
# comment them out in the settings.py file.


#2.2 - creating models

# in our simple poll app we will create the models 'Question' and 'Choice'

#Question has (question, publication date)

#Choice has two fields: (the text of the choice, vote tally)

#the following will create classes representing these two models

#the following code shoudl be added to teh models.py file in /polls

from django.db import models #this code is baked in to models file, it imports the models module from django.db

class Question(models.Model): #the class that represents the model 'Question', models.Model subclassses django.db.models.Model
	question_text = models.CharField(max_length=200) #each field is represented by an instance of a Field class. Field classes represent a database table column
							#the field class indicates to django the type of data the field holds. 
							#.Charfield is for character fields
	pub_date = models.DateTimeField('date published')#the pub_date is a name for the field instance in machine friendly format. the database will use the argument 'date published' as a human-friendly column name
							#DateTimeFields is for datetimes

class Choice(models.Model): #the class that represents the model 'Choice'
	question = models.ForeignKey(Question, on_delete=models.CASCADE) #a relationship is defined using Foreignkey. This tells django that each Choice is related to a single question
	choice_text = models.CharField(max_length=200) #some fields have required arguments, for Charfield a max_length is required, here it is set to 200
	votes = models.IntegerField(default=0)#some fields have optional arguments, in this case we set the default value of votes to 0



#2.3 - Activating models


# with the model code we have provided django is able to 

# 1. creat a database schema for this app
# 2. create a python database-access API for accessing Question and Choice objects. 

# now we need to tell our project that the 'polls' app is installed

'''
An important note:

Django apps are “pluggable”: You can use an app in multiple projects, 
and you can distribute apps, because they don’t have to be tied to a given Django installation.

'''

# to include the app in our project we must add a reference to its configuration class in 'INSTALLED_APPS' in 'settings.py'

#add polls.apps.PollsConfig
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# make sure that in models.py the code includes CharField, not Charfield. 


# run code 'python manage.py makemigrations polls'

# makemigrations tells django that you have made changes to your models. It also states that we want the changes to be logged as a migration. 


# the migrate commmand takes all migrations that have not been applied, (against a database called 'django migrations' also in migrations folder)
#0001_initial.py is the file where the migration is stored, you can read through it manually

# Migrations allow you to change your models over time without needing to delete your database or tables and make new ones


# it specializes in upgrading database live without losing data


#sqlmigrate command will take migration names and return their sql

#run $ python manage.py sqlmigrate polls 0001


# this wil be the sql output

'''

BEGIN;
--
-- Create model Choice
--
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "c                                                                                                                                    hoice_text" varchar(200) NOT NULL, "votes" integer NOT NULL);
--
-- Create model Question
--
CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,                                                                                                                                     "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
--
-- Add field question to choice
--
ALTER TABLE "polls_choice" RENAME TO "polls_choice__old";
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "c                                                                                                                                    hoice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" integ                                                                                                                                    er NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "polls_choice" ("id", "choice_text", "votes", "question_id") SELECT                                                                                                                                     "id", "choice_text", "votes", NULL FROM "polls_choice__old";
DROP TABLE "polls_choice__old";
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id                                                                                                                                    ");
COMMIT;

'''
#note the following:

# The exact output will vary depending on the database you are using. The example above is generated for PostgreSQL.

# Table names are automatically generated by combining the name of the app (polls) and the lowercase name of the model – question and choice. (You can override this behavior.)

# Primary keys (IDs) are added automatically. (You can override this, too.)

# By convention, Django appends "_id" to the foreign key field name. (Yes, you can override this, as well.)

# The foreign key relationship is made explicit by a FOREIGN KEY constraint. Don’t worry about the DEFERRABLE parts;
#  that’s just telling PostgreSQL to not enforce the foreign key until the end of the transaction.

# It’s tailored to the database you’re using, so database-specific field types such as auto_increment (MySQL), serial (PostgreSQL), 
# or integer primary key autoincrement (SQLite) are handled for you automatically. Same goes for the quoting of field names – e.g.,
#  using double quotes or single quotes.

# The sqlmigrate command doesn’t actually run the migration on your database - it just prints it to the screen so that 
# you can see what SQL Django thinks is required. It’s useful for checking what Django
#  is going to do or if you have database administrators who require SQL scripts for changes.

#  now run python manage.py migrate
'''
The following is the 3 step guide to making migrations:
1. change models in models.py 
2. run python manage.py makemigrations to create migrations for those changes
3. run python manage.py migrate to apply the changes to the database


'''

#2.4 - playing with the API

# to invoke the python shell use the command "python manage.py shell"



#2.5 introducing the django admin
admin = 'administration'

#it works! look at site adminitration and play around with all the editable fields
# this is a working django app and proof that all this shit is easier on linux fo sho. 

# 2.6 explore with free admin functionality

# 3.0 Overview

# views are a 'type' of web page in my Django Application that serves a function and has a template.

# For Example a blog might have:

# 1. Homepage that displays the latest entries 
# 2. Entry 'detail' page permalink page for a single entry. 
# 3. year/month/day based archive page
# 4. Comment sectionview

# Our poll application has the following four views:
# 1. Question "index" page
# 2. Question "detail" page
# 3. Question "Results" page
# 4. Vote action

# Django delivers pages etc. via views. Views are represented by a simple python function. 
# One function for each view. Django chooses a view based on the URL that is requested. 

# A view pattern is the template the URL: domain.com/subject/variable1/varible2

# To get from URL to view Django uses URLconfs. A URLconf maps URL patterns to views! 

# What we are going to do now in this tutorial is basic use of URLconfs

# see URL dispatcher 'https://docs.djangoproject.com/en/2.1/topics/http/urls/'

# 3.2 Writing more views

# add the following to polls/views.py

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

# And in order to wire it together, add the following to polls/url.py:

   path('<int:question_id>/', views.detail, name = 'detail'),
    # ex: /polls/5/results/ 
    path('<int:question_id>/results/', views.results, name = 'results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name = 'vote'),


# 3.3 Writing views that actually do something:

# each view is responsible for doing one of two things: returning an HttpResponse object
# that contains the content for the requested page

# or

# raises an acception such as Http404

# Views can read from a database 

# or they can generate files or anything really

# The following will create  new index view which will disply the latest 5 poll 
# questions in the system 

# in polls/views
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

# Now we need to separate the python code so using templates, so that we don't need to go directly into the code to make changes

# create a directory called 'templates' in /polls --> /home/joshua/wickedfine/Practice/mysite/polls/templates


# the TEMPLATES setting indicates how Django will use templates. 

# the default file contains DjangoTemplates backend. 

# DjangoTemplates looks for a 'templates' subdirectory in each of your 'INSTALLED_APPS' as defined in settings


# now create another directory called polls, and inside that index.html:

# path = polls/templates/polls/index.html


# the app_directories templates loader allows us to refer to this template within django simply as polls/index.html


'''
Template namespacing

Now we might be able to get away with putting our templates directly in polls/templates 
(rather than creating another polls subdirectory), but it would actually be a bad idea. 
Django will choose the first template it finds whose name matches, and if you had a 
template with the same name in a different application, Django would be unable to 
distinguish between them. We need to be able to point Django at the right one, and the 
way to ensure this is by namespacing them. That is, by putting those templates inside 
another directory named for the application itself.
'''

put the following in our templates/polls/index.html file

{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}

# now we update our index view in /polls/views.py to use this template we created


# Remember that each view is only one function 

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))




#3.4 A shortcut: render()

# It's a very common idiom to load a templat, fill a context and return an HttpResponse object 
# with the reulst of the rendered template. Django let's us use a shortcut. 

# The following is a rewritten version of the previous code in polls/views:


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)




#3.5 Raising a 404 error 

# for the Question detail view (the view that displays the question text for a given poll)

# in polls/views

from django.http import Http404
from django.shortcuts import render

from .models import Question
# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

# The new concept here: The view raises the Http404 exception if a question with the requested ID doesn’t exist.

# create a new .html file template in /polls/templates/polls/detail.html



# 3.6 a shortcut: get_object_or_404

# Often you will use the idiom : get() and raise Http404 if the object you want doesn't exist

# a shortcut for this idiom is to replace the try except block with get_object_or_404()

# for an example we will rewrite the detail() function in /polls/views. Compare the previous code to the following:

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


# get_object_or_404() takes a django model as its first argument and a number of keyward arguments after. It then passes these to the get( function of the model's manage. It raises Http404 if the object doesn't exist

# Just as in the try except block we replaced would do. 




# 3.7 Use the template system

#dot lookup syntax means that when the template system encounters a variable name, it tries lookups in the following order:

# it will use the first lookup type that works

# for foo.bar

# 1.Dictionary lookup foo is a dictionary and bar is a key in the dictionary foo['bar']

# 2.attribute lookup looks for bar attribut in foo. 

# 3. List-index lookup, it will try to access the bar index in the list foo : foo[bar]

# git  git git 