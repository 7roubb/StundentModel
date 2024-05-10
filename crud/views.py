from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Student,SupportMessage,studentsReg,Courses
from django.urls import reverse_lazy
from .models import Courses
from .form import CourseForm
from django.contrib.auth import logout
import time 
from .models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .form import StudentForm
from django.views.generic import DetailView
def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return render(request, 'sign.html')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return render(request, 'sign.html')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                user_model = User.objects.get(username=username)
                new_student = Student.objects.create(user=user_model, id_user=user_model.id,fullname=name)
                new_student.save()
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return render(request, 'sign.html')

        
    else:
        return render(request, 'sign.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return render(request, 'sign.html')


    else:
        return render(request, 'sign.html')
    
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return render(request, 'sign.html')

def test(request):
    pass

@login_required(login_url='/login'  )
def home(request):
    userl = request.user
    print(f'Logged-in user: {userl}')
    
    student = Student.objects.filter(user=userl).first()
    print(f'Student found: {student}')
    
    courses = []
    
    if student:
        registrations = studentsReg.objects.filter(student_id=student)
        print(f'Registrations found: {registrations.count()}')
        
        for registration in registrations:
            course = registration.course_id
            courses.append(course)
            print(f'Registered Course: {course.name}, Code: {course.code}')
    
    return render(request, 'index.html', {'student': student, 'courses': courses})


@login_required(login_url='login')

def logout_view(request):
    auth.logout(request)  
    return redirect('/')


@login_required(login_url='login')
def support(request):
    userl = request.user
    print(f'Logged-in user: {userl}')
    
    student = Student.objects.filter(user=userl).first()
    print(f'Student found: {student}')
    
    return render(request, 'support.html', {'student': student})

@login_required(login_url='login')
def support_message(request):
 if request.method == "POST":
        email = request.POST.get('email')
        message = request.POST.get('message')
        if email and message:
            SupportMessage.objects.create(email=email, message=message)
        else:
            pass
 time.sleep(1)
 return render(request, 'support.html')



def signupview(request):
    return render(request, 'signup.html')

@login_required(login_url='login')
def profile(request):
    userl = request.user
    print(f'Logged-in user: {userl}')
    
    student = Student.objects.filter(user=userl).first()
    print(f'Student found: {student}')
    
    
    return render(request, 'userd.html', {'student': student})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            schedule_id = form.cleaned_data['schedule_id']
            if Courses.objects.filter(schedule_id=schedule_id).exists():
                form.add_error('schedule_id', 'This schedule is already in use. Please select another.')
            else:
                new_course = form.save(commit=False)
                new_course.save()
                form.save_m2m()  
               
    else:
        form = CourseForm()

    return render(request, 'add_course.html', {'form': form})



@login_required
def search_courses(request):
    userl = request.user
    print(f'Logged-in user: {userl}')
    
    student = Student.objects.filter(user=userl).first()
    print(f'Student found: {student}')
    
    
    if request.method == "GET":
        query = request.GET.get('search', '')
        if query:
            courses = Courses.objects.filter(
                Q(code__icontains=query) | Q(name__icontains=query) | Q(instractor__icontains=query)
            )
            return render(request, 'search_results.html', {'courses': courses, 'student': student})
        else:
            return render(request, 'index.html')
    return redirect('')


@login_required
def register_course(request, course_code):
    if request.method == "POST":
        course = Courses.objects.get(code=course_code)
        student = Student.objects.get(user=request.user)
        if not studentsReg.objects.filter(student_id=student, course_id=course).exists():
            registration = studentsReg(student_id=student, course_id=course)
            registration.save()
            # return redirect('course_registration_success')
        # else:
        #     return render(request, 'courses/registration_error.html', {'error': 'You are already registered for this course.'})
    return redirect('')

@login_required(login_url='/login'  )
def mycourses(request):
    userl = request.user
    print(f'Logged-in user: {userl}')
    
    student = Student.objects.filter(user=userl).first()
    print(f'Student found: {student}')
    

    courses_with_schedules = []    
    if student:
        registrations = studentsReg.objects.filter(student_id=student).select_related('course_id__schedule_id')       
        print(f'Registrations found: {registrations.count()}')
        for registration in registrations:
            course = registration.course_id
            schedule = course.schedule_id
            courses_with_schedules.append({
                'course_name': course.name,
                'course_code': course.code,
                'schedule_days': schedule.days if schedule else 'No schedule',
                'start_time': schedule.start_time if schedule else 'N/A',
                'end_time': schedule.end_time if schedule else 'N/A',
                'room_no': schedule.room_no if schedule else 'N/A'
            })
            print(f'Registered Course: {course.name}, Code: {course.code}, Schedule: {schedule}')
    
    return render(request, 'my_courses.html', {'student': student, 'courses': courses_with_schedules})

@login_required(login_url='/login'  )

def sittings(request):
    
    userl = request.user
    print(f'Logged-in user: {userl}')
    
    student = Student.objects.filter(user=userl).first()
    print(f'Student found: {student}')
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('')  # Assuming you have a URL named 'students_list'
    else:
        form = StudentForm(instance=student)
    

    return render(request, 'sitting.html' ,{'student': student, 'form': form})


class CourseDetailView(DetailView):
    model = Courses
    template_name = 'course.html'
    context_object_name = 'course'
    slug_field = 'code'
    slug_url_kwarg = 'course_code'
@login_required(login_url='/login'  )
def course_detail(request, course_code):
    course = get_object_or_404(Courses, code=course_code)
    userl = request.user
    print(f'Logged-in user: {userl}')
    
    student = Student.objects.filter(user=userl).first()
    context = {
        'course': course,
        'schedule': course.schedule_id,
        'student': student
    }
    return render(request, 'course.html', context)