from datetime import datetime, timedelta

from passlib.hash import sha256_crypt

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

	username = request.POST.get("username", "")
	password = request.POST.get("password", "")
	
	query = UserModel.objects.filter(username=username)

	if len(query) == 1:
		new_session = query[0]

	if sha256_crypt.verify(password, new_session.password):
		print True
		return index(request)

	return HttpResponse(template.render(context))

def signUp(request):
	template = loader.get_template("signUp.html")
	context = RequestContext(request, {})

	email = request.POST.get("email", "")
	username = request.POST.get("username", "")
	password = request.POST.get("password", "")
	password_repeat = request.POST.get("password_repeat", "")

	if UserModel.objects.filter(email=email).exists():
		# Notify user if email is taken.
		print "email taken"

		return HttpResponse(template.render(context))
	if password != password_repeat:
		# Notify user passwords not matching
		print "password not matching"

		return HttpResponse(template.render(context))
	if UserModel.objects.filter(username=username).exists():
		# Notify user that username is taken
		print "username taken"
		return HttpResponse(template.render(context))

	user = UserModel(
		username=username,
		password=sha256_crypt.encrypt(password), 
		email=email
	)
	print user.password
	# for u in UserModel.objects.all():
		# u.delete()
	user.save()
	return HttpResponse(template.render(context))

# Test function to see what's inside a db-table
def display(request):
	template = loader.get_template_from_string("""<table>
		<tr>
		  <th>username</th>
		  <th>email</th>
		  <th>password</th>
		</tr>
		{% for b in obj %}
		<tr>
		  <td>{{ b.username }}</td>
		  <td>{{ b.email }}</td>
		  <td>{{ b.password }}</td>
		</tr>
		{% endfor %}
		</table>"""
	)
	context = RequestContext(request, {'obj':UserModel.objects.all()})
	# return render_to_response('template.tmpl', {'obj': UserModel.objects.all()})
	return HttpResponse(template.render(context))
