from django.contrib import admin
from django.contrib.auth.models import Group
from Bot.filters import DistrictFilter

from Bot.models import User, District, BoardingSchool

admin.site.unregister(Group)
# admin.site.site_header = settings.PROJECT_NAME
# admin.site.site_title = settings.PROJECT_NAME
admin.site.index_title = "Xush Kelibsiz"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Bot User"""

    list_display = ['first_name', 'username', 'contact', 'user_id', 'school']
    search_fields = ['user_id', 'username', 'fullname', 'contact']
    list_filter = [DistrictFilter]
    
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    """District admin"""

    list_display = ['title', 'public_schools', 'total_students']
    
@admin.register(BoardingSchool)
class BoardingSchoolAdmin(admin.ModelAdmin):
    """BoardingSchool admin"""
    
    list_display = ['title']