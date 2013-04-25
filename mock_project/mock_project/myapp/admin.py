from django.contrib import admin

from flexible_content.admin import ContentAreaAdmin

from .models import BlogPost


class BlogPostAdmin(ContentAreaAdmin):
    pass


admin.sites.register(BlogPost, BlogPostAdmin)
