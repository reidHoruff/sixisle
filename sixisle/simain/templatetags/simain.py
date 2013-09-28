from django import template
from datetime import *
from .. import dateutils as du

register = template.Library()

@register.simple_tag(takes_context=True)
def smart_date(context, date):
  i = du.date_info(date)

  if i['is_today']:
    return du.strftime("<span class='today'>Today <shy>the {S}</shy></span>", date)

  if i['is_yesterday']:
    return du.strftime("<span>Yesterday <shy>the {S}</shy></span>", date)

  if i['is_tomorrow']:
    return du.strftime("<span class='sw'>Tomorrow <shy>the {S}</shy></span>", date)

  if i['same_week']:
    return du.strftime("<span class='sw'>%A <shy>the {S}</shy></span>", date)

  if i['next_week']:
    return du.strftime("<span class='nw'>next %A <shy>the {S}</shy></span>", date)

  if i['last_week']:
    return du.strftime("<span>last %A <shy>the {S}</shy></span>", date)
  
  return du.strftime("<span>%B <shy>the {S}</shy></span>", date)

