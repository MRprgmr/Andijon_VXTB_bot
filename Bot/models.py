from django.db import models

from utils.database import get_file_id


class District(models.Model):
    """Model of District"""

    title = models.CharField(max_length=100, verbose_name="Nomi", unique=True)

    def __str__(self) -> str:
        return self.title

    @property
    def total_students(self):
        return str(self.user_set.all().count())

    @property
    def schools(self):
        return str(self.school_set.all().count())

    total_students.fget.short_description = "Umumiy o'quvchilar"
    schools.fget.short_description = "Maktablar"

    class Meta:
        verbose_name = "Tuman"
        verbose_name_plural = "Tumanlar"


class School(models.Model):
    """Models of schools"""

    title = models.CharField(max_length=100, verbose_name="Nomi")
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title}"

    @property
    def total_students(self):
        return str(self.user_set.all().count())

    total_students.fget.short_description = "O'quvchilar"

    class Meta:
        verbose_name = "Maktab"
        verbose_name_plural = "Maktablar"


class User(models.Model):
    """Model of User"""

    user_id = models.IntegerField(verbose_name='ID User', primary_key=True, unique=True)
    username = models.CharField(
        max_length=100, verbose_name='@username', null=True, blank=True)
    is_allowed = models.BooleanField(default=False)
    first_name = models.CharField(
        max_length=100, verbose_name='Name in Telegram')
    contact = models.CharField(
        max_length=100, verbose_name='Contact', null=True, blank=True)
    full_name = models.CharField(
        max_length=255, verbose_name='Full Name', null=True, blank=True)
    is_registered = models.BooleanField(
        verbose_name="Is Registered", default=False)
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name="Tumani", null=True)
    school = models.ForeignKey(School, on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        """Provide name of user in the best available way"""
        return self.full_name if self.full_name else self.first_name

    def mention_link(self) -> str:
        """Generate user mention link"""
        return f"tg://user?id={self.user_id}"

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


class Subject(models.Model):
    """Models of subjects for quiz"""

    title = models.CharField(max_length=255, verbose_name="Nomi", unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"


class Test(models.Model):
    """Models of tests"""

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Yo'nalish")
    test_id = models.IntegerField(verbose_name="Variant raqami", unique=True)
    answers = models.CharField(max_length=255, verbose_name="Javoblar")
    file = models.FileField(verbose_name="Test", upload_to="tests/", blank=True)
    source_id = models.CharField(max_length=255)

    def __str__(self):
        return str(self.test_id)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.source_id = get_file_id(self.file.path)
        super().save()

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"


class BookCategory(models.Model):
    """Categories of books"""

    title = models.CharField(max_length=255, verbose_name="Kategoriya nomi", unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class Author(models.Model):
    """Authors of books"""

    full_name = models.CharField(max_length=255, verbose_name="Ismi")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Muallif"
        verbose_name_plural = "Mualliflar"


class Book(models.Model):
    """Model of books"""

    language_choices = [
        ("english", "🇬🇧 English"),
        ("uzbek", "🇺🇿 O'zbekcha"),
        ("russian", "🇷🇺 Русский")
    ]

    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, verbose_name="Kategoriya")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Muallif")
    title = models.CharField(max_length=255, verbose_name="Nomi")
    language = models.CharField(max_length=100, choices=language_choices, default="uzbek", verbose_name="Til")
    total_pages = models.IntegerField(verbose_name="Sahifalar soni")
    published_date = models.DateField(verbose_name="Nashr etilgan yili")
    file = models.FileField(verbose_name="Test", upload_to="books/", blank=True)
    source_id = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.source_id = get_file_id(self.file.path)
        super().save()

    class Meta:
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"

