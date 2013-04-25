from django.views.generic import DetailView, ListView

from .models import BlogPost


class PostListView(ListView):
    queryset = BlogPost.objects.all()
list_posts = PostListView.as_view()


class PostDetailView(DetailView):
    queryset = BlogPost.objects.all()
post = PostDetailView.as_view()
