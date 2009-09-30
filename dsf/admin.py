from django.contrib import admin
from models import Thread, Category

class ThreadAdmin(admin.ModelAdmin):
    fields = ('title', 'body', 'category')
    list_display = ('title', 'author', 'pub_date')
    date_hierarchy = 'pub_date'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Category)
