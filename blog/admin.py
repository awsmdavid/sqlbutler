from django.contrib import admin
 
# class GiftAdmin(admin.ModelAdmin):
#     # fields display on change list
#     list_display = ['title', 'description']
#     # fields to search in change list
#     search_fields = ['title', 'description', 'content']
#     # enable the save buttons on top on change form
#     save_on_top = True
#     # prepopulate the slug from the title - big timesaver!
#     prepopulated_fields = {"slug": ("title",)}
 
# admin.site.register(GiftIdea, GiftAdmin)