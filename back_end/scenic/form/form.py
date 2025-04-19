from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from scenic.utils.encrypt import md5
from scenic.models import *

# class AttractionModelForm(BootStrapModelForm):
class AttractionModelForm(forms.ModelForm):
    class Meta:
        model = Attraction
        # fields = ["attraction_name", "scenic", "attraction_lng", "attraction_lat", "address", "description", "category", "fee", "open_time", "close_time", "flow_limit", "status", "phone"]
        fields = "__all__"
        exclude = ["count"]
    # 验证方式2：钩子方法，clean_字段名
    # def clean_attraction_name(self):
    #     input_name = self.cleaned_data["attraction_name"]
    #     input_scenic = self.cleaned_data["scenic"]
    #     exist = Attraction.objects.filter(attraction_name=input_name, scenic=input_scenic).exists()
    #     if exist:
    #         raise ValidationError("该景区已存在该景点")
    #     return input_name

class UpForm(forms.Form):
    attraction_name = forms.CharField(label="景点名称")
    attraction_img = forms.FileField(label="图片")


class UpModelForm(forms.ModelForm):
    class Meta:
        model = Attraction
        fields = "__all__"

class UserModelForm(forms.ModelForm):
    # 验证方式1：
    phone = forms.CharField(
        label="联系电话",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '格式错误')]
    )
    confirm_password = forms.CharField(label="确认密码", max_length=50, widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = User
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }
    # 验证方式2：钩子方法，clean_字段名
    def clean_phone(self):
        input_phone = self.cleaned_data["phone"]
        exist = User.objects.filter(phone=input_phone).exists()
        if exist:
            raise ValidationError("该手机号已注册")
        return input_phone

    def clean_confirm_password(self):
        input_pwd = self.cleaned_data["password"]
        input_con = md5(self.cleaned_data["confirm_password"])
        if input_con != input_pwd:
            raise ValidationError("密码不一致")
        return input_con

    def clean_password(self):
        input_pwd = self.cleaned_data["password"]
        return md5(input_pwd)


class TourRouteModelForm(forms.ModelForm):
    class Meta:
        model = TourRoute
        fields = "__all__"


class TourOrderModelForm(forms.ModelForm):
    class Meta:
        model = TourOrder
        fields = "__all__"
        exclude = ["tour_route"]
