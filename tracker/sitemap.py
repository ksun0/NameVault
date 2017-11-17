from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

class StaticSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""
    changefreq = "daily"
    priority = 0.8

    def items(self):
        # Return list of url names for views to include in sitemap
        return ['tracker:index', 'registration_register','tracker:leagueview', 'tracker:minecraftview', 'tracker:runescapeview', 'tracker:maplestoryview', 'tracker:profile']

    def location(self, item):
        return reverse(item)
