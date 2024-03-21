from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import Blog, Comment, Rating, Bookmark
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg
from blogs.utils import send_email_to_owner


class IndexView(LoginRequiredMixin, View):
    template_name = "blog_index.html"

    def get(self, request):
        queryset = Blog.objects.filter(is_published=True)

        if request.GET.get('search'):
            queryset = queryset.filter(
                title__icontains=request.GET.get('search'))

        paginator = Paginator(queryset, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        avg_rate_dict = {}
        for query in page_obj:
            rating = Rating.objects.filter(blog=query)
            avg_rating = rating.aggregate(
                Avg("rating", default=0))['rating__avg']
            avg_rate_dict[query.id] = avg_rating

        # list of ids bookmarked blogs by the current user
        user = request.user
        bookmark_blog_ids = Bookmark.objects.filter(
            user=user, is_bookmarked=True).values_list('blog_id', flat=True)

        context = {
            'page_obj': page_obj,
            'avg_rate_dict': avg_rate_dict,
            'bookmark_blog_ids': bookmark_blog_ids,
        }
        return render(request, self.template_name, context)


class DeleteBlogView(LoginRequiredMixin, View):

    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        blog.delete()
        messages.info(request, "Your Blog has been deleted")
        return redirect('/blogs')

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        blog = get_object_or_404(Blog, pk=self.kwargs["blog_id"])
        if request.user == blog.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.info(request, "Permission Denied")
            return redirect('/blogs/')


class UpdateBlogView(LoginRequiredMixin, View):
    template_name = "blog_update.html"

    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=self.kwargs["blog_id"])
        context = {
            'blog': blog
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=self.kwargs["blog_id"])
        data = request.POST
        title = data.get('title')
        content = data.get('content')

        blog.title = title
        blog.content = content
        return redirect('/blogs/')

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        blog = get_object_or_404(Blog, pk=self.kwargs["blog_id"])
        if request.user == blog.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.info(request, "Permission Denied")
            return redirect('/blogs/')


class AddBlogView(LoginRequiredMixin, View):
    template_name = "blog_add.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user
        title = data.get('title')
        content = data.get('content')
        Blog.objects.create(
            user=user,
            title=title,
            content=content,
        )
        send_email_to_owner()
        return redirect('/blogs/')


class BlogDetailView(LoginRequiredMixin, View):
    template_name = 'blog_detail.html'

    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        comments = Comment.objects.filter(blog=blog, parent=None)
        replies = Comment.objects.filter(blog=blog).exclude(parent=None)
        curr_user_rate = Rating.objects.filter(
            blog=blog, user=request.user).first()

        reply_dict = {}
        for reply in replies:
            if reply.parent.id not in reply_dict.keys():
                reply_dict[reply.parent.id] = [reply]
            else:
                reply_dict[reply.parent.id].append(reply)

        context = {
            'blog': blog,
            'comments': comments,
            'reply_dict': reply_dict,
            'curr_user_rate': curr_user_rate,
        }
        return render(request, self.template_name, context)


class CommentView(LoginRequiredMixin, View):

    def post(self, request):
        data = request.POST
        user = request.user
        comment = data.get('comment')
        blogid = data.get('blogid')
        blog = get_object_or_404(Blog, pk=blogid)
        commentid = data.get('commentid')
        if not commentid:
            Comment.objects.create(
                comment_text=comment,
                user=user,
                blog=blog,
            )
            messages.info(
                request, "Comment Posted", extra_tags='comment_posted')
        else:
            parent = get_object_or_404(Comment, pk=commentid)
            Comment.objects.create(
                comment_text=comment,
                user=user,
                blog=blog,
                parent=parent,
            )
            messages.info(request, "Reply Posted", extra_tags='reply_posted')
        return redirect('/blogs/blog_detail/'+blogid+'/')


class CommentDeleteView(LoginRequiredMixin, View):

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        blogid = comment.blog_id
        comment.delete()
        return redirect('/blogs/blog_detail/'+str(blogid)+'/')


class RatingView(LoginRequiredMixin, View):

    def post(self, request, blog_id):
        data = request.POST
        user = request.user
        rating = data.get('rating')
        blog = Blog.objects.get(id=blog_id)
        rating_object = Rating.objects.get_or_create(
            user=user,
            blog=blog,
        )
        rating_object[0].rating = rating
        rating_object[0].save()
        messages.info(request, "Rating Posted", extra_tags="rating_posted")
        return redirect('/blogs/blog_detail/'+blog_id+'/')


class BookmarkView(LoginRequiredMixin, View):
    template_name = "blog_bookmark.html"

    def get(self, request):
        user = request.user
        queryset = Bookmark.objects.filter(
            user=user,
            is_bookmarked=True,
        )
        avg_rate_dict = {}
        for query in queryset:
            rating = Rating.objects.filter(blog=query.blog)
            avg_rating = rating.aggregate(
                Avg("rating", default=0))['rating__avg']
            avg_rate_dict[query.blog.id] = avg_rating

        bookmark_blog_ids = Bookmark.objects.filter(
            user=user, is_bookmarked=True).values_list('blog_id', flat=True)

        context = {
            'queryset': queryset,
            'avg_rate_dict': avg_rate_dict,
            'bookmark_blog_ids': bookmark_blog_ids
        }
        return render(request, self.template_name, context)

    def post(self, request, blog_id):
        data = request.POST
        user = request.user
        is_bookmarked = data.get('is_bookmarked')
        bookmark_obj = Bookmark.objects.get_or_create(
            user=user,
            blog_id=blog_id,
        )[0]
        if is_bookmarked:
            bookmark_obj.is_bookmarked = True
            bookmark_obj.save()
            message = "Added to Bookmark"
            return HttpResponse(message)
        else:
            bookmark_obj.is_bookmarked = False
            bookmark_obj.save()
            message = "Remove from Bookmark"
            return HttpResponse(message)
