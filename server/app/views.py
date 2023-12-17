import json
import time

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from app import models

'''
基础处理类，其他处理继承这个类
'''
class BaseView(View):

    '''
    检查指定的参数是否存在
    存在返回 True
    不存在返回 False
    '''
    def isExit(param):

        if (param == None) or (param == ''):
            return False
        else:
            return True

    '''
    转换分页查询信息
    '''
    def parasePage(pageIndex, pageSize, pageTotal, count, data):
        return {'pageIndex': pageIndex, 'pageSize': pageSize, 'pageTotal': pageTotal, 'count': count, 'data': data}

    '''
    成功响应信息
    '''
    def success(msg='处理成功'):
        resl = {'code': 0, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    成功响应信息, 携带数据
    '''
    def successData(data, msg='处理成功'):
        resl = {'code': 0, 'msg': msg, 'data': data}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    系统警告信息
    '''
    def warn(msg='操作异常，请重试'):
        resl = {'code': 1, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    系统异常信息
    '''
    def error(msg='系统异常'):
        resl = {'code': 2, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

'''
系统请求处理
'''
class SysView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'login':
            return render(request, 'login.html')

        elif module == 'exit':
            del request.session["userId"]
            del request.session["type"]
            return HttpResponseRedirect('/projects/login')

        if module == 'info':
            return SysView.getSessionInfo(request)

        elif module == 'show':
            return render(request, 'index.html')

    def post(self, request, module, *args, **kwargs):

        if module == 'login':
            return SysView.login(request)

        if module == 'info':
            return SysView.updSessionInfo(request)

        if module == 'pwd':
            return SysView.updSessionPwd(request)

    def login(request):

        userName = request.POST.get('userName')
        passWord = request.POST.get('passWord')

        user = models.Users.objects.filter(userName=userName)

        if (user.exists()):

            user = user.first()
            if user.passWord == passWord:
                request.session["userId"] = user.id
                request.session["type"] = user.type

                return SysView.success()
            else:
                return SysView.warn('用户密码输入错误')
        else:
            return SysView.warn('用户名输入错误')

    def getSessionInfo(request):

        userId = request.session.get('userId')

        data = models.Users.objects.filter(id=userId).first()

        if data.type == 0:
            return SysView.successData({
                'id': data.id,
                'userName': data.userName,
                'passWord': data.passWord,
                'gender': data.gender,
                'name': data.name,
                'age': data.age,
                'phone': data.phone,
                'type': data.type,
            })
        elif data.type == 1:

            teacher = models.Teachers.objects.filter(id=userId).first()
            return SysView.successData({
                'id': data.id,
                'userName': data.userName,
                'passWord': data.passWord,
                'gender': data.gender,
                'name': data.name,
                'age': data.age,
                'phone': data.phone,
                'type': data.type,
                'record': teacher.record,
                'address': teacher.address,
            })
        elif data.type == 2:

            student = models.Students.objects.filter(id=userId).first()
            return SysView.successData({
                'id': data.id,
                'userName': data.userName,
                'passWord': data.passWord,
                'gender': data.gender,
                'name': data.name,
                'age': data.age,
                'phone': data.phone,
                'type': data.type,
                'gradeId': student.grade.id,
            })

    def updSessionInfo(request):

        userId = request.session.get('userId')

        models.Users.objects.filter(id=userId).update(
            userName=request.POST.get('userName'),
            name=request.POST.get('name'),
            age=request.POST.get('age'),
            gender=request.POST.get('gender'),
            phone=request.POST.get('phone'),
        )

        return SysView.success()

    def updSessionPwd(request):

        userId = request.session.get('userId')

        models.Users.objects.filter(id=userId).update(
            passWord=request.POST.get('password'),
        )

        return SysView.success()

'''
课程信息处理
'''
class ProjectsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'projects.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.Projects.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'createTime': data.createTime
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        qruery = Q();

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        data = models.Projects.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'createTime': item.createTime
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self,request):

        models.Projects.objects.create(name=request.POST.get('name'),
                                       createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                      )

        return BaseView.success()

    def updInfo(self, request):

        models.Projects.objects.filter(id=request.POST.get('id')) \
            .update(
            name=request.POST.get('name')
        )
        return BaseView.success()

    def delInfo(self, request):

        if ((models.WorkLogs.objects.filter(project__id=request.POST.get('id')).exists()) or
            (models.SelectLogs.objects.filter(project__id=request.POST.get('id')).exists()) or
            (models.ScoreLogs.objects.filter(project__id=request.POST.get('id')).exists())):

            return BaseView.warn('存在关联内容无法删除')
        else:
            models.Projects.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
班级信息处理
'''
class GradesView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':

            projects = models.Projects.objects.all().values()
            return render(request, 'grades.html', {'projects': list(projects) })
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.Grades.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'createTime': data.createTime
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        qruery = Q();

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        data = models.Grades.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'createTime': item.createTime
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self,request):

        models.Grades.objects.create(name=request.POST.get('name'),
                                       createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                      )

        return BaseView.success()

    def updInfo(self, request):

        models.Grades.objects.filter(id=request.POST.get('id')) \
            .update(
            name=request.POST.get('name')
        )
        return BaseView.success()

    def delInfo(self, request):

        if ((models.Students.objects.filter(grade__id=request.POST.get('id')).exists()) or
            (models.WorkLogs.objects.filter(grade__id=request.POST.get('id')).exists()) or
            (models.SelectLogs.objects.filter(grade__id=request.POST.get('id')).exists()) or
            (models.ScoreLogs.objects.filter(grade__id=request.POST.get('id')).exists())):

            return BaseView.warn('存在关联内容无法删除')
        else:
            models.Grades.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
学生信息处理
'''
class StudentsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':

            grades = models.Grades.objects.all().values()
            return render(request, 'students.html', {'grades': list(grades) })
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.Students.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id.id,
            'userName': data.id.userName,
            'passWord': data.id.passWord,
            'name': data.id.name,
            'gender': data.id.gender,
            'age': data.id.age,
            'phone': data.id.phone,
            'gradeId': data.grade.id,
            'gradeName': data.grade.name
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        userName = request.GET.get('userName')
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        gradeId = request.GET.get('gradeId')

        qruery = Q();

        if BaseView.isExit(userName):
            qruery = qruery & Q(id__userName__contains=userName)

        if BaseView.isExit(name):
            qruery = qruery & Q(id__name__contains=name)

        if BaseView.isExit(phone):
            qruery = qruery & Q(id__phone__contains=phone)

        if BaseView.isExit(gradeId):
            qruery = qruery & Q(grade__id=gradeId)

        data = models.Students.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id.id,
                'gradeId': item.grade.id,
                'gradeName': item.grade.name,
                'userName': item.id.userName,
                'passWord': item.id.passWord,
                'name': item.id.name,
                'gender': item.id.gender,
                'age': item.id.age,
                'phone': item.id.phone
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    @transaction.atomic
    def addInfo(self,request):

        models.Users.objects.create(
            id=request.POST.get('id'),
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            age=request.POST.get('age'),
            phone=request.POST.get('phone'),
            type=request.POST.get('type')
        )
        models.Students.objects.create(
            id=models.Users.objects.get(id=request.POST.get('id')),
            grade=models.Grades.objects.get(id=request.POST.get('gradeId')),
        )

        return BaseView.success()

    @transaction.atomic
    def updInfo(self, request):

        models.Users.objects.filter(id=request.POST.get('id')) \
            .update(
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            age=request.POST.get('age'),
            phone=request.POST.get('phone')
        )
        models.Students.objects.filter(id=models.Users.objects.get(id=request.POST.get('id'))) \
            .update(
            grade=models.Grades.objects.get(id=request.POST.get('gradeId')),
        )
        return BaseView.success()

    def delInfo(self, request):

        if ((models.SelectLogs.objects.filter(student__id=request.POST.get('id')).exists()) or
            (models.ScoreLogs.objects.filter(student__id=request.POST.get('id')).exists())):

            return BaseView.warn('存在关联内容无法删除')
        else:
            models.Users.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()


'''
教师信息处理
'''
class TeachersView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':

            return render(request, 'teachers.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getInfo(self, request):

        data = models.Teachers.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id.id,
            'userName': data.id.userName,
            'passWord': data.id.passWord,
            'name': data.id.name,
            'gender': data.id.gender,
            'age': data.id.age,
            'phone': data.id.phone,
            'record': data.record,
            'address': data.address
        }

        return BaseView.successData(resl)

    def getPageInfo(self, request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        userName = request.GET.get('userName')
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        record = request.GET.get('record')

        qruery = Q();

        if BaseView.isExit(userName):
            qruery = qruery & Q(id__userName__contains=userName)

        if BaseView.isExit(name):
            qruery = qruery & Q(id__name__contains=name)

        if BaseView.isExit(phone):
            qruery = qruery & Q(id__phone__contains=phone)

        if BaseView.isExit(record):
            qruery = qruery & Q(record=record)

        data = models.Teachers.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id.id,
                'record': item.record,
                'address': item.address,
                'userName': item.id.userName,
                'passWord': item.id.passWord,
                'name': item.id.name,
                'gender': item.id.gender,
                'age': item.id.age,
                'phone': item.id.phone
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(pageData)

    @transaction.atomic
    def addInfo(self,request):

        models.Users.objects.create(
            id=request.POST.get('id'),
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            age=request.POST.get('age'),
            phone=request.POST.get('phone'),
            type=request.POST.get('type')
        )
        models.Teachers.objects.create(
            id=models.Users.objects.get(id=request.POST.get('id')),
            record=request.POST.get('record'),
            address=request.POST.get('address'),
        )

        return BaseView.success()

    @transaction.atomic
    def updInfo(self, request):

        models.Users.objects.filter(id=request.POST.get('id')) \
            .update(
            userName=request.POST.get('userName'),
            passWord=request.POST.get('passWord'),
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            age=request.POST.get('age'),
            phone=request.POST.get('phone')
        )
        models.Teachers.objects.filter(id=models.Users.objects.get(id=request.POST.get('id'))) \
            .update(
            record=request.POST.get('record'),
            address=request.POST.get('address'),
        )
        return BaseView.success()

    def delInfo(self, request):

        if ((models.WorkLogs.objects.filter(teacher__id=request.POST.get('id')).exists()) or
            (models.ScoreLogs.objects.filter(teacher__id=request.POST.get('id')).exists())):

            return BaseView.warn('存在关联内容无法删除')
        else:
            models.Users.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()


'''
授课安排处理
'''
class WorksView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'teachershow':

            return render(request, 'teacherShow.html')
        elif module == 'studentshow':

            return render(request, 'studentShow.html')
        elif module == 'workshow':

            return render(request, 'workShow.html', {'gradeId': request.GET.get('gradeId') })
        elif module == 'pagegrade':

            return self.getPageGradeWork(request)
        elif module == 'pageteacher':

            return self.getPageTeacherWork(request)
        elif module == 'pagestudent':

            return self.getPageStudentWork(request)
        elif module == 'gradeprojects':

            return self.getGradeProjects(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'setwork':
            return self.setWork(request)
        elif module == 'delwork':
            return self.delWork(request)
        else:
            return self.error()

    def getGradeProjects(self, request):

        resl = []

        projects = models.Projects.objects.all().values()

        for item in list(projects):

            qruery = Q()
            qruery = qruery & Q(grade__id=request.GET.get('gradeId'))
            qruery = qruery & Q(project__id=item["id"])

            if models.WorkLogs.objects.filter(qruery).exists():
                pass
            else:
                resl.append({
                    'id': item["id"],
                    'name': item["name"],
                })

        return BaseView.successData(resl)


    def getPageGradeWork(self, request):

        data = models.WorkLogs.objects.filter(grade__id=request.GET.get('gradeId'))

        resl = []

        for item in list(data):
            temp = {
                'id': item.id,
                'term': item.term,
                'year': item.year,
                'score': item.score,
                'hours': item.hours,
                'gradeId': item.grade.id,
                'gradeName': item.grade.name,
                'projectId': item.project.id,
                'projectName': item.project.name,
                'teacherId': item.teacher.id,
                'teacherName': item.teacher.name,
            }
            resl.append(temp)

        return BaseView.successData(resl)

    def getPageTeacherWork(self, request):

        userId = request.session.get('userId')

        data = models.WorkLogs.objects.filter(teacher__id=userId)

        resl = []

        for item in list(data):
            temp = {
                'id': item.id,
                'term': item.term,
                'year': item.year,
                'score': item.score,
                'hours': item.hours,
                'gradeId': item.grade.id,
                'gradeName': item.grade.name,
                'projectId': item.project.id,
                'projectName': item.project.name,
                'teacherId': item.teacher.id,
                'teacherName': item.teacher.name,
            }
            resl.append(temp)

        return BaseView.successData(resl)

    def getPageStudentWork(self, request):

        userId = request.session.get('userId')

        student = models.Students.objects.filter(id__id=userId).first()

        data = models.WorkLogs.objects.filter(grade__id=student.grade.id)

        resl = []

        for item in list(data):

            qruery = Q();
            qruery = qruery & Q(student__id=userId)
            qruery = qruery & Q(project__id=item.project.id)

            temp = {
                'id': item.id,
                'term': item.term,
                'year': item.year,
                'score': item.score,
                'hours': item.hours,
                'gradeId': item.grade.id,
                'gradeName': item.grade.name,
                'projectId': item.project.id,
                'projectName': item.project.name,
                'teacherId': item.teacher.id,
                'teacherName': item.teacher.name,
                'isSelect': models.SelectLogs.objects.filter(qruery).exists()
            }
            resl.append(temp)

        return BaseView.successData(resl)

    def setWork(self,request):

        models.WorkLogs.objects.create(
            id=request.POST.get('id'),
            term=request.POST.get('term'),
            year=timezone.now().year,
            score=request.POST.get('score'),
            hours=request.POST.get('hours'),
            teacher=models.Users.objects.get(id=request.POST.get('teacherId')),
            project=models.Projects.objects.get(id=request.POST.get('projectId')),
            grade=models.Grades.objects.get(id=request.POST.get('gradeId')),
        )

        return BaseView.success()

    def delWork(self,request):

        models.WorkLogs.objects.filter(id=request.POST.get('id')).delete()

        return BaseView.success()

'''
选课记录处理
'''
class SelectsView(BaseView):

    # def get(self, request, module, *args, **kwargs):
    #
    #     if module == 'teachershow':
    #
    #         return render(request, 'teacherShow.html')
    #     if module == 'teachershow':
    #
    #         return render(request, 'teacherShow.html')
    #     else:
    #         return self.error()

    def post(self, request, module, *args, **kwargs):

        if module == 'selectproject':
            return self.selectProject(request)
        elif module == 'cancelproject':
            return self.cancelProject(request)
        else:
            return self.error()

    def selectProject(self,request):

        userId = request.session.get('userId')

        models.SelectLogs.objects.create(
            term=request.POST.get('term'),
            year=timezone.now().year,
            createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            student=models.Users.objects.get(id=userId),
            project=models.Projects.objects.get(id=request.POST.get('projectId')),
            grade=models.Grades.objects.get(id=request.POST.get('gradeId')),
        )

        return BaseView.success()

    def cancelProject(self,request):

        models.SelectLogs.objects.filter(id=request.POST.get('id')).delete()

        return BaseView.success()

'''
学生成绩处理
'''
class ScoresView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'scoreshow':

            type = request.session.get('type')

            if type == 0:

                grades = models.Grades.objects.all().values()
                projects = models.Projects.objects.all().values()
                return render(request, 'scoreShow.html', {'grades': list(grades), 'projects': list(projects)})
            elif type == 1:

                userId = request.session.get('userId')

                gradeList = []
                projectList = []

                grades = models.Grades.objects.all().values()
                projects = models.Projects.objects.all().values()

                for item in list(grades):

                    qruery1 = Q();
                    qruery1 = qruery1 & Q(teacher__id=userId)
                    qruery1 = qruery1 & Q(grade__id=item['id'])

                    if models.WorkLogs.objects.filter(qruery1).exists():
                        gradeList.append({
                            'id': item['id'],
                            'name': item['name']
                        })

                for item in list(projects):

                    qruery1 = Q();
                    qruery1 = qruery1 & Q(teacher__id=userId)
                    qruery1 = qruery1 & Q(project__id=item['id'])

                    if models.WorkLogs.objects.filter(qruery1).exists():
                        projectList.append({
                            'id': item['id'],
                            'name': item['name']
                        })

                return render(request, 'scoreShow.html', {'grades': list(gradeList), 'projects': list(projectList)})
            else:
                userId = request.session.get('userId')

                projectList = []
                projects = models.Projects.objects.all().values()

                for item in list(projects):

                    qruery1 = Q();
                    qruery1 = qruery1 & Q(student__id=userId)
                    qruery1 = qruery1 & Q(project__id=item['id'])

                    if models.SelectLogs.objects.filter(qruery1).exists():
                        projectList.append({
                            'id': item['id'],
                            'name': item['name']
                        })

                return render(request, 'scoreShow.html', {'projects': list(projectList)})
        elif module == 'pagescore':
            return self.getPageInfos(request)

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return self.addInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getPageInfos(self, request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)

        projectId = request.GET.get('projectId')
        gradeId = request.GET.get('gradeId')
        studentName = request.GET.get('studentName')
        teacherName = request.GET.get('teacherName')

        qruery = Q();

        if request.session.get('type')==1:
            qruery = qruery & Q(teacher__id__id=request.session.get('userId'))

        if request.session.get('type')==2:
            qruery = qruery & Q(student__id__id=request.session.get('userId'))

        if BaseView.isExit(projectId):
            qruery = qruery & Q(project__id=projectId)

        if BaseView.isExit(gradeId):
            qruery = qruery & Q(grade__id=gradeId)

        if BaseView.isExit(studentName):
            qruery = qruery & Q(student__id__name__contains=studentName)

        if BaseView.isExit(teacherName):
            qruery = qruery & Q(teacher__id__name__contains=teacherName)

        data = models.ScoreLogs.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'term': item.term,
                'year': item.year,
                'score': item.score,
                'createTime': item.createTime,
                'gradeId': item.grade.id,
                'gradeName': item.grade.name,
                'projectId': item.project.id,
                'projectName': item.project.name,
                'teacherId': item.teacher.id.id,
                'teacherName': item.teacher.id.name,
                'studentId': item.student.id.id,
                'studentName': item.student.id.name,
            }
            resl.append(temp)

        pageData = BaseView.parasePage(pageIndex, pageSize,
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return BaseView.successData(pageData)

    def addInfo(self,request):

        student = models.Students.objects.get(id__id=request.POST.get('studentId'))

        userId = request.session.get('userId')

        qruery = Q();
        qruery = qruery & Q(term=request.POST.get('term'))
        qruery = qruery & Q(year=timezone.now().year)
        qruery = qruery & Q(project__id=request.POST.get('projectId'))
        qruery = qruery & Q(grade__id=student.grade.id)
        qruery = qruery & Q(student__id=request.POST.get('studentId'))

        if models.SelectLogs.objects.filter(qruery).exists():

            models.ScoreLogs.objects.create(
                score=request.POST.get('score'),
                term=request.POST.get('term'),
                year=timezone.now().year,
                createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                student=student,
                teacher=models.Teachers.objects.get(id__id=userId),
                project=models.Projects.objects.get(id=request.POST.get('projectId')),
                grade=student.grade,
            )

            return BaseView.success()
        else:

            return BaseView.warn('录入信息异常')

    def delInfo(self,request):

        models.ScoreLogs.objects.filter(id=request.POST.get('id')).delete()

        return BaseView.success()