from django import forms
from django.shortcuts import render, render_to_response
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from models import User
# Create your views here.

class UserForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

def regist(req):
	if(req.method == 'POST'):
		uf = UserForm(req.POST)
		if uf.is_valid():
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			User.objects.create(username = username, password = password)
			return HttpResponseRedirect('/login/')
	else:
		uf = UserForm()
	return TemplateResponse(req, 'regist.html', {'uf', uf})

def login(req):
	if(req.method == 'POST'):
		uf = UserForm(req.POST)
		if uf.is_valid():
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			users = User.objects.filter(username__exact = username, password__exact = password)
			if users:
				req.session["username"] = username
				req.session["password"] = password				
				response =  HttpResponseRedirect('/index/')
				#response.set_cookie('username', username, 3600)
				return response
			else:
				return HttpResponseRedirect('/login/')
	else:
		uf = UserForm()
	return TemplateResponse(req, 'login.html', {'uf', uf})

def index(req):
	username = req.session.get('username', 'guest')
	#username = req.COOKIES.get('username')
	return TemplateResponse(req, 'index.html', {'user': username})

def logout(req):
	del req.session['username']
	del req.session['password']
	response = HttpResponse('logout')
	return response
