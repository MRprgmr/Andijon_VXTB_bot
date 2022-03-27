from django.contrib.admin import SimpleListFilter

from Bot.models import District, BookCategory, Author


class DistrictFilter(SimpleListFilter):
    """Filter that extracts students list in a specific district"""

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


class CategoryFilter(SimpleListFilter):
    """Filter that extracts books list in a specific category"""

    title = "Kategoriyalar"

    parameter_name = 'books_in_category'

    def lookups(self, request, model_admin):
        categories = BookCategory.objects.all()

        return ((category.id, category.title) for category in categories)

    def queryset(self, request, queryset):
        if self.value() is not None:
            category = BookCategory.objects.get(id=self.value())
            custom_list = [book.id for book in category.book_set.all()]
            return queryset.filter(id__in=custom_list)


class AuthorFilter(SimpleListFilter):
    """Filter that extracts books list of specific author"""

    title = "Mualliflar"

    parameter_name = 'books_of_author'

    def lookups(self, request, model_admin):
        authors = Author.objects.all()

        return ((author.id, author.full_name) for author in authors)

    def queryset(self, request, queryset):
        if self.value() is not None:
            author = Author.objects.get(id=self.value())
            custom_list = [book.id for book in author.book_set.all()]
            return queryset.filter(id__in=custom_list)


class LanguageFilter(SimpleListFilter):
    """Filter that extracts books list of specific language"""

    title = "Tillar"

    parameter_name = 'books_in_language'

    def lookups(self, request, model_admin):
        language_choices = (
            ("english", "English"),
            ("uzbek", "O'zbekcha"),
            ("russian", "Русский")
        )

        return language_choices

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(language=self.value())
