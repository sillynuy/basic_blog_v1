from django import forms


class AddPostForm(forms.Form):
    headline = forms.CharField(label='Заголовок', widget=forms.Textarea(attrs={'rows': 1, 'cols': 70}))
    text = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'rows': 30, 'cols': 70}))


"""
class SetMarkPostForm(forms.Form):
    mark = forms.ChoiceField(label='Оценка', choices=(('pos', "+"), ('neg', "-")))
"""


class SetMarkPostForm(forms.Form):
    btn = forms.CharField()


class AddCommentForm(forms.Form):
    author = forms.CharField(label='Автор', max_length=40)
    text = forms.CharField(label='Комментарий', widget=forms.Textarea)


class AddCommentFormAuth(forms.Form):
    author = forms.CharField(widget=forms.HiddenInput(), required=False)
    text = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'rows': 3, 'cols': 70}))


class ConfirmPostDelete(forms.Form):
    btn = forms.CharField()
