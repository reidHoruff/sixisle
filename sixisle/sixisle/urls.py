from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('simain.views',
  url(r'^$', 'view_home', name='home'),
  url(r'^snipertest/$', 'sniper_test', name='sniper_test'),
  url(r'^submit_comment/$', 'submit_comment', name='submit_comment'),
  url(r'^snipertemplate/$', 'sniper_template', name='sniper_template'),
  url(r'^register/$', 'register', name='view_register'),
  url(r'^login/$', 'login', name='view_login'),
  url(r'^profile/$', 'profile', name='view_profile'),
  url(r'^isles/$', 'isles', name='view_isles'),
  url(r'^deleted/$', 'deleted', name='view_deleted'),
)

#async
urlpatterns += patterns('simain.async',
  url(r'^async/register/$', 'register', name='async_register'),
  url(r'^async/login/$', '_login', name='async_login'),
  url(r'^async/logout/$', '_logout', name='async_logout'),
  url(r'^async/create_isle/$', 'create_isle', name='async_create_isle'),
  url(r'^async/create_task/$', 'create_task', name='async_create_task'),
  url(r'^async/del_isle/$', 'del_isle', name='async_del_isle'),
  url(r'^async/del_isle_perm/$', 'del_isle_perm', name='async_del_isle_perm'),
  url(r'^async/restore_isle/$', 'restore_isle', name='restore_isle'),
)

#dialogs
urlpatterns += patterns('simain.dialogs',
  url(r'^dialogs/create_isle/$', 'create_isle', name='dialog_create_isle'),
  url(r'^dialogs/create_task/$', 'create_task', name='dialog_create_task'),
  url(r'^dialogs/isle_info/$', 'isle_info', name='dialog_isle_info'),
  url(r'^dialogs/edit_isle/$', 'edit_isle', name='dialog_edit_isle'),
)
