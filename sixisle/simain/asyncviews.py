
from islemanager import *
from sniper.snipers import *

class AsyncViewSniper(InsertTemplate):
  TEMPLATE_DIR = 'simain/async/'
  TEMPLATE = None
  DEFAULT_SELECTOR = None

  def _construct(self):
    template = self.TEMPLATE_DIR + self.TEMPLATE
    selector = self.DEFAULT_SELECTOR
    InsertTemplate._construct(self, selector, template, request_context=True)

class IsleTableSniper(AsyncViewSniper):
  TEMPLATE = 'isles_table.html'
  DEFAULT_SELECTOR = '#isles-table'

  def _construct(self, manager):
    AsyncViewSniper._construct(self)
    self.set(
      isles=manager.gen_isles(),
      tasks=manager.get_table()
    )

class DeletedIslesListSniper(AsyncViewSniper):
  TEMPLATE = 'delete_perm.html'
  DEFAULT_SELECTOR = '#deleted'

  def _construct(self, manager):
    AsyncViewSniper._construct(self)
    self.set(isles=manager.get_deleted_isles())

ALERT_ERROR = 'alert-error'
ALERT_SUCCESS = 'alert-success'
ALERT_INFO = 'alert-info'
class AlertBoxSniper(AsyncViewSniper):
  TEMPLATE = 'alert_box.html'
  DEFAULT_SELECTOR = '#alert-boxes'

  def _construct(self, message, alert=ALERT_ERROR):
    AsyncViewSniper._construct(self)
    self.selector=selector
    self.set(mesage=message, alert_type=alert)
