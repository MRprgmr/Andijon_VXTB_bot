from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ExportActionMixin

from Bot.filters import DistrictFilter, CategoryFilter, AuthorFilter, LanguageFilter
from Bot.models import User, District, School, Subject, Test, BookCategory, Author, Book

admin.site.unregister(Group)
# admin.site.site_header = settings.PROJECT_NAME
# admin.site.site_title = settings.PROJECT_NAME
admin.site.index_title = "Xush Kelibsiz"


@admin.register(User)
class UserAdmin(ExportActionMixin, admin.ModelAdmin):
    """Bot User"""

    list_display = ['first_name', 'username', 'contact', 'user_id', 'school', 'district']
    search_fields = ['first_name', 'full_name', 'username', 'contact']
    list_filter = [DistrictFilter]


class SchoolInline(admin.TabularInline):
    readonly_fields = ["total_students"]
    model = School
    extra = 1


@admin.register(School)
class SchoolAdmin(ExportActionMixin, admin.ModelAdmin):
    """BoardingSchool admin"""

    list_display = ['title']


@admin.register(District)
class DistrictAdmin(ExportActionMixin, admin.ModelAdmin):
    """District admin"""

    list_display = ['title', 'total_students', 'schools']
    inlines = [SchoolInline]


@admin.register(Subject)
class SubjectAdmin(ExportActionMixin, admin.ModelAdmin):
    """Subject admin"""
    list_display = ['title']


@admin.register(Test)
class TestAdmin(ExportActionMixin, admin.ModelAdmin):
    """Test admin"""

    fields = ["subject", "test_id", "answers", "file"]
    list_display = ["test_id", "subject"]


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    """Admin of book categories"""
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Author admin"""
    pass


@admin.register(Book)
class BookAdmin(ExportActionMixin, admin.ModelAdmin):
    """Admin of books"""

    fields = ["category", "author", "title", "language", "total_pages", "published_date", "file"]
    list_display = ["title", "author", "category", "language"]
    list_filter = [CategoryFilter, AuthorFilter, LanguageFilter]
