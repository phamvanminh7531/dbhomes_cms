from django.contrib.sitemaps import Sitemap
from news.models import NewsPage
from project.models import ProjectPage


class NewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return NewsPage.objects.live().public().specific()

    def lastmod(self, obj):
        return obj.last_published_at or obj.latest_revision_created_at

    def location(self, obj):
        # Return only the path, not the full URL
        url_parts = obj.get_url_parts()
        return url_parts[-1] if url_parts else obj.slug


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ProjectPage.objects.live().public().specific()

    def lastmod(self, obj):
        return obj.last_published_at or obj.latest_revision_created_at

    def location(self, obj):
        # Return only the path, not the full URL
        url_parts = obj.get_url_parts()
        return url_parts[-1] if url_parts else obj.slug