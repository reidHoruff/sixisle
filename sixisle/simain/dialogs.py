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

  def __init__(self, args={}):
    args['modal_id'] = self.NAME
    args['width'] = self.WIDTH
    args['margin_left'] = self.WIDTH/(-2)

    InsertTemplate.__init__(
      self, 
      self.CONTAINER,
      self.TEMPLATE_DIR+self.TEMPLATE_NAME, 
      request_context=True, 
      args=args
    )


"""
create isle dialog
"""
class CreateIsleDialog(BaseDialog):
  NAME = 'create_isle'
  TEMPLATE_NAME = 'create_isle.html'

@sniper.sniper(authenticate=True)
def create_isle(request):
  yield CreateIsleDialog()


"""
create isle task
"""
class CreateTaskDialog(BaseDialog):
  NAME = 'create_task'
  TEMPLATE_NAME = 'create_task.html'

@sniper.sniper(authenticate=True)
def create_task(request):
  manager = IsleManager(request.user)
  args = {
    'form': forms.CreateTask(),
    'isles': manager.gen_isles(), 
  }
  yield CreateTaskDialog(args)


"""
isle info dialog
"""
class IsleInfoDialog(BaseDialog):
  NAME = 'isle_info'
  TEMPLATE_NAME = 'isle_info.html'

  def __init__(self, isle):
    args = {
      'name': isle.name,
      'description': isle.description,
      'id': isle.id,
    }
    BaseDialog.__init__(self, args)

@sniper.sniper(authenticate=True)
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

@sniper.sniper(authenticate=True)
def edit_isle(request):
  manager = IsleManager(request.user)
  isle = manager.fetch_isle(request.GET['id'])
  yield EditIsleInfoDialog(isle)
