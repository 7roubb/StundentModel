from django import forms
from .models import Courses, CoruseSchedules,Student
from django.forms import inlineformset_factory

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['code', 'name', 'description', 'prerequisites', 'instractor', 'capacity', 'schedule_id']

    def clean_schedule_id(self):
        schedule_id = self.cleaned_data.get('schedule_id')
        if Courses.objects.filter(schedule_id=schedule_id).exists():
            raise forms.ValidationError("This schedule is already in use. Please select another.")
        return schedule_id

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'avatar','fullname', 'email', 'id_user', 'bio']
        def __init__(self, *args, **kwargs):
            super(StudentForm, self).__init__(*args, **kwargs)
            self.fields['avatar'].widget = forms.ClearableFileInput(attrs={'initial_text': 'Current Avatar', 'input_text': 'Change', 'clear_checkbox_label': 'Clear current image'})
            self.fields['avatar'].widget.clear_checkbox_label = None

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['code', 'name', 'description', 'instractor', 'capacity']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = CoruseSchedules
        fields = ['days', 'start_time', 'end_time', 'room_no']
