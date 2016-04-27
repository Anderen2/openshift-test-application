from datetime import datetime, timedelta

from passlib.hash import sha256_crypt

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.db import connection

from web.models import UserModel, RoomModel, MessageModel

def index(request):
	template = loader.get_template("index.html")

	context = RequestContext(request, {})
	if "username" not in request.session.keys():
		return HttpResponseRedirect("/login")

	return HttpResponse(template.render(context))

def post(request):
	content = request.GET.get("message_input", None)
	if not content:
		return HttpResponse("Go fuck a goat")

	message = MessageModel(
		device_type=getDeviceType(request),
		username=request.session['username'],
		content=content,
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
			'avatar':message.device_type,
			'username':message.username,
			'date':message.datetime.strftime("%Y-%m-%d %H:%M:%S"),
			'content':message.content,
			'rating':''
		})
		return HttpResponse(template.render(context))

	return HttpResponse("")

def login(request):
	WRONG_PASSWORD, WRONG_USERNAME, LOGIN_CORRECT = range(1, 4)

	login_status = 0

	username = request.POST.get("username", "")
	password = request.POST.get("password", "")

	if "username" in request.session:
		print "------------------------------"
		return HttpResponseRedirect("/")

	try:
		user = UserModel.objects.get(username=username)
		if sha256_crypt.verify(password, user.password):
			request.session['username'] = user.username
			login_status = LOGIN_CORRECT
			return HttpResponseRedirect("/")
		else:
			login_status = WRONG_PASSWORD if password else 0
	except UserModel.DoesNotExist:
		login_status = WRONG_USERNAME if username else 0

	template = loader.get_template("login.html")
	context = RequestContext(request, {
		'login_status':login_status
	})
	return HttpResponse(template.render(context))

def logout(request):
	try:
		del request.session['username']
	except KeyError:
		pass
	return HttpResponseRedirect("/login")


def signUp(request):
	EMAIL_ERROR, PASSWORD_ERROR, USERNAME_ERROR = range(1, 4)
	signup_status = 0

	template = loader.get_template("signUp.html")

	email = request.POST.get("email", "")
	username = request.POST.get("username", "")
	password = request.POST.get("password", "")
	password_repeat = request.POST.get("password_repeat", "")

	if UserModel.objects.filter(email=email).exists():
		print "Email taken"
		signup_status = EMAIL_ERROR if email else 0

	if password != password_repeat:
		print "Password missmatch"
		signup_status = PASSWORD_ERROR

	if UserModel.objects.filter(username=username).exists():
		print "Username taken"
		signup_status = USERNAME_ERROR if username else 0

	context = RequestContext(request, {
		'signup_status':signup_status
	})

	if email and username and password and password_repeat and signup_status == 0:
		user = UserModel(
			username=username,
			password=sha256_crypt.encrypt(password), 
			email=email
		)
		user.save()
		return HttpResponseRedirect("/login")
	
	return HttpResponse(template.render(context))

# Test view to see what's inside a db-table
def displayDatabase(request):
	template = loader.get_template('database.html')

	models = []
	for model in [UserModel, MessageModel, RoomModel]:
		models.append({
			'name':model._meta.db_table,
			'columns':sorted(model._meta.get_all_field_names()),
			'rows':[[m.__dict__[c] for c in sorted(m.__dict__.keys()) if not c[0]=="_"] for m in model.objects.all()]
		})

	context = RequestContext(request, {
		'models':models
	})
	return HttpResponse(template.render(context))
