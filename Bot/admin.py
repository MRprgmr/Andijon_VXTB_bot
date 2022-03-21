from django.contrib import admin
from django.contrib.auth.models import Group

from Bot.filters import DistrictFilter
from Bot.models import User, District, School, Subject, Test

admin.site.unregister(Group)
# admin.site.site_header = settings.PROJECT_NAME
# admin.site.site_title = settings.PROJECT_NAME
admin.site.index_title = "Xush Kelibsiz"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Bot User"""

    list_display = ['first_name', 'username', 'contact', 'user_id', 'school', 'district']
    search_fields = ['user_id', 'username', 'fullname', 'contact']
    list_filter = [DistrictFilter]


class SchoolInline(admin.TabularInline):
    readonly_fields = ["total_students"]
    model = School
    extra = 1


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    """BoardingSchool admin"""

    list_display = ['title']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    """District admin"""

    list_display = ['title', 'total_students', 'schools']
    inlines = [SchoolInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Subject admin"""
    list_display = ['title']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """Test admin"""
    list_display = ["test_id", "subject"]
