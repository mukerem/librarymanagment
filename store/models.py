from django.db import models
from collectionfield.models import CollectionField
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
from PIL import Image


class User(models.Model):
    user_id = models.CharField(max_length=200, blank=True, unique=True)
    name = models.CharField(max_length=200, help_text='Enter user Name')
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$',
        message='Phone number must be entered in the format : 0987654321 or +251987654321 up to 15 digits allowed'
    )
    phone = models.CharField(validators=[phone_regex], max_length=15)
    year = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    department = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(blank=True)
    password_regex = RegexValidator(
        regex=r'^\S{6,1024}',
        message='password must be at least 6 character'
    )
    password = models.CharField(validators=[password_regex], max_length=1024)
    password_hint = models.CharField(max_length=200, blank=True)
    sex = models.CharField(max_length=200, choices=(('male', 'male'), ('female', 'female')))
    photo = models.ImageField(blank=True, default='null.png')
    register_date = models.DateField()

    def __str__(self):
        return self.name+' '+self.middle_name

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150"/>' % self.photo.url)
    image_tag.short_description = 'Photo'
    image_tag.allow_tags = True


class Librarian(models.Model):
    librarian_id = models.CharField(max_length=200, blank=True, unique=True)
    name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$',
        message='Phone number must be entered in the format : 0987654321 or +251987654321 up to 15 digits allowed'
    )
    phone = models.CharField(validators=[phone_regex], max_length=15)
    year = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    department = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(blank=True)
    password_regex = RegexValidator(
        regex=r'^\S{6,1024}',
        message='password must be at least 6 character'
    )
    password = models.CharField(validators=[password_regex], max_length=1024)
    password_hint = models.CharField(max_length=200, blank=True)
    sex = models.CharField(max_length=200, choices=(('male', 'male'), ('female', 'female')))
    photo = models.ImageField(blank=True, default='null.png')
    register_date = models.DateField()

    def __str__(self):
        return self.name+' '+self.middle_name

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150"/>' % self.photo.url)
    image_tag.short_description = 'Photo'
    image_tag.allow_tags = True


class Admin(models.Model):
    admin_id = models.CharField(max_length=200, blank=True, unique=True)
    name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$',
        message='Phone number must be entered in the format : 0987654321 or +251987654321 up to 15 digits allowed'
    )
    phone = models.CharField(validators=[phone_regex], max_length=15)
    year = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    department = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(blank=True)
    password_regex = RegexValidator(
        regex=r'^\S{6,1024}',
        message='password must be at least 6 character'
    )
    password = models.CharField(validators=[password_regex], max_length=1024)
    password_hint = models.CharField(max_length=200, blank=True)
    sex = models.CharField(max_length=200, choices=(('male', 'male'), ('female', 'female')))
    photo = models.ImageField(blank=True, default='null.png')
    register_date = models.DateField()

    def __str__(self):
        return self.name+' '+self.middle_name

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150"/>' % self.photo.url)
    image_tag.short_description = 'Photo'
    image_tag.allow_tags = True


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    range_start = models.PositiveSmallIntegerField()
    range_end = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Book(models.Model):
    code = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    pub_year = models.PositiveSmallIntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    page = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(default=1)
    specific_code = CollectionField(sort=True, unique_items=True, collection_type=set)
    borrow_specific_code = CollectionField(sort=True, unique_items=True, collection_type=set, blank=True)
    image = models.ImageField(upload_to='', blank=True, default='book.png')
    register_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'author', 'page')

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150"/>' % self.image.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    librarian = models.ForeignKey(Librarian, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='borrow_librarian')
    specific_code = models.CharField(max_length=200)
    borrow_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    return_to = models.ForeignKey(Librarian, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='return_librarian')

    def __str__(self):
        return self.book.title + ' by ' + self.user.name


class LostBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    specific_code = models.CharField(max_length=200)
    verifier_admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    lost_date = models.DateField()

    def __str__(self):
        return self.book.title + ' specified code ' + self.specific_code

