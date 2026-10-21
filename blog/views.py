from django.views.generic import DetailView, ListView

from .models import Post


class PublishedPostMixin:
    # Built per request so "published before now" uses the current time.
    def get_queryset(self):
        return Post.published.all()


class PostListView(PublishedPostMixin, ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10


class PostDetailView(PublishedPostMixin, DetailView):
    template_name = "blog/post_detail.html"
    context_object_name = "post"
