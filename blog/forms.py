from django import forms


class AddPostForm(forms.Form):
    headline = forms.CharField(label='Заголовок', max_length=40)
    text = forms.CharField(label='Текст', widget=forms.Textarea)


"""
class SetMarkPostForm(forms.Form):
    mark = forms.ChoiceField(label='Оценка', choices=(('pos', "+"), ('neg', "-")))
"""


class SetMarkPostForm(forms.Form):
    btn = forms.CharField()


class AddCommentForm(forms.Form):
    author = forms.CharField(label='Автор', max_length=40)
    text = forms.CharField(label='Комментарий', widget=forms.Textarea)


class ConfirmPostDelete(forms.Form):
    btn = forms.CharField()
