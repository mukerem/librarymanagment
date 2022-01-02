"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.librarian_login, name='home'),
    path('librarianLogin/', views.librarian_login, name='librarian_login'),
    path('adminLogin/', views.admin_login, name='admin_login'),
    path('userLogin/', views.user_login, name='user_login'),
    path('Logout/<role>/', views.logout, name='logout'),
    path('librarian-homepage/', views.librarian_homepage, name='librarian_homepage'),
    path('admin-homepage/', views.admin_homepage, name='admin_homepage'),
    path('user-homepage/', views.user_homepage, name='user_homepage'),
    path('userRegister/', views.user_register, name='user_register'),
    path('librarianRegister/', views.librarian_register, name='librarian_register'),
    path('adminRegister/', views.admin_register, name='admin_register'),
    path('addCategory/', views.add_category, name='add_category'),
    path('bookRegister/', views.book_register, name='book_register'),
    path('bookRegisterByCodeGenerator/', views.book_register_by_code_generator, name='book_register_by_code_generator'),
    path('addBook/', views.add_book_by_merge, name='add_book'),
    path('bookBorrow/', views.book_borrow, name='book_borrow'),
    path('loadSpecificCode/', views.load_specific_code, name='ajax_load_specific_code'),
    path('loadBorrowBook/', views.load_borrow_book, name='ajax_load_book_list'),
    path('returnBook/', views.return_book, name='return_book'),
    path('viewAdminProfile/', views.view_admin_profile, name='view_admin_profile'),
    path('viewLibrarianProfile/', views.view_librarian_profile, name='view_librarian_profile'),
    path('viewUserProfile/', views.view_user_profile, name='view_user_profile'),
    path('ChangePassword/<role>/', views.change_password, name='ChangePassword'),
    path(r'notDelete/<page>/', views.not_delete, name='NotDelete'),
    path(r'deleteLibrarianConfirm/<librarian_id>/', views.delete_librarian_confirm, name='DeleteLibrarianConfirm'),
    path(r'deleteLibrarian/<librarian_id>/', views.delete_librarian, name='DeleteLibrarian'),
    path('view-librarian-by-admin/', views.librarian_view_by_admin, name='view-librarian-by-admin'),
    path(r'deleteAdminConfirm/<admin_id>/', views.delete_admin_confirm, name='DeleteAdminConfirm'),
    path(r'deleteAdmin/<admin_id>/', views.delete_admin, name='DeleteAdmin'),
    path('admin-list/', views.admin_list, name='admin-list'),
    path('librarian-view-by-librarian/', views.librarian_view_by_librarian, name='librarian-view-by-librarian'),
    path('user-view-by-librarian/', views.user_view_by_librarian, name='user-view-by-librarian'),
    path(r'deleteUserConfirm/<user_id>/', views.delete_user_confirm, name='DeleteUserConfirm'),
    path(r'deleteUser/<user_id>/', views.delete_user, name='DeleteUser'),
    path('book-view-by-librarian/', views.book_view_by_librarian, name='book-view-by-librarian'),
    path(r'view-book-history-by-librarian/<book_id>/', views.view_book_history_by_librarian,
         name='view-book-history-by-librarian'),
    path('book-view-by-admin/', views.book_view_by_admin, name='book-view-by-admin'),
    path(r'view-book-history-by-admin/<book_id>/', views.view_book_history_by_admin, name='view-book-history-by-admin'),
    path(r'deleteBook/<book_id>/', views.delete_book, name='deleteBook'),
    path(r'deleteBookConfirm/<book_id>/', views.delete_book_confirm, name='deleteBookConfirm'),
    path(r'view-user-history-by-librarian/<user_id>/', views.view_user_history_by_librarian,
         name='view-user-history-by-librarian'),
    path(r'view-borrow-history-by-user/', views.view_borrow_history_by_user, name='view-borrow-history-by-user'),
    path(r'view-return-history-by-user/', views.view_return_history_by_user, name='view-return-history-by-user'),
    path('book-view-by-user/', views.book_view_by_user, name='book-view-by-user'),
    path('view-book-borrow-by-admin/', views.view_book_borrow_by_admin, name='view_book_borrow_by_admin'),
    # path('view-book-return-by-admin/', views.view_book_return_by_admin, name='view_book_return_by_admin'),
    path('view-book-borrow-by-librarian/', views.view_book_borrow_by_librarian, name='view_book_borrow_by_librarian'),
    path('view-book-return-by-librarian/', views.view_book_return_by_librarian, name='view_book_return_by_librarian'),
    path(r'view-unreturn-book-by-user/', views.view_unreturn_book_by_user, name='view-unreturn-book-by-user'),
    path(r'view-unreturn-book-by-librarian/', views.view_unreturn_book_by_librarian,
         name='view-unreturn-book-by-librarian'),
    path(r'view-unreturn-book-by-admin/', views.view_unreturn_book_by_admin, name='view-unreturn-book-by-admin'),
    path(r'view-lost-books/', views.view_lost_books, name='view-lost-books'),
    path(r'add-lost-book/', views.add_lost_book, name='add-lost-book'),
    path(r'lost-book-confirm/<code>/<specific_code>/', views.lost_book_confirm, name='lost-book-confirm'),
    path('loadSpecificCodeForLostBooks/', views.load_specific_code_for_lost_book,
         name='ajax_load_specific_code_for_lost_books'),
    path('search-book-borrow-by-admin/', views.search_book_borrow_by_admin, name='search_book_borrow_by_admin'),
    path('search-return-book-by-admin/', views.search_book_return_by_admin, name='search_return_book_by_admin'),
    path('search-borrow-book-by-librarian/', views.search_borrow_book_by_librarian,
         name='search_borrow_book_by_librarian'),
    path('search-return-book-by-librarian/', views.search_return_book_by_librarian,
         name='search_return_book_by_librarian'),
    path('search-borrow-book-by-user/', views.search_borrow_book_by_user, name='search_borrow_book_by_user'),
    path('search-return-book-by-user/', views.search_return_book_by_user, name='search_return_book_by_user'),
    path('print-statistics/', views.print_statistics, name='print_statistics'),
    path('view-statistics/', views.view_statistics, name='view_statistics'),
    path(r'editBook/<book_id>/', views.edit_book, name='EditBook'),
    path('view-book-return/', views.view_book_return_by_admin, name='view_book_return_by_admin'),
    path(r'deleteBorrowConfirm/<borrow_id>/', views.delete_borrow_confirm, name='DeleteBorrowConfirm'),
    path(r'deleteBorrow/<borrow_id>/', views.delete_borrow, name='DeleteBorrow'),
    path(r'upload-csv/', views.csv_file_upload, name='upload_csv'),
]

