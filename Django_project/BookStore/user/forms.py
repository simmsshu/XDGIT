from django import forms

class ContactForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean() #继承clean()方法
        username= cleaned_data.get("username") #获取值
        password = cleaned_data.get("password")
        if username and password: #两者必须同时满足才可以
            if "Mrcao" not in username: #验证用户名字
                raise forms.ValidationError(
                       "USE is  error or password is error"
                )

class LoginForm(forms.Form):
    username=forms.CharField(label="用户名",min_length=6,max_length=12)
    password=forms.CharField(label="用户密码",min_length=8)

class TestForm(forms.Form):
    a = forms.CharField(required=False)#a不是必填字段，可以不提供
    b=forms.CharField(max_length=20)#最大长度为20
    c=forms.IntegerField(max_value=10,min_value=1)#最大值为10最小值1