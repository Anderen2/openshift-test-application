from datetime import datetime, timedelta

from passlib.hash import sha256_crypt

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render

from web.models import UserModel, RoomModel, MessageModel

def index(request):
	template = loader.get_template("index.html")

	context = RequestContext(request, {})

	print "Cookie", request.COOKIES

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
	WRONG_PASSWORD, WRONG_USERNAME, LOGIN_CORRECT = range(1, 4)

	loginStatus = 0

	username = request.POST.get("username", "")
	password = request.POST.get("password", "")

	if "username" in request.session:
		print "------------------------------"
		return HttpResponseRedirect("/")

	try:
		user = UserModel.objects.get(username=username)
		if sha256_crypt.verify(password, user.password):
			request.session['username'] = user.username
			loginStatus = LOGIN_CORRECT
			return HttpResponseRedirect("/")
		else:
			loginStatus = WRONG_PASSWORD if password else 0
	except UserModel.DoesNotExist:
		loginStatus = WRONG_USERNAME if username else 0

	template = loader.get_template("login.html")
	context = RequestContext(request, {
		'loginStatus':loginStatus
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
	signupStatus = 0

	template = loader.get_template("signUp.html")

	email = request.POST.get("email", "")
	username = request.POST.get("username", "")
	password = request.POST.get("password", "")
	password_repeat = request.POST.get("password_repeat", "")

	if UserModel.objects.filter(email=email).exists():
		print "Email taken"
		signupStatus = EMAIL_ERROR if email else 0
		# return HttpResponse(template.render(context))

	if password != password_repeat:
		print "Passwrod missmatch"
		signupStatus = PASSWORD_ERROR
		# return HttpResponse(template.render(context))

	if UserModel.objects.filter(username=username).exists():
		print "Username taken"
		signupStatus = USERNAME_ERROR if username else 0
		# return HttpResponse(template.render(context))

	context = RequestContext(request, {
		'signupStatus':signupStatus
	})

	print signupStatus

	if email and username and password and password_repeat and signupStatus == 0:
		user = UserModel(
			username=username,
			password=sha256_crypt.encrypt(password), 
			email=email
		)
		user.save()
		return HttpResponseRedirect("/login")
	
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
	return HttpResponse(template.render(context))
