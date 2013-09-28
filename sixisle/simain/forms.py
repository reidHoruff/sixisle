from django import forms

class SiForm(forms.Form):
  def get_errors(self):
    return self.errors.items()[0][1]

  def get_first_error(self):
    errors = self.get_errors()

    if errors:
      return errors[0]

    return None

class PasswordField(forms.CharField):
  def __init__(self, *args, **kwargs):
    kwargs['widget'] = forms.PasswordInput()
    forms.CharField.__init__(self, *args, **kwargs)

def field_with_errors(field, name, *args, **kwargs):
  kwargs['error_messages'] = { 
    'invalid': '%s is Invalid.'%name,
    'required': '%s is Required'%name,
    'min_length': '%s is Too short.'%name,
    'max_length': '%s is Too Long.'%name,
    'invalid_choice': 'Invalid Choice for %s.'%name,
  }
  return field(*args, **kwargs)

def text_input(name, min=1, max=100, required=True):
  return field_with_errors(
    field=forms.CharField,
    name=name,
    min_length=min,
    max_length=max,
    required=required,
    widget=forms.TextInput(attrs={'placeholder': name}),
  )

def hidden_input():
  return forms.CharField(
    widget=forms.HiddenInput(),
  )

def password_input(name, min=1, max=100, required=True):
  return field_with_errors(
    field=forms.CharField,
    name=name,
    min_length=min,
    max_length=max,
    required=required,
    widget=forms.PasswordInput(attrs={'placeholder': name}),
  )

def email_input(name, min=1, max=100, required=True):
  return field_with_errors(
    field=forms.EmailField,
    name=name,
    min_length=min,
    max_length=max,
    required=required,
    widget=forms.TextInput(attrs={'placeholder': name}),
  )
  
def date_input(name, required=True):
  return field_with_errors(
    field=forms.CharField,
    name=name,
    required=required,
    widget=forms.TextInput(attrs={'placeholder': name, 'class': 'datepicker'}),
  )

def select(name, required=True, choices=()):
  return field_with_errors(
    field=forms.ChoiceField,
    name=name,
    required=required,
    choices=choices,
    widget=forms.Select(attrs={'class': 'btn'}),
  )

def textarea(name, min=1, max=100, required=True):
  return field_with_errors(
    field=forms.CharField,
    name=name,
    min_length=min,
    max_length=max,
    required=required,
    widget=forms.Textarea(attrs={'placeholder': name}),
  )

def hidden_integer(required=True):
  return forms.IntegerField(
    required=required,
    widget=forms.HiddenInput(),
  )

class Register(SiForm):
  password1 = password_input(name='Password')
  password2 = password_input(name='Confirm Password')
  email = email_input(name='Email') 

class CreateTask(SiForm):
  def __init__(self, manager, *args, **kwargs):
    super(SiForm, self).__init__(*args, **kwargs)
    self.fields['isle'].choices = [(isle.id, isle.name) for isle in manager.gen_isles()]

  def set_field_defaults(self, task):
    self.fields['name'].initial = task.name    
    self.fields['desc'].initial = task.description    
    self.fields['date'].initial = task.date    
    self.fields['isle'].initial = task.isle.id    
    self.fields['id'].initial = task.id

  name = text_input(name='Task Name')
  desc = textarea(name='Task Description', max=2000)
  date = date_input(name='Date')
  isle = select(name='Isle')
  id = hidden_integer(required=False)


class CreateIsle(SiForm):
  def set_field_defaults(self, isle):
    self.fields['name'].initial = task.name    
    self.fields['desc'].initial = task.description    
    self.fields['id'].initial = task.id

  name = text_input(name='Task Name')
  desc = textarea(name='Task Description')
  id = hidden_integer(required=False)

class LoginForm(SiForm):
  def set_next(self, next):
    self.fields['next'].initial = next

  email = text_input(name='Email')
  password = password_input(name='Password')
  next = hidden_input()
