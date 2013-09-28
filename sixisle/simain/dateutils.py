from datetime import *
def p(d):
  return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def strftime(format, t):
  return t.strftime(format).replace('{S}', str(t.day) + p(t.day))

def today():
  return datetime.now().date()

def from_today(date):
  return (date - today()).days

def date_info(date):
  info = dict()

  today = datetime.now().date()
  days_left_in_week = 6-today.weekday()
  
  this_sunday = today + timedelta(days=days_left_in_week) 
  last_sunday = this_sunday - timedelta(days=7)
  next_sunday = this_sunday + timedelta(days=7)
  two_sundays_ago = last_sunday - timedelta(days=7)

  in_past = date < today
  in_future = date > today
  same_week = (date > last_sunday) and (date <= this_sunday)
  next_week = (date > this_sunday) and (date <= next_sunday)
  last_week = (date > two_sundays_ago) and (date <= last_sunday)
  is_today = date == today
  is_tomorrow = (date == (today + timedelta(days=1)))
  is_yesterday = date == (today - timedelta(days=1))

  info['in_past'] = in_past
  info['in_future'] = in_future
  info['same_week'] = same_week
  info['next_week'] = next_week
  info['last_week'] = last_week
  info['is_today'] = is_today
  info['is_tomorrow'] = is_tomorrow
  info['is_yesterday'] = is_yesterday

  return info
