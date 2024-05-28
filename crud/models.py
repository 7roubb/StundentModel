from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.utils.timezone import now

User = get_user_model()
class Student(models.Model):
    fullname = models.CharField(max_length=90,null=False,default='No Name Provided')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    email = models.CharField(max_length=100)
    id_user = models.IntegerField( null=True)  
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default= 'defult.png')
    bio = models.CharField(max_length=250 , null=True, blank=True, default='None')
  
class CoruseSchedules(models.Model):
    id = models.AutoField(primary_key=True)  # Changed to AutoField for automatic ID handling
    DAY_CHOICES= (('Monday - Wensday','Monday - Wensday' ),('Sunday-Tuesday-Thursday','Sunday-Tuesday-Thursday'))
    days = models.CharField(max_length=100, choices=DAY_CHOICES, default='Monday - Wensday')    
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_no = models.CharField(max_length=5)
    class Meta:
        unique_together = ('days', 'start_time', 'end_time', 'room_no')

    def __str__(self):
        return f"{self.days} {self.start_time}-{self.end_time} in {self.room_no}"

class Courses(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    prerequisites = models.ManyToManyField('self', through='Prerequisties', symmetrical=False)
    instractor = models.CharField(max_length=30,default='')
    capacity = models.IntegerField(default=0)
    schedule_id = models.ForeignKey(CoruseSchedules,on_delete=models.CASCADE,null=True,unique=True)
    color = models.CharField(max_length=7, default='#FFFFFF') 

    def _str_(self):
        return self.name

class Prerequisties(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='required_by')
    course_prerequisite = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='requires')

class studentsReg(models.Model):
    id = models.IntegerField(primary_key=True)
    student_id= models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    
class SupportMessage(models.Model):
    message = models.CharField(max_length=255)
    email = models.EmailField(max_length=120)
    
class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title