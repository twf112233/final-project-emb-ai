from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # المسارات الأساسية الموجودة مسبقاً (مثل course_details، registration، login...)
    path(route='', view=views.CourseListView.as_view(), name='index'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),

    # المسارات المطلوبة لـ Task 6:
    # 1. مسار إرسال نموذج الامتحان (submit)
    path('<int:course_idA public GitHub file URL generally follows this format:

```text
[https://github.com/](https://github.com/)<your-username>/<your-repo-name>/blob/<branch-name>/<path-to-file>/urls.py
