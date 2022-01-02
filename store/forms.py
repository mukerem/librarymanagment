from django import forms
from django.forms import ChoiceField
from .models import User, Librarian, Admin, Category, Book, Borrow
from django.core.validators import RegexValidator
from datetime import datetime
import time


class UserRegister(forms.ModelForm):
    choices = [(True, 'campus student'), (False, 'city resident')]
    status = ChoiceField(choices=choices, initial=True, widget=forms.Select())

    class Meta:
        model = User
        fields = ['user_id', 'name', 'middle_name', 'last_name', 'phone', 'year', 'department', 'email', 'status',
                  'photo']
        help_texts = {
            'user_id': "Enter user id (if the user is student)",
            'name': "* Enter user first name",
            'middle_name': "* Enter user middle name",
            'last_name': "* Enter user last name",
            'phone': "* Enter user phone number",
            'year': "Enter user academic year (if the user is student)",
            'department': "Enter user academic department (if the user is student)",
            'email': "Enter user email (if any)",
            'status': "*choose user status (if the user is student choose campus student else city resident)",
            'photo': "Enter user photo (if any)",

        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        middle_name = cleaned_data.get('middle_name')
        last_name = cleaned_data.get('last_name')
        status = cleaned_data.get('status')
        user_id = cleaned_data.get('user_id')
        year = cleaned_data.get('year')
        department = cleaned_data.get('department')

        if (not name) or (not middle_name) or (not last_name):
            raise forms.ValidationError("Please correct the errors below.")

        if status == 'True':
            if (not user_id) or (not department) or (not year):
                raise forms.ValidationError("user id, year and department is required if you choose campus student "
                                            "status")
        return cleaned_data


class LibrarianRegister(forms.ModelForm):
    choices = [(True, 'campus student'), (False, 'city resident')]
    status = ChoiceField(choices=choices, initial=True, widget=forms.Select())

    class Meta:
        model = Librarian
        fields = ['librarian_id', 'name', 'middle_name', 'last_name', 'phone', 'year', 'department', 'email', 'photo']
        help_texts = {
            'librarian_id': "Enter librarian id (if the librarian is student)",
            'name': "* Enter librarian first name",
            'middle_name': "* Enter librarian middle name",
            'last_name': "* Enter librarian last name",
            'phone': "* Enter librarian phone number",
            'year': "Enter librarian academic year (if the librarian is student)",
            'department': "Enter librarian academic department (if the librarian is student)",
            'email': "Enter librarian email (if any)",
            'status': "*choose user status (if the user is student choose campus student else city resident)",
            'photo': "Enter librarian photo (if any)",

        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        middle_name = cleaned_data.get('middle_name')
        last_name = cleaned_data.get('last_name')
        status = cleaned_data.get('status')
        librarian_id = cleaned_data.get('librarian_id')
        year = cleaned_data.get('year')
        department = cleaned_data.get('department')

        if (not name) or (not middle_name) or (not last_name):
            raise forms.ValidationError("Please correct the errors below.")

        if status == 'True':
            if (not librarian_id) or (not department) or (not year):
                raise forms.ValidationError("librarian id, year and department is required if you choose campus student"
                                            "status")
        return cleaned_data


class AdminRegister(forms.ModelForm):
    choices = [(True, 'campus student'), (False, 'city resident')]
    status = ChoiceField(choices=choices, initial=True, widget=forms.Select())

    class Meta:
        model = Admin
        fields = ['admin_id', 'name', 'middle_name', 'last_name', 'phone', 'year', 'department', 'email', 'photo']
        help_texts = {
            'admin_id': "Enter admin id (if the admin is student)",
            'name': "* Enter admin first name",
            'middle_name': "* Enter admin middle name",
            'last_name': "* Enter admin last name",
            'phone': "* Enter admin phone number",
            'year': "Enter admin academic year (if the admin is student)",
            'department': "Enter admin academic department (if the admin is student)",
            'email': "Enter admin email (if any)",
            'status': "*choose user status (if the user is student choose campus student else city resident)",
            'photo': "Enter admin photo (if any)",

        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        middle_name = cleaned_data.get('middle_name')
        last_name = cleaned_data.get('last_name')
        status = cleaned_data.get('status')
        admin_id = cleaned_data.get('admin_id')
        year = cleaned_data.get('year')
        department = cleaned_data.get('department')

        if (not name) or (not middle_name) or (not last_name):
            raise forms.ValidationError("Please correct the errors below.")

        if status == 'True':
            if (not admin_id) or (not department) or (not year):
                raise forms.ValidationError("admin id, year and department is required if you choose campus student"
                                            "status")
        return cleaned_data


class AddCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'range_start', 'range_end']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        range_start = cleaned_data.get('range_start')
        range_end = cleaned_data.get('range_end')

        if (not name) or (not range_start) or (not range_end):
            raise forms.ValidationError("Please correct the errors below.")
        if range_start >= range_end:
            raise forms.ValidationError("range start must be less than range end.")
        try:
            category = Category.objects.get(range_start__lte=range_start, range_end__gte=range_start)
            raise forms.ValidationError(category.name+" was range b/n "+str(category.range_start)+" and " +
                                        str(category.range_end) + " so you must change range start.")
        except Category.DoesNotExist:
            pass
        try:
            category = Category.objects.get(range_start__lte=range_end, range_end__gte=range_end)
            raise forms.ValidationError(category.name+" was range b/n "+str(category.range_start)+" and " +
                                        str(category.range_end)+" so you must change range end.")
        except Category.DoesNotExist:
            pass
        if range_end >= 10000:
            raise forms.ValidationError("The range b/n 10000 up to 20000 is already occupy for none category")
        return cleaned_data


class BookRegister(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['code', 'title', 'author', 'pub_year', 'category', 'description', 'page', 'amount',
                  'specific_code', 'image']
        help_texts = {
            'code': "* Enter book code",
            'title': "* Enter book title",
            'author': "* Enter book author",
            'pub_year': "Enter publication year of the book",
            'category': "Choose the genera of book",
            'description': "Enter book description (if any)",
            'page': "* Enter number of pages",
            'amount': "* Enter amount of book",
            'specific_code': "* Enter all specific codes separating by coma(only use uppercase letters)",
            'image': "Enter book photo (if any)",

        }

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        page = cleaned_data.get('page')
        amount = cleaned_data.get('amount')
        specific_code = cleaned_data.get('specific_code')

        if amount == 0:
            raise forms.ValidationError("Amount must be greater than 0.")

        if (not code) or (not title) or (not author) or (not page) or (not amount) or (not specific_code):
            raise forms.ValidationError("Please correct the errors below.")

        try:
            code = int(cleaned_data.get('code'))
            category = cleaned_data.get('category')
            if not category:
                if code < 10000:
                    raise forms.ValidationError("Book code for non categorized book must be greater than 10000")
            else:
                if code < category.range_start or code > category.range_end:
                    raise forms.ValidationError("for " + category.name + " category the book code must be b/n " +
                                                str(category.range_start)+" and "+str(category.range_end))
        except ValueError:
            pass
        check_specific_codes = set()
        for i in specific_code:
            check_specific_codes.add(i.upper())

        for n in check_specific_codes:
            if not n.isalpha():
                raise forms.ValidationError(n + " is not alphabet. The specific codes must be alphabets separated "
                                                "by coma.")
        if amount != len(check_specific_codes):
            raise forms.ValidationError("The number of amount is not matched with specific codes or some specific "
                                        "codes are repeated.")
        return cleaned_data


class BookRegisterByCodeGenerator(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'pub_year', 'category', 'description', 'page', 'amount', 'image']
        help_texts = {
            'title': "* Enter book title",
            'author': "* Enter book author",
            'pub_year': "Enter publication year of the book",
            'category': "Choose the genera of book",
            'description': "Enter book description (if any)",
            'page': "* Enter number of pages",
            'amount': "* Enter amount of book",
            'image': "Enter book photo (if any)",

        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        page = cleaned_data.get('page')
        amount = cleaned_data.get('amount')

        if amount == 0:
            raise forms.ValidationError("Amount must be greater than 0.")

        if (not title) or (not author) or (not page) or (not amount):
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data


class AddBook(forms.Form):

    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
        help_text="* Enter title of book"
    )
    author = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
        help_text="* Enter the author of the book"
    )
    amount = forms.IntegerField(
        widget=forms.NumberInput,
        min_value=1,
        help_text="*Enter the number of books"
    )

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        amount = cleaned_data.get('amount')

        if (not title) or (not author) or (not amount):
            raise forms.ValidationError("Please correct the errors below.")
        try:
            Book.objects.get(title=title, author=author)
        except Book.DoesNotExist:
            raise forms.ValidationError("There is no book with this title and author.")
        return cleaned_data


class BookBorrow(forms.Form):
    def __init__(self, *args, **kwargs):
        self.sex = kwargs.pop('sex')
        super(BookBorrow, self).__init__(*args, **kwargs)

        try:
            code_id = self.data.get('code')
            book = [(i, i) for i in Book.objects.get(code=code_id).specific_code]
            book.sort()
            book.insert(0, (None, '--------------'))

        except (ValueError, TypeError, Book.DoesNotExist):
            book = []

        self.fields['user_id'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            help_text="* Enter user id"
        )
        self.fields['code'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            help_text="* Enter book code"
        )
        self.fields['specific_code'] = ChoiceField(
            widget=forms.Select(),
            choices=book,
            help_text="*Choose specific book code"
        )

    user_id = forms.CharField()
    code = forms.CharField()
    specific_code = ChoiceField()

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        code = cleaned_data.get('code')
        specific_code = cleaned_data.get('specific_code')

        if (not user_id) or (not code) or (not specific_code):
            raise forms.ValidationError("Please correct the errors below.")

        try:
            User.objects.get(user_id=user_id, sex=self.sex)
        except User.DoesNotExist:
            raise forms.ValidationError("There is no user with this user id.")
        try:
            Book.objects.get(code=code)
        except Book.DoesNotExist:
            raise forms.ValidationError("There is no book with this code.")
        return cleaned_data


class ReturnBook(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ReturnBook, self).__init__(*args, **kwargs)

        try:
            user_id = self.data.get('user_id')
            user = User.objects.get(user_id=user_id)
            book = Borrow.objects.filter(user=user, return_date=None)
            book = sorted(book, key=lambda x: x.borrow_date, reverse=False)
            book_list = [(data.id, data.book.code+' '+data.specific_code) for data in book]
            book_list.insert(0, (None, '--------------'))
        except (ValueError, TypeError, User.DoesNotExist, Borrow.DoesNotExist):
            book_list = []

        self.fields['user_id'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            help_text="* Enter user id"
        )
        self.fields['book_code'] = ChoiceField(
            widget=forms.Select(),
            choices=book_list,
            help_text="* Choose book code"
        )

    user_id = forms.CharField()
    book_code = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        book_code = cleaned_data.get('book_code')
        try:
            user = User.objects.get(user_id=user_id)
            book = Borrow.objects.filter(user=user, return_date=None)
            if not book:
                raise forms.ValidationError(user.name + " was not borrowed any book.")

        except User.DoesNotExist:
            raise forms.ValidationError("There is no user with this user id.")

        if (not user_id) or (not book_code):
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data


class LibrarianLogin(forms.Form):
    librarian_id = forms.CharField(
        max_length=1024,
        widget=forms.TextInput(),
    )
    password = forms.CharField(
        max_length=1024,
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        librarian_id = cleaned_data.get('librarian_id')

        if password and librarian_id:
            try:
                librarian = Librarian.objects.get(librarian_id=librarian_id)

                if password == librarian.password:
                    return
                else:
                    raise forms.ValidationError("Please enter the correct password.")
            except Librarian.DoesNotExist:
                raise forms.ValidationError("Please enter the correct librarian id.There is no librarian with this id. "
                                            "Note that fields may be case-sensitive. ")
        else:
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data


class AdminLogin(forms.Form):
    admin_id = forms.CharField(
        max_length=1024,
        widget=forms.TextInput(),
    )
    password = forms.CharField(
        max_length=1024,
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        admin_id = cleaned_data.get('admin_id')

        if password and admin_id:
            try:
                admin = Admin.objects.get(admin_id=admin_id)

                if password == admin.password:
                    return
                else:
                    raise forms.ValidationError("Please enter the correct password.")
            except Admin.DoesNotExist:
                raise forms.ValidationError("Please enter the correct admin id.There is no admin with this id. "
                                            "Note that fields may be case-sensitive. ")
        else:
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data


class UserLogin(forms.Form):
    user_id = forms.CharField(
        max_length=1024,
        widget=forms.TextInput(),
    )
    password = forms.CharField(
        max_length=1024,
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        user_id = cleaned_data.get('user_id')

        if password and user_id:
            try:
                user = User.objects.get(user_id=user_id)

                if password == user.password:
                    return
                else:
                    raise forms.ValidationError("Please enter the correct password.")
            except User.DoesNotExist:
                raise forms.ValidationError("Please enter the correct user id.There is no user with this id. "
                                            "Note that fields may be case-sensitive. ")
        else:
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data


class EditAdminProfile(forms.Form):

    def __init__(self, *args, **kwargs):
        self.admin_id = kwargs.pop('key')

        super(EditAdminProfile, self).__init__(*args, **kwargs)

        admin = Admin.objects.get(admin_id=self.admin_id)
        self.year = admin.year
        self.fields['admin_id'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=admin.admin_id,
        )
        self.fields['name'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=admin.name,
        )
        self.fields['middle_name'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=admin.middle_name,
        )
        self.fields['last_name'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=admin.last_name,
        )
        phone_regex = RegexValidator(
            regex=r'^\+?1?\d{10,15}$',
            message='Phone number must be entered in the format : 0987654321 or +251987654321 up to 15 digits allowed'
        )
        self.fields['phone'] = forms.CharField(
            validators=[phone_regex],
            max_length=15,
            widget=forms.TextInput(),
            initial=admin.phone,
        )

        if admin.year != 0 and admin.year:
            self.fields['year'] = forms.IntegerField(
                widget=forms.NumberInput,
                min_value=1,
                required=True,
                initial=admin.year,
            )

            self.fields['department'] = forms.CharField(
                widget=forms.TextInput(),
                max_length=200,
                required=True,
                initial=admin.department,
            )
        else:
            self.fields['year'] = forms.IntegerField(
                widget=forms.HiddenInput(),
                required=False,
                initial=admin.year,
            )
            self.fields['department'] = forms.CharField(
                widget=forms.HiddenInput(),
                required=False,
                initial=admin.department,
            )

        self.fields['email'] = forms.EmailField(
            max_length=254,
            required=False,
            widget=forms.TextInput(),
            initial=admin.email,
        )
        self.fields['photo'] = forms.ImageField(
            required=False,
            initial="Images/" + str(admin.photo),
        )
        self.fields['sex'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            disabled=True,
            initial=admin.sex,
        )
        self.fields['registered_date'] = forms.DateField(
            widget=forms.DateInput(),
            initial=admin.register_date,
            disabled=True,
        )

    admin_id = forms.CharField()
    name = forms.CharField()
    middle_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()
    year = forms.IntegerField()
    department = forms.CharField()
    email = forms.EmailField()
    photo = forms.ImageField()
    sex = forms.CharField()
    registered_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        admin_id = cleaned_data.get('admin_id')
        name = cleaned_data.get('name')
        middle_name = cleaned_data.get('middle_name')
        last_name = cleaned_data.get('last_name')
        phone = cleaned_data.get('phone')
        year = cleaned_data.get('year')
        department = cleaned_data.get('department')

        if (not admin_id) or (not name) or (not middle_name) or (not last_name) or (not phone):
            raise forms.ValidationError("Please correct the errors below.")

        if not self.year == 0 and self.year:
            if (not year) or (not department):
                raise forms.ValidationError("Please correct the errors below.")
        if self.admin_id != admin_id:
            try:
                Admin.objects.get(admin_id=admin_id)
                raise forms.ValidationError("Admin with this id already exists. ")
            except Admin.DoesNotExist:
                pass

        return cleaned_data


class EditLibrarianProfile(forms.Form):

    def __init__(self, *args, **kwargs):
        self.librarian_id = kwargs.pop('key')

        super(EditLibrarianProfile, self).__init__(*args, **kwargs)

        librarian = Librarian.objects.get(librarian_id=self.librarian_id)
        self.year = librarian.year
        self.fields['librarian_id'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=librarian.librarian_id,
        )
        self.fields['name'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=librarian.name,
        )
        self.fields['middle_name'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=librarian.middle_name,
        )
        self.fields['last_name'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=librarian.last_name,
        )
        phone_regex = RegexValidator(
            regex=r'^\+?1?\d{10,15}$',
            message='Phone number must be entered in the format : 0987654321 or +251987654321 up to 15 digits allowed'
        )
        self.fields['phone'] = forms.CharField(
            validators=[phone_regex],
            max_length=15,
            widget=forms.TextInput(),
            initial=librarian.phone,
        )

        if librarian.year != 0 and librarian.year:
            self.fields['year'] = forms.IntegerField(
                widget=forms.NumberInput,
                min_value=1,
                required=True,
                initial=librarian.year,
            )

            self.fields['department'] = forms.CharField(
                widget=forms.TextInput(),
                max_length=200,
                required=True,
                initial=librarian.department,
            )
        else:
            self.fields['year'] = forms.IntegerField(
                widget=forms.HiddenInput(),
                required=False,
                initial=librarian.year,
            )
            self.fields['department'] = forms.CharField(
                widget=forms.HiddenInput(),
                required=False,
                initial=librarian.department,
            )

        self.fields['email'] = forms.EmailField(
            max_length=254,
            required=False,
            widget=forms.TextInput(),
            initial=librarian.email,
        )
        self.fields['photo'] = forms.ImageField(
            required=False,
            initial="Images/" + str(librarian.photo),
        )
        self.fields['sex'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            disabled=True,
            initial=librarian.sex,
        )
        self.fields['registered_date'] = forms.DateField(
            widget=forms.DateInput(),
            initial=librarian.register_date,
            disabled=True,
        )

    librarian_id = forms.CharField()
    name = forms.CharField()
    middle_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()
    year = forms.IntegerField()
    department = forms.CharField()
    email = forms.EmailField()
    photo = forms.ImageField()
    sex = forms.CharField()
    registered_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        librarian_id = cleaned_data.get('librarian_id')
        name = cleaned_data.get('name')
        middle_name = cleaned_data.get('middle_name')
        last_name = cleaned_data.get('last_name')
        phone = cleaned_data.get('phone')
        year = cleaned_data.get('year')
        department = cleaned_data.get('department')

        if (not librarian_id) or (not name) or (not middle_name) or (not last_name) or (not phone):
            raise forms.ValidationError("Please correct the errors below.")

        if not self.year == 0 and self.year:
            if (not year) or (not department):
                raise forms.ValidationError("Please correct the errors below.")
        if self.librarian_id != librarian_id:
            try:
                Librarian.objects.get(librarian_id=librarian_id)
                raise forms.ValidationError("Librarian with this id already exists. ")
            except Librarian.DoesNotExist:
                pass
        return cleaned_data


class EditUserProfile(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('key')

        super(EditUserProfile, self).__init__(*args, **kwargs)

        user = User.objects.get(user_id=self.user_id)
        self.year = user.year
        self.fields['user_id'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=user.user_id,
        )
        self.fields['name'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=user.name,
        )
        self.fields['middle_name'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=user.middle_name,
        )
        self.fields['last_name'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=user.last_name,
        )
        phone_regex = RegexValidator(
            regex=r'^\+?1?\d{10,15}$',
            message='Phone number must be entered in the format : 0987654321 or +251987654321 up to 15 digits allowed'
        )
        self.fields['phone'] = forms.CharField(
            validators=[phone_regex],
            max_length=15,
            widget=forms.TextInput(),
            initial=user.phone,
        )

        if user.year != 0 and user.year:
            self.fields['year'] = forms.IntegerField(
                widget=forms.NumberInput,
                min_value=1,
                required=True,
                initial=user.year,
            )

            self.fields['department'] = forms.CharField(
                widget=forms.TextInput(),
                max_length=200,
                required=True,
                initial=user.department,
            )
        else:
            self.fields['year'] = forms.IntegerField(
                widget=forms.HiddenInput(),
                required=False,
                initial=user.year,
            )
            self.fields['department'] = forms.CharField(
                widget=forms.HiddenInput(),
                required=False,
                initial=user.department,
            )

        self.fields['email'] = forms.EmailField(
            max_length=254,
            required=False,
            widget=forms.TextInput(),
            initial=user.email,
        )
        self.fields['photo'] = forms.ImageField(
            required=False,
            initial="Images/" + str(user.photo),
        )
        self.fields['sex'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            disabled=True,
            initial=user.sex,
        )
        self.fields['registered_date'] = forms.DateField(
            widget=forms.DateInput(),
            initial=user.register_date,
            disabled=True,
        )

    user_id = forms.CharField()
    name = forms.CharField()
    middle_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()
    year = forms.IntegerField()
    department = forms.CharField()
    email = forms.EmailField()
    photo = forms.ImageField()
    sex = forms.CharField()
    registered_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        name = cleaned_data.get('name')
        middle_name = cleaned_data.get('middle_name')
        last_name = cleaned_data.get('last_name')
        phone = cleaned_data.get('phone')
        year = cleaned_data.get('year')
        department = cleaned_data.get('department')

        if (not user_id) or (not name) or (not middle_name) or (not last_name) or (not phone):
            raise forms.ValidationError("Please correct the errors below.")

        if not self.year == 0 and self.year:
            if (not year) or (not department):
                raise forms.ValidationError("Please correct the errors below.")
        if self.user_id != user_id:
            try:
                User.objects.get(user_id=user_id)
                raise forms.ValidationError("User with this id already exists. ")
            except User.DoesNotExist:
                pass

        return cleaned_data


class ChangePassword(forms.Form):
    def __init__(self, *args, **kwargs):
        self.password = kwargs.pop('key')
        self.hint = kwargs.pop('hint')

        super(ChangePassword, self).__init__(*args, **kwargs)

        self.fields['password_hint'] = forms.CharField(
            max_length=1024,
            widget=forms.TextInput(),
            help_text='Enter password hint',
            initial=self.hint
        )
    old_password = forms.CharField(
        max_length=1024,
        widget=forms.PasswordInput(),
    )
    password_regex = RegexValidator(
        regex=r'^\S{6,1024}',
        message='password must be at least 6 character'
    )
    new_password = forms.CharField(
        validators=[password_regex],
        max_length=1024,
        widget=forms.PasswordInput(),
        help_text='*Enter your new password minimum 6 character'
    )
    confirm = forms.CharField(
        label='Confirm Password',
        max_length=1024,
        widget=forms.PasswordInput(),
        help_text='*Enter your new password again'
    )
    password_hint = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm')
        if (not old_password) or (not new_password) or (not confirm_password):
            raise forms.ValidationError("Please correct the errors below.")

        if old_password == self.password:
            if new_password:
                if new_password == confirm_password:
                    return
                else:
                    raise forms.ValidationError("password is not confirmed")
        else:
            raise forms.ValidationError("Please enter the correct old password. ")

        return cleaned_data


class DateSearchEngine(forms.Form):
    search_date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('search_date')

        if not date:
            raise forms.ValidationError("Please correct the errors below.")
        if date > datetime.now().date():
            raise forms.ValidationError("Date must be less than or equal to "+str(datetime.now().date()))

        return cleaned_data


class AddLostBook(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddLostBook, self).__init__(*args, **kwargs)

        try:
            code_id = self.data.get('code')
            book = Book.objects.get(code=code_id)
            current_specific_code = book.specific_code
            borrow_specific_code = book.borrow_specific_code
            for i in borrow_specific_code:
                current_specific_code.add(i)
            specific_code = [(i, i) for i in current_specific_code]
            specific_code.sort()
            specific_code.insert(0, (None, '--------------'))

        except (ValueError, TypeError, Book.DoesNotExist):
            specific_code = []

        self.fields['code'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            help_text="* Enter book code"
        )
        self.fields['specific_code'] = ChoiceField(
            widget=forms.Select(),
            choices=specific_code,
            help_text="*Choose specific book code"
        )

    code = forms.CharField()
    specific_code = ChoiceField()

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        specific_code = cleaned_data.get('specific_code')

        if (not code) or (not specific_code):
            raise forms.ValidationError("Please correct the errors below.")

        try:
            Book.objects.get(code=code)
        except Book.DoesNotExist:
            raise forms.ValidationError("There is no book with this code.")
        return cleaned_data


class HumanSearch(forms.Form):
    search_engine = forms.CharField(
        label='',
        max_length=1024,
        widget=forms.TextInput(attrs={'placeholder': 'Search...'}),
    )
    catalog = ChoiceField(
        label='',
        widget=forms.Select(),
        choices=[('name', 'name'), ('id', 'id'), ('department', 'department'), ('year', 'year'), ('phone', 'phone')],
        initial='name'
    )


class BookSearch(forms.Form):
    search_engine = forms.CharField(
        label='',
        max_length=1024,
        widget=forms.TextInput(attrs={'placeholder': 'Search...'}),
    )
    catalog = ChoiceField(
        label='',
        widget=forms.Select(),
        choices=[('code', 'code'), ('title', 'title'), ('author', 'author'), ('category', 'category'),
                 ('pub_year', 'publication year')],
        initial='code'
    )


class BorrowBookSearch(forms.Form):
    search_engine = forms.CharField(
        label='',
        max_length=1024,
        widget=forms.TextInput(attrs={'placeholder': 'Search...'}),
    )
    catalog = ChoiceField(
        label='',
        widget=forms.Select(),
        choices=[('code', 'code'), ('title', 'title'), ('user_id', 'user id'), ('user_name', 'user name')],
        initial='code'
    )


class BorrowBookSearchByUser(forms.Form):
    search_engine = forms.CharField(
        label='',
        max_length=1024,
        widget=forms.TextInput(attrs={'placeholder': 'Search...'}),
    )
    catalog = ChoiceField(
        label='',
        widget=forms.Select(),
        choices=[('code', 'code'), ('title', 'title')],
        initial='code'
    )


class PrintStatistics(forms.Form):

    catalog = ChoiceField(
        label='',
        widget=forms.Select(),
        choices=[('', '---------------'), ('borrow', 'borrow list'), ('return', 'return list'),
                 ('unreturn', 'unreturn list'), ('book', 'book list')],
        initial='',
        help_text = "*Choose types of statistics"
    )

    def clean(self):
        cleaned_data = super().clean()
        catalog = cleaned_data.get('catalog')

        if not catalog:
            raise forms.ValidationError("Please choose from the list.")

        return cleaned_data


class EditBook(forms.Form):

    def __init__(self, *args, **kwargs):
        self.abc = kwargs.pop('key')
        super(EditBook, self).__init__(*args, **kwargs)

        self.options = [[i, i.name] for i in Category.objects.all().order_by('name')]
        self.options.insert(0, [None, '--------------'])

        book = Book.objects.get(pk=self.abc)
        self.code = book.code
        if book.category:
            self.initial['category'] = book.category

        self.fields['code'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=book.code,
        )

        self.fields['title'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=book.title,
        )
        self.fields['author'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            initial=book.author,
        )
        self.fields['publication_year'] = forms.IntegerField(
            widget=forms.NumberInput,
            required=False,
            max_value=time.localtime()[0],
            min_value=0,
            initial=book.pub_year,
        )

        self.fields['category'] = forms.ChoiceField(
            widget=forms.Select(),
            choices=self.options,
            required=False,
        )
        self.fields['description'] = forms.CharField(
            max_length=1000,
            required=False,
            widget=forms.Textarea(),
            initial=book.description,
        )
        self.fields['photo'] = forms.ImageField(
            required=False,
            initial="Images/"+str(book.image),
        )

        self.fields['page'] = forms.IntegerField(
            widget=forms.NumberInput,
            min_value=0,
            initial=book.page,
        )
        self.fields['registered_date'] = forms.DateField(
            widget=forms.DateInput(),
            initial=book.register_date,
            disabled=True,
        )

    code = forms.CharField()
    title = forms.CharField()
    author = forms.CharField()
    publication_year = forms.IntegerField()
    category = forms.ChoiceField()
    description = forms.CharField()
    photo = forms.ImageField()
    page = forms.IntegerField()
    registered_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        page = cleaned_data.get('page')
        if (not title) or (not author) or (not page):
            raise forms.ValidationError("Please correct the errors below.")

        if self.code != code:
            try:
                Book.objects.get(code=code)
                raise forms.ValidationError("Book with this code already exists. ")
            except Book.DoesNotExist:
                pass

        try:
            code = int(cleaned_data.get('code'))
            category = cleaned_data.get('category')
            if not category:
                if code < 10000:
                    raise forms.ValidationError("Book code for non categorized book must be greater than 10000")
            else:
                book_category = Category.objects.get(pk=category)
                if code < book_category.range_start or code > book_category.range_end:
                    raise forms.ValidationError("for " + book_category.name + " category the book code must be b/n " +
                                                str(book_category.range_start)+" and "+str(book_category.range_end))
        except ValueError:
            pass

        return cleaned_data


class CSVFileUpload(forms.Form):
    file = forms.FileField(
        label='Choose File',
        widget=forms.FileInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')

        if not file:
            raise forms.ValidationError("Please correct the errors below.")
