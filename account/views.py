from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
import models as account_models
from forms import *

def index(request):
	if request.user.is_authenticated():
	# doesn't need to signup
		return HttpResponseRedirect("/account/settings/")
	if request.method=="POST":
	# verify fields and login
		email=request.POST['email']
		username=User.objects.get(email=email)
		password=request.POST['password']
	        user = authenticate(username=username, password=password)
		if user is not None:
			# authenticated so returning as authenticated
			login(request,user)
			return HttpResponseRedirect("/");
		else:
			# error page with retry
			return render_to_response("account_login_register.html",{"reg_form":SignupForm(),"login_form":LoginForm()}) 
	else:
        # if method is get returns login form 
		return render_to_response("account_login_register.html",{"reg_form":SignupForm(),"login_form":LoginForm()});


def signup(request):
	if request.user.is_authenticated():
	# cant allow a logged in user to signup
		return render_to_response("message.html",{"message":"You are already logged in. Please logout and then signup for a new account"})
	else:
		if request.method=="POST":
		# Submission 
			suForm=SignupForm(request.POST)
			if suForm.is_valid():
			        user=User.objects.create_user(request.POST['email'],request.POST['email'],request.POST['password1']) #create a User with the given name and password and email
                                user.first_name=request.POST['first_name']
                                user.last_name=request.POST['last_name']
                                user.save()
                                #save the other credentials of the Person
                                person = account_models.person()
                                person.user_ptr = user
                                person.first_name = request.POST['first_name']
                                person.last_name = request.POST['last_name']
                                person.email = request.POST['email']
                                person.password = request.POST['password1']
                                person.sex = request.POST['sex']
                                person.occupation = request.POST['occupation']
                                person.phno = request.POST['phno']
                                person.institution = request.POST['institution']
                                person.address = request.POST['address']
                                person.pin = request.POST['pin']
                                person.save()
                                user.save()	
                                # log him in and go to home page
                                logged_in_user = authenticate(username=request.POST['username'],password=request.POST['password1'])
				if logged_in_user is not None:
					login(request,logged_in_user)
                                return HttpResponseRedirect("/")        
			else:
			# invalid form
				return render_to_response("account_login_register.html",{"reg_form":suForm,"login_form":LoginForm()})
	        else:
		# unauthenticated user so return a blank form
			return render_to_response("account_login_register.html",{"reg_form":SignupForm(),"login_form":LoginForm()})

def settings(request):
        if request.user.is_authenticated():
		return render_to_response("account_settings.html")
	else:
		return render_to_response("account_login_fields.html")

def logout(request):
        if request.user.is_authenticated():	
		auth_logout(request)
		return HttpResponseRedirect("/")
	else:
		return render_to_response("message.html",{"message":"You are not authorised to be here"})
