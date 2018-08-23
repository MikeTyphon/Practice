#! python3

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