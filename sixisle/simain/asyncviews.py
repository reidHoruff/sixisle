
from islemanager import *
from sniper.snipers import *

class AsyncViewSniper(InsertTemplate):
  TEMPLATE_DIR = 'simain/async/'
  TEMPLATE = None
  DEFAULT_SELECTOR = None

  def __init__(self, *largs, **kwargs):
    self.selector = self.DEFAULT_SELECTOR
    self.template = self.TEMPLATE_DIR + self.TEMPLATE
    self.args = {}
    self.construct(*largs, **kwargs)
    InsertTemplate.__init__(self, self.selector, self.template, self.args, request_context=True)

  def construct(self, *args, **kwargs):
    pass

class IsleTableSniper(AsyncViewSniper):
  TEMPLATE = 'isles_table.html'
  DEFAULT_SELECTOR = '#isles-table'

  def construct(self, manager):
    self.args = {
      'isles': manager.gen_isles(),
      'tasks': manager.get_table(),
    }

class DeletedIslesListSniper(AsyncViewSniper):
  TEMPLATE = 'delete_perm.html'
  DEFAULT_SELECTOR = '#deleted'

  def construct(self, manager):
    self.args = {
      'isles': manager.get_deleted_isles(),
    }

ALERT_ERROR = 'alert-error'
ALERT_SUCCESS = 'alert-success'
ALERT_INFO = 'alert-info'
class AlertBoxSniper(AsyncViewSniper):
  TEMPLATE = 'alert_box.html'
  DEFAULT_SELECTOR = '#alert-boxes'

  def construct(self, message, alert=ALERT_ERROR, selector='#alert-boxes'):
    self.selector=selector
    self.args = {
      'message': message,
      'alert_type': alert,
    }
