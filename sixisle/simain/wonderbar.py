from sniper.snipers import BaseSniper, JSLog
from django.template.loader import render_to_string
from django.template import RequestContext
import othersnipers as os

NOTIFY = 'wonderbar-type-notify'
ERROR = 'wonderbar-type-error'
DANGER = 'wonderbar-type-error'
SUCCESS = 'wonderbar-type-success'

LONG = 7000
MEDIUM = 4000
SHORT = 1000
NONE = 0

class Message(BaseSniper):
  IDENTITY = '__wonder_bar_show'
  BEFORE_ME = [os.HideModal()]

  def _construct(self, html, theme=NOTIFY, autohide=MEDIUM):
    self['html'] = html
    self['theem'] = theme
    self['autohide'] = autohide

class Template(BaseSniper):
  IDENTITY = '__wonder_bar_show'
  BEFORE_ME = [os.HideModal()]

  def _construct(self, template, args={}, theme=NOTIFY, autohide=MEDIUM):
    self.template = "simain/wonder/"+template
    self.theme = theme
    self.args = args
    self.autohide = autohide

  def process(self, request):
    context_instance = RequestContext(request)
    self['html'] = render_to_string(self.template, self.args, context_instance) 
    self['theme'] = self.theme
    self['autohide'] = self.autohide
    
class Confirm(Template):
  TEMPLATE = 'confirm.html'
  BEFORE_ME = [os.HideModal()]

  def _construct(self, message, endpoint, data={}, confirm="Yes", cancel="Cancel", autohide=NONE):
    args = {
      'message': message,
      'endpoint': endpoint,
      'confirm': confirm,
      'cancel': cancel,
      'data': data,
    }
    Template._construct(self, self.TEMPLATE, args, DANGER, autohide)
