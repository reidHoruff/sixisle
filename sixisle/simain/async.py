from django.template import RequestContext
from django.http import *
from sniper.snipers import *
import sniper.decorators as sniper
from short.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from simain.islemanager import *
import simain.wonderbar as w
from simain.asyncviews import *
import simain.othersnipers as os 
import forms

@sniper.ajax()
def register(request):
  form = forms.Register(request.POST)

  if form.is_valid():
    yield w.Message('success', w.ERROR), None
  else:
    yield w.Message(form.get_first_error(), w.ERROR)

  try:
    user = User.objects.create_user(
      username,
      '%s@foobar.com' % (username), 
      password1,
    )
  except:
    user = None

@sniper.ajax()
def _login(request):
  form = forms.LoginForm(request.POST)

  if form.is_valid():
    email = form.cleaned_data['email']
    if email == 'root':
      email = 'root@root.com'
    password = form.cleaned_data['password']
    user = authenticate(username=email, password=password)

    if user and user.is_active:
      login(request, user)
      n = form.cleaned_data['next']
      if n:
        yield RedirectBrowser(n), None
      else:
        yield RedirectBrowser('/profile/'), None

  yield w.Message('Sorry, that login is invalid :(', w.ERROR)

@sniper.ajax()
def _logout(request):
  logout(request)
  n = request.REQUEST.get('next')
  if n:
    yield RedirectBrowser(n)
  else:
    yield RefreshBrowser()

@sniper.ajax()
def create_isle(request):
  form = forms.CreateIsle(request.POST)

  if form.is_valid():
    manager = IsleManager(request.user)
    manager.create_isle_from_form(form)
    message = 'Isle <strong>%s</strong> has been created' % request.POST['name']
    yield w.Message(message, w.SUCCESS)
    yield IsleTableSniper(manager)

  else:
    yield AlertBoxSniper(form.get_first_error())

@sniper.ajax()
def create_task(request):
  manager = IsleManager(request.user)
  form = forms.CreateTask(manager, request.POST)
    
  if form.is_valid():
    if form.cleaned_data['id'] is not None:
      manager.update_task_from_form(form)
      message = "Task has been updated."
    else:
      manager.create_task_from_form(form)
      message = "Task has been created."

    yield IsleTableSniper(manager)
    yield w.Message(message, w.SUCCESS, w.SHORT)
  else:
    yield AlertBoxSniper(form.get_first_error())

@sniper.ajax(authenticate=True)
def del_isle_perm(request):
  id = request.REQUEST['id']
  manager = IsleManager(request.user)
 # manager.delete_isle_perm(id)
  yield DeletedIslesListSniper(manager)
  yield w.Message("Isle has been deleted.", w.SUCCESS)

@sniper.ajax(authenticate=True)
def restore_isle(request):
  id = request.REQUEST['id']
  manager = IsleManager(request.user)
  manager.restore_isle(id)
  yield DeletedIslesListSniper(manager)
  yield w.Message("Isle has been Restored.", w.SUCCESS)

@sniper.ajax(authenticate=True)
def del_task(request):
  id = request.REQUEST['id']
  manager = IsleManager(request.user)
  manager.delete_task(id)
  yield IsleTableSniper(manager)
  yield w.Message("Task has been Deleted", w.SUCCESS)

@sniper.ajax(authenticate=True)
def del_isle(request):
  id = request.REQUEST['id']
  manager = IsleManager(request.user)
  isle = manager.fetch_isle(id)
  action = request.REQUEST.get('action', 'confirm')

  data = {
    'id': id,
    'action': None,
  }

  if action == 'delete':
    manager.delete_isle(isle.id)
    data['action'] = 'undo'
    yield w.Confirm(
      "<strong>%s</strong> has been deleted. " % isle.name, 
      confirm="Undo",
      cancel=None,
      endpoint="async_del_isle",
      data=data,
    )
    yield IsleTableSniper(manager)
    yield None

  elif action == 'undo':
    manager.restore_isle(isle.id)
    data['action'] = 'none'
    yield IsleTableSniper(manager)
    yield w.Message(
      "Isle <strong>%s</strong> has been restored." % isle.name, 
      w.SUCCESS
    )
    yield None

  elif action == 'confirm':
    yield JSLog('yea bitch')
    data['action'] = 'delete'
    yield w.Confirm(
     "Are you sure you want to delete isle <strong>%s</strong>?" % isle.name, 
     endpoint="async_del_isle",
     data=data,
    )
    yield None

