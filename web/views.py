from datetime import datetime

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
		"messages_": messages
	})

	return HttpResponse(template.render(context))
	
def post (request):
	print(request.POST)

	content = request.POST.get("text_input", None)
	if not content:
		return HttpResponse("Go fuck a goat")

	message = MessageModel(
		content=content,
		datetime=datetime.now(),
		rating=""
	)
	message.save()
	return HttpResponseRedirect("/")
