from django.contrib import admin
from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """ Register the post model in the admin site """
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created_at", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug":("title", )}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]

# ADD COMMENT MODEL TO DJANGO ADMIN
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "active"]
    list_filter = ["created_at", "updated_at", "email", "active"]
    search_fields = ["name", "email", "body"]