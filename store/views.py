from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404, JsonResponse, FileResponse
from .forms import UserRegister, LibrarianRegister, AdminRegister, AddCategory, BookRegister, LibrarianLogin,\
    BookRegisterByCodeGenerator, AddBook, BookBorrow, ReturnBook, AdminLogin, UserLogin, EditAdminProfile,\
    EditUserProfile, EditLibrarianProfile, ChangePassword, DateSearchEngine, AddLostBook, HumanSearch, BookSearch, \
    BorrowBookSearch, BorrowBookSearchByUser, PrintStatistics, EditBook, CSVFileUpload
from django.contrib import messages
from django.db import IntegrityError
from .models import User, Librarian, Admin, Book, Borrow, LostBook, Category
from datetime import datetime, timedelta
import csv, os
# Create your views here.


def user_register(request):
    librarian_id = request.session.get('librarian_auth')
    if not librarian_id:
        raise Http404("You are not Logged in")
    librarian = Librarian.objects.get(librarian_id=librarian_id)
    if request.method == "POST":
        form = UserRegister(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            date = datetime.now().date()

            if request.FILES.get('photo'):
                post.photo = request.FILES.get('photo')
            post.register_date = date
            post.sex = librarian.sex
            post.password_hint = 'your id number'

            if request.POST.get('status') == 'False':
                hijra = User.objects.filter(user_id__contains='user').values_list('user_id', flat=True).distinct()
                user_id = list(hijra)

                for i in range(1, len(user_id)+2):
                    new_id = 'user/'+str(i)
                    if user_id.count(new_id) == 0:
                        post.user_id = new_id
                        break
                post.year = 0
                post.department = ''
                post.password = post.user_id
                post.save()
                messages.success(request, "The user "+post.name+" was added successfully, and user id is "+new_id)
            else:
                post.password = post.user_id
                post.save()
                messages.success(request, "The user "+post.name+" was added successfully.")
    else:
        form = UserRegister()
    return render(request, 'webpages/user_register.html', {'form': form})


def librarian_register(request):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    admin = Admin.objects.get(admin_id=admin_id)
    if request.method == "POST":
        form = LibrarianRegister(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            date = datetime.now().date()

            if request.FILES.get('photo'):
                post.photo = request.FILES.get('photo')
            post.password_hint = 'your id number'
            post.register_date = date
            post.sex = admin.sex

            if request.POST.get('status') == 'False':
                hijra = Librarian.objects.filter(librarian_id__contains='librarian').values_list('librarian_id',
                                                                                                 flat=True).distinct()
                librarian_id = list(hijra)

                for i in range(1, len(librarian_id)+2):
                    new_id = 'librarian/'+str(i)
                    if librarian_id.count(new_id) == 0:
                        post.librarian_id = new_id
                        break
                post.year = 0
                post.department = ''
                post.password = post.librarian_id
                post.save()
                messages.success(request, "The librarian "+post.name+" was added successfully, and librarian id is "+new_id)
            else:
                post.password = post.librarian_id
                post.save()
                messages.success(request, "The librarian "+post.name+" was added successfully.")

    else:
        form = LibrarianRegister()
    return render(request, 'webpages/librarian_register.html', {'form': form})


def admin_register(request):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    admin = Admin.objects.get(admin_id=admin_id)
    if request.method == "POST":
        form = AdminRegister(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            date = datetime.now().date()

            if request.FILES.get('photo'):
                post.photo = request.FILES.get('photo')
            post.password_hint = 'your id number'
            post.register_date = date
            post.sex = admin.sex

            if request.POST.get('status') == 'False':
                hijra = Admin.objects.filter(admin_id__contains='admin').values_list('admin_id', flat=True).distinct()
                admin_id = list(hijra)

                for i in range(1, len(admin_id)+2):
                    new_id = 'admin/'+str(i)
                    if admin_id.count(new_id) == 0:
                        post.admin_id = new_id
                        break
                post.year = 0
                post.department = ''
                post.password = post.admin_id
                post.save()
                messages.success(request, "The admin "+post.name+" was added successfully, and admin id is "+new_id)
            else:
                post.password = post.admin_id
                post.save()
                messages.success(request, "The admin "+post.name+" was added successfully.")

    else:
        form = AdminRegister()
    return render(request, 'webpages/admin_register.html', {'form': form})


def add_category(request):
    if not request.session.get('admin_auth'):
        raise Http404("You are not Logged in")
    if request.method == "POST":
        form = AddCategory(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "The category "+post.name+" was added successfully.")

    else:
        form = AddCategory()
    return render(request, 'webpages/add_category.html', {'form': form})


def book_register(request):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    if request.method == "POST":
        form = BookRegister(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            date = datetime.now().date()

            if request.FILES.get('image'):
                post.image = request.FILES.get('image')
            post.register_date = date
            specific_codes = set()
            for n in post.specific_code:
                specific_codes.add(n.upper())
            post.specific_code = specific_codes
            post.save()
            messages.success(request, "The book "+post.title+" was added successfully.")
    else:
        form = BookRegister()
    return render(request, 'webpages/book_register.html', {'form': form})


def book_register_by_code_generator(request):
    if not request.session.get('admin_auth'):
        raise Http404("You are not Logged in")
    if request.method == "POST":
        form = BookRegisterByCodeGenerator(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            date = datetime.now().date()

            if request.FILES.get('image'):
                post.image = request.FILES.get('image')
            post.register_date = date

            category = post.category
            genera = Book.objects.filter(category=category).values_list('code', flat=True).distinct()
            code = list(genera)
            if category:
                first = category.range_start
                last = category.range_end + 1
            else:
                first = 10000
                last = 50000

            for i in range(first, last):
                new_code = str(i)
                if code.count(new_code) == 0:
                    post.code = new_code
                    break
            if not post.code:
                messages.warning(request, 'The range for ' + category.name + ' is full , you must create new range')

            specific_code = set()
            display = ''
            for i in range(1, post.amount+1):
                j = i
                temp = ''
                while True:
                    r = int(j % 26)
                    j = int(j / 26)
                    if r == 0:
                        r = r+26
                        j = j-1
                    temp = chr(r+64) + temp
                    if j == 0:
                        break
                specific_code.add(temp)
                display += temp + ','
            post.specific_code = specific_code
            post.save()

            display = display[:-1]
            messages.success(request, "The book was added successfully, and book code is " + new_code +
                             ' and the specific codes are '+display)
    else:
        form = BookRegisterByCodeGenerator()
    return render(request, 'webpages/book_register_by_code_generator.html', {'form': form})


def add_book_by_merge(request):
    if not request.session.get('admin_auth'):
        raise Http404("You are not Logged in")
    if request.method == "POST":
        form = AddBook(request.POST)
        if form.is_valid():

            title = request.POST.get('title')
            author = request.POST.get('author')
            amount = int(request.POST.get('amount'))

            book = Book.objects.get(title=title, author=author)
            specific_code = book.specific_code

            display = ''
            i = 1
            count = 0
            while True:
                j = i
                temp = ''
                while True:
                    r = int(j % 26)
                    j = int(j / 26)
                    if r == 0:
                        r = r+26
                        j = j-1
                    temp = chr(r+64) + temp
                    if j == 0:
                        break
                if not (temp in specific_code):
                    specific_code.add(temp)
                    display += temp + ','
                    count += 1
                i += 1
                if count == amount:
                    break

            book.specific_code = specific_code
            book.amount += amount
            book.save()

            display = display[:-1]
            messages.success(request, "The book was added successfully, and the new specific codes are "+display +
                             ' and the total amount is increased to '+str(book.amount))
    else:
        form = AddBook()
    return render(request, 'webpages/book_merge.html', {'form': form})


def book_borrow(request):
    librarian_id = request.session.get('librarian_auth')
    if not librarian_id:
        raise Http404("You are not Logged in")
    try:
        librarian = Librarian.objects.get(librarian_id=librarian_id)
    except Librarian.DoesNotExist:
        raise Http404("You are not Logged in")
    if request.method == "POST":
        form = BookBorrow(request.POST, sex=librarian.sex)
        if form.is_valid():

            user_id = request.POST.get('user_id')
            code = request.POST.get('code')
            specific_code = request.POST.get('specific_code')
            book = Book.objects.get(code=code)
            user = User.objects.get(user_id=user_id)

            date = datetime.now().date()

            insert = Borrow(user=user, book=book, librarian=librarian, specific_code=specific_code, borrow_date=date)
            insert.save()

            new_specific_code = book.specific_code
            new_specific_code.remove(specific_code)
            new_borrow_code = book.borrow_specific_code
            new_borrow_code.add(specific_code)

            book.specific_code = new_specific_code
            book.borrow_specific_code = new_borrow_code
            book.save()
            messages.success(request, "The book "+book.title+" was borrowed successfully by "+user.name)
            return HttpResponseRedirect('/bookBorrow/')
    else:
        form = BookBorrow(sex=librarian.sex)
    return render(request, 'webpages/book_borrow.html', {'form': form})


def load_specific_code(request):

    code = request.GET.get('code')
    try:
        specific_code = Book.objects.get(code=code).specific_code
    except Book.DoesNotExist:
        specific_code = Book.objects.none()
    specific_code = sorted(specific_code)
    return render(request, 'webpages/specific_code_drop_down_list.html', {'specific_code': specific_code})


def return_book(request):
    librarian_id = request.session.get('librarian_auth')
    if not librarian_id:
        raise Http404("You are not Logged in")
    if request.method == "POST":
        form = ReturnBook(request.POST)
        if form.is_valid():

            # user_id = request.POST.get('user_id')
            borrow_book_id = request.POST.get('book_code')
            borrow_book = Borrow.objects.get(pk=borrow_book_id)
            book = borrow_book.book
            specific_code = borrow_book.specific_code
            librarian = Librarian.objects.get(librarian_id=librarian_id)

            date = datetime.now().date()

            borrow_book.return_date = date
            borrow_book.return_to = librarian
            borrow_book.save()

            new_specific_code = book.specific_code
            new_specific_code.add(specific_code)
            new_borrow_code = book.borrow_specific_code
            new_borrow_code.remove(specific_code)

            book.specific_code = new_specific_code
            book.borrow_specific_code = new_borrow_code
            book.save()

            day_gap = (datetime.now().date() - borrow_book.borrow_date).days
            if book.page <= 100:
                left_date = 7-day_gap
            else:
                left_date = 15-day_gap

            if left_date >= 0:
                messages.success(request, "The book "+book.title+" was returned successfully. and "+str(left_date) +
                                 " days left.")
            else:
                messages.success(request, "The book " + book.title + " was returned successfully. and " +
                                 str(abs(left_date)) + " days passed.")
            return HttpResponseRedirect('/returnBook/')
    else:
        form = ReturnBook()
    return render(request, 'webpages/book_return.html', {'form': form})


def load_borrow_book(request):
    user_id = request.GET.get('user')
    librarian_id = request.session.get('librarian_auth')
    try:
        librarian = Librarian.objects.get(librarian_id=librarian_id)
    except Librarian.DoesNotExist:
        raise Http404("You are not Logged in")
    try:
        user = User.objects.get(user_id=user_id, sex=librarian.sex)
        book = Borrow.objects.filter(user=user, return_date=None)
        book = sorted(book, key=lambda x: x.borrow_date, reverse=False)
    except User.DoesNotExist:
        book = Book.objects.none()
    return render(request, 'webpages/borrow_book_list_drop_down.html', {'book': book})


def logout(request, role):
    if role == 'librarian':
        request.session['librarian_auth'] = None
        return redirect('/librarianLogin/')
    elif role == 'admin':
        request.session['admin_auth'] = None
        return redirect('/adminLogin/')
    elif role == 'user':
        request.session['user_auth'] = None
        return redirect('/userLogin/')
    else:
        pass


def librarian_login(request):
    if request.method == "POST":
        form = LibrarianLogin(request.POST)
        if form.is_valid():
            librarian_id = request.POST.get('librarian_id')
            try:
                Librarian.objects.get(librarian_id=librarian_id)
                request.session['librarian_auth'] = librarian_id
                return redirect('/librarian-homepage/')
            except Librarian.DoesNotExist:
                raise Http404("Librarian does not exist")

    else:
        form = LibrarianLogin()
    return render(request, 'webpages/librarian_login.html', {'form': form})


def admin_login(request):
    if request.method == "POST":
        form = AdminLogin(request.POST)
        if form.is_valid():
            admin_id = request.POST.get('admin_id')
            try:
                Admin.objects.get(admin_id=admin_id)
                request.session['admin_auth'] = admin_id
                return redirect('/admin-homepage/')
            except Admin.DoesNotExist:
                raise Http404("Admin does not exist")

    else:
        form = AdminLogin()
    return render(request, 'webpages/admin_login.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            try:
                User.objects.get(user_id=user_id)
                request.session['user_auth'] = user_id
                return redirect('/user-homepage/')
            except User.DoesNotExist:
                raise Http404("User does not exist")

    else:
        form = UserLogin()
    return render(request, 'webpages/user_login.html', {'form': form})


def librarian_homepage(request):
    if request.session.get('librarian_auth'):
        return render(request, 'webpages/homepage.html', {'role': 'librarian'})
    else:
        raise Http404("You are not Logged in")


def admin_homepage(request):
    if request.session.get('admin_auth'):
        return render(request, 'webpages/homepage.html', {'role': 'admin'})
    else:
        raise Http404("You are not Logged in")


def user_homepage(request):
    if request.session.get('user_auth'):
        return render(request, 'webpages/homepage.html', {'role': 'user'})
    else:
        raise Http404("You are not Logged in")


def view_admin_profile(request):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    if request.method == "POST":
        form = EditAdminProfile(request.POST, request.FILES, key=admin_id)
        if form.is_valid():
            admin = Admin.objects.get(admin_id=admin_id)
            admin.admin_id = request.POST.get('admin_id')
            admin.name = request.POST.get('name')
            admin.middle_name = request.POST.get('middle_name')
            admin.last_name = request.POST.get('last_name')
            admin.phone = request.POST.get('phone')
            admin.email = request.POST.get('email')
            admin.year = request.POST.get('year')
            admin.department = request.POST.get('department')
            if request.FILES.get('photo'):
                admin.photo = request.FILES.get('photo')
            admin.save()

            request.session['admin_auth'] = request.POST.get('admin_id')
            messages.success(request, "The admin "+admin.name+" was update successfully.")
            return redirect('/viewAdminProfile/')

    else:
        form = EditAdminProfile(key=admin_id)
    return render(request, 'webpages/admin_profile.html', {'form': form})


def view_librarian_profile(request):
    librarian_id = request.session.get('librarian_auth')
    if not librarian_id:
        raise Http404("You are not Logged in")
    if request.method == "POST":
        form = EditLibrarianProfile(request.POST, request.FILES, key=librarian_id)
        if form.is_valid():
            librarian = Librarian.objects.get(librarian_id=librarian_id)
            librarian.librarian_id = request.POST.get('librarian_id')
            librarian.name = request.POST.get('name')
            librarian.middle_name = request.POST.get('middle_name')
            librarian.last_name = request.POST.get('last_name')
            librarian.phone = request.POST.get('phone')
            librarian.email = request.POST.get('email')
            librarian.year = request.POST.get('year')
            librarian.department = request.POST.get('department')
            if request.FILES.get('photo'):
                librarian.photo = request.FILES.get('photo')
            librarian.save()

            request.session['librarian_auth'] = request.POST.get('librarian_id')
            messages.success(request, "The librarian "+librarian.name+" was update successfully.")
            return redirect('/viewLibrarianProfile/')

    else:
        form = EditLibrarianProfile(key=librarian_id)
    return render(request, 'webpages/librarian_profile.html', {'form': form})


def view_user_profile(request):
    user_id = request.session.get('user_auth')
    if not user_id:
        raise Http404("You are not Logged in")
    if request.method == "POST":
        form = EditUserProfile(request.POST, request.FILES, key=user_id)
        if form.is_valid():
            user = User.objects.get(user_id=user_id)
            user.user_id = request.POST.get('user_id')
            user.name = request.POST.get('name')
            user.middle_name = request.POST.get('middle_name')
            user.last_name = request.POST.get('last_name')
            user.phone = request.POST.get('phone')
            user.email = request.POST.get('email')
            user.year = request.POST.get('year')
            user.department = request.POST.get('department')
            if request.FILES.get('photo'):
                user.photo = request.FILES.get('photo')
            user.save()

            request.session['user_auth'] = request.POST.get('user_id')

            messages.success(request, "The user "+user.name+" was update successfully.")
            return redirect('/viewUserProfile/')

    else:
        form = EditUserProfile(key=user_id)
    return render(request, 'webpages/user_profile.html', {'form': form})


def change_password(request, role):
    if role == 'user':
        user_id = request.session.get('user_auth')
        if user_id:
            user = User.objects.get(user_id=user_id)
            if request.method == "POST":
                form = ChangePassword(request.POST, key=user.password, hint=user.password_hint)
                if form.is_valid():
                    user.password = request.POST.get('new_password')
                    user.password_hint = request.POST.get('password_hint')
                    user.save()
                    messages.success(request, "The password was changed successfully.")
                    return HttpResponseRedirect('/viewUserProfile/')

            else:
                form = ChangePassword(key=user.password, hint=user.password_hint)
        else:
            raise Http404("You are not logged in")

    elif role == 'librarian':
        librarian_id = request.session.get('librarian_auth')
        if librarian_id:
            librarian = Librarian.objects.get(librarian_id=librarian_id)
            if request.method == "POST":
                form = ChangePassword(request.POST, key=librarian.password, hint=librarian.password_hint)
                if form.is_valid():
                    librarian.password = request.POST.get('new_password')
                    librarian.password_hint = request.POST.get('password_hint')
                    librarian.save()
                    messages.success(request, "The password was changed successfully.")
                    return HttpResponseRedirect('/viewLibrarianProfile/')
            else:
                form = ChangePassword(key=librarian.password, hint=librarian.password_hint)
        else:
            raise Http404("You are not logged in")

    elif role == 'admin':
        admin_id = request.session.get('admin_auth')
        if admin_id:
            admin = Admin.objects.get(admin_id=admin_id)
            if request.method == "POST":
                form = ChangePassword(request.POST, key=admin.password, hint=admin.password_hint)
                if form.is_valid():
                    admin.password = request.POST.get('new_password')
                    admin.password_hint = request.POST.get('password_hint')
                    admin.save()
                    messages.success(request, "The password was changed successfully.")

                    return HttpResponseRedirect('/viewAdminProfile/')
            else:
                form = ChangePassword(key=admin.password, hint=admin.password_hint)
        else:
            raise Http404("You are not logged in")
    else:
        raise Http404("You are not logged in")

    return render(request, 'webpages/change_password.html', {'form': form})


def not_delete(request, page):
    if page == 'librarian_delete':
        return redirect('/view-librarian-by-admin/')
    elif page == 'admin_delete':
        return redirect('/admin-list/')
    elif page == 'user_delete':
        return redirect('/user-view-by-librarian/')
    elif page == 'book_delete':
        return HttpResponseRedirect('/book-view-by-admin/')
    elif page == 'lost_book':
        return HttpResponseRedirect('/view-lost-books/')
    elif page == 'borrow_delete':
        return HttpResponseRedirect('/view-book-borrow-by-librarian/')


def delete_librarian_confirm(request, librarian_id):
    if request.session.get('admin_auth'):
        librarian = Librarian.objects.get(pk=librarian_id)
        return render(request, 'webpages/delete_librarian_confirmation.html', {'librarian': librarian})

    else:
        raise Http404("You are not logged in")


def librarian_view_by_admin(request):
    if request.session.get('admin_auth'):
        admin_id = request.session.get('admin_auth')
        admin = Admin.objects.get(admin_id=admin_id)

        if request.method == "POST":
            form = HumanSearch(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')

            if catalog == 'name':
                male_librarian = Librarian.objects.filter(sex='male', name__contains=text) | \
                                 Librarian.objects.filter(sex='male', middle_name__contains=text) | \
                                 Librarian.objects.filter(sex='male', last_name__contains=text)
                female_librarian = Librarian.objects.filter(sex='female', name__contains=text) | \
                                   Librarian.objects.filter(sex='female', middle_name__contains=text) | \
                                   Librarian.objects.filter(sex='female', last_name__contains=text)
            elif catalog == 'id':
                male_librarian = Librarian.objects.filter(sex='male', librarian_id__contains=text)
                female_librarian = Librarian.objects.filter(sex='female', librarian_id__contains=text)
            elif catalog == 'department':
                male_librarian = Librarian.objects.filter(sex='male', department__contains=text)
                female_librarian = Librarian.objects.filter(sex='female', department__contains=text)
            elif catalog == 'phone':
                male_librarian = Librarian.objects.filter(sex='male', phone__contains=text)
                female_librarian = Librarian.objects.filter(sex='female', phone__contains=text)
            else:
                try:
                    year = int(text)
                    male_librarian = Librarian.objects.filter(sex='male', year=year)
                    female_librarian = Librarian.objects.filter(sex='female', year=year)
                except ValueError:
                    male_librarian = Librarian.objects.none()
                    female_librarian = Librarian.objects.none()

        else:
            form = HumanSearch()
            male_librarian = Librarian.objects.filter(sex='male')
            female_librarian = Librarian.objects.filter(sex='female')

        male_librarian = sorted(male_librarian, key=lambda x: x.name, reverse=False)
        female_librarian = sorted(female_librarian, key=lambda x: x.name, reverse=False)

        for i in male_librarian:
            i.image = "Images/" + str(i.photo)
        for i in female_librarian:
            i.image = "Images/" + str(i.photo)

        if admin.sex == 'male':
            return render(request, 'webpages/librarian_view_by_male_admin.html',
                          {'form': form, 'male_librarian': male_librarian, 'female_librarian': female_librarian})
        elif admin.sex == 'female':
            return render(request, 'webpages/librarian_view_by_female_admin.html',
                          {'form': form, 'male_librarian': male_librarian, 'female_librarian': female_librarian})
        else:
            raise Http404("Please check your profile sex is empty")


def delete_librarian(request, librarian_id):
    if request.session.get('admin_auth'):
        try:
            librarian = Librarian.objects.get(pk=librarian_id)
            return_to = Borrow.objects.filter(return_to=librarian)
            borrow = Borrow.objects.filter(librarian=librarian)
            for i in borrow:
                i.librarian = None
                i.save()
            for i in return_to:
                i.return_to = None
                i.save()
            librarian.delete()
            messages.success(request, "The librarian " + librarian.name + " was deleted successfully.")
            return redirect('/view-librarian-by-admin/')
        except Librarian.DoesNotExist:
            raise Http404("This Librarian is not registered")
    else:
        raise Http404("You are not logged in")


def admin_list(request):
    if request.session.get('admin_auth'):
        admin_id = request.session.get('admin_auth')
        active_admin = Admin.objects.get(admin_id=admin_id)

        if request.method == "POST":
            form = HumanSearch(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')

            if catalog == 'name':
                male_admin = Admin.objects.filter(sex='male', name__contains=text).exclude(admin_id=admin_id) | \
                             Admin.objects.filter(sex='male', middle_name__contains=text).exclude(admin_id=admin_id) | \
                             Admin.objects.filter(sex='male', last_name__contains=text).exclude(admin_id=admin_id)
                female_admin = Admin.objects.filter(sex='female', name__contains=text).exclude(admin_id=admin_id) | \
                               Admin.objects.filter(sex='female',
                                                    middle_name__contains=text).exclude(admin_id=admin_id) | \
                               Admin.objects.filter(sex='female', last_name__contains=text).exclude(admin_id=admin_id)
            elif catalog == 'id':
                male_admin = Admin.objects.filter(sex='male', admin_id__contains=text).exclude(admin_id=admin_id)
                female_admin = Admin.objects.filter(sex='female', admin_id__contains=text).exclude(admin_id=admin_id)
            elif catalog == 'department':
                male_admin = Admin.objects.filter(sex='male', department__contains=text).exclude(admin_id=admin_id)
                female_admin = Admin.objects.filter(sex='female', department__contains=text).exclude(admin_id=admin_id)
            elif catalog == 'phone':
                male_admin = Admin.objects.filter(sex='male', phone__contains=text).exclude(admin_id=admin_id)
                female_admin = Admin.objects.filter(sex='female', phone__contains=text).exclude(admin_id=admin_id)
            else:
                try:
                    year = int(text)
                    male_admin = Admin.objects.filter(sex='male', year=year).exclude(admin_id=admin_id)
                    female_admin = Admin.objects.filter(sex='female', year=year).exclude(admin_id=admin_id)
                except ValueError:
                    male_admin = Admin.objects.none()
                    female_admin = Admin.objects.none()
        else:
            form = HumanSearch()
            male_admin = Admin.objects.filter(sex='male').exclude(admin_id=admin_id)
            female_admin = Admin.objects.filter(sex='female').exclude(admin_id=admin_id)

        male_admin = sorted(male_admin, key=lambda x: x.name, reverse=False)
        female_admin = sorted(female_admin, key=lambda x: x.name, reverse=False)
        for i in male_admin:
            i.image = "Images/" + str(i.photo)
        for i in female_admin:
            i.image = "Images/" + str(i.photo)
        if active_admin.sex == 'male':
            return render(request, 'webpages/admin_view_by_male_admin.html',
                          {'form': form, 'male_admin': male_admin, 'female_admin': female_admin})
        elif active_admin.sex == 'female':
            return render(request, 'webpages/admin_view_by_female_admin.html',
                          {'form': form, 'male_admin': male_admin, 'female_admin': female_admin})
        else:
            raise Http404("Please check your profile sex is empty")


def delete_admin_confirm(request, admin_id):
    if request.session.get('admin_auth'):
        admin = Admin.objects.get(pk=admin_id)
        return render(request, 'webpages/delete_admin_confirmation.html', {'admin': admin})

    else:
        raise Http404("You are not logged in")


def delete_admin(request, admin_id):
    if request.session.get('admin_auth'):
        try:
            admin = Admin.objects.get(pk=admin_id)

            admin.delete()
            messages.success(request, "The admin " + admin.name + " was deleted successfully.")
            return redirect('/admin-list/')
        except Admin.DoesNotExist:
            raise Http404("This admin is not registered")
    else:
        raise Http404("You are not logged in")


def librarian_view_by_librarian(request):
    if request.session.get('librarian_auth'):
        librarian_id = request.session.get('librarian_auth')
        active_librarian = Librarian.objects.get(librarian_id=librarian_id)

        if not active_librarian.sex:
            raise Http404("Please check your profile sex is empty")
        if request.method == "POST":
            form = HumanSearch(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')

            if catalog == 'name':
                librarian = Librarian.objects.filter(sex=active_librarian.sex, name__contains=text) | \
                            Librarian.objects.filter(sex=active_librarian.sex, middle_name__contains=text) | \
                            Librarian.objects.filter(sex=active_librarian.sex, last_name__contains=text)
            elif catalog == 'id':
                librarian = Librarian.objects.filter(sex=active_librarian.sex, librarian_id__contains=text)
            elif catalog == 'department':
                librarian = Librarian.objects.filter(sex=active_librarian.sex, department__contains=text)
            elif catalog == 'phone':
                librarian = Librarian.objects.filter(sex=active_librarian.sex, phone__contains=text)
            else:
                try:
                    year = int(text)
                    librarian = Librarian.objects.filter(sex=active_librarian.sex, year=year)
                except ValueError:
                    librarian = Librarian.objects.none()

        else:
            form = HumanSearch()
            librarian = Librarian.objects.filter(sex=active_librarian.sex)
        librarian = sorted(librarian, key=lambda x: x.name, reverse=False)
        for i in librarian:
            i.image = "Images/" + str(i.photo)
        return render(request, 'webpages/librarian_view_by_librarian.html', {'form': form, 'librarian': librarian})


def user_view_by_librarian(request):
    if request.session.get('librarian_auth'):
        librarian_id = request.session.get('librarian_auth')
        librarian = Librarian.objects.get(librarian_id=librarian_id)

        if not librarian.sex:
            raise Http404("Please check your profile sex is empty")
        if request.method == "POST":
            form = HumanSearch(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')

            if catalog == 'name':
                user = User.objects.filter(sex=librarian.sex, name__contains=text) | \
                       User.objects.filter(sex=librarian.sex, middle_name__contains=text) | \
                       User.objects.filter(sex=librarian.sex, last_name__contains=text)
            elif catalog == 'id':
                user = User.objects.filter(sex=librarian.sex, user_id__contains=text)
            elif catalog == 'department':
                user = User.objects.filter(sex=librarian.sex, department__contains=text)
            elif catalog == 'phone':
                user = User.objects.filter(sex=librarian.sex, phone__contains=text)
            else:
                try:
                    year = int(text)
                    user = User.objects.filter(sex=librarian.sex, year=year)
                except ValueError:
                    user = User.objects.none()

        else:
            form = HumanSearch()
            user = User.objects.filter(sex=librarian.sex)

        user = sorted(user, key=lambda x: x.name, reverse=False)

        for i in user:
            i.image = "Images/" + str(i.photo)
        return render(request, 'webpages/user_view_by_librarian.html', {'form': form, 'user': user})

    else:
        raise Http404("You are not logged in")


def delete_user_confirm(request, user_id):
    if request.session.get('librarian_auth'):
        user = User.objects.get(pk=user_id)
        borrow = Borrow.objects.filter(user=user, return_date=None).order_by('borrow_date')

        return render(request, 'webpages/delete_user_confirmation.html', {'user': user, 'borrow': borrow})

    else:
        raise Http404("You are not logged in")


def delete_user(request, user_id):
    if request.session.get('librarian_auth'):
        try:
            user = User.objects.get(pk=user_id)

            user.delete()
            messages.success(request, "The user " + user.name + " was deleted successfully.")
            return redirect('/user-view-by-librarian/')
        except User.DoesNotExist:
            raise Http404("This user is not registered")
    else:
        raise Http404("You are not logged in")


def book_view_by_librarian(request):
    if request.session.get('librarian_auth'):
        if request.method == "POST":
            form = BookSearch(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')
            if catalog == 'code':
                book = Book.objects.filter(code__contains=text)
            elif catalog == 'title':
                book = Book.objects.filter(title__contains=text)
            elif catalog == 'author':
                book = Book.objects.filter(author__contains=text)
            elif catalog == 'category':
                book = Book.objects.filter(category__name__contains=text)
            else:
                try:
                    year = int(text)
                    book = Book.objects.filter(pub_year__contains=year)
                except ValueError:
                    book = Book.objects.none()
        else:
            form = BookSearch()
            book = Book.objects.all()
        try:
            book = sorted(book, key=lambda x: int(x.code), reverse=False)
        except ValueError:
            book = sorted(book, key=lambda x: x.code, reverse=False)

        for i in book:
            i.photo = "Images/" + str(i.image)
            i.current_amount = len(i.specific_code)

            current = list(i.specific_code)
            current.sort()
            i.current_specific_codes = ','.join(current)
            if len(i.current_specific_codes) == 0:
                i.current_specific_codes = '-'
            elif len(i.current_specific_codes) > 40:
                new = ''
                last = 40
                while last < len(i.current_specific_codes):
                    new += i.current_specific_codes[last-40:last]+'\n'
                    last += 40
                new += i.current_specific_codes[last-40:]+'\n'
                i.current_specific_codes = new

            borrow = list(i.borrow_specific_code)
            borrow.sort()
            i.current_borrow_specific_codes = ','.join(borrow)
            if i.current_borrow_specific_codes == '':
                i.current_borrow_specific_codes = '-'
            elif len(i.current_borrow_specific_codes) > 40:
                new = ''
                last = 40
                while last < len(i.current_borrow_specific_codes):
                    new += i.current_borrow_specific_codes[last-40:last]+'\n'
                    last += 40
                new += i.current_borrow_specific_codes[last-40:]+'\n'
                i.current_borrow_specific_codes = new

            total = current
            total.extend(borrow)
            total.sort()
            i.total_specific_codes = ','.join(total)
            if i.total_specific_codes == '':
                i.total_specific_codes = '-'
            elif len(i.total_specific_codes) > 40:
                new = ''
                last = 40
                while last < len(i.total_specific_codes):
                    new += i.total_specific_codes[last-40:last]+'\n'
                    last += 40
                new += i.total_specific_codes[last-40:]+'\n'
                i.total_specific_codes = new

        return render(request, 'webpages/book_view_by_librarian.html', {'form': form, 'book': book})

    else:
        raise Http404("You are not logged in")


def view_book_history_by_librarian(request, book_id):
    if request.session.get('librarian_auth'):
        try:
            librarian = Librarian.objects.get(librarian_id=request.session.get('librarian_auth'))
            book = Book.objects.get(pk=book_id)
            borrow = Borrow.objects.filter(book=book).order_by('borrow_date')
            for i in borrow:
                i.user.image = "Images/" + str(i.user.photo)
                if i.librarian:
                    i.librarian.image = "Images/" + str(i.librarian.photo)
                if i.return_to:
                    i.return_to.image = "Images/" + str(i.return_to.photo)

            return render(request, 'webpages/view_book_history_by_librarian.html',
                          {'borrow': borrow, 'title': book.title, 'code': book.code, 'sex': librarian.sex})
        except Book.DoesNotExist:
            raise Http404("This book is not registered")
    else:
        raise Http404("You are not logged in")


def book_view_by_admin(request):
    if request.session.get('admin_auth'):
        if request.method == "POST":
            form = BookSearch(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')
            if catalog == 'code':
                book = Book.objects.filter(code__contains=text)
            elif catalog == 'title':
                book = Book.objects.filter(title__contains=text)
            elif catalog == 'author':
                book = Book.objects.filter(author__contains=text)
            elif catalog == 'category':
                book = Book.objects.filter(category__name__contains=text)
            else:
                try:
                    year = int(text)
                    book = Book.objects.filter(pub_year__contains=year)
                except ValueError:
                    book = Book.objects.none()
        else:
            form = BookSearch()
            book = Book.objects.all()
        try:
            book = sorted(book, key=lambda x: int(x.code), reverse=False)
        except ValueError:
            book = sorted(book, key=lambda x: x.code, reverse=False)

        for i in book:
            i.photo = "Images/" + str(i.image)
            i.current_amount = len(i.specific_code)

            current = list(i.specific_code)
            current.sort()
            i.current_specific_codes = ','.join(current)
            if len(i.current_specific_codes) == 0:
                i.current_specific_codes = '-'
            elif len(i.current_specific_codes) > 40:
                new = ''
                last = 40
                while last < len(i.current_specific_codes):
                    new += i.current_specific_codes[last-40:last]+'\n'
                    last += 40
                new += i.current_specific_codes[last-40:]+'\n'
                i.current_specific_codes = new

            borrow = list(i.borrow_specific_code)
            borrow.sort()
            i.current_borrow_specific_codes = ','.join(borrow)
            if i.current_borrow_specific_codes == '':
                i.current_borrow_specific_codes = '-'
            elif len(i.current_borrow_specific_codes) > 40:
                new = ''
                last = 40
                while last < len(i.current_borrow_specific_codes):
                    new += i.current_borrow_specific_codes[last-40:last]+'\n'
                    last += 40
                new += i.current_borrow_specific_codes[last-40:]+'\n'
                i.current_borrow_specific_codes = new

            total = current
            total.extend(borrow)
            total.sort()
            i.total_specific_codes = ','.join(total)
            if i.total_specific_codes == '':
                i.total_specific_codes = '-'
            elif len(i.total_specific_codes) > 40:
                new = ''
                last = 40
                while last < len(i.total_specific_codes):
                    new += i.total_specific_codes[last-40:last]+'\n'
                    last += 40
                new += i.total_specific_codes[last-40:]+'\n'
                i.total_specific_codes = new

        return render(request, 'webpages/book_view_by_admin.html', {'form': form, 'book': book})

    else:
        raise Http404("You are not logged in")


def view_book_history_by_admin(request, book_id):
    if request.session.get('admin_auth'):
        try:
            admin = Admin.objects.get(admin_id=request.session.get('admin_auth'))
            book = Book.objects.get(pk=book_id)
            borrow = Borrow.objects.filter(book=book).order_by('borrow_date')
            for i in borrow:
                i.user.image = "Images/" + str(i.user.photo)
                if i.librarian:
                    i.librarian.image = "Images/" + str(i.librarian.photo)
                if i.return_to:
                    i.return_to.image = "Images/" + str(i.return_to.photo)

            return render(request, 'webpages/view_book_history_by_admin.html',
                          {'borrow': borrow, 'title': book.title, 'code': book.code, 'sex': admin.sex})
        except Book.DoesNotExist:
            raise Http404("This book is not registered")
    else:
        raise Http404("You are not logged in")


def delete_book_confirm(request, book_id):
    if request.session.get('admin_auth'):
        book = Book.objects.get(pk=book_id)
        borrow = Borrow.objects.filter(book=book, return_date=None).order_by('borrow_date')
        return render(request, 'webpages/delete_book_confirmation.html', {'book': book, 'borrow': borrow})

    else:
        raise Http404("You are not logged in")


def delete_book(request, book_id):
    if request.session.get('admin_auth'):
        try:
            book = Book.objects.get(pk=book_id)

            book.delete()
            messages.success(request, "The book " + book.title + " was deleted successfully.")
            return redirect('/book-view-by-admin/')
        except Book.DoesNotExist:
            raise Http404("This book is not registered")
    else:
        raise Http404("You are not logged in")


def view_user_history_by_librarian(request, user_id):
    if request.session.get('librarian_auth'):
        try:
            user = User.objects.get(pk=user_id)
            borrow = Borrow.objects.filter(user=user).order_by('borrow_date')
            for i in borrow:
                i.book.photo = "Images/" + str(i.book.image)
                if i.librarian:
                    i.librarian.image = "Images/" + str(i.librarian.photo)
                if i.return_to:
                    i.return_to.image = "Images/" + str(i.return_to.photo)

            return render(request, 'webpages/view_user_history_by_librarian.html',
                          {'borrow': borrow, 'name': user.name+' '+user.middle_name, 'user_id': user.user_id, })
        except User.DoesNotExist:
            raise Http404("This user is not registered")
    else:
        raise Http404("You are not logged in")


def view_borrow_history_by_user(request):
    user_id = request.session.get('user_auth')
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise Http404("This user is not registered")
        if request.method == "POST":
            form = DateSearchEngine(request.POST)
            if form.is_valid():

                date = request.POST.get('search_date')
                borrow = Borrow.objects.filter(user=user, borrow_date=date)
                for i in borrow:
                    i.book.photo = "Images/" + str(i.book.image)
                    if i.librarian:
                        i.librarian.image = "Images/" + str(i.librarian.photo)
                    if i.return_to:
                        i.return_to.image = "Images/" + str(i.return_to.photo)

                return render(request, 'webpages/view_borrow_history_by_user.html',
                              {'form': form, 'borrow': borrow, 'date': date})
            return render(request, 'webpages/view_borrow_history_by_user.html', {'form': form, 'date': None})

        else:
            form = DateSearchEngine()
            borrow = Borrow.objects.filter(user=user).order_by('borrow_date').reverse()
            for i in borrow:
                i.book.photo = "Images/" + str(i.book.image)
                if i.librarian:
                    i.librarian.image = "Images/" + str(i.librarian.photo)
                if i.return_to:
                    i.return_to.image = "Images/" + str(i.return_to.photo)
            return render(request, 'webpages/view_borrow_history_by_user.html',
                          {'form': form, 'borrow': borrow, 'date': 'All time'})

    else:
        raise Http404("You are not logged in")


def view_return_history_by_user(request):
    user_id = request.session.get('user_auth')
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise Http404("This user is not registered")
        if request.method == "POST":
            form = DateSearchEngine(request.POST)
            if form.is_valid():

                date = request.POST.get('search_date')
                borrow = Borrow.objects.filter(user=user, return_date=date).order_by('borrow_date')
                for i in borrow:
                    i.book.photo = "Images/" + str(i.book.image)
                    if i.librarian:
                        i.librarian.image = "Images/" + str(i.librarian.photo)
                    if i.return_to:
                        i.return_to.image = "Images/" + str(i.return_to.photo)

                return render(request, 'webpages/view_return_history_by_user.html',
                              {'form': form, 'borrow': borrow, 'date': date})
            return render(request, 'webpages/view_return_history_by_user.html', {'form': form, 'date': None})

        else:
            form = DateSearchEngine()
            borrow = Borrow.objects.filter(user=user).exclude(return_date=None).order_by('borrow_date').reverse()
            for i in borrow:
                i.book.photo = "Images/" + str(i.book.image)
                if i.librarian:
                    i.librarian.image = "Images/" + str(i.librarian.photo)
                if i.return_to:
                    i.return_to.image = "Images/" + str(i.return_to.photo)
            return render(request, 'webpages/view_return_history_by_user.html',
                          {'form': form, 'borrow': borrow, 'date': 'All time'})

    else:
        raise Http404("You are not logged in")


def book_view_by_user(request):
    if request.session.get('user_auth'):
        if request.method == "POST":
            form = BookSearch(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')
            if catalog == 'code':
                book = Book.objects.filter(code__contains=text)
            elif catalog == 'title':
                book = Book.objects.filter(title__contains=text)
            elif catalog == 'author':
                book = Book.objects.filter(author__contains=text)
            elif catalog == 'category':
                book = Book.objects.filter(category__name__contains=text)
            else:
                try:
                    year = int(text)
                    book = Book.objects.filter(pub_year__contains=year)
                except ValueError:
                    book = Book.objects.none()
        else:
            form = BookSearch()
            book = Book.objects.all()
        book = sorted(book, key=lambda x: x.code, reverse=False)
        for i in book:
            i.photo = "Images/" + str(i.image)
            i.current_amount = len(i.specific_code)

        return render(request, 'webpages/book_view_by_user.html', {'form': form, 'book': book})

    else:
        raise Http404("You are not logged in")


def view_book_borrow_by_admin(request):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    admin = Admin.objects.get(admin_id=admin_id)
    if request.method == "POST":
        form = DateSearchEngine(request.POST)
        if form.is_valid():
            date = request.POST.get('search_date')
            borrow = Borrow.objects.filter(borrow_date=date)
            for i in borrow:
                i.book.photo = "Images/" + str(i.book.image)
                i.user.image = "Images/" + str(i.user.photo)
                if i.librarian:
                    i.librarian.image = "Images/" + str(i.librarian.photo)
                if i.return_to:
                    i.return_to.image = "Images/" + str(i.return_to.photo)
            return render(request, 'webpages/view_book_borrow_by_admin.html',
                          {'form': form, 'borrow': borrow, 'date': date, 'sex': admin.sex})

        return render(request, 'webpages/view_book_borrow_by_admin.html', {'form': form, 'date': None})

    else:
        form = DateSearchEngine()
        borrow = Borrow.objects.all().order_by('borrow_date').reverse()
        for i in borrow:
            i.book.photo = "Images/" + str(i.book.image)
            i.user.image = "Images/" + str(i.user.photo)
            if i.librarian:
                i.librarian.image = "Images/" + str(i.librarian.photo)
            if i.return_to:
                i.return_to.image = "Images/" + str(i.return_to.photo)

        return render(request, 'webpages/view_book_borrow_by_admin.html',
                      {'form': form, 'borrow': borrow, 'date': 'All time', 'sex': admin.sex})


def view_book_return_by_admin(request):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    admin = Admin.objects.get(admin_id=admin_id)
    if request.method == "POST":
        form = DateSearchEngine(request.POST)
        if form.is_valid():
            date = request.POST.get('search_date')
            borrow = Borrow.objects.filter(return_date=date)
            for i in borrow:
                i.book.photo = "Images/" + str(i.book.image)
                i.user.image = "Images/" + str(i.user.photo)
                if i.librarian:
                    i.librarian.image = "Images/" + str(i.librarian.photo)
                if i.return_to:
                    i.return_to.image = "Images/" + str(i.return_to.photo)
            return render(request, 'webpages/view_book_return_by_admin.html',
                          {'form': form, 'borrow': borrow, 'date': date, 'sex': admin.sex})

        return render(request, 'webpages/view_book_return_by_admin.html', {'form': form, 'date': None})

    else:
        form = DateSearchEngine()
        borrow = Borrow.objects.all().exclude(return_date=None).order_by('return_date').reverse()
        for i in borrow:
            i.book.photo = "Images/" + str(i.book.image)
            i.user.image = "Images/" + str(i.user.photo)
            if i.librarian:
                i.librarian.image = "Images/" + str(i.librarian.photo)
            if i.return_to:
                i.return_to.image = "Images/" + str(i.return_to.photo)

        return render(request, 'webpages/view_book_return_by_admin.html',
                      {'form': form, 'borrow': borrow, 'date': 'All time', 'sex': admin.sex})


def view_book_borrow_by_librarian(request):
    librarian_id = request.session.get('librarian_auth')
    if not librarian_id:
        raise Http404("You are not Logged in")
    librarian = Librarian.objects.get(librarian_id=librarian_id)
    if request.method == "POST":
        form = DateSearchEngine(request.POST)
        if form.is_valid():
            date = request.POST.get('search_date')
            borrow = Borrow.objects.filter(borrow_date=date, librarian=librarian)
            for i in borrow:
                i.book.photo = "Images/" + str(i.book.image)
                i.user.image = "Images/" + str(i.user.photo)
                if i.return_to:
                    i.return_to.image = "Images/" + str(i.return_to.photo)
                    i.delete_borrow = 'false'
                elif i.borrow_date == datetime.now().date():
                    i.delete_borrow = 'true'
                else:
                    i.delete_borrow = 'false'
            return render(request, 'webpages/view_book_borrow_by_librarian.html',
                          {'form': form, 'borrow': borrow, 'date': date})

        return render(request, 'webpages/view_book_borrow_by_librarian.html', {'form': form, 'date': None})

    else:
        form = DateSearchEngine()
        borrow = Borrow.objects.filter(librarian=librarian).order_by('borrow_date').reverse()
        for i in borrow:
            i.book.photo = "Images/" + str(i.book.image)
            i.user.image = "Images/" + str(i.user.photo)
            if i.return_to:
                i.return_to.image = "Images/" + str(i.return_to.photo)
                i.delete_borrow = 'false'
            elif i.borrow_date == datetime.now().date():
                i.delete_borrow = 'true'
            else:
                i.delete_borrow = 'false'

        return render(request, 'webpages/view_book_borrow_by_librarian.html',
                      {'form': form, 'borrow': borrow, 'date': 'All time'})


def view_book_return_by_librarian(request):
    librarian_id = request.session.get('librarian_auth')
    if not librarian_id:
        raise Http404("You are not Logged in")
    librarian = Librarian.objects.get(librarian_id=librarian_id)
    if request.method == "POST":
        form = DateSearchEngine(request.POST)
        if form.is_valid():
            date = request.POST.get('search_date')
            borrow = Borrow.objects.filter(return_date=date, return_to=librarian)
            for i in borrow:
                i.book.photo = "Images/" + str(i.book.image)
                i.user.image = "Images/" + str(i.user.photo)
                if i.librarian:
                    i.librarian.image = "Images/" + str(i.librarian.photo)
            return render(request, 'webpages/view_book_return_by_librarian.html',
                          {'form': form, 'borrow': borrow, 'date': date})

        return render(request, 'webpages/view_book_return_by_librarian.html', {'form': form, 'date': None})

    else:
        form = DateSearchEngine()
        borrow = Borrow.objects.filter(return_to=librarian).exclude(return_date=None).\
            order_by('return_date').reverse()
        for i in borrow:
            i.book.photo = "Images/" + str(i.book.image)
            i.user.image = "Images/" + str(i.user.photo)
            if i.librarian:
                i.librarian.image = "Images/" + str(i.librarian.photo)

        return render(request, 'webpages/view_book_return_by_librarian.html',
                      {'form': form, 'borrow': borrow, 'date': 'All time'})


def view_unreturn_book_by_user(request):
    user_id = request.session.get('user_auth')
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise Http404("This user is not registered")
        if request.method == "POST":
            form = BorrowBookSearchByUser(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')

            if catalog == 'code':
                borrow = Borrow.objects.filter(user=user, book__code__contains=text, return_date=None)
            else:
                borrow = Borrow.objects.filter(user=user, book__title__contains=text, return_date=None)

        else:
            form = BorrowBookSearchByUser()
            borrow = Borrow.objects.filter(user=user, return_date=None)
        for i in borrow:
            day_gap = (datetime.now().date() - i.borrow_date).days
            if i.book.page <= 100:
                left_date = 7 - day_gap
            else:
                left_date = 15 - day_gap
            i.left_date = left_date
            i.book.photo = "Images/" + str(i.book.image)
            if i.librarian:
                i.librarian.image = "Images/" + str(i.librarian.photo)
            if i.return_to:
                i.return_to.image = "Images/" + str(i.return_to.photo)
        borrow = sorted(borrow, key=lambda x: x.left_date, reverse=False)
        return render(request, 'webpages/view_unreturn_book_by_user.html', {'form': form, 'borrow': borrow})

    else:
        raise Http404("You are not logged in")


def view_unreturn_book_by_librarian(request):
    librarian_id = request.session.get('librarian_auth')
    if librarian_id:
        try:
            librarian = Librarian.objects.get(librarian_id=librarian_id)
        except Librarian.DoesNotExist:
            raise Http404("This librarian is not registered")
        if request.method == "POST":
            form = BorrowBookSearch(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')

            if catalog == 'code':
                borrow = Borrow.objects.filter(book__code__contains=text, return_date=None)
            elif catalog == 'title':
                borrow = Borrow.objects.filter(book__title__contains=text, return_date=None)
            elif catalog == 'user_id':
                borrow = Borrow.objects.filter(user__user_id__contains=text, user__sex=librarian.sex, return_date=None)
            else:
                borrow = Borrow.objects.filter(user__name__contains=text, user__sex=librarian.sex, return_date=None) | \
                         Borrow.objects.filter(user__middle_name__contains=text, user__sex=librarian.sex,
                                               return_date=None) | \
                         Borrow.objects.filter(user__last_name__contains=text, user__sex=librarian.sex, return_date=None)

        else:
            form = BorrowBookSearch()
            borrow = Borrow.objects.filter(return_date=None)

        for i in borrow:
            day_gap = (datetime.now().date() - i.borrow_date).days
            if i.book.page <= 100:
                left_date = 7 - day_gap
            else:
                left_date = 15 - day_gap
            i.left_date = left_date
            i.user.image = "Images/" + str(i.user.photo)
            i.book.photo = "Images/" + str(i.book.image)
            if i.librarian:
                i.librarian.image = "Images/" + str(i.librarian.photo)
            if i.return_to:
               i.return_to.image = "Images/" + str(i.return_to.photo)
        borrow = sorted(borrow, key=lambda x: x.left_date, reverse=False)
        return render(request, 'webpages/view_unreturn_book_by_librarian.html',
                      {'form': form, 'borrow': borrow, 'sex': librarian.sex})

    else:
        raise Http404("You are not logged in")


def view_unreturn_book_by_admin(request):
    admin_id = request.session.get('admin_auth')
    if admin_id:
        try:
            admin = Admin.objects.get(admin_id=admin_id)
        except Admin.DoesNotExist:
            raise Http404("This admin is not registered")
        if request.method == "POST":
            form = BorrowBookSearch(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')

            if catalog == 'code':
                borrow = Borrow.objects.filter(book__code__contains=text, return_date=None)
            elif catalog == 'title':
                borrow = Borrow.objects.filter(book__title__contains=text, return_date=None)
            elif catalog == 'user_id':
                borrow = Borrow.objects.filter(user__user_id__contains=text, user__sex=admin.sex, return_date=None)
            else:
                borrow = Borrow.objects.filter(user__name__contains=text, user__sex=admin.sex, return_date=None) | \
                         Borrow.objects.filter(user__last_name__contains=text, user__sex=admin.sex, return_date=None) |\
                         Borrow.objects.filter(user__middle_name__contains=text, user__sex=admin.sex, return_date=None)

        else:
            form = BorrowBookSearch()
            borrow = Borrow.objects.filter(return_date=None)

        for i in borrow:
            day_gap = (datetime.now().date() - i.borrow_date).days
            if i.book.page <= 100:
                left_date = 7 - day_gap
            else:
                left_date = 15 - day_gap
            i.left_date = left_date
            i.user.image = "Images/" + str(i.user.photo)
            i.book.photo = "Images/" + str(i.book.image)
            if i.librarian:
                i.librarian.image = "Images/" + str(i.librarian.photo)
            if i.return_to:
                i.return_to.image = "Images/" + str(i.return_to.photo)
        borrow = sorted(borrow, key=lambda x: x.left_date, reverse=False)
        return render(request, 'webpages/view_unreturn_book_by_admin.html',
                      {'form': form, 'borrow': borrow, 'sex': admin.sex})

    else:
        raise Http404("You are not logged in")


def view_lost_books(request):
    admin_id = request.session.get('admin_auth')
    if admin_id:
        try:
            admin = Admin.objects.get(admin_id=admin_id)
        except Admin.DoesNotExist:
            raise Http404("This admin is not registered")
        lost = LostBook.objects.all().order_by('lost_date').reverse()
        for i in lost:

            i.verifier_admin.image = "Images/" + str(i.verifier_admin.photo)
            i.book.photo = "Images/" + str(i.book.image)

        return render(request, 'webpages/view_lost_books.html', {'lost': lost, 'sex': admin.sex})

    else:
        raise Http404("You are not logged in")


def add_lost_book(request):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    if request.method == "POST":
        form = AddLostBook(request.POST)
        if form.is_valid():

            code = request.POST.get('code')
            specific_code = request.POST.get('specific_code')
            book = Book.objects.get(code=code)

            try:
                borrow = Borrow.objects.get(book=book, specific_code=specific_code, return_date=None)
            except Borrow.DoesNotExist:
                borrow = Borrow.objects.none()

            return render(request, 'webpages/lost_book_confirmation.html',
                          {'borrow': borrow, 'title': book.title, 'code': code, 'specific_code': specific_code})
    else:
        form = AddLostBook()
    return render(request, 'webpages/add_lost_book.html', {'form': form})


def lost_book_confirm(request, code, specific_code):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    try:
        admin = Admin.objects.get(admin_id=admin_id)
    except Admin.DoesNotExist:
        raise Http404("This admin is not registered")

    book = Book.objects.get(code=code)
    date = datetime.now().date()

    try:
        borrow = Borrow.objects.get(book=book, specific_code=specific_code, return_date=None)
        borrow.delete()
        new_borrow_code = book.borrow_specific_code
        new_borrow_code.remove(specific_code)
        book.borrow_specific_code = new_borrow_code
    except Borrow.DoesNotExist:
        new_specific_code = book.specific_code
        new_specific_code.remove(specific_code)
        book.specific_code = new_specific_code

    book.amount = book.amount - 1
    book.save()

    lost = LostBook(book=book, specific_code=specific_code, verifier_admin=admin, lost_date=date)
    lost.save()

    messages.success(request, "The book "+book.title+" specified code "+specific_code +
                     " was added to lost cart successfully by "+admin.name)
    return redirect('/view-lost-books/')


def load_specific_code_for_lost_book(request):

    code = request.GET.get('code')
    try:
        book = Book.objects.get(code=code)
        specific_code = book.specific_code
        borrow_specific_code = book.borrow_specific_code
        for i in borrow_specific_code:
            specific_code.add(i)
    except Book.DoesNotExist:
        specific_code = Book.objects.none()
    specific_code = sorted(specific_code)
    return render(request, 'webpages/specific_code_drop_down_list.html', {'specific_code': specific_code})


def search_book_borrow_by_admin(request):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    admin = Admin.objects.get(admin_id=admin_id)
    if request.method == "POST":
        form = BorrowBookSearch(request.POST)
        text = request.POST.get('search_engine')
        catalog = request.POST.get('catalog')
        if catalog == 'code':
            borrow = Borrow.objects.filter(book__code__contains=text)
        elif catalog == 'title':
            borrow = Borrow.objects.filter(book__title__contains=text)
        elif catalog == 'user_id':
            borrow = Borrow.objects.filter(user__sex=admin.sex, user__user_id__contains=text)
        else:
            borrow = Borrow.objects.filter(user__sex=admin.sex, user__name__contains=text) | \
                     Borrow.objects.filter(user__sex=admin.sex, user__last_name__contains=text) | \
                     Borrow.objects.filter(user__sex=admin.sex, user__middle_name__contains=text)
    else:
        form = BorrowBookSearch()
        borrow = Borrow.objects.all()
    borrow = sorted(borrow, key=lambda x: x.borrow_date, reverse=True)

    for i in borrow:
        i.book.photo = "Images/" + str(i.book.image)
        i.user.image = "Images/" + str(i.user.photo)
        if i.librarian:
            i.librarian.image = "Images/" + str(i.librarian.photo)
        if i.return_to:
           i.return_to.image = "Images/" + str(i.return_to.photo)

    return render(request, 'webpages/search_book_borrow_by_admin.html',
                  {'form': form, 'borrow': borrow, 'sex': admin.sex})


def search_book_return_by_admin(request):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    admin = Admin.objects.get(admin_id=admin_id)
    if request.method == "POST":
        form = BorrowBookSearch(request.POST)
        text = request.POST.get('search_engine')
        catalog = request.POST.get('catalog')
        if catalog == 'code':
            borrow = Borrow.objects.filter(book__code__contains=text).exclude(return_date=None)
        elif catalog == 'title':
            borrow = Borrow.objects.filter(book__title__contains=text).exclude(return_date=None)
        elif catalog == 'user_id':
            borrow = Borrow.objects.filter(user__sex=admin.sex, user__user_id__contains=text).exclude(return_date=None)
        else:
            borrow = Borrow.objects.filter(user__sex=admin.sex, user__name__contains=text).exclude(return_date=None) | \
                     Borrow.objects.filter(user__sex=admin.sex, user__last_name__contains=text).\
                         exclude(return_date=None) | \
                     Borrow.objects.filter(user__sex=admin.sex, user__middle_name__contains=text).\
                         exclude(return_date=None)
    else:
        form = BorrowBookSearch()
        borrow = Borrow.objects.all().exclude(return_date=None)
    borrow = sorted(borrow, key=lambda x: x.return_date, reverse=True)

    for i in borrow:
        i.book.photo = "Images/" + str(i.book.image)
        i.user.image = "Images/" + str(i.user.photo)
        if i.librarian:
            i.librarian.image = "Images/" + str(i.librarian.photo)
        if i.return_to:
            i.return_to.image = "Images/" + str(i.return_to.photo)

    return render(request, 'webpages/search_return_book_by_admin.html',
                  {'form': form, 'borrow': borrow, 'sex': admin.sex})


def search_borrow_book_by_librarian(request):
    librarian_id = request.session.get('librarian_auth')
    if not librarian_id:
        raise Http404("You are not Logged in")
    librarian = Librarian.objects.get(librarian_id=librarian_id)
    if request.method == "POST":
        form = BorrowBookSearch(request.POST)
        text = request.POST.get('search_engine')
        catalog = request.POST.get('catalog')
        if catalog == 'code':
            borrow = Borrow.objects.filter(librarian=librarian, book__code__contains=text)
        elif catalog == 'title':
            borrow = Borrow.objects.filter(librarian=librarian, book__title__contains=text)
        elif catalog == 'user_id':
            borrow = Borrow.objects.filter(librarian=librarian, user__sex=librarian.sex, user__user_id__contains=text)
        else:
            borrow = Borrow.objects.filter(librarian=librarian, user__sex=librarian.sex, user__name__contains=text) | \
                     Borrow.objects.filter(librarian=librarian, user__sex=librarian.sex,
                                           user__middle_name__contains=text)| \
                    Borrow.objects.filter(librarian=librarian, user__sex=librarian.sex, user__last_name__contains=text)
    else:
        form = BorrowBookSearch()
        borrow = Borrow.objects.filter(librarian=librarian)
    borrow = sorted(borrow, key=lambda x: x.borrow_date, reverse=True)

    for i in borrow:
        i.book.photo = "Images/" + str(i.book.image)
        i.user.image = "Images/" + str(i.user.photo)
        if i.return_to:
           i.return_to.image = "Images/" + str(i.return_to.photo)

    return render(request, 'webpages/search_borrow_book_by_librarian.html',
                  {'form': form, 'borrow': borrow, 'sex': librarian.sex})


def search_return_book_by_librarian(request):
    librarian_id = request.session.get('librarian_auth')
    if not librarian_id:
        raise Http404("You are not Logged in")
    librarian = Librarian.objects.get(librarian_id=librarian_id)
    if request.method == "POST":
        form = BorrowBookSearch(request.POST)
        text = request.POST.get('search_engine')
        catalog = request.POST.get('catalog')
        if catalog == 'code':
            borrow = Borrow.objects.filter(return_to=librarian, book__code__contains=text).exclude(return_date=None)
        elif catalog == 'title':
            borrow = Borrow.objects.filter(return_to=librarian, book__title__contains=text).exclude(return_date=None)
        elif catalog == 'user_id':
            borrow = Borrow.objects.filter(return_to=librarian, user__sex=librarian.sex, user__user_id__contains=text).\
                exclude(return_date=None)
        else:
            borrow = Borrow.objects.filter(return_to=librarian, user__sex=librarian.sex, user__name__contains=text).\
                         exclude(return_date=None) | \
                     Borrow.objects.filter(return_to=librarian, user__sex=librarian.sex,
                                           user__middle_name__contains=text).exclude(return_date=None)| \
                     Borrow.objects.filter(return_to=librarian, user__sex=librarian.sex, user__last_name__contains=text).\
                         exclude(return_date=None)
    else:
        form = BorrowBookSearch()
        borrow = Borrow.objects.filter(return_to=librarian).exclude(return_date=None)
    borrow = sorted(borrow, key=lambda x: x.return_date, reverse=True)

    for i in borrow:
        i.book.photo = "Images/" + str(i.book.image)
        i.user.image = "Images/" + str(i.user.photo)
        if i.librarian:
           i.librarian.image = "Images/" + str(i.librarian.photo)

    return render(request, 'webpages/search_return_book_by_librarian.html',
                  {'form': form, 'borrow': borrow, 'sex': librarian.sex})


def search_borrow_book_by_user(request):
    user_id = request.session.get('user_auth')
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise Http404("This user is not registered")
        if request.method == "POST":
            form = BorrowBookSearchByUser(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')

            if catalog == 'code':
                borrow = Borrow.objects.filter(user=user, book__code__contains=text)
            else:
                borrow = Borrow.objects.filter(user=user, book__title__contains=text)

        else:
            form = BorrowBookSearchByUser()
            borrow = Borrow.objects.filter(user=user)
        for i in borrow:
            i.book.photo = "Images/" + str(i.book.image)
            if i.librarian:
                i.librarian.image = "Images/" + str(i.librarian.photo)
            if i.return_to:
                i.return_to.image = "Images/" + str(i.return_to.photo)
        borrow = sorted(borrow, key=lambda x: x.borrow_date, reverse=True)
        return render(request, 'webpages/search_borrow_book_by_user.html', {'form': form, 'borrow': borrow})

    else:
        raise Http404("You are not logged in")


def search_return_book_by_user(request):
    user_id = request.session.get('user_auth')
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise Http404("This user is not registered")
        if request.method == "POST":
            form = BorrowBookSearchByUser(request.POST)
            text = request.POST.get('search_engine')
            catalog = request.POST.get('catalog')

            if catalog == 'code':
                borrow = Borrow.objects.filter(user=user, book__code__contains=text).exclude(return_date=None)
            else:
                borrow = Borrow.objects.filter(user=user, book__title__contains=text).exclude(return_date=None)

        else:
            form = BorrowBookSearchByUser()
            borrow = Borrow.objects.filter(user=user).exclude(return_date=None)
        for i in borrow:
            i.book.photo = "Images/" + str(i.book.image)
            if i.librarian:
                i.librarian.image = "Images/" + str(i.librarian.photo)
            if i.return_to:
                i.return_to.image = "Images/" + str(i.return_to.photo)
        borrow = sorted(borrow, key=lambda x: x.return_date, reverse=True)
        return render(request, 'webpages/search_return_book_by_user.html', {'form': form, 'borrow': borrow})

    else:
        raise Http404("You are not logged in")


def print_statistics(request):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    admin = Admin.objects.get(admin_id=admin_id)
    if request.method == "POST":
        form = PrintStatistics(request.POST)
        if form.is_valid():
            start = datetime.strptime('Aug 1 2018', '%b %d %Y').date()
            date = datetime.now().date()
            catalog = request.POST.get('catalog')
            if catalog == 'borrow':
                file = open('backup files\\borrow'+str(date)+' .txt', mode='w', encoding='utf-8')
                file.write('verified by:  ' + admin.name + ' ' + admin.middle_name + '\n\n\n')
                dash = ''
                for i in range(90):
                    dash += '-'
                file.write('%-15s%-30s%-15s%-20s%-30s\n%s\n' % ('user id', 'user name', 'book code',
                                                                'specific code', 'title', dash))
                while start <= date:
                    borrow = Borrow.objects.filter(borrow_date=date)
                    if borrow:
                        file.write('\n\n\n\nDate of borrow: '+str(date)+'\n')

                    for i in borrow:
                        file.write(
                            '%-15s%-30s%-15s%-20s%-30s\n' % (i.user.user_id, i.user.name + ' ' + i.user.middle_name,
                                                             i.book.code, i.specific_code, i.book.title))
                    date += timedelta(days=-1)
                file.close()
                messages.success(request, "Borrow book list was printed successfully.")

            elif catalog == 'return':
                file = open('backup files\\return '+str(date)+' .txt', mode='w', encoding='utf-8')
                file.write('verified by:  ' + admin.name + ' ' + admin.middle_name + '\n\n\n')
                dash = ''
                for i in range(90):
                    dash += '-'
                file.write('%-15s%-30s%-15s%-20s%-30s\n%s\n' % ('user id', 'user name', 'book code',
                                                                'specific code', 'title', dash))
                while start <= date:
                    borrow = Borrow.objects.filter(return_date=date)
                    if borrow:
                        file.write('\n\n\n\nDate of return: '+str(date)+'\n')

                    for i in borrow:
                        file.write(
                            '%-15s%-30s%-15s%-20s%-30s\n' % (i.user.user_id, i.user.name + ' ' + i.user.middle_name,
                                                             i.book.code, i.specific_code, i.book.title))
                    date += timedelta(days=-1)
                file.close()
                messages.success(request, "Return book list was printed successfully.")

            elif catalog == 'unreturn':
                file = open('backup files\\unreturn '+str(date)+' .txt', mode='w', encoding='utf-8')
                file.write('verified by:  ' + admin.name + ' ' + admin.middle_name + '\n\n\n')
                dash = ''
                for i in range(105):
                    dash += '-'
                file.write('%-15s%-30s%-20s%-15s%-20s%-30s\n%s\n' % ('user id', 'user name', 'borrow date', 'book code',
                                                                     'specific code', 'title', dash))

                borrow = Borrow.objects.filter(return_date=None)
                for i in borrow:
                    file.write(
                        '%-15s%-30s%-20s%-15s%-20s%-30s\n' % (i.user.user_id, i.user.name + ' ' + i.user.middle_name,
                                                              str(i.borrow_date), i.book.code, i.specific_code,
                                                              i.book.title))
                file.close()
                messages.success(request, "Unreturn book list was printed successfully.")

            elif catalog == 'book':
                file = open('backup files\\book '+str(date)+' .txt', mode='w', encoding='utf-8')
                file.write('verified by:  ' + admin.name + ' ' + admin.middle_name + '\n\n\n')
                dash = ''
                for i in range(135):
                    dash += '-'
                file.write('%-15s%-30s%-15s%-15s%-20s%-15s%-30s\n%s\n' % ('code', 'author', 'page', 'amount',
                                                                          'category', 'pub. year', 'title', dash))

                book = Book.objects.all()
                for i in book:
                    file.write(
                        ('%-15s%-30s%-15d%-15d%-20s%-15s%-30s\n' % (i.code, i.author, i.page, i.amount,
                                                                        i.category.name, str(i.pub_year), i.title)))
                file.close()
                messages.success(request, "Book list was printed successfully.")


    else:
        form = PrintStatistics()

    return render(request, 'webpages/print_statistics.html', {'form': form})


def view_statistics(request):
    admin_id = request.session.get('admin_auth')
    if admin_id:
        admin = Admin.objects.get(admin_id=admin_id)
        book = Borrow.objects.all()
        borrow_books = [i.book for i in book]
        book_set = set(borrow_books)
        book_rank = []
        for i in book_set:
            book_rank.append([borrow_books.count(i), i])
        book_rank = sorted(book_rank, key=lambda x: x[0], reverse=True)

        rank = 1
        for i in book_rank:
            i.insert(0, rank)
            rank += 1
        if len(book_rank) > 10:
            book_rank = book_rank[:10]

        user = Borrow.objects.filter(user__sex=admin.sex).exclude(return_date=None)
        borrow_users = [i.user for i in user]
        user_set = set(borrow_users)
        user_rank = []
        for i in user_set:
            user_rank.append([borrow_users.count(i), i])
        user_rank = sorted(user_rank, key=lambda x: x[0], reverse=True)
        rank = 1
        for i in user_rank:
            i.insert(0, rank)
            rank += 1
        if len(user_rank) > 10:
            user_rank = user_rank[:10]
        return render(request, 'webpages/view_statistics.html', {'top_book': book_rank, 'top_user': user_rank})
    else:
        raise Http404('You are not Logged in')


def edit_book(request, book_id):
    if request.session.get('admin_auth'):
        if request.method == "POST":
            form = EditBook(request.POST, request.FILES, key=book_id)
            if form.is_valid():
                try:
                    book = Book.objects.get(pk=book_id)
                except Book.DoesNotExist:
                    raise Http404("Book does not exist")

                book.code = request.POST.get('code')
                book.title = request.POST.get('title')
                book.author = request.POST.get('author')
                book.pub_year = request.POST.get('publication_year')
                book.category.id = request.POST.get('category')
                book.description = request.POST.get('description')
                if request.FILES.get('image'):
                    book.cover_page = request.FILES.get('image')
                book.page = request.POST.get('page')

                book.save()
                messages.success(request, "The book "+book.title+" was update successfully.")
                return redirect('/book-view-by-admin/')
                #return HttpResponseRedirect('/book-view-by-admin/')

        else:
            form = EditBook(key=book_id)
        return render(request, 'webpages/edit_book.html', {'form': form})
    else:
        raise Http404("You are not logged in")


def delete_borrow_confirm(request, borrow_id):
    if request.session.get('librarian_auth'):
        try:
            borrow = Borrow.objects.get(pk=borrow_id)
        except Borrow.DoesNotExist:
            raise Http404("This borrow is not exist.")
        return render(request, 'webpages/delete_borrow_confirmation.html', {'borrow': borrow})

    else:
        raise Http404("You are not logged in")


def delete_borrow(request, borrow_id):
    if request.session.get('librarian_auth'):
        try:
            borrow = Borrow.objects.get(pk=borrow_id)
            book = borrow.book
            specific_code = borrow.specific_code

            new_specific_code = book.specific_code
            new_specific_code.add(specific_code)
            new_borrow_code = book.borrow_specific_code
            new_borrow_code.remove(specific_code)

            book.specific_code = new_specific_code
            book.borrow_specific_code = new_borrow_code
            book.save()

            borrow.delete()
            messages.success(request, "The borrow was deleted successfully.")
            return redirect('/view-book-borrow-by-librarian/')
        except User.DoesNotExist:
            raise Http404("This borrow is not registered")
    else:
        raise Http404("You are not logged in")


def csv_file_upload(request):
    admin_id = request.session.get('admin_auth')
    if not admin_id:
        raise Http404("You are not Logged in")
    if request.method == "POST":
        form = CSVFileUpload(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES.get('file')
            path = file.name
            if not file.content_type == 'application/vnd.ms-excel':
                messages.warning(request, "The file is not csv format.")
                return redirect('/book-view-by-admin/')

            catalog = Category.objects.all()
            with open(path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    specific_codes = set()
                    specific_code_text = row['specific_code']

                    text = ''
                    for i in specific_code_text:
                        if i == '_':
                            specific_codes.add(text)
                            text = ''
                        else:
                            if not i.isalpha():
                                messages.warning(request,
                                                 "in code " + row['code'] + " the specific codes are not alphabet."
                                                 "The specific codes must be alphabets separated by coma.")
                                continue
                            else:
                                text += i.upper()
                    specific_codes.add(text)

                    try:
                        amount = int(row['amount'])
                    except ValueError:
                        messages.warning(request, "in code " + row['code'] + " the amount is not integer. ")
                        continue
                    try:
                        year_text = row['year']
                        year = int(year_text)
                    except ValueError:
                        if len(year_text) == year_text.count(' '):
                            year = None
                        else:
                            messages.warning(request,
                                             "in code " + row['code'] + " the publication year is invalid.")
                            continue
                    try:
                        page_text = row['page']
                        page = int(page_text)
                    except ValueError:
                        if page_text == '':
                            messages.warning(request,
                                             "in code " + row['code'] + " the page is empty.")
                            return redirect('/book-view-by-admin/')
                        else:
                            messages.warning(request,
                                             "in code " + row['code'] + " the page is invalid.")
                            continue

                    if len(specific_codes) != amount:
                        messages.warning(request,
                                         "in code " + row['code'] + " the amount is not match with specific codes.")
                        continue
                    category = None
                    try:
                        book_code = int(row['code'])
                        for i in catalog:
                            if i.range_start <= book_code <= i.range_end:
                                category = i
                                break

                    except ValueError:
                        category = None
                    try:
                        obj, created = Book.objects.get_or_create(
                            code=row['code'],
                            title=row['title'],
                            author=row['author'],
                            pub_year=year,
                            page=page,
                            amount=amount,
                            specific_code=specific_codes,
                            category=category,
                            register_date=datetime.now().date()
                        )
                    except IntegrityError:
                        pass
            messages.success(request, "The book was upload successfully.")
            return redirect('/book-view-by-admin/')

    else:
        form = CSVFileUpload()
    return render(request, 'webpages/csv_upload.html', {'form': form})


