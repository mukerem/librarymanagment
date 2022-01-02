"""library URL Configuration

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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import  settings


urlpatterns = [
    path('', include('store.urls')),
    path('admin/', admin.site.urls),
    path('librarianLogin/', include('store.urls')),
    path('adminLogin/', include('store.urls')),
    path('userLogin/', include('store.urls')),
    path('Logout/<role>/', include('store.urls')),
    path('librarian-homepage/', include('store.urls')),
    path('admin-homepage/', include('store.urls')),
    path('user-homepage/', include('store.urls')),
    path('userRegister/', include('store.urls')),
    path('librarianRegister/', include('store.urls')),
    path('adminRegister/', include('store.urls')),
    path('addCategory/', include('store.urls')),
    path('bookRegister/', include('store.urls')),
    path('bookRegisterByCodeGenerator/', include('store.urls')),
    path('addBook/', include('store.urls')),
    path('bookBorrow/', include('store.urls')),
    path('loadSpecificCode/', include('store.urls')),
    path('loadBorrowBook/', include('store.urls')),
    path('returnBook/', include('store.urls')),
    path('viewAdminProfile/', include('store.urls')),
    path('viewLibrarianProfile/', include('store.urls')),
    path('viewUserProfile/', include('store.urls')),
    path('ChangePassword/<role>/', include('store.urls')),
    path(r'notDelete/<page>/', include('store.urls')),
    path(r'deleteLibrarianConfirm/<librarian_id>/', include('store.urls')),
    path(r'deleteLibrarian/<librarian_id>/', include('store.urls')),
    path('view-librarian-by-admin/', include('store.urls')),
    path(r'deleteAdminConfirm/<admin_id>/', include('store.urls')),
    path(r'deleteAdmin/<admin_id>/', include('store.urls')),
    path('admin-list/', include('store.urls')),
    path('librarian-view-by-librarian/', include('store.urls')),
    path('user-view-by-librarian/', include('store.urls')),
    path(r'deleteUserConfirm/<user_id>/', include('store.urls')),
    path(r'deleteUser/<user_id>/', include('store.urls')),
    path('book-view-by-librarian/', include('store.urls')),
    path(r'view-book-history-by-librarian/<book_id>/', include('store.urls')),
    path('book-view-by-admin/', include('store.urls')),
    path(r'deleteBook/<book_id>/', include('store.urls')),
    path(r'deleteBookConfirm/<book_id>/', include('store.urls')),
    path(r'view-user-history-by-librarian/<user_id>/', include('store.urls')),
    path(r'view-borrow-history-by-user/', include('store.urls')),
    path(r'view-return-history-by-user/', include('store.urls')),
    path('book-view-by-user/', include('store.urls')),
    path('view-book-borrow-by-admin/', include('store.urls')),
    # path('view-book-return-by-admin/', include('store.urls')),
    path('view-book-borrow-by-librarian/', include('store.urls')),
    path('view-book-return-by-librarian/', include('store.urls')),
    path(r'view-unreturn-book-by-user/', include('store.urls')),
    path(r'view-unreturn-book-by-librarian/', include('store.urls')),
    path(r'view-unreturn-book-by-admin/', include('store.urls')),
    path(r'view-lost-books/', include('store.urls')),
    path(r'add-lost-book/', include('store.urls')),
    path(r'lost-book-confirm/<code>/<specific_code>/', include('store.urls')),
    path(r'loadSpecificCodeForLostBooks/', include('store.urls')),
    path('search-book-borrow-by-admin/', include('store.urls')),
    path('search-return-book-by-admin/', include('store.urls')),
    path('search-borrow-book-by-librarian/', include('store.urls')),
    path('search-return-book-by-librarian/', include('store.urls')),
    path('search-borrow-book-by-user/', include('store.urls')),
    path('search-return-book-by-user/', include('store.urls')),
    path('print-statistics/', include('store.urls')),
    path('view-statistics/', include('store.urls')),
    path(r'editBook/<book_id>/', include('store.urls')),
    path(r'deleteBorrowConfirm/<borrow_id>/', include('store.urls')),
    path(r'deleteBorrow/<borrow_id>/', include('store.urls')),
    path(r'upload-csv/', include('store.urls')),
    path('admin/', include('store.urls')),

]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)