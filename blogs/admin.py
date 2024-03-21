from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Blog, Comment, Rating, Bookmark
from django.db.models import Avg

# Register your models here.

admin.site.unregister(User)

class BlogInline(admin.TabularInline):
    model = Blog
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [
        BlogInline,
    ]


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "avg_rating")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title__icontains", )

    def avg_rating(self, obj):
        avg_rating = Rating.objects.filter(
            blog=obj).aggregate(Avg("rating", default=True))['rating__avg']
        return avg_rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "blog", "rating")
    search_fields = ("blog__title__icontains", )


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "blog", "is_bookmarked")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("blog", "user", "comment_text", "parent")
    search_fields = ("comment_text__icontains", )