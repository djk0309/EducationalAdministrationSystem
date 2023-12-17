from django.db import models

# 课程信息
class Projects(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('课程名称',  max_length=32, null=False)
    createTime = models.CharField('添加时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'projects'

# 班级信息
class Grades(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('班级名称',  max_length=32, null=False)
    createTime = models.CharField('添加时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'grades'

# 用户信息
class Users(models.Model):
    id = models.CharField('记录编号', max_length=20, primary_key=True)
    userName = models.CharField('用户账号', db_column='user_name', max_length=32, null=False)
    passWord = models.CharField('用户密码', db_column='pass_word', max_length=32, null=False)
    name = models.CharField('用户姓名', max_length=20, null=False)
    gender = models.CharField('用户性别', max_length=4, null=False)
    age = models.IntegerField('用户年龄', null=False)
    phone = models.CharField('联系电话', max_length=11, null=False)
    type = models.IntegerField('用户身份', null=False)
    class Meta:
        db_table = 'users'

# 学生信息
class Students(models.Model):
    id = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True, db_column='id')
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, db_column='grade_id')
    class Meta:
        db_table = 'students'

# 教师信息
class Teachers(models.Model):
    id = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True, db_column='id')
    record = models.CharField('教师学历', max_length=20, null=False)
    address = models.CharField('联系地址', max_length=64, null=False)
    class Meta:
        db_table = 'teachers'

# 工作安排
class WorkLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    term = models.CharField('学期', max_length=2, null=False)
    year = models.IntegerField('学年', null=False)
    score = models.FloatField('学分', null=False)
    hours = models.FloatField('学时', null=False)
    teacher = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='teacher_id')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, db_column='project_id')
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, db_column='grade_id')
    class Meta:
        db_table = 'work_logs'

# 选课记录
class SelectLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    term = models.CharField('学期', max_length=2, null=False)
    year = models.IntegerField('学年', null=False)
    createTime = models.CharField('添加时间', db_column='create_time', max_length=19)
    student = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='student_id')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, db_column='project_id')
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, db_column='grade_id')
    class Meta:
        db_table = 'select_logs'

# 成绩记录
class ScoreLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    term = models.CharField('学期', max_length=2, null=False)
    year = models.IntegerField('学年', null=False)
    score = models.FloatField('成绩', null=False)
    createTime = models.CharField('添加时间', db_column='create_time', max_length=19)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, db_column='student_id')
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, db_column='teacher_id')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, db_column='project_id')
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, db_column='grade_id')
    class Meta:
        db_table = 'score_logs'