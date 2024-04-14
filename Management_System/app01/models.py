from django.db import models

# Create your models here.


class Admin(models.Model):
    """  管理员  """
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=64, verbose_name="密码")


class StudentInfo(models.Model):
    """  集训队队员表  """
    is_active = models.BooleanField(default=True, verbose_name='用户状态')
    name = models.CharField(max_length=32, verbose_name='姓名')
    class_name = models.CharField(max_length=64, verbose_name='班级')
    student_id = models.CharField(max_length=32, verbose_name='学号')
    CodeForce_id = models.CharField(max_length=32, verbose_name='CodeForce账号', default="Null")
    AtCoder_id = models.CharField(max_length=32, verbose_name='AtCoder账号', default="Null")
    VJudge_id = models.CharField(max_length=32, verbose_name='VJudge账号', default="Null")
    NewCoder_id = models.CharField(max_length=32, verbose_name='牛客账号')
    NewCoder_num = models.CharField(max_length=32, verbose_name='牛客用户id', default="Null")
    LuoGu_id = models.CharField(max_length=32, verbose_name='洛谷账号')
    LuoGu_num = models.CharField(max_length=32, verbose_name='洛谷用户id', default="Null")

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class CfInfo(models.Model):
    """  CodeForce数据表  """
    name = models.ForeignKey(max_length=32, verbose_name='姓名', to="StudentInfo", to_field="id",
                             on_delete=models.CASCADE)
    CodeForce_id = models.CharField(max_length=32, verbose_name='CodeForce账号')
    rating = models.IntegerField(verbose_name='Rank分数', default=0)
    max_rating = models.IntegerField(verbose_name='最高Rank分数', default=0)
    solved_all_time = models.IntegerField(verbose_name='总做题数', default=0)
    solved_last_month = models.IntegerField(verbose_name='过去一个月做题数', default=0)
    solved_last_year = models.IntegerField(verbose_name='过去一年做题数', default=0)

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class AtCoderInfo(models.Model):
    """  AtCoder数据表  """
    name = models.ForeignKey(max_length=32, verbose_name='姓名', to="StudentInfo", to_field="id",
                             on_delete=models.CASCADE)
    AtCoder_id = models.CharField(max_length=32, verbose_name='AtCoder账号')
    rank = models.CharField(verbose_name='Rank排名', max_length=32, default="——")
    rating = models.IntegerField(verbose_name='Rank分数', default=0)
    max_rating = models.IntegerField(verbose_name='最高Rank分数', default=0)
    Rated_Matches = models.IntegerField(verbose_name='参加过的比赛场数', default=0)
    Last_Competed = models.CharField(verbose_name='最近一次参加比赛的时间', max_length=32, default="——")

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class NewCodeInfo(models.Model):
    """  NewCode数据表  """
    name = models.ForeignKey(max_length=32, verbose_name='姓名', to="StudentInfo", to_field="id",
                             on_delete=models.CASCADE)
    NewCoder_id = models.CharField(max_length=32, verbose_name='NewCoder账号')
    NewCoder_num = models.CharField(max_length=32, verbose_name='NewCode账户编号')
    rating = models.IntegerField(verbose_name='Rank分数', default=0)
    rank = models.CharField(verbose_name='排名', max_length=32, default="——")
    solved = models.IntegerField(verbose_name='做题数', default=0)

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class VJudgeInfo(models.Model):
    """  VJudge数据表  """
    name = models.ForeignKey(max_length=32, verbose_name='姓名', to="StudentInfo", to_field="id",
                             on_delete=models.CASCADE)
    VJudge_id = models.CharField(max_length=32, verbose_name='VJudge账号')
    Overall_solved = models.IntegerField(verbose_name='总做题数', default=0)
    last_24hours_solved = models.CharField(verbose_name='过去一天做题数', max_length=32, default="0")
    last_7days_solved = models.CharField(verbose_name='过去一周做题数', max_length=32, default="0")
    last_30days_solved = models.CharField(verbose_name='过去一个月做题数', max_length=32, default="0")

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class LuoGuInfo(models.Model):
    """  LuoGu数据表  """
    name = models.ForeignKey(max_length=32, verbose_name='姓名', to="StudentInfo", to_field="id",
                             on_delete=models.CASCADE)
    LuoGu_id = models.CharField(max_length=32, verbose_name='LuoGu账户')
    LuoGu_num = models.CharField(max_length=32, verbose_name='LuoGu账户编号')
    solved = models.IntegerField(verbose_name='总做题数', default=0)
    rating = models.CharField(verbose_name='洛谷中排名', max_length=32, default='——')

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class CFContestInfo(models.Model):
    """  CFContestInfo  """
    name = models.CharField(max_length=128, verbose_name='比赛名称')
    start_time = models.CharField(max_length=32, verbose_name='比赛开始时间')
    duration = models.CharField(max_length=32, verbose_name='比赛持续时长')


class AtCoderContestInfo(models.Model):
    """  AtCoderContestInfo  """
    name = models.CharField(max_length=128, verbose_name='比赛名称')
    start_time = models.CharField(max_length=32, verbose_name='比赛开始时间')
    duration = models.CharField(max_length=32, verbose_name='比赛持续时长')


class NewCodeContestInfo(models.Model):
    """  NewCodeContestInfo  """
    name = models.CharField(max_length=128, verbose_name='比赛名称')
    registration_time = models.CharField(max_length=128, verbose_name='报名时间')
    start_time = models.CharField(max_length=128, verbose_name='比赛时间')
    duration = models.CharField(max_length=32, verbose_name='比赛持续时长')


class StrengthInfo(models.Model):
    """  StrengthInfo """
    name = models.ForeignKey(max_length=32, verbose_name='姓名', to="StudentInfo", to_field="id",
                             on_delete=models.CASCADE)
    score = models.IntegerField(verbose_name='分数', default=0)

    solved_all = models.IntegerField(verbose_name='总做题数', default=0)
    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, default=1)


class Formula(models.Model):
    """ 实力计算公式 """
    cf_solved = models.SmallIntegerField(verbose_name='cf做题数占比', default=0)
    cf_rating = models.SmallIntegerField(verbose_name='cf当前分数占比', default=0)
    cf_maxRating = models.SmallIntegerField(verbose_name='cf最高分数占比', default=0)
    atcoder_rating = models.IntegerField(verbose_name='atcoder分数占比', default=0)
    atcoder_maxRating = models.SmallIntegerField(verbose_name='atcoder最高分数占比', default=0)
    newCode_rating = models.SmallIntegerField(verbose_name='newCode分数占比', default=0)
    newCode_solved = models.SmallIntegerField(verbose_name='newCode做题数占比', default=0)
    vJudge_solved = models.SmallIntegerField(verbose_name='vJudge做题数占比', default=0)
    luogu_solved = models.SmallIntegerField(verbose_name='luogu做题数占比', default=0)


class VJudgeContest(models.Model):
    name = models.CharField(max_length=255, verbose_name="比赛名称")
    num = models.CharField(max_length=255, verbose_name="比赛的编号")
    start_date = models.CharField(max_length=255, verbose_name="开始时间")
    end_date = models.CharField(max_length=255, verbose_name="结束时间")

    def __str__(self):
        return self.num


class VJudgeContestData(models.Model):
    vJudgeContest = models.ForeignKey(VJudgeContest, on_delete=models.CASCADE, verbose_name="关联的比赛编号")
    name = models.CharField(max_length=255, verbose_name="用户名")
    solved = models.IntegerField(verbose_name='做题数', default=0)
    time = models.IntegerField(verbose_name='罚时', default=0)

    def __str__(self):
        return f"{self.name} - {self.vJudgeContest.num}"


class NewCodeContest(models.Model):
    name = models.CharField(max_length=255, verbose_name="比赛名称")
    num = models.CharField(max_length=255, verbose_name="比赛的编号")
    start_date = models.CharField(max_length=255, verbose_name="开始时间")
    end_date = models.CharField(max_length=255, verbose_name="结束时间")

    def __str__(self):
        return self.num


class NewCodeContestData(models.Model):
    newCodeContest = models.ForeignKey(NewCodeContest, on_delete=models.CASCADE, verbose_name="关联的比赛编号")
    name = models.CharField(max_length=255, verbose_name="用户名")
    solved = models.IntegerField(verbose_name='做题数', default=0)
    time = models.IntegerField(verbose_name='罚时', default=0)

    def __str__(self):
        return f"{self.name} - {self.newCodeContest.num}"


# 这里创建汇总牛客和VJudge的表
class NC_VJ_Contest(models.Model):
    name = models.CharField(max_length=255, verbose_name="比赛名称")
    num = models.CharField(max_length=255, verbose_name="比赛的编号")
    start_date = models.CharField(max_length=255, verbose_name="开始时间")
    end_date = models.CharField(max_length=255, verbose_name="结束时间")

    def __str__(self):
        return self.num


class NC_VJ_ContestData(models.Model):
    nC_VJ_Contest = models.ForeignKey(NC_VJ_Contest, on_delete=models.CASCADE, verbose_name="关联的比赛编号")
    name = models.CharField(max_length=255, verbose_name="用户名")
    solved = models.IntegerField(verbose_name='做题数', default=0)
    time = models.IntegerField(verbose_name='罚时', default=0)

    def __str__(self):
        return f"{self.name} - {self.nC_VJ_Contest.num}"


# 这里创建一张表，里面的数据是每个人对应每天的做题数据

class StudentRecord(models.Model):
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE, verbose_name="学生信息")
    date = models.DateField(verbose_name='日期')
    solved_today = models.IntegerField(verbose_name='当天做题数', default=0)
