from django.contrib import admin
from .models import Category, News, ContactUs, Comment

# News modelini admin panelda ko'rsatish
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # column lar
    list_display = ['title', 'slug', 'publish_time', 'status']
    # filtrlash uchun
    list_filter = ['status', 'created_time', 'publish_time']
    # slugga o'tkazish uchun
    prepopulated_fields = {"slug": ('title',)}
    # vaqt bo'yicha iarerhoyalash
    date_hierarchy = 'publish_time'
    # qidirish uchun
    search_fields = ['title', 'body']
    # tartiblash
    ordering = ['status', 'publish_time']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(ContactUs)
#admin.site.register(Comment)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comments', 'activeta_comment']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def activeta_comment(self, request, queryset):
        queryset.update(active=False)



