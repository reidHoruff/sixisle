from sniper.snipers import *
from simain.islemanager import *
import sniper.decorators as sniper
from simain.wonderbar import *
import forms as forms 

class BaseDialog(InsertTemplate):
  NAME = 'base'
  CONTAINER = '#dialogs'
  TEMPLATE_DIR = 'simain/dialogs/'
  TEMPLATE_NAME = 'base.html'
  BEFORE_ME = [JSCall('hide_modal')]
  WIDTH = 640

  def __init__(self, *args, **kwargs):
    self.container = self.CONTAINER

    self.args = {}
    self.args['modal_id'] = self.NAME
    self.args['width'] = self.WIDTH
    self.args['margin_left'] = self.WIDTH/(-2)
    
    self.construct(*args, **kwargs)

    InsertTemplate.__init__(
      self, 
      self.container,
      self.TEMPLATE_DIR+self.TEMPLATE_NAME, 
      request_context=True, 
      args=self.args
    )

  def set(self, **kwargs):
    for k, v in kwargs.iteritems():
      self.args[k] = v

  def construct(self, *args, **kwargs):
    pass


"""
create isle dialog
"""
class CreateIsleDialog(BaseDialog):
  NAME = 'create_isle'
  TEMPLATE_NAME = 'create_isle.html'
  
  def construct(self, isle=None):
    form = forms.CreateIsle()
    if isle:
      form.set_field_defaults(isle)
    self.args['form'] = form

@sniper.ajax(authenticate=True)
def create_isle(request):
  yield CreateIsleDialog()

"""
view task
"""
class ViewTaskDialog(BaseDialog):
  NAME = 'view_task'
  TEMPLATE_NAME = 'view_task.html'

  def construct(self, task):
    self.set(task=task)

@sniper.ajax(authenticate=True)
def view_task(request):
  id = request.GET['id']
  manager = IsleManager(request.user)
  yield ViewTaskDialog(manager.fetch_task(id))

"""
create task
"""
class CreateTaskDialog(BaseDialog):
  NAME = 'create_task'
  TEMPLATE_NAME = 'create_task.html'

  def construct(self, manager, task=None):
    form = forms.CreateTask(manager)

    if task:
      self.set(task=task)
      form.set_field_defaults(task)

    self.set(form=form)

@sniper.ajax(authenticate=True)
def create_task(request):
  manager = IsleManager(request.user)
  yield CreateTaskDialog(manager)

@sniper.ajax(authenticate=True)
def edit_task(request):
  manager = IsleManager(request.user)
  id = request.REQUEST['id']
  task = manager.fetch_task(id)
  yield CreateTaskDialog(manager, task)

"""
isle info dialog
"""
class IsleInfoDialog(BaseDialog):
  NAME = 'isle_info'
  TEMPLATE_NAME = 'isle_info.html'

  def construct(self, isle):
    self.set(
      name=isle.name,
      description = isle.description,
      id=isle.id,
    )

@sniper.ajax(authenticate=True)
def isle_info(request):
  manager = IsleManager(request.user)
  isle = manager.fetch_isle(request.GET['id'])
  yield IsleInfoDialog(isle)

"""
edit info dialog
"""
class EditIsleInfoDialog(BaseDialog):
  NAME = 'edit_isle_info'
  TEMPLATE_NAME = 'edit_isle.html'

  def __init__(self, isle):
    args = {
      'name': isle.name,
      'description': isle.description,
      'id': isle.id,
    }
    BaseDialog.__init__(self, args)

@sniper.ajax(authenticate=True)
def edit_isle(request):
  manager = IsleManager(request.user)
  isle = manager.fetch_isle(request.GET['id'])
  yield EditIsleInfoDialog(isle)
