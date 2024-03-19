from django.urls import path
from blogs.views import AddBlogView, UpdateBlogView, DeleteBlogView, \
    BlogDetailView, IndexView, CommentView, CommentDeleteView, RatingView, \
    BookmarkView

app_name = "blogs"
urlpatterns = [
    path("", IndexView.as_view()),
    path("add_blog/", AddBlogView.as_view()),
    path("delete_blog/<blog_id>/", DeleteBlogView.as_view()),
    path("update_blog/<blog_id>/", UpdateBlogView.as_view()),
    path("blog_detail/<blog_id>/", BlogDetailView.as_view()),
    path("comment/", CommentView.as_view()),
    path("delete_comment/<comment_id>/", CommentDeleteView.as_view()),
    path("rating/<blog_id>/", RatingView.as_view()),
    path("bookmark/<blog_id>/", BookmarkView.as_view()),
    path("bookmark_details/", BookmarkView.as_view()),
]
