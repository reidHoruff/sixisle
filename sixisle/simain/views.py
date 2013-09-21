from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import *
from sniper.snipers import *
import sniper.decorators as sniper
from short.decorators import *
from random import choice
from simain.islemanager import * 
from simain.asyncviews import *
import templateresponses as tr
import simain.forms as forms

@context_template_response
def view_home(request):
  return 'simain/home.html'

@context_template_response
def register(request):
  return 'simain/register.html', {'form': forms.Register}

@context_template_response
def login(request):
  return 'simain/login.html'

@context_template_response
def profile(request):
  return 'simain/profile.html'

@sniper.sniper(authenticate=True)
def isles(request):
  manager = IsleManager(request.user) 
  yield TemplateResponse('simain/isles.html', request_context=True)
  yield IsleTableSniper(manager)

@sniper.sniper()
def deleted(request):
  manager = IsleManager(request.user)
  yield tr.DeletedIslesTemplateResponse()
  yield DeletedIslesListSniper(manager)

@sniper.sniper()
def sniper_test(request):
  yield JSLog("im inserting text", "reid", 1, ['foo'])
  yield InsertTemplate("#container", "content.html")
  yield PushState("bar")

  if not request.is_ajax():
    yield TemplateResponse("simain/home.html")

def sniper_template(request):
  args = {
    'id': 0,
    'title': 'this is the root',
    'body': 'hey yall',
  }

  yield InsertTemplate(
    "#comments", 
    "simain/comment.html", 
    args, 
    context_instance=RequestContext(request)
  )
  yield TemplateResponse("simain/sniper.html", context_instance=RequestContext(request))

@sniper.sniper()
def submit_comment(request):
  title = request.POST['title']
  body = request.POST['body']
  id = request.POST['id']

  if not title:
    yield InsertText("#errors-"+id, "<p class='error'>title is empty</p>"), None

  if not body:
    yield InsertText("#errors-"+id, "<p class='error'>body is empty</p>"), None

  yield DeleteFromDOM(".error")

  args = {
    'id': int(id)+1,
    'title': title,
    'body': body,
  }

  yield AppendTemplate(
    "#comment-%s-children" % id, 
    "simain/comment.html", 
    args, 
    context_instance=RequestContext(request),
  )

