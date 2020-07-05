from django import forms
from django.forms import widgets
from backstage.models import UserInfo
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


class UserForm(forms.Form):
    user = forms.CharField(
        max_length=32,
        error_messages={
            "required": "用户名不能为空",
        },
        label="用户名",
        widget=widgets.TextInput(attrs={"class": "form-control"},)
    )
    name = forms.CharField(
        max_length=16,
        error_messages={
            "required": "真实姓名不能为空"
        },
        label="真实姓名",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )

    pwd = forms.CharField(
        max_length=32,
        min_length=6,
        label="密码",
        error_messages={
            "min_length": "密码不能少于6位",
            "required": "密码不能为空",

        },
        widget=widgets.PasswordInput(attrs={"class": "form-control"},)

    )

    re_pwd = forms.CharField(
        max_length=32,
        label="确认密码",
        error_messages={
          "required": "请确认密码！"
        },
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(max_length=32,
                             label="邮箱",
                             error_messages={
                                 'invalid': '邮箱格式不对',
                                 "required": "邮箱不能为空",
                             },
                             widget=widgets.EmailInput(attrs={"class": "form-control"})
                             )

    def clean_user(self):
        val = self.cleaned_data.get("user")
        
        user = UserInfo.objects.filter(username=val).first()
        if not user:
            return val
        else:
            raise ValidationError("该用户已注册！")
        
    def clean(self):
        pwd=self.cleaned_data.get("pwd")
        re_pwd=self.cleaned_data.get("re_pwd")
        
        if pwd and re_pwd:
            if pwd==re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("输入密码不一致!")
        else:
            return self.cleaned_data
        
        
        