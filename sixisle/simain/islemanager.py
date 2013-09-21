from simain.models import *

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

  def delete_isle_perm(self, id):
    isle = Isle.objects.get(id=id, owner=self.user).delete()
    return isle

  def get_deleted_isles(self):
    return Isle.objects.filter(owner=self.user, deleted=True)

  def get_table(self):
    all_tasks = self.user.get_all_tasks()

    if not all_tasks:
      return []

    isle_ranking = {
      isle.id: index for index, isle in enumerate(self.gen_isles())
    }

    for_date = []
    same_date = []
    cur_group_date = None

    for task in all_tasks:
      if task.date != cur_group_date:
        if same_date:
          for_date.append({
            'date': cur_group_date,
            'tasks': same_date,
          })
        same_date = [[] for x in range(len(self.gen_isles()))]
        cur_group_date = task.date

      same_date[isle_ranking[task.isle.id]].append(task)

    if same_date:
      for_date.append({
        'date': cur_group_date,
        'tasks': same_date,
      })

    return for_date



    for_date_sorted = []

    for on_date in for_date:  
      for_date_sorted.append(
        sorted(
          on_date,
          cmp=lambda a, b: isle_ranking[a.id] - isle_ranking[b.id]
        )
      )

    return for_date_sorted
