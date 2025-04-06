from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Wish, Comment
from django.contrib.contenttypes.models import ContentType

class WishForm(forms.ModelForm):
    
    class Meta:
        model = Wish
        fields = ['name', 'is_public']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        
        self.fields['is_public'].widget = forms.CheckboxInput()
        



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.wish = kwargs.pop('wish', None)
        super().__init__(*args, **kwargs)

    def save(self, user=None, commit=True):
        comment = super().save(commit=False)
        if self.wish:
            comment.related_object = self.wish
        if user:
            comment.user = user
        if commit:
            comment.save()
        return comment
