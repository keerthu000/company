from . import views
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    path('',views.genicpage,name='genicpage'),
    path('register_company',views.register_company,name='register_company'),
    path('registercompany_view',views.registercompany_view,name='registercompany_view'),
    path('company_list',views.company_list,name='company_list'),
    path('update_company_view/<int:company_id>/', views.update_company_view, name='update_company_view'),
    path('delete_company_view/<int:company_id>/',views.delete_company_view,name="delete_company_view"),
    path('login_view',views.login_view,name="login_view"),
    path('createhrmanger',views.createhrmanger,name='createhrmanger'),
    path('addhr',views.addhr,name='addhr'),
    path('createmanager',views.createmanager,name='createmanager'),
    path('Employeecreate',views.Employeecreate,name='Employeecreate'),
    path('employeeadd',views.employeeadd,name='employeeadd'),
    path('employee_edit/<int:employee_id>/',views.employee_edit,name='employee_edit'),
    path('delete_employee/<int:employee_id>/',views.delete_employee,name='delete_employee'),
    path('employee_list',views.employee_list,name='employee_list'),
    path('department',views.department,name="department"),
    path('add_department',views.add_department,name='add_department'),
    path('roles',views.roles,name='roles'),
    path('add_roles',views.add_roles,name='add_roles'),
    path('attendancepage',views.attendancepage,name='attendancepage'),
    path('track_attendance',views.track_attendance,name='track_attendance'),
    path('attendance_list',views.attendance_list,name='attendance_list'),
    path('Leave',views.Leave,name='Leave'),
    path('leave_application',views.leave_application,name='leave_application'),
    path('leavelist',views.leavelist,name='leavelist'),
    path('leavelist_approval',views.leavelist_approval,name='leavelist_approval'),
    path('update_leave_status/<int:leave_id>/',views.update_leave_status,name='update_leave_status'),
    path('dashboard_view',views.dashboard_view,name='dashboard_view'),
    path('profile/<int:',views.profile,name='profile'),
    path('genicpage',views.genicpage,name='genicpage'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('register_manager',views.register_manager,name='register_manager'),
    path('employee_profile/<int:pk>/',views.employee_profile,name='employee_profile'),
]