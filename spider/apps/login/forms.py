from django import forms

#创建表单类,用来产生表单
class UserForm(forms.Form):
    username=forms.CharField(label='用户名',max_length=64,widget=forms.TextInput(attrs={
        'placeholder':'用户名'}))
    password=forms.CharField(label='密码',max_length=16,widget=forms.PasswordInput(attrs={
        'placeholder':'密码'}))

class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=64, widget=forms.TextInput(attrs={
        'placeholder': '请设置用户名'}))
    password1 = forms.CharField(label='密码', max_length=16, widget=forms.PasswordInput(attrs={
        'placeholder': '请设置密码'}))
    password2 = forms.CharField(label='密码', max_length=16, widget=forms.PasswordInput(attrs={
        'placeholder': '请再次输入密码'}))
    email=forms.EmailField(label='邮箱地址',widget=forms.EmailInput(attrs={
        'placeholder': '请输入邮箱'}))
    pnumber=forms.CharField(label='性别',max_length=11,widget=forms.TextInput(attrs={
        'placeholder': '请输入手机号'}))