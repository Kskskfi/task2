from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import DesignRequest
from .models import Category

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Почта')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    username = forms.CharField(max_length=30, required=True, label='Имя пользователя')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название'}),
            'description': forms.Textarea(attrs={'placeholder': 'Введите описание', 'rows': 4}),
            'category': forms.Select(attrs={'placeholder': 'Выберите категорию'}),
            'image': forms.ClearableFileInput(attrs={'placeholder': 'Загрузите изображение'}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'image': '',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Максимальный размер изображения — 2Мб.')
        return image

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите название категории'}),
        }
        labels = {
            'name': 'Название',
        }

class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['status', 'design_image', 'comment']
        labels = {
            'status': 'Статус заявки',
            'design_image': 'Изображение дизайна (обязательно для статуса "Выполнено")',
            'comment': 'Комментарий (обязательно для статуса "Принято в работу")',
        }
        widgets = {
            'design_image': forms.FileInput(attrs={'id': 'file-upload', 'class': 'file-input'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Введите комментарий', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        design_image = cleaned_data.get('design_image')
        comment = cleaned_data.get('comment')

        if status == 'Выполнено' and not design_image:
            raise forms.ValidationError('Для изменения статуса на "Выполнено" необходимо добавить изображение дизайна.')
        if status == 'Принято в работу' and not comment:
            raise forms.ValidationError('Для изменения статуса на "Принято в работу" необходимо добавить комментарий.')

        return cleaned_data



    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        design_image = cleaned_data.get('design_image')
        comment = cleaned_data.get('comment')

        if status == 'Выполнено' and not design_image:
            raise forms.ValidationError('Для изменения статуса на "Выполнено" необходимо добавить изображение дизайна.')
        if status == 'Принято в работу' and not comment:
            raise forms.ValidationError('Для изменения статуса на "Принято в работу" необходимо добавить комментарий.')
        if status == 'Новая':
            raise forms.ValidationError('Нельзя изменить статус обратно на "Новая".')

        return cleaned_data