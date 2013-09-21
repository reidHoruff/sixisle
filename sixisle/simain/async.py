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

@sniper.sniper()
def register(request):
  message = lambda m: InsertText('#messages', m)

  yield InsertText('#messages', '')

  if request.method != 'POST':
    yield message('error'), None

  password1 = request.POST['password1']
  password2 = request.POST['password2']
  username = request.POST['username']

  if not username:
    yield message('Username Required'), None

  if len(username) < 3: 
    yield message('Username too short'), None

  if not password1:
    yield message('Password Required'), None

  if password1 != password2:
    yield message('passwords do not match'), None


  try:
    user = User.objects.create_user(
      username,
      '%s@foobar.com' % (username), 
      password1,
    )
  except:
    user = None

  if not user:
      yield message("Username already in use"), None

@sniper.sniper()
def _login(request):
  message = lambda m: InsertText('#messages', m)

  yield InsertText('#messages', '')

  if request.method != 'POST':
    yield message('error'), None

  password = request.POST['password']
  username = request.POST['username']
  user = authenticate(username=username, password=password)

  if user and user.is_active:
    login(request, user)
    yield RedirectBrowser('/profile/')

  else:
    yield w.Message('Sorry, that login is invalid :(', w.ERROR), None

@sniper.sniper()
def _logout(request):
  logout(request)
  yield RefreshBrowser()

@sniper.sniper()
def create_isle(request):
  form = forms.CreateIsle(request.POST)

  if form.is_valid():
    manager = IsleManager(request.user)
    manager.create_isle_from_form(form)
    yield os.HideModal()
    message = 'Isle <strong>%s</strong> has been created' % request.POST['name']
    yield w.Message(message, w.SUCCESS)
    yield IsleTableSniper(manager)

  else:
    yield AlertBoxSniper(form.get_first_error())

@sniper.sniper()
def create_task(request):
  manager = IsleManager(request.user)
  form = forms.CreateTask(manager, request.POST)
    
  if form.is_valid():
    if form.cleaned_data['id'] is not None:
      manager.update_task_from_form(form)
    else:
      manager.create_task_from_form(form)

    yield IsleTableSniper(manager)
    yield w.Message("task has been created", w.SUCCESS, w.SHORT)
    yield os.HideModal()
  else:
    yield AlertBoxSniper(form.get_first_error())

@sniper.sniper(authenticate=True)
def del_isle_perm(request):
  id = request.REQUEST['id']
  manager = IsleManager(request.user)
  manager.delete_isle_perm(id)
  yield DeletedIslesListSniper(manager)
  yield w.Message("Isle has been deleted.", w.SUCCESS)

@sniper.sniper(authenticate=True)
def restore_isle(request):
  id = request.REQUEST['id']
  manager = IsleManager(request.user)
  manager.restore_isle(id)
  yield DeletedIslesListSniper(manager)
  yield w.Message("Isle has been Restored.", w.SUCCESS)

@sniper.sniper(authenticate=True)
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
    yield os.HideModal()
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
    yield os.HideModal()
    yield IsleTableSniper(manager)
    yield w.Message(
      "Isle <strong>%s</strong> has been restored." % isle.name, 
      w.SUCCESS
    )
    yield None

  elif action == 'confirm':
    data['action'] = 'delete'
    yield os.HideModal()
    yield w.Confirm(
     "Are you sure you want to delete isle <strong>%s</strong>?" % isle.name, 
     endpoint="async_del_isle",
     data=data,
    )
    yield None

