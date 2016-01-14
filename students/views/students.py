# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Student, Group
from datetime import datetime
from django.views.generic import UpdateView,DeleteView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from django.forms import ModelForm

def students_list(request):
    students = Student.objects.all()
    #try to order students list
    order_by = request.GET.get('order_by','')
    if order_by in ('last_name','first_name','ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse','') == '1':
            students = students.reverse()
    #paginate!!!
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
        students = paginator.page(paginator.num_pages)
    return render(request, 'students/students_list.html',
        {'students': students})

def students_add(request):
    #was form posted?
    if request.method == "POST":
        #was form add button clicked?
        if request.POST.get('add_button') is not None:
            #errors collection
            errors = {}
            #validate student data will go HttpResponseRedirect
            data = {'middle_name':request.POST.get('middle_name'),
                    'notes':request.POST.get('notes')}
            #validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not first_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday,'%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Веведіть коректний формат дати y-m-d"
                else:
                    data['birthday'] = birthday
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]
            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo
            if not errors:
               #create student object
                student = Student(**data)
                student.save()
                #redirect user to students list
                return HttpResponseRedirect(
                    u'%s?status_message=Студента успішно додано!' %
                    reverse('home'))
            else:
                #render form with errors and previous user input
                return render(request,'students/students_add.html',
                {'groups':Group.objects.all().order_by('title'),
                'errors':errors})
        elif request.POST.get('cancel_button') is not None:
            #redirect to home on cancel button
            return HttpResponseRedirect(
                u'%s?status_message=Додавання студента скасовано!' %
                reverse('home'))
            #Перевіряємо дані на коректність та збираємо помилки
    else:
        #initial form render
        return render(request, 'students/students_add.html',
            {'groups':Group.objects.all().order_by('title')})

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm,self).__init__(*args,**kwargs)

        self.helper = FormHelper(self)

        #set form tag attributes
        self.helper.form_action = reverse('students_edit',
        kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        #set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        #add buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати',css_class = "btn btn-link")
        )
class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=Редагування студента вімінено!'%
                reverse('home'))
        else:
            return super(StudentsUpdateView, self).post(requset, *args, **kwargs)
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Студента успішно видалено!' % reverse('home')
