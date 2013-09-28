from simain.models import *
from simain.dateutils import *

class IsleManager(object):
  
  def __init__(self, user):
    self.user = user
    self.isles = None

  def gen_isles(self):
    if self.isles:
      return self.isles

    self.isles = self.user.get_all_isles()
    return self.isles

  def add_isle(self, name, desc):
    Isle.objects.create(name=name, description=desc, owner=self.user)
    self.isles = None

  def create_isle_from_form(self, form):
    data = form.cleaned_data

    Isle.objects.create(
      name=data['name'], 
      description=data['desc'], 
      owner=self.user
    )
    self.isles = None

  def fetch_isle(self, id):
    return Isle.objects.get(owner=self.user, id=id)

  def fetch_existing_isle(self, id):
    return Isle.objects.get(owner=self.user, id=id, deleted=False)

  def restore_isle(self, id):
    self.isles = None
    isle = self.fetch_isle(id)
    isle.deleted = False
    isle.save()

  def delete_isle(self, id):
    self.isles = None
    isle = Isle.objects.get(id=id, owner=self.user)
    isle.deleted = True
    isle.save()

  def delete_task(self, id):
    task = Task.objects.get(id=id, owner=self.user)
    task.delete()

  def delete_isle_perm(self, id):
    isle = Isle.objects.get(id=id, owner=self.user).delete()
    return isle

  def update_task_from_form(self, form):
    data = form.cleaned_data
    task = self.fetch_task(data['id'])

    task.isle = self.fetch_isle(data['isle'])
    task.name = data['name']
    task.data = data['date']
    task.description = data['desc']
    task.save()

  def create_task_from_form(self, form):
    data = form.cleaned_data
    isle = self.fetch_isle(data['isle'])
    
    task = Task.objects.create(
      name=data['name'],
      isle=isle,
      owner=self.user,
      date=data['date'],
      description=data['desc'],
    )

    task.save()

  def fetch_task(self, id):
    return Task.objects.get(owner=self.user, id=id)

  def get_deleted_isles(self):
    return Isle.objects.filter(owner=self.user, deleted=True)

  def get_table(self):
    """
    BRACE YOURSELVES
    """
    all_tasks = self.user.get_all_tasks()
    isles = self.gen_isles()

    if not all_tasks:
      return []

    isle_ranking = {
      isle.id: index for index, isle in enumerate(isles)
    }

    for_date = []
    same_date = []
    cur_group_date = None
    info = {}
    had_present = False

    for task in all_tasks:
      if task.date != cur_group_date:
        if same_date:
          info = date_info(cur_group_date)
          had_present |= info['is_today']
          for_date.append({
            'date': cur_group_date,
            'tasks': same_date,
            'props': [k for k, v in info.iteritems() if v],
          })
        same_date = [[] for x in isles]
        cur_group_date = task.date

        if date_info(cur_group_date)['in_future'] and not had_present:
          had_present = True
          for_date.append({
            'date': today(),
            'tasks': [[] for x in isles],
            'props': ['is_today'],
          })

      same_date[isle_ranking[task.isle.id]].append(task)

    info = date_info(cur_group_date)
    if same_date:
      for_date.append({
        'date': cur_group_date,
        'tasks': same_date,
        'props': [k for k, v in info.iteritems() if v],
      })

    return for_date
