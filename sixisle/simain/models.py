from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from simain.dateutils import *

class MyUserManager(BaseUserManager):

  def create_user(self, email, password=None):
    if not email:
      raise ValueError('Users must have an email address')

    user = self.model(
      email=MyUserManager.normalize_email(email),
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password):

    user = self.create_user(email,
      password=password
    )
    user.is_admin = True
    user.save(using=self._db)
    return user


class User(AbstractBaseUser):
  email = models.EmailField(
    verbose_name='Email address',
    max_length=255,
    unique=True,
    db_index=True,
  )
  first_name = models.CharField(max_length=30, blank=False)
  last_name = models.CharField(max_length=30, blank=False)

  """
  getter methods
  """

  def get_all_isles(self):
    return self.isles.filter(deleted=False)

  def get_all_tasks(self):
    return self.tasks.filter(isle__deleted=False).order_by('date')

  """
  shit required because django's new auth system is still fucked
  VVVV
  """

  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)

  objects = MyUserManager()

  USERNAME_FIELD = 'email'

  def auth(self):
    return self.is_authenticated

  def is_staff(self):
    return self.is_admin

  def get_username(self):
    return self.email
    
  def get_short_name(self):
    return self.first_name

  def full_name(self):
    return self.first_name + " " + self.last_name 

  def has_perm(self, perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True

  def __unicode__(self):
    return self.email


class Isle(models.Model):
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=1000)
  owner = models.ForeignKey('User', related_name='isles')
  deleted = models.BooleanField(default=False)

  def __unicode__(self):
    return self.name

class Task(models.Model):
  name = models.CharField(max_length=200)
  isle = models.ForeignKey('Isle', related_name='tasks')
  owner = models.ForeignKey('User', related_name='tasks')
  description = models.CharField(max_length=1000)
  date = models.DateField()

  def in_past(self):
    return date_info(self.date)['in_past']

  def in_future(self):
    return date_info(self.date)['in_future']

  def next_week(self):
    return date_info(self.date)['next_week']

  def last_week(self):
    return date_info(self.date)['last_week']

  def days_due(self):
    return from_today(self.date) 

  def days_due_pretty(self):
    days = self.days_due()
    if days == 0:
      return "Today"
    if days == 1:
      return "Tomorrow"
    if days == -1:
      return "Yesterday"
    if days > 1:
      return "In %s Days" % days
    return "%s Days Ago" % abs(days)

  def __unicode__(self):
    return "(%s) %s -> %s" % (self.id, self.isle.name, self.name)

class Subtask(models.Model):
  name = models.CharField(max_length=200)
  task = models.ForeignKey('Task', related_name='subtasks')
  owner = models.ForeignKey('User', related_name='all_subtasks')
  time = models.IntegerField(default=1)
  completed = models.BooleanField(default=False)
  description = models.CharField(max_length=1000)
