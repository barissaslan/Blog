from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "timestamp", "updated", "image", "slug"]
    list_display_links = ["title", "updated"]
    # list_editable = ["title"]
    list_filter = ["updated", "timestamp", "draft"]
    search_fields = ["title", "content", "tags"]

    prepopulated_fields = {"slug": ("title",)}

    class Meta:
        model = Post


class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "post", "approved_comment"]
    list_filter = ["post", "approved_comment"]
    search_fields = ["text", "name"]

    class Meta:
        model = Comment

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

