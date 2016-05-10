#!/usr/bin/python

# Structchat Web
# Component: Web frontend
# Module: Boobs

#Std. lib
from datetime import datetime, timedelta

#Django modules
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.db import connection

#Third-party
from passlib.hash import sha256_crypt
from markdown2 import markdown # use this maybe?

#Self-contained
from web.models import UserModel, RoomModel, MessageModel
from utils import escaping

def index(request):
	template = loader.get_template("index.html")

	messages = []
	for message in MessageModel.objects.all():
		messages.append({
			'devicetype':message.device_type,
			'username':message.username,
			'date':message.datetime.strftime("%Y-%m-%d %H:%M:%S"),
			'content':message.content,
			'rating':''
		})

	context = RequestContext(request, {
		'request':request,
		'posts':messages,
		'last_timestamp':messages[-1]['date']
	})
	if "username" not in request.session.keys():
		return HttpResponseRedirect("/login")

	return HttpResponse(template.render(context))

def post(request):
	content = escaping.escape_tags(request.GET.get("message_input", None))
	if not content:
		return HttpResponse("Go fuck a goat")

	message = MessageModel(
		device_type=getDeviceType(request),
		username=request.session['username'],
		content=markdown(content, extras=["fenced-code-blocks"]),
		datetime=datetime.now(),
		rating=""
	)
	message.save()
	return HttpResponse(content)

# Helper function for getting deivce type icon
def getDeviceType(request):
	meta = request.META['HTTP_USER_AGENT'].lower()
	linux = 'linux'
	windows = 'windows'
	android = 'android'
	apple = 'apple'
	if android in meta:
		return android
	elif linux in meta:
		return linux
	elif windows in meta:
		return windows
	elif apple in meta:
		return apple
	return 'user'

def getLatestPost(request):
	timestamp = request.GET.get("timestamp", None)
	if not timestamp:
		earlier = datetime.now() - timedelta(weeks=12)
	else:
		earlier = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") + timedelta(seconds=1)

	query = MessageModel.objects.filter(datetime__range=(earlier, datetime.now()))

	template = loader.get_template("event.html")
	for message in query:
		context = RequestContext(request, {
			'request':request,
			'post': {
				'devicetype':message.device_type,
				'username':message.username,
				'date':message.datetime.strftime("%Y-%m-%d %H:%M:%S"),
				'content':message.content,
				'rating':''
			}
		})
		return HttpResponse(template.render(context))

	return HttpResponse("")

def login(request):
	if "username" in request.session:
		return HttpResponseRedirect("/")

	if request.method == 'POST':

		username = request.POST.get("username", "")
		password = request.POST.get("password", "")


		try:
			user = UserModel.objects.get(username=username)
			if sha256_crypt.verify(password, user.password):
				request.session['username'] = user.username
				return HttpResponse('success')
			else:
				return HttpResponse('password_error')
		except UserModel.DoesNotExist:
			return HttpResponse('username_error')

	template = loader.get_template("login.html")
	context = RequestContext(request, {'request':request})
	return HttpResponse(template.render(context))

def logout(request):
	try:
		del request.session['username']
	except KeyError:
		pass
	return HttpResponseRedirect('/login')


def signUp(request):
	template = loader.get_template("signUp.html")
	if request.method == "POST":
		email = request.POST.get("email", "")
		username = request.POST.get("username", "")
		password = request.POST.get("password", "")
		password_repeat = request.POST.get("password_repeat", "")

		if UserModel.objects.filter(email=email).exists():
			return HttpResponse("email_error")

		if password != password_repeat:
			return HttpResponse("password_missmatch")

		if UserModel.objects.filter(username=username).exists():
			return HttpResponse("username_error")

		context = RequestContext(request, {'request':request})

		if email and username and password and password_repeat:
			user = UserModel(
				username=username,
				password=sha256_crypt.encrypt(password),
				email=email
			)
			user.save()
			return HttpResponse('success')

	context = RequestContext(request, {'request':request})
	return HttpResponse(template.render(context))

# Test view to see what's inside a db-table
def displayDatabase(request):
	if 'username' not in request.session or request.session['username'].lower() not in ['sebastian', 'seb', 'ajs']:
		context = RequestContext(request, {'errornumber':520, 'errormessage':'You do not have permission to enter this page.'})
		return HttpResponse(loader.get_template('errorPage.html').render(context))
		# return HttpResponse('You do not have permission to enter this page.\n')
	template = loader.get_template('database.html')

	models = []
	for model in [UserModel, MessageModel, RoomModel]:
		models.append({
			'name':model._meta.db_table,
			'columns':sorted(model._meta.get_all_field_names()),
			'rows':[[m.__dict__[c] for c in sorted(m.__dict__.keys()) if not c[0]=="_"] for m in model.objects.all()]
		})

	context = RequestContext(request, {
		'models':models,
		'request':request
	})
	return HttpResponse(template.render(context))

def home(request):
	template = loader.get_template('home.html')
	context = RequestContext(request, {'request':request})
	return HttpResponse(template.render(context))
