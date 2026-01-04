from modeltranslation.admin import TranslationAdmin
from django.contrib import admin
from .models import Author, Category, Post, PostCategory


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    list_display = (
        'title',
        'author',
        'categoryType',
        'dateCreation',
        'rating',
    )

    list_filter = (
        'categoryType',
        'dateCreation',
        'author',
    )

    search_fields = (
        'title',
        'text',
    )

    ordering = ('-dateCreation',)

    list_per_page = 10

    readonly_fields = ('dateCreation',)

    inlines = [PostCategoryInline]


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')
    search_fields = ('authorUser__username',)
    ordering = ('-ratingAuthor',)
