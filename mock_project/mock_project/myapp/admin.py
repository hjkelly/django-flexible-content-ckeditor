from django.contrib import admin

from flexible_content.admin import ContentAreaAdmin

from .models import BlogPost


class BlogPostAdmin(ContentAreaAdmin):
    pass


admin.site.register(BlogPost, BlogPostAdmin)
