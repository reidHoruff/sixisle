from sniper.snipers import TemplateResponse

class SimainTemplateResponse(TemplateResponse):
  TEMPLATE_DIR = 'simain/'
  TEMPLATE = None

  def __init__(self, *args, **kwargs):
    self.template = self.TEMPLATE_DIR + self.TEMPLATE
    self.args = {}
    self.construct(self, *args, **kwargs)
    TemplateResponse.__init__(self, template=self.template, dictionary=self.args, request_context=True)

  def construct(self, *args, **kwargs):
    pass

  
class DeletedIslesTemplateResponse(SimainTemplateResponse):
  TEMPLATE = 'deleted.html'
