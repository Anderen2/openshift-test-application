#!/usr/bin/python

# Structchat Web
# Component: Web frontend
# Module: Views

#Std. lib
import json
from datetime import datetime, timedelta

#Django modules
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.db import connection

#Third-party
from passlib.hash import sha256_crypt
from markdown2 import markdown

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
			# 'content':message.content,
			'content':markdown(message.content,extras=["fenced-code-blocks"]).replace("&amp;lt", "&lt").replace("&amp;gt", "&gt"),
			'rating':'',
			'id':message.pk
		})

	context = RequestContext(request, {
		'request':request,
		'posts':messages,
		'device':getDeviceType(request)
	})
	if "username" not in request.session.keys():
		return HttpResponseRedirect("/login")

	return HttpResponse(template.render(context))

def post(request):
	content = escaping.escape_tags(request.GET.get("message_input", None))
	if not content:
		return HttpResponse("Go fuck a goat")

	# markdowns = markdown(content, extras=["fenced-code-blocks"])
	# markdowns = markdowns.replace("&amp;lt", "&lt")
	# markdowns = markdowns.replace("&amp;gt", "&gt")
	markdowns = content

	message = MessageModel(
		device_type=getDeviceType(request),
		username=request.session['username'],
		content=markdowns,
		datetime=datetime.now(),
		rating="",
		room_id=0,
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
	message_id = int(request.GET.get("message_id", 0))
	if not message_id:
		earlier = datetime.now() - timedelta(weeks=12)
		query = MessageModel.objects.filter(datetime__range=(earlier, datetime.now()))
	else:
		query = MessageModel.objects.filter(pk=message_id+1)


	template = loader.get_template("event.html")
	for message in query:
		context = RequestContext(request, {
			'request':request,
			'post': {
				'devicetype':message.device_type,
				'username':message.username,
				'date':message.datetime.strftime("%Y-%m-%d %H:%M:%S"),
				# 'content':message.content,
				'content':markdown(message.content,extras=["fenced-code-blocks"]).replace("&amp;lt", "&lt").replace("&amp;gt", "&gt"),
				'rating':'',
				'id':message.pk
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

def home(request):
	template = loader.get_template('home.html')
	context = RequestContext(request, {'request':request})
	return HttpResponse(template.render(context))


# Test view to see what's inside a db-table
def editDatabase(request):
	if 'username' not in request.session or request.session['username'].lower() not in ['sebastian', 'seb', 'asj']:
		context = RequestContext(request, {'errornumber':520, 'errormessage':'You do not have permission to enter this page.'})
		return HttpResponse(loader.get_template('errorPage.html').render(context))
	template = loader.get_template('database.html')

	models = []
	for model in [UserModel, MessageModel, RoomModel]:
		data = model.objects.values()
		if model == MessageModel:
			for i, row in enumerate(data):
				data[i]['datetime'] = str(data[i]['datetime'])
			
		models.append({
			'name':model._meta.db_table,
			'items':data
		})

		# columns = model._meta.get_all_field_names()
		# data = model.objects.all()
		# models.append({
		# 	'name':model._meta.db_table,
		# 	'items':[dict(zip(columns, [m.__dict__[c] for c in sorted(m.__dict__.keys()) if not c[0]=="_"])) for m in model.objects.all()]
		# })

	context = RequestContext(request, {
		'models':models,
		'request':request
	})
	return HttpResponse(template.render(context))

def removeRowFromModel(request):
	if 'username' not in request.session or request.session['username'].lower() not in ['sebastian', 'seb', 'asj']:
		context = RequestContext(request, {'errornumber':520, 'errormessage':'You do not have permission to perform this page action.'})
		return HttpResponse(loader.get_template('errorPage.html').render(context))
	if request.method == 'POST':
		row_nr = int(request.POST.get('row_nr', 0))
		model_nr = int(request.POST.get('model_nr', 0))
		model = {1:UserModel, 2:MessageModel, 3:RoomModel}[model_nr]
		query = model.objects.filter(pk=row_nr)
		if query.count() == 1:
			query.delete()
			return HttpResponse('success')
		return HttpResponse('error')

def editRowInModel(request):
	if 'username' not in request.session or request.session['username'].lower() not in ['sebastian', 'seb', 'asj']:
		context = RequestContext(request, {'errornumber':520, 'errormessage':'You do not have permission to perform this page action.'})
		return HttpResponse(loader.get_template('errorPage.html').render(context))
	if request.method == 'POST':
		model_nr = request.POST.get('model_nr', None)
		data = request.POST.get('data', None)
		if not data:
			return HttpResponse("data_error")
		if not model_nr:
			return HttpResponse("model_error")
		data = json.loads(data)
		# Evaluate data
		try:
			for key, value in data.items():
				if 'id' in key:
					data[key] = int(value)
				# else:
					# data[key] = str(value)
		except Exception as e:
			print e
		model_nr = int(model_nr[0])
		model = {1:UserModel, 2:MessageModel, 3:RoomModel}[model_nr]
		try:
			model.objects.filter(id=data['id']).update(**data)
		except Exception as e:
			print e
		return HttpResponse("success")
