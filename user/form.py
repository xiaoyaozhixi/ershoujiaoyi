from django import forms
from captcha.fields import CaptchaField


class Change_password(forms.Form):
    password1 = forms.CharField(
        label='旧密码',
        required=True,
        min_length=5,
        widget=forms.TextInput(attrs={'class': 'password'}),
        error_messages={"required": "必须填写旧密码", "min_length": "密码最少为5位"}
    )
    password2 = forms.CharField(
        label='新密码',
        required=True,
        min_length=5,
        widget=forms.TextInput(attrs={'class': 'password'}),
        error_messages={"required": "必须填写新密码", "min_length": "密码最少为5位"}
    )
    password3 = forms.CharField(
        label='确认新密码',
        required=True,
        min_length=5,
        widget=forms.TextInput(attrs={'class': 'password'}),
        error_messages={"required": "必须填写新密码", "min_length": "密码最少为5位"}
    )
    captcha = CaptchaField(
        label='验证码',
        required=True,
        error_messages={
            'required': '验证码不能为空'
        }
    )
