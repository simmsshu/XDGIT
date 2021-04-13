from django.shortcuts import render
import hashlib
from django.http import HttpResponse
from user.models import User
# Create your views here.
def reg_view(request):
    #用户注册逻辑代码
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        #处理提交数据
        username = request.POST.get('username')
        if not username:
            username_error = '请输入正确的用户名'
            return render(request, 'user/register.html', locals())
        password_1 = request.POST.get('password_1')
        #1 生成hash算法对象对密码进行加密
        m = hashlib.md5()
        #2 对待加密明文使用update方法！要求输入明文为字节串
        m.update(password_1.encode())
        #3 调用对象的 hexdigest[16进制],通常存16进制
        password_m1 = m.hexdigest()
        print(password_m1)#加密后的密文会显示在终端上
        password_2 = request.POST.get('password_2')
        #对password_2执行MD5加密处理
        m = hashlib.md5()
        m.update(password_2.encode())
        password_m2 = m.hexdigest()
        print(password_m2)
        #可以设定密码格式，判断是都符合
        if not password_m1 or not password_m2:
            password_1_error = '请输入正确的密码'
            return render(request, 'user/register.html', locals())
         #判断两次密码输入是否一致
        if password_m1 != password_m2:
            password_2_error = '两次密码不一致'
            return render(request, 'user/register.html', locals())
        #查询用户名是否已注册过
        try:
            old_user = User.objects.get(username=username)
            #当前用户名已被注册
            username_error = '用户已经被注册 !'
            return render(request, 'user/register.html',locals())
        except Exception as e:
            # 若没查到的情况下进行报错，则证明当前用户名可用
            print('%s是可用用户名--%s'%(username, e))
            try:
                user = User.objects.create(username=username, password=password_m1)
                #注册成功后
                html = '''
                注册成功 点击<a href='/index/'>进入首页</a>
                '''
                #存session
                request.session['username'] = username
                return HttpResponse(html)
            #若创建不成功会抛出异常
            except Exception as e:
                # 还可能存在用户名被重复使用的情况
                print(e)
                username_error = '该用户名已经被占用 '
                return render(request, 'user/register.html', locals())