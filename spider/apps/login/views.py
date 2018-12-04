from django.shortcuts import render,redirect
from . import forms
from . import models
import hashlib

#这个负责加密密码,加一个salt防止撞库,
def hash_code(s, salt='mysite'):
    #采用SHA256加密算法
    h = hashlib.sha256()
    s += salt
    h.update(s.encode('utf-8'))  # update方法只接收bytes类型
    return h.hexdigest()
#用来产生会话
def create_session(request,user):
    request.session['is_login'] = True
    # 记录用户的id,username
    request.session['user_id'] = user.id
    request.session['user_name'] = user.username
    # 设置标志位用来标志这是新登录的账号,限制一个账号只能登录一个设备
    request.session['new'] = True
    if request.POST.get('savepwd'):
        request.session.set_expiry(60*60*24*7)
    else:
        request.session.set_expiry(0)


def login(request):
    #判断是否已经登录。登录了重定向到搜索页面
    if request.session.get('is_login',None):
        return redirect('/homepage/')
    if request.method=='POST':
        #发来的是post请求,根据发来数据生成表单类对象
        login_form=forms.UserForm(request.POST)
        message = '密码跟用户名不能为空'
        #判断数据的合法性
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                #查询数据库是否有相关的的用户
                user = models.User.objects.get(username=username)
                # 有用户的情况下判断密码是否正确,并且创建会话
                if user.password == hash_code(password):
                    create_session(request,user)
                    return redirect('/homepage/')
                else:
                    message = "用户不存在或密码不正确！"
            except:
                message = "用户不存在或密码不正确！"
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    # 如果登录了就把他重定向到搜索页面
    if request.session.get('is_login',None):
        return redirect('/homepage')
    #如果是post请求则检查输入项
    if request.method=='POST':
        register_form=forms.RegisterForm(request.POST)
        message='请检查输入内容'
        #判断输入的合法性
        if register_form.is_valid():
            #如果合法表单类对象会把数据放到cleaned_data字典,取出对应的数据
            username=register_form.cleaned_data['username']
            password1=register_form.cleaned_data['password1']
            password2=register_form.cleaned_data['password2']
            email=register_form.cleaned_data['email']
            pnumber=register_form.cleaned_data['pnumber']
            #判断两次密码是否一致
            if password1!=password2:
                message='两次输入密码不同'
                return render(request,'login/register.html',locals())
            else:
                same_name_user=models.User.objects.filter(username=username)
                #检查用户名是否重复
                if same_name_user:
                    message='用户名已经存在。请重新选择用户名'
                    return render(request,'login/register.html',locals())
                same_name_user=models.User.objects.filter(email=email)
                #检查邮箱是否已经使用
                if same_name_user:
                    message='该邮箱已经被使用，请使用别的邮箱'
                    return render(request, 'login/register.html', locals())
                #数据没有问题则把数据存到数据库
                new_user=models.User()
                new_user.username=username
                #密码用SHA256加密算法加密储存
                new_user.password=hash_code(password1)
                new_user.email=email
                new_user.pnumber=pnumber
                new_user.save()
                #产生一个会话
                user = models.User.objects.get(username=username)
                create_session(request, user)
                # 把页面重定向到搜索界面
                return redirect('/homepage/')
    #如果不是post请求则生成一个空表单
    register_form=forms.RegisterForm()
    return render(request,'login/register.html',locals())

def repwd(request):
    # 如果登录了就把他重定向到搜索页面
    if request.session.get('is_login', None):
        return redirect('/homepage')
    # 如果是post请求则检查输入项
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = '请检查输入内容'
        # 判断输入的合法性
        if register_form.is_valid():
            # 如果合法表单类对象会把数据放到cleaned_data字典,取出对应的数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            pnumber = register_form.cleaned_data['pnumber']
            # 判断两次密码是否一致
            if password1 != password2:
                message = '两次输入密码不同'
                return render(request, 'login/repwd.html', locals())
            else:
                # 检查用户名是否存在
                try:
                    user = models.User.objects.filter(username=username)[0]
                except:
                    message = '输入信息有误，请核对'
                    return render(request, 'login/repwd.html', locals())
                if user.email==email and user.pnumber==pnumber:
                    user.password=hash_code(password1)
                    user.save()
                    return redirect('/',locals())
                else:
                    #用户信息不存在则让用户检查
                    message='输入信息有误，请核对'
                    return render(request, 'login/repwd.html', locals())
    # 如果不是post请求则生成一个空表单
    register_form = forms.RegisterForm()
    return render(request, 'login/repwd.html', locals())


def logout(request):
    #用户退出登录则清除会话
    request.session.flush()
    return redirect('/')

