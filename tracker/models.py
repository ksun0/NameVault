# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime
import requests
import json
import calendar
import time

class Name(models.Model):
    #FIELDS
    username = models.CharField(max_length=500)
    game = models.CharField(max_length=50)
    release_date = models.DateTimeField(null=True, blank=True)
    notified = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('tracker:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Name: ' + self.username + " - Game: " + self.game + " - Release Date: " + str(self.release_date)

    def send_mail(self):
        # Send an email notifying of the names availability to all
        # following users.
        followers = self.customuser_set.all()
        if self.available:
            for user in followers:
                if 'LoL' in self.game:
                    user.email_user(self.username + " is available!", "Get it now!",  html_message="""<h1>Get it now!</h1>Need some Riot Points for a name swap? Buy them on Amazon:<br><a target="_blank" href="https://www.amazon.com/gp/product/B014X427WM/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B014X427WM&linkCode=as2&tag=name05-20&linkId=e47cbd79daee9054f72839509f4dd619">League of Legends $10 Gift Card - 1380 Riot Points - NA Server Only [Online Game Code]</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=name05-20&l=am2&o=1&a=B014X427WM" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />""")
                elif 'RuneScape' in self.game:
                    user.email_user(self.username + " is available!", "Get it now!", html_message="""<h1>Get it now!</h1>Need some Runecoins for a name swap? Buy them on Amazon:<br><a target="_blank" href="https://www.amazon.com/gp/product/B00VKLMFPQ/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00VKLMFPQ&linkCode=as2&tag=name05-20&linkId=87ab5a2e5ad3d633a29295eec21d667d">420 RuneCoins: RuneScape [Instant Access]</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=name05-20&l=am2&o=1&a=B00VKLMFPQ" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />""")
                else:
                    user.email_user(self.username + " is available!", "Get it now!",  html_message="""<h1>Get it now!</h1>""")
        else:
            for user in followers:
                user.email_user(self.username + " will soon be available!", "Get it on " + "{:%B %d, %Y}".format(release_date))
        return

    def generate_card(self, user, id_):
        # Generate a card containing information about the name.
        response = """<div class="row"><div class="col-xs-12">
                      <div class="card fade-card" id="name{}">
                      <div class="content content-""".format(id_)

        # Set the color of the card.
        if not self.available:
            response += "danger"
        elif self.release_date:
            response += "warning"
        else:
            response += "success"

        response += """"><h5 class="category-social">
                        <i class="fa fa-globe"></i>{}
                    </h5>
                        <h4 class="card-title">""".format(self.game)

        # Set availability message.
        if self.available:
            if self.release_date:
                response += "Available"
            else:
                response += "Free"
        elif self.valid:
            response += "Taken"
        else:
            response += "Invalid Name"

        response += """</h4><p class="card-description">"""

        if self.release_date:
            if not self.available:
                response += "If the owner remains inactive, " + self.username + " will be available with a name swap on " + self.release_date.strftime('%b %d, %Y') + "."
            else:
                response += "A player currently has this name, but you can take it with a name swap."
        response += """
              </p>
              <div class="footer">
              """
        if user.is_authenticated():
            if self in user.names.all():
                response += '<button data-name="' + self.username + '" data-game="' + self.game + '" class="quickUnfollowButton btn btn-block btn-default">Unfollow</button>'
            elif len(user.names.all()) > 100:
                response += '<button data-name="' + self.username + '" data-game="' + self.game + '" class="disabled btn btn-block btn-default">Limit Reached (100 Names)</button>'
            else:
                response += '<button data-name="' + self.username + '" data-game="' + self.game + '" class="quickFollowButton btn btn-block btn-default">Follow</button>'
        else:
            response+= """<a class="btn btn-default btn-block" href='""" + reverse('auth_login')+ """'>Login First to Follow</a>"""
        response +="""      </div>
            </div>
          </div>
        </div>
        </div>"""
        return response

    # STATIC METHODS
    def check_valid(username, game):
        if "LoL" in game:
            if len(username) > 16 or len(username) < 3:
                return False
            if game == "LoL_NA":
                temp = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                for c in username:
                    if c not in temp:
                        return False
            if game == "LoL_BR":
                temp = " 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÇÉÊÍÓÔÕÚàáâãçéêíóôõú"
                for c in username:
                    if c not in temp:
                        return False
            if game == "LoL_EUNE":
                temp = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzªµºÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿĂăĄąĆćĘęıŁłŃńŐőŒœŚśŞşŠšŢţŰűŸŹźŻżŽžƒȘșȚțˆˇˉΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩάέήίαβγδεζηθικλμνξοπρςστυφχψωόύώﬁﬂ"
                for c in username:
                    if c not in temp:
                        return False
            if game == "LoL_EUW":
                temp = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzªµºÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿĄąĆćĘęıŁłŃńŒœŚśŠšŸŹźŻżŽžƒˆˇˉμﬁﬂ"
                for c in username:
                    if c not in temp:
                        return False
            if game == "LoL_TR":
                temp = " ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïð 0123456789ABCDEFGĞHIİJKLMNOPQRSŞTUVWXYZabcçdefgğhıijklmnoöpqrsştuvwxyzªµºÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿıŁłŒœŠšŸŽžƒˆˇˉμﬁﬂĄąĘęÓóĆćŁłŃńŚśŹźŻż"
                for c in username:
                    if c not in temp:
                        return False
            return True
        if game == "Minecraft":
            temp = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
            for c in username:
                if c not in temp:
                    return False
            if len(username) > 16 or len(username) < 3:
                return False
            return True
        if game == "RuneScape":
            temp = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
            for c in username:
                if c not in temp:
                    return False
            if len(username) > 12:
                return False
            return True
        if game == "Maplestory":
            temp = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-àáâäåæèéêëìíîïòóôöøùúûüýÿ"
            for c in username:
                if c not in temp:
                    return False
            if len(username) > 12 or len(username) < 4:
                return False
            return True

    def get_info(username, game):
        def add_months(sourcedate,months):
            month = sourcedate.month - 1 + months
            year = int(sourcedate.year + month / 12 )
            month = month % 12 + 1
            day = min(sourcedate.day,calendar.monthrange(year,month)[1])
            return datetime(year,month,day, sourcedate.hour, sourcedate.minute)
        def get_league_info(username, server):
            request = requests.get('https://' + server + '.api.pvp.net/api/lol/' + server + '/v1.4/summoner/by-name/' + username + '?api_key=RGAPI-8a1ff48b-0a67-4a61-82ee-deda7d47e774')
            if str(request) == '<Response [404]>':
                return (True, None)
            else:
                request_dict = json.loads(request.text)
                months_left = max(6, int(request_dict[username.lower().replace(" ", "")]['summonerLevel']))
                games = requests.get('https://' + server + '.api.pvp.net/api/lol/' + server + '/v1.3/game/by-summoner/' + str(request_dict[username.lower().replace(" ", "")]['id']) + '/recent?api_key=RGAPI-8a1ff48b-0a67-4a61-82ee-deda7d47e774')
                try:
                    last_played = datetime.fromtimestamp(int(json.loads(games.text)['games'][0]['createDate']) / 1e3)
                except:
                    # The player has never played a game. Set last_played to the
                    # account creation time.
                    last_played = datetime.fromtimestamp(int(request_dict[username.lower()]['revisionDate']) / 1e3)
                release_date = add_months(last_played, months_left)
                if release_date < datetime.now():
                    return (True, release_date)
                return (False, release_date)

        def get_minecraft_info(username):
            request = requests.get('https://api.mojang.com/users/profiles/minecraft/' + username)
            if str(request) == '<Response [204]>':
                return (True, None)
            else:
                return (False, None)
        def get_runescape_info(username):
            # request = requests.get('http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=' + username)
            # if str(request) == '<Response [404]>':
            #     request = requests.get('https://services.runescape.com/m=hiscore/ranking?user=' + username)
            #     if 'was not found' in request.text:
            #         return (True, None)
            #     else:
            #         return (False, None)
            # else:
            #     return (False, None)
            request = requests.get('http://possupatonki.com/rsn.php?u=' + username)
            if 'available' in request.text:
                return (True, None)
            else:
                return (False, None)
        def get_maplestory_info(username):
            request = requests.get('http://maplestory.io/api/character/' + username)
            if 'Could not find character' in request.text:
                return (True, None)
            else:
                return (False, None)

        if game == "LoL_NA":
            return get_league_info(username, "na")
        elif game == "LoL_BR":
            return get_league_info(username, "br")
        elif game == "LoL_EUNE":
            return get_league_info(username, "eune")
        elif game == "LoL_EUW":
            return get_league_info(username, "euw")
        elif game == "LoL_KR":
            return get_league_info(username, "kr")
        elif game == "LoL_TR":
            return get_league_info(username, "tr")
        if game == "Minecraft":
            return get_minecraft_info(username)
        if game == "RuneScape":
            return get_runescape_info(username)
        if game == "Maplestory":
            return get_maplestory_info(username)
        return (False, None)

    def update(names):
        for name in names:
            followers = name.customuser_set.all()
            if len(followers) == 0:
                # Delete all old names.
                name.delete()
                continue

            # Update details
            try:
                available, release_date = Name.get_info(name.username, name.game)
            except KeyError as e:
                available, release_date = (name.available, name.release_date)
            was_available = name.available
            name.available = available
            name.release_date = release_date

            if not name.notified:
                # If an email has not been sent already.
                if name.available or (name.release_date and (name.release_date - datetime.now()).days < 7):
                    name.send_mail()
                    name.notified = True
            if (was_available or (name.release_date and (name.release_date - datetime.now()).days > 7)) and not name.available:
                # If name has become taken again.
                name.notified = False
            name.save()
            time.sleep(1)
