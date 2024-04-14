from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from django import forms


class StudentModelForm(BootStrapModelForm):
    # 这里可以重写元素进行数据判断是否合法，譬如对元素的长度进行修改
    class Meta:
        model = models.StudentInfo
        fields = ['name', 'gender', 'class_name', 'student_id', 'CodeForce_id', 'AtCoder_id', 'VJudge_id',
                  'NewCoder_id', 'NewCoder_num', 'LuoGu_id', 'LuoGu_num']
        # widgets = {
        #     "name": forms.TextInput(attrs={'class': 'form-control'})
        # }



