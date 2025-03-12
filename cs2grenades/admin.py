from django.contrib import admin
from cs2grenades.models import ActiveMapPool, ReserveMapPool, Tags, GuidePosts, TutorialPosts
from django_summernote.admin import SummernoteModelAdmin


@admin.register(ActiveMapPool)
class ActiveMapPoolAdmin(admin.ModelAdmin):
    list_display = 'id', 'map_name',
    list_display_links = 'map_name',
    ordering = '-id',
    search_fields = 'id', 'map_name',


@admin.register(ReserveMapPool)
class ReserveMapPoolAdmin(admin.ModelAdmin):
    list_display = 'id', 'map_name',
    list_display_links = 'map_name',
    ordering = '-id',
    search_fields = 'id', 'map_name',


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = 'id', 'tag_name', 'help_text',
    list_display_links = 'id', 'tag_name', 'help_text',
    search_fields = 'tag_name',
    search_fields = 'id', 'tag_name',


@admin.register(GuidePosts)
class GuidePostsAdmin(SummernoteModelAdmin):
    summernote_fields = 'content'
    prepopulated_fields = {'slug': ['title']}
    list_display = 'id', 'title', 'public',
    list_display_links = 'id', 'title',
    readonly_fields = 'created_at', 'updated_at',
    list_editable = 'public',
    ordering = '-pk',
    autocomplete_fields = 'tags',
    search_fields = 'id', 'title',


@admin.register(TutorialPosts)
class TutorialPostsAdmin(SummernoteModelAdmin):
    summernote_fields = 'tutorial_video'
    list_display = 'id', 'tutorial_title', 'public',
    list_display_links = 'id', 'tutorial_title',
    readonly_fields = 'created_at', 'updated_at',
    list_editable = 'public',
    ordering = '-pk',
    autocomplete_fields = 'tags',
    search_fields = 'id', 'tutorial_title',
