from django.shortcuts import render
from django.template import Template,Context
from django.http import HttpResponse
from django.views import View
from index.models import *

class LoginView(View): #需要继承自View类
    username='xiaoli'
    def get(self,request):
        return HttpResponse(f"登录成功{self.username}")
    def post(self,request):
        pass

def test_for(request):
      #调用template()方法生成模板
      t1=Template("""
                    {% for item in list %}
                        <li style="color:#FF0000;"><b>{{ item }}<b></li>
                    {% empty %}
                        <div style="background-color:#00FF00;color:#0000FF;font-family:宋体;font-size:40px;"><h1>如果找不到你想要，可以来C语言中文网(网址：http://c.biancheng.net/)</h1></div>
                    {% endfor %}
                              """)
      #调用 Context()方法
      c1= Context({'list':[]})
      html=t1.render(c1)
      return HttpResponse(html)
def test_html(request):
    a={} #创建空字典，模板必须以字典的形式进行传参
    a['name']='C语言中文网'
    a['course']=["Python","C","C++","Java"]
    a['b']={'name':'C语言中文网','address':'http://c.biancheng.net/'}
    a['test_hello']=test_hello
    a['class_obj']=Website()
    return render(request,'test_html.html',a)
def test_hello():
    return '欢迎来到C语言中文网'
class Website:
    def Web_name(self):
        return 'Hello，C语言中文网!'
    #Web_name.alters_data=True #不让Website()方法被模板调用
def test_if(request):
    dic={'x':2**4}
    return render(request,'test_if.html',dic)


def test_forloop(request):
    a = Template("""
     {% for item in lists %}
     <div>
        <p><b>{{ forloop.counter }}:{{ item }}</b></p>
     </div>
     {% endfor %}
     """)
    b = Context({'lists': ['c语言中网', 'Django官网', 'Pytho官网']})
    html = a.render(b)
    return HttpResponse(html)  # 数字与元素以 1:'c语言中文网' 的形式出现

def test_filter(request):
    a = Template('''
    <h1>word-len:{{word|length}}</h1>
    <h1>word-upper:{{word|upper}}</h1>
    <h1>word-first:{{word|first}}</h1>
    <h1>word-last:{{word|last}}</h1>
    <h1>word-add-n:{{word|add:"you are"}}</h1>
    <h1>word-join:{{word|join:"-"}}</h1>
    ''')
    page = a.render(Context({"word":"what"}))
    return HttpResponse(page)
def test_urls(request):
    print("locals:",locals())
    return render(request,'test_url.html')

def test_urls(request,id):
    return render(request,'test_url.html')

#定义父模板视图函数
def base_html(request):
    return render(request,'base.html')
#定义子模板视图函数
def index_html(request):
    name='xiaoming'
    course=['python','django','flask']
    return render(request,'test1_html.html',locals())

def redict_url(request):
    return render(request,'newtest.html')

def BookName(request):
    books=Book.objects.raw("select * from index_book") #书写sql语句
    return render(request,"index/allbook.html",locals())

from django import forms
class LoginForm(forms.Form): #继承自Form类，
    user_name=forms.CharField(label="用户名",min_length=6,max_length=12)#新建表单字段
    user_password=forms.CharField(label="用户密码",min_length=8)
#第二步围绕form对象完成表单。
def login(request):#定义登录处理函数login()
    print(f"loing_method is {locals()}")
    if request.method == "POST": #request是 HttpRequest的对象，利用它的的method属性，判断请求方法。
        form = LoginForm(request.POST)#实例化对象，post提交数据是QuerySet类型的字典，GET方法与其一样。
        if form.is_valid(): #提供验证判断是否有效，成立则返回是Ture
            return HttpResponse("登录成功")
    else:
        form=LoginForm()
    return render(request, "index/login.html",locals())

def login_page(request):
    form = LoginForm(request.POST)
    return render(request, "index/login.html",locals())

#用来显示查询页面
def search_ttile_form(request):
    return render(request,'index/search_title.html')

#用来显示查询结果
def serch_title(request):
    #查询title忽略大小写,所得类型为QuerySet
    if not request.GET.get("title",""):
        errors = ["输入的书无效","请重新输入"]
        #在这里使用列表的原因，是因为随着表单功能的修改可能需要传递多个字段，这时可能会有多个不同的错误信息需要展示。
        return render(request,'index/search_title.html',locals())
    elif len(request.GET.get("title","")) <= 5:
        errors = ["书名长度不能少于5位"]
        # 在这里使用列表的原因，是因为随着表单功能的修改可能需要传递多个字段，这时可能会有多个不同的错误信息需要展示。
        return render(request, 'index/search_title.html', locals())
    title=Book.objects.filter(title__icontains=request.GET['title'])
    print(title.__str__())
    return render(request,"index/book_list.html",locals())
    # return render(request,'index/book_list.html',locals())

def book_table(request):
    try:
        all_book=Book.objects.all().order_by('-price')
        if not all_book:
            return HttpResponse('书籍信息表为空，请录入！')
    except Exception as e:
        print(e)
    return render(request, 'index/book_table.html', locals())