from sniper.snipers import BaseSniper, JSLog
from django.template.loader import render_to_string
from django.template import RequestContext

NOTIFY = 'wonderbar-type-notify'
ERROR = 'wonderbar-type-error'
DANGER = 'wonderbar-type-error'
SUCCESS = 'wonderbar-type-success'

LONG = 7000
MEDIUM = 4000
SHORT = 2500
NONE = 0

class Message(BaseSniper):
  IDENTITY = '__wonder_bar_show'

  def __init__(self, html, theme=NOTIFY, autohide=MEDIUM):
    self.kwargs = {
      'html': html,
      'theme': theme,
      'autohide': autohide,
    }

class Template(BaseSniper):
  IDENTITY = '__wonder_bar_show'

  def __init__(self, template, args={}, theme=NOTIFY, autohide=MEDIUM):
    self.template = "simain/wonder/"+template
    self.theme = theme
    self.args = args
    self.autohide = autohide

  def process(self, request):
    context_instance = RequestContext(request)
    self.kwargs = {
      'html': render_to_string(self.template, self.args, context_instance),
      'theme': self.theme,
      'autohide': self.autohide,
    }
    
class Confirm(Template):
  TEMPLATE = 'confirm.html'

  def __init__(self, message, endpoint, data={}, confirm="Yes", cancel="Cancel", autohide=NONE):
    args = {
      'message': message,
      'endpoint': endpoint,
      'confirm': confirm,
      'cancel': cancel,
      'data': data,
    }
    Template.__init__(self, self.TEMPLATE, args, DANGER, autohide)
