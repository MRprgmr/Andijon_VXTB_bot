from django.db import models

class BoardingSchool(models.Model):
    """Model of Boarding school"""
    
    title = models.CharField(max_length=100, verbose_name="Nomi", unique=True)
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Iqtisoslashgan maktab"
        verbose_name_plural = "Iqtisoslashgan maktablar"

class District(models.Model):
    """Model of District"""
    
    title = models.CharField(max_length=100, verbose_name="Tuman", unique=True)
    public_schools = models.IntegerField(verbose_name="Maktablar soni", blank=True)
    boarding_schools = models.ManyToManyField(BoardingSchool, verbose_name="Iqtisoslashgan maktablar", blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    @property
    def total_students(self):
        return str(self.user_set.all().count())
    
    total_students.fget.short_description = "Umumiy o'quvchilar"
    
    class Meta:
        verbose_name = "Tuman"
        verbose_name_plural = "Tumanlar"


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
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Tumani", null=True)
    school = models.CharField(
        max_length=100, verbose_name='School', null=True, blank=True)
    
    def __str__(self) -> str:
        """Provide name of user in the best available way"""
        return self.full_name if self.full_name else self.first_name

    def mention_link(self) -> str:
        """Generate user mention link"""
        return f"tg://user?id={self.user_id}"

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"