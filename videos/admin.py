from django.contrib import admin
from .models import VidStream
from .models import Category , Comment, Like





class VidStreamAdmin(admin.ModelAdmin):
	list_display = ('category', 'title', 'description','views')
	prepopulated_fields = {'slug':('title','category')}


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description','number_of_videos')
	prepopulated_fields={'slug':('name','description')}

	class Meta:
		ordering = ['name']

admin.site.register(VidStream, VidStreamAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Like)


