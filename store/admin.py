from django.contrib import admin
from .models import User, Librarian, Admin, Category, Book, Borrow, LostBook

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    fields = ('code', 'title', 'author', 'pub_year', 'category', 'description', 'page',
              'amount', 'specific_code', 'borrow_specific_code', 'image_tag', 'image', 'register_date')
    readonly_fields = ('image_tag',)


class UserAdmin(admin.ModelAdmin):
    fields = ('user_id', 'name', 'middle_name', 'last_name', 'phone', 'year', 'department', 'email', 'password',
              'password_hint', 'sex', 'image_tag', 'photo', 'register_date')
    readonly_fields = ('image_tag',)


class LibrarianAdmin(admin.ModelAdmin):
    fields = ('librarian_id', 'name', 'middle_name', 'last_name', 'phone', 'year', 'department', 'email', 'password',
              'password_hint', 'sex', 'image_tag', 'photo', 'register_date')
    readonly_fields = ('image_tag',)


class AdminsAdmin(admin.ModelAdmin):
    fields = ('admin_id', 'name', 'middle_name', 'last_name', 'phone', 'year', 'department', 'email', 'password',
              'password_hint', 'sex', 'image_tag', 'photo', 'register_date')
    readonly_fields = ('image_tag',)


admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Librarian, LibrarianAdmin)
admin.site.register(Admin, AdminsAdmin)
admin.site.register(Category)
admin.site.register(Borrow)
admin.site.register(LostBook)

