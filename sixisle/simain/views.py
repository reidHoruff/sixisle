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
from django.contrib.auth.decorators import login_required

class Template(TemplateResponse):
  TEMPLATE_DIR = 'simain/'
  
  def __init__(self, template, *args, **kwargs):
    template = self.TEMPLATE_DIR + template
    TemplateResponse.__init__(self, template, request_context=True, *args, **kwargs)

@sniper.template()
def view_home(request):
  yield Template('home.html')

@sniper.template()
def register(request):
  yield Template('register.html').set(form=forms.Register())

@sniper.template()
def login(request):
  n = request.REQUEST.get('next')
  form = forms.LoginForm()
  form.set_next(n)
  yield Template('login.html').set(form=form, next=n)

@login_required
@sniper.template()
def profile(request):
  yield TemplateResponse('simain/profile.html', request_context=True)

@login_required
@sniper.template()
def isles(request):
  manager = IsleManager(request.user) 
  yield Template('isles.html')
  yield IsleTableSniper(manager)

@login_required
@sniper.template()
def deleted(request):
  manager = IsleManager(request.user)
  yield tr.DeletedIslesTemplateResponse()
  yield DeletedIslesListSniper(manager)
