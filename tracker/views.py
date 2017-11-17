from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .models import Name
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.urls import reverse
from django.middleware import csrf
from tracker.tasks import manual_update_names

def logoutView(request):
    logout(request)
    return redirect('tracker:index')

def testView(request):
    manual_update_names()
    return HttpResponse("Hello")

class IndexView(generic.TemplateView):
    template_name = 'tracker/index.html'

class ProfileView(generic.TemplateView):
    template_name = 'tracker/profile.html'

# @csrf_exempt
def riottxt(request):
    content = "f3b613fc-872a-4a6f-bb1b-70d1750e4c44"
    response = StreamingHttpResponse(content)
    response['Content-Type'] = 'text/plain; charset=utf8'
    return response

# Helper method for search views.
def getName(search, game):
    existing = Name.objects.filter(username=search, game=game)
    if len(existing) != 0:
        temp = existing[0]
    else:
        temp = Name()
        temp.username = search
        temp.game = game
    temp.valid = Name.check_valid(temp.username, temp.game)
    if temp.valid:
        available, release_date = Name.get_info(temp.username, temp.game)
        temp.available = available
        temp.release_date = release_date
    else:
        temp.available = False
        temp.release_date = None
    if len(existing) != 0:
        temp.save()
    return temp

class LeagueView(View):
    def search(self, request):
        search = request.GET.get('search').strip().replace("%20", " ")
        games = ["LoL_NA", "LoL_TR",
        "LoL_BR", "LoL_EUW", "LoL_EUNE",
        "LoL_KR"]
        return render(request, 'tracker/namesearch.html', {'title': '| League Search','search': search, 'games': games})

    def lookup(self, request):
        # Initialize name object.
        search = request.GET.get('lookup')
        game = request.GET.get('game')
        id_ = request.GET.get('number')
        name = getName(search, game)

        # Create the name's card.
        response = name.generate_card(request.user, id_)
        return HttpResponse(response)

    def get(self, request, *args, **kwargs):
        if len(request.GET) == 0:
            return render(request, 'tracker/league_index.html', {'title': '| League of Legends'})
        elif 'search' in request.GET:
            return self.search(request)
        elif 'lookup' in request.GET and 'game' in request.GET:
            return self.lookup(request)
        else:
            # Change to page not found.
            return render(request, 'tracker/league_index.html')


class MinecraftView(View):
    def search(self, request):
        search = request.GET.get('search').strip().replace("%20", " ")
        return render(request, 'tracker/namesearch.html', {'title': '| Minecraft Search', 'search': search, 'games': ['Minecraft']})

    def lookup(self, request):
        # Initialize name object.
        search = request.GET.get('lookup')
        game = request.GET.get('game')
        id_ = request.GET.get('number')
        name = getName(search, game)

        # Create the name's card.
        response = name.generate_card(request.user, id_)
        return HttpResponse(response)

    def get(self, request):
        if len(request.GET) == 0:
            return render(request, 'tracker/minecraft_index.html', {'title': '| Minecraft'})
        elif 'search' in request.GET:
            return self.search(request)
        elif 'lookup' in request.GET and 'game' in request.GET:
            return self.lookup(request)
        else:
            # Change to page not found.
            return render(request, 'tracker/index.html')

class RuneScapeView(View):
    def search(self, request):
        search = request.GET.get('search').strip().replace("%20", " ")
        return render(request, 'tracker/namesearch.html', {'title': '| Runescape Search', 'search': search, 'games': ['RuneScape']})

    def lookup(self, request):
        # Initialize name object.
        search = request.GET.get('lookup')
        game = request.GET.get('game')
        id_ = request.GET.get('number')
        name = getName(search, game)

        # Create the name's card.
        response = name.generate_card(request.user, id_)
        return HttpResponse(response)

    def get(self, request):
        if len(request.GET) == 0:
            return render(request, 'tracker/runescape_index.html', {'title': '| Runescape'})
        elif 'search' in request.GET:
            return self.search(request)
        elif 'lookup' in request.GET and 'game' in request.GET:
            return self.lookup(request)
        else:
            # Change to page not found.
            return render(request, 'tracker/index.html')

class MaplestoryView(View):
    def search(self, request):
        search = request.GET.get('search').strip().replace("%20", " ")
        return render(request, 'tracker/namesearch.html', {'title': '| Maplestory Search', 'search': search, 'games': ['Maplestory']})

    def lookup(self, request):
        # Initialize name object.
        search = request.GET.get('lookup')
        game = request.GET.get('game')
        id_ = request.GET.get('number')
        name = getName(search, game)

        # Create the name's card.
        response = name.generate_card(request.user, id_)
        return HttpResponse(response)

    def get(self, request):
        if len(request.GET) == 0:
            return render(request, 'tracker/maplestory_index.html', {'title': '| Maplestory'})
        elif 'search' in request.GET:
            return self.search(request)
        elif 'lookup' in request.GET and 'game' in request.GET:
            return self.lookup(request)
        else:
            # Change to page not found.
            return render(request, 'tracker/index.html')

class DetailView(generic.DetailView):
    model = Name
    template_name = 'tracker/detail.html'

class ProfileView(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(reverse('registration_register'))
        return render(request, 'tracker/profile.html')

class FollowView(View):
    def get(self, request, username, game):
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(reverse('registration_register'))
        # username = self.kwargs['username']
        # game = self.kwargs['game']
        existing = Name.objects.filter(username=username, game=game)
        if len(existing) != 0:
            if existing[0] not in user.names.all():
                user.names.add(existing[0])
                user.save()
                return HttpResponse("")
            else:
                return HttpResponseRedirect(reverse('tracker:index'))
        temp = Name()
        temp.username = username
        temp.game = game
        available, release_date = Name.get_info(temp.username, temp.game)
        temp.available = available
        temp.release_date = release_date
        temp.notified = False
        temp.save()
        user.names.add(temp)
        user.save()
        return HttpResponse("")

class UnfollowView(View):
    def get(self, request, username, game):
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(reverse('tracker:index'))
        existing = Name.objects.filter(username=username, game=game)
        if len(existing) != 0:
            if existing[0] in user.names.all():
                user.names.remove(existing[0])
                user.save()
                return HttpResponse("")
            else:
                return HttpResponseRedirect(reverse('tracker:index'))
        return HttpResponseRedirect(reverse('tracker:index'))
