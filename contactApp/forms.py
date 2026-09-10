from django import forms
from .models import Resume


class AdForm(forms.Form):
    nickname = forms.CharField(
        max_length=50,
        required=True,
        strip=True,
        label='御主昵称',
    )
    message = forms.CharField(
        max_length=500,
        required=True,
        strip=True,
        label='留言内容',
        widget=forms.Textarea,
    )
    contact_info = forms.CharField(
        max_length=100,
        required=False,
        strip=True,
        label='联系方式',
    )


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('name', 'sex', 'personID', 'email', 'birth', 'edu', 'school',
                  'major', 'experience', 'position', 'photo')
        sex_list = (
            ('男', '男'),
            ('女', '女'),
        )
        edu_list = (
            ('大专', '大专'),
            ('本科', '本科'),
            ('硕士', '硕士'),
            ('博士', '博士'),
            ('其它', '其它'),
        )
        widgets = {
            'sex': forms.Select(choices=sex_list),
            'edu': forms.Select(choices=edu_list),
            'photo': forms.FileInput(),
        }
