import json
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from web.models import UserModel, RoomModel, MessageModel

# Create your views here.
def index (request):
	template = loader.get_template("index.html")
	
	query = MessageModel.objects.all()
	messages = []
	for message in query:
		print message.content
		messages.append({
			'avatar':'linux',
			'username':'root',
			'date':message.datetime.strftime("%Y-%m-%d %H:%M:%S"),
			'content':message.content,
			'rating':''
		})

	context = RequestContext(request, {
		# "messages_": messages
	})

	return HttpResponse(template.render(context))

def post (request):
	print(request.GET)

	content = request.GET.get("text_input", None)
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
	print(request.GET)

	timestamp = request.GET.get("timestamp", None)
	if not timestamp:
		earlier = datetime.now() - timedelta(weeks=12)
	else:
		earlier = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") + timedelta(seconds=1)

	query = MessageModel.objects.filter(datetime__range=(earlier, datetime.now()))

	template = loader.get_template("event.html")

	for message in query:
		print message.content
		context = RequestContext(request, {
			'avatar':'linux',
			'username':'root',
			'date':message.datetime.strftime("%Y-%m-%d %H:%M:%S"),
			'content':message.content,
			'rating':''
		})
		return HttpResponse(template.render(context))

	return HttpResponse("")

def login (request):
	template = loader.get_template("login.html")
	context = RequestContext(request, {

	})
	return HttpResponse(template.render(context))