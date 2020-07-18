from django import forms
from .models import Comment


# форма отправки email
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    body = forms.CharField(required=False, widget=forms.Textarea)


# форма для создания комментариев
# автоматическое создание формы (форма будет динамически генерироваться)
class CommentFrom(forms.ModelForm):
    class Meta:
        # Название модели
        model = Comment
        # какие поля использовать
        fields = ('name', 'email', 'body')


# форма полнотекстового поиска
class SearchForm(forms.Form):
    query = forms.CharField()