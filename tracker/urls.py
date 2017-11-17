from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

app_name= 'tracker'

urlpatterns = [
    # /
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^test/$', views.testView, name='testview'),

    # /name
    # url(r'^names/$', views.NameView.as_view(), name='names'),

    url(r'^league/$', views.LeagueView.as_view(), name='leagueview'),
    url(r'^riot.txt$', views.riottxt, name='riottxt'),
    url(r'^minecraft/$', views.MinecraftView.as_view(), name='minecraftview'),

    url(r'^runescape/$', views.RuneScapeView.as_view(), name='runescapeview'),

    url(r'^maplestory/$', views.MaplestoryView.as_view(), name='maplestoryview'),

    # /tracker/id/
    url(r'^names/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'^names/follow/(?P<game>.+)/(?P<username>.+)/$', views.FollowView.as_view(), name='follow'),
    url(r'^names/unfollow/(?P<game>.+)/(?P<username>.+)/$', views.UnfollowView.as_view(), name='unfollow'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
]
