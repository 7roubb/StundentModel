from django import forms
from .models import Courses, CoruseSchedules,Student
from django.forms import inlineformset_factory

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'avatar','fullname', 'email',  'bio']
        def __init__(self, *args, **kwargs):
            super(StudentForm, self).__init__(*args, **kwargs)
            self.fields['avatar'].widget = forms.ClearableFileInput(attrs={'initial_text': 'Current Avatar', 'input_text': 'Change', 'clear_checkbox_label': 'Clear current image'})
            self.fields['avatar'].widget.clear_checkbox_label = None

class CourseForm(forms.ModelForm):
    prerequisites = forms.ModelMultipleChoiceField(
        queryset=Courses.objects.all(),
        required=False,
        widget=forms.Select,
    )

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        # Include a default option
        self.fields['prerequisites'].choices = [(None, 'No Prerequisites')] + [
            (course.pk, course.name) for course in Courses.objects.all()
        ]

    class Meta:
        model = Courses
        fields = ['code', 'name', 'description', 'instractor', 'capacity', 'prerequisites']
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = CoruseSchedules
        fields = ['days', 'start_time', 'end_time', 'room_no']
