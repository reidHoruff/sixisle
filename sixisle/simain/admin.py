from simain.models import *
from django.contrib import admin


'''
I don't care if this is the wrong fucking way to do this.
fuck django, why did it take you so long to make custom user attributes and
when you finally did in 1.5 they're totally fucked?
'''

admin.site.register(User)
admin.site.register(Isle)
admin.site.register(Task)
