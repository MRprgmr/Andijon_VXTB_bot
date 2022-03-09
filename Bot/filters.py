from django.contrib.admin import SimpleListFilter

from Bot.models import District


class DistrictFilter(SimpleListFilter):
    """Filter that extracts students list in a spesific district"""

    title = "Tumanlar"

    parameter_name = 'pupils_in_district'

    def lookups(self, request, model_admin):
        districts = District.objects.all()

        return ((district.id, district.title) for district in districts)

    def queryset(self, request, queryset):
        if self.value() is not None:
            district = District.objects.get(id=self.value())
            custom_list = [user.user_id for user in district.user_set.all()]
            return queryset.filter(user_id__in=custom_list)