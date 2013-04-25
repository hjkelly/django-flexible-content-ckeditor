from django.db import models
from flexible_content.models import ContentArea


class BlogPost(ContentArea):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    class Meta:
        verbose_name = "blog post"

    @models.permalink
    def get_absolute_url(self):
        return ('mock_project.myapp.views.post', (), {'post_slug': self.slug})
