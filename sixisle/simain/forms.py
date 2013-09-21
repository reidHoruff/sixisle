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
  password1 = PasswordField(
    min_length=2,
    max_length=50,
    error_messages={
      'invalid': 'First name is Invalid.',
      'required': 'First name is Required',
      'min_length': 'First name is too short',
      'max_length': 'First name is too long',
    }
  )

  password2 = PasswordField(
    min_length=2,
    max_length=50,
    error_messages={
      'invalid': 'First name is Invalid.',
      'required': 'First name is Required',
      'min_length': 'First name is too short',
      'max_length': 'First name is too long',
    }
  )

  email = forms.EmailField(
    error_messages={
      'invalid': 'Email is Invalid.',
      'required': 'Email is Required',
      'min_length': 'Email is too short',
      'max_length': 'Email is too long',
    }
  )

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
  desc = textarea(name='Task Description')
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
