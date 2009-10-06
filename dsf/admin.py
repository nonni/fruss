from django.contrib import admin
from models import Thread, Category, Post
"""
class ThreadAdmin(admin.ModelAdmin):
    fields = ('title', 'body', 'category')
    list_display = ('title', 'author', 'pub_date')
    date_hierarchy = 'pub_date'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
"""
admin.site.register(Thread)
admin.site.register(Category)
admin.site.register(Post)

