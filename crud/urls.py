from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    

    path('register', views.signup),
    path('', views.home, name=''),
    path('login', views.signin,name='login'),
    path('signup', views.signupview,name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('support', views.support, name='support'),
    path('profile', views.profile, name='profile'),
    path('submit-message/', views.support_message, name='submit-message'),
    path('search/', views.search_courses, name='search_courses'),
    path('register/<str:course_code>/', views.register_course, name='register_course'),   
    path('my_courses', views.mycourses, name='mycourses'),
    path('sittings', views.sittings, name='sittings'),
    path('course/<str:course_code>/', views.course_detail, name='course'),  # or using the class-based view
    path('addcourse/', views.add_course, name='addcourse'),
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/add/', views.add_notification, name='add_notification'),

  
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
