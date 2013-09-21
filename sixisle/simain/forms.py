from django import forms

class SiForm(forms.Form):
  def errors(self):
    return self.errors.items()[0][1]

  def first_error(self):
    errors = self.errors()

    if errors:
      return self.errors()[0]

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
  name = text_input(name='Task Name')
  desc = textarea(name='Task Description')
  date = text_input(name='Date')
  isle = select(name='Isle', choices=(('a','a'), ('b','b')))

