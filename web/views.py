from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from web.models import UserModel, RoomModel, MessageModel

def index(request):
	template = loader.get_template("index.html")

	context = RequestContext(request, {})

	return HttpResponse(template.render(context))

def post(request):
	# print(request.GET)

	content = request.GET.get("message_input", None)
	if not content:
		return HttpResponse("Go fuck a goat")

	message = MessageModel(
		content=content,
		datetime=datetime.now(),
		rating=""
	)
	message.save()
	return HttpResponse(content)

def getLatestPost(request):
	# print(request.GET)

	timestamp = request.GET.get("timestamp", None)
	if not timestamp:
		earlier = datetime.now() - timedelta(weeks=12)
	else:
		earlier = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") + timedelta(seconds=1)

	query = MessageModel.objects.filter(datetime__range=(earlier, datetime.now()))

	template = loader.get_template("event.html")

	for message in query:
		# print message.content
		context = RequestContext(request, {
			'avatar':'linux',
			'username':'root',
			'date':message.datetime.strftime("%Y-%m-%d %H:%M:%S"),
			'content':message.content,
			'rating':''
		})
		return HttpResponse(template.render(context))

	return HttpResponse("")

def login(request):
	template = loader.get_template("login.html")
	context = RequestContext(request, {})

	username = request.POST.get("username")
	password = request.POST.get("password")
	new_session = UserModel.objects.filter(username=username)
	# print new_session

	return HttpResponse(template.render(context))

def signUp(request):
	template = loader.get_template("signUp.html")
	context = RequestContext(request, {})

	email = request.POST.get("email")
	username = request.POST.get("username")
	password = request.POST.get("password")
	password_repeat = request.POST.get("password_repeat")

	if len(UserModel.objects.filter(email=email)):
		# Notify user if email is taken.
		pass
	if password != password_repeat:
		# Notify user passwords not matching
		pass
	if len(UserModel.objects.filter(username=username)):
		# Notify user that username is taken
		pass

	return HttpResponse(template.render(context))
