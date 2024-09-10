from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomerUser,Company,Hr_manger,Manger,Employee,Departments,Role,Attendance,LeaveRequest
from .serializers import CompanySerializer
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from datetime import datetime
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.db.models import Count,Q

# Create your views here.
def register_company(request):
     return render(request,'reg_company.html') 

# @api_view(['POST'])
# def registercompany_view(request):
#     serializer = CompanySerializer(data=request.data)
#     if serializer.is_valid():
#         # Save company data
#         serializer.save()

#         # Handle logo file upload
#         if 'imageUpload' in request.FILES:
#             company = Company.objects.latest('id')  # Get the latest saved company
#             company.logo = request.FILES['imageUpload']  # Assign the uploaded file to logo field
#             company.save()  # Save the company with the uploaded logo

#         return redirect('/')  # Assuming '/login' is your login page URL
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#@user_passes_test(is_admin)
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'company_list.html', {'companies': companies})
     
   
def registercompany_view(request):
    if request.method == 'POST':
        # Access form data from request.POST
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a company with this email already exists before saving
        if Company.objects.filter(email=email).exists():
            messages.error(request, 'A company with this email already exists.')
            return redirect('register_company')

        # Check if a user with this email (username) already exists
        User = CustomerUser  # Use your custom user model
        if User.objects.filter(username=email).exists():
            return render(request, 'reg_company.html', {'error_message': 'Username already exists'})

        # Create a new user (cutomerUser)
        try:
            user = User.objects.create_user(
                first_name=company_name,
                username=email,
                password=password,
                email=email,
            )
            user.is_admin = True
            user.save()
            # Create the company and link it to the user
            company = Company(
                user=user,  # Link the user to the company
                company_name=company_name,
                address=address,
                contact_number=contact_number,
                email=email,
                password=password
            )
            company.save()

            # Handle logo file upload if provided
            if 'imageUpload' in request.FILES:
                company.logo = request.FILES['imageUpload']
                company.save()

            messages.success(request, 'Company registered successfully.')

            # Redirect to the company list page after successful registration
            return redirect('login_view')

        except IntegrityError:
            messages.error(request, 'An error occurred while registering the company.')
            return render(request, 'reg_company.html')

    # If GET request, render the registration form
    return render(request, 'reg_company.html')



def update_company_view(request, company_id):
   
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
       
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')

      
        company.company_name = company_name
        company.address = address
        company.contact_number = contact_number
        company.email = email

        try:
           
            if 'imageUpload' in request.FILES:
                company.logo = request.FILES['imageUpload']

            
            company.save()

            messages.success(request, 'Company profile updated successfully.')
            return redirect('company_list')

        except IntegrityError:
            messages.error(request, 'An error occurred while updating the company.')
            return render(request, 'comapanyedit.html', {'company': company})

   
    return render(request, 'comapanyedit.html', {'company': company})



def delete_company_view(request, company_id):
   
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
       
        company.delete()
        messages.success(request, 'Company deleted successfully.')
        return redirect('company_list')  
    
    return render(request, 'delete_company.html', {'company': company})



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Email: {email}, Password: {password}")  # Print the input values

        # Authenticate using email and password
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print(f"Authenticated user: {user}")  # Check if authentication succeeds
            if user.is_active:
                login(request, user)
                if user.is_admin:
                    return redirect('profile')
                elif user.is_hr_manager:
                    return redirect('profile')
                elif user.is_manager:
                    return redirect('profile')
                elif user.is_employee:
                    return redirect('profile')
                else:
                    return redirect('/')
            else:
                messages.error(request, 'Your account is inactive.')
        else:
            print('Invalid login attempt')  # For debugging authentication failure
            messages.error(request, 'Invalid email or password.')
    return render(request, 'loginform.html')



def createhrmanger(request):
    cmpny=Company.objects.all()
    print(cmpny)
    return render(request, 'hrmangerform.html',{'cmpny':cmpny})

def addhr(request):
    if request.method == 'POST':
        print('entered')
        # Access form data from request.POST
        hr_name = request.POST.get('hr_name')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        comapny_id=request.POST.get('companyname')
        company = get_object_or_404(Company, id=comapny_id)

        # Check if a company with this email already exists before saving
        if Hr_manger.objects.filter(email=email).exists():
            messages.error(request, ' This email already exists.')
            return redirect('createhrmanger')

        # Check if a user with this email (username) already exists
        User =CustomerUser  # Use your custom user model
        # if User.objects.filter(username=email).exists():
        #     return render(request, 'hrmangerform.html', {'error_message': 'Username already exists'})

        # Create a new user (cutomerUser)
        try:
            user = User.objects.create_user(
                first_name=hr_name,
                username=email,
                password=password,
                email=email,
            )
            user.is_hr_manager = True
            user.save()
            # Create the company and link it to the user
            hr =  Hr_manger(
                user=user,  # Link the user to the company
                hr_name=hr_name,
                address=address,
                contact_number=contact_number,
                email=email,
                password=password,
                company=company
            )
            hr.save()
            return redirect('login_view')
        except IntegrityError:
            messages.error(request, 'An error occurred while registering the company.')
            return render(request, 'hrmangerform.html')

    # If GET request, render the registration form
    return render(request, 'hrmangerform.html')
def createmanager(request):
    cmpny=Company.objects.all()
    
    return render(request, 'mangerreg.html',{'cmpny':cmpny})




def register_manager(request):
    if request.method == 'POST':
        # Collect form data
        mngr_name = request.POST.get('mng_name')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        company_id = request.POST.get('companyname')

        # Get company object
        company = Company.objects.get(id=company_id) if company_id else None

        # Validate if the email already exists
        if Manger.objects.filter(email=email).exists():
            messages.error(request, 'Manager with this email already exists.')
            return redirect('register_manager')

        # Assuming CustomerUser is your custom user model
        User = CustomerUser

        try:
            # Create the user
            user = User.objects.create_user(
               
                first_name=mngr_name,
                username=email,
                password=password,
                email=email,
            )
            user.is_manager = True  # Set the manager role
            user.save()  # Corrected save() method call

            # Save manager details in the database
            manager = Manger(
                user=user,
                mngr_name=mngr_name,
                address=address,
                contact_number=contact_number,
                email=email,
                password=password,  # Password should ideally be hashed
                company=company,
            )
            manager.full_clean()  # Validate the model fields
            manager.save()

            messages.success(request, 'Manager registered successfully!')
            return redirect('login_view')  # Redirect to login page
        except ValidationError as e:
            messages.error(request, f"Error: {e}")
            return redirect('register_manager')

    # GET request - Display the registration form
    companies = Company.objects.all()
    return render(request, 'mangerreg.html', {'cmpny': companies})



def Employeecreate(request):
    total_employees = Employee.objects.count() + 1
    company_list = Company.objects.all()
    
    # Assuming you want to fetch all departments and roles regardless of the user
    department = Departments.objects.all()
    roles = Role.objects.all()
    
    return render(request, 'employee.html', {
        'total_employees': total_employees,
        'company': company_list,
        'department': department,
        'roles': roles
    })



def employeeadd(request):
    if request.method == 'POST':
        # Extract data from the POST request
        emp_name = request.POST.get('employeename')
        emp_id = request.POST.get('emp_id')
        address = request.POST.get('address')
        department_id = request.POST.get('department')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role_id = request.POST.get('role')
        joining_date_str = request.POST.get('join_date')
        salary = request.POST.get('salary')
        company_id = request.POST.get('company')
        
        # Validate required fields
        if not email or not password:
            return HttpResponse("Email and Password are required!", status=400)
        
        # Check if the email is unique
        if Employee.objects.filter(email=email).exists():
            return HttpResponse("Employee with this email already exists!", status=400)

        # Retrieve company and department
        try:
            company = Company.objects.get(id=company_id)
            department = Departments.objects.get(id=department_id)
        except (Company.DoesNotExist, Departments.DoesNotExist):
            return HttpResponse("Company or Department does not exist!", status=400)

        # Retrieve role
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return HttpResponse("Role does not exist!", status=400)

        # Create a new user
        try:
            user = CustomerUser.objects.create_user(
                first_name=emp_name,
                username=email,
                password=password,
                email=email,
            )
            user.is_employee = True
            user.save()
        except Exception as e:
            return HttpResponse(f"Error creating user: {e}", status=400)

        # Parse the joining date
        try:
            joining_date = datetime.strptime(joining_date_str, '%Y-%m-%d').date() if joining_date_str else None
        except ValueError:
            return HttpResponse("Invalid date format for joining_date!", status=400)

        # Create the Employee instance
        employee = Employee(
            user=user,
            emp_name=emp_name,
            emp_id=emp_id,
            address=address,
            department=department,  # Assign department instance
            email=email,
            password=password,
            role=role,  # Assign role instance
            joining_date=joining_date,
            salary=salary,
            company=company  # Assign company instance
        )

        # Save the employee instance
        try:
            employee.full_clean()  # Validate before saving
            employee.save()
            messages.success(request, 'Employee added successfully.')
            return redirect('/')  # Redirect to a success page or employee list
        except ValidationError as e:
            return HttpResponse(f"Validation error: {e.message_dict}", status=400)
        except Exception as e:
            return HttpResponse(f"Error saving employee: {e}", status=400)
    
    # If GET request, render the employee form
    # Fetch data needed for the form
    company = Company.objects.all()
    department = Departments.objects.all()
    roles = Role.objects.all()
    
    return render(request, 'employee.html')

def employee_edit(request, employee_id):
    user = request.user
    
    # Check if the user has the required role to access this page
    if not (user.is_admin or user.is_hr_manager or user.is_manager or user.is_employee):
        return HttpResponseForbidden("You do not have permission to edit employees.")
    
    # Fetch the employee object
    employee = get_object_or_404(Employee, id=employee_id)
    
    # Handle the case where no company is found for the user
    try:
        companies = Company.objects.filter(user=user)
        cmpny = companies.first()
    except Company.DoesNotExist:
        return HttpResponse("Company does not exist for the current user.", status=404)
    
    departments = Departments.objects.all()
    roles = Role.objects.all()
    
    if request.method == 'POST':
        # Extract data from the POST request
        emp_name = request.POST.get('employeename')
        emp_id = request.POST.get('emp_id')
        address = request.POST.get('address')
        department_id = request.POST.get('department')  # Now this will be an ID
        email = request.POST.get('email')
        password = request.POST.get('password')
        role_id = request.POST.get('role')
        joining_date_str = request.POST.get('join_date')
        salary = request.POST.get('salary')
        company_id = request.POST.get('company')

        # Fetch the corresponding Department and Role instances using their IDs
        try:
            department = Departments.objects.get(id=department_id)  # Use the ID to fetch department
        except Departments.DoesNotExist:
            return HttpResponse("Selected department does not exist!", status=400)
        
        try:
            role = Role.objects.get(id=role_id)  # Use the ID to fetch role
        except Role.DoesNotExist:
            return HttpResponse("Selected role does not exist!", status=400)
        
        # Update the user model if any relevant fields have changed
        employee_user = employee.user
        if emp_name:
            employee_user.first_name = emp_name
        if email:
            if CustomerUser.objects.filter(email=email).exclude(id=employee_user.id).exists():
                return HttpResponse("Another user with this email already exists!", status=400)
            employee_user.email = email
            employee_user.username = email  # Update username to email if needed
        
        if password:
            employee_user.set_password(password)  # Update password only if a new password is provided
        
        employee_user.save()

        # Update the employee instance
        employee.emp_name = emp_name
        employee.emp_id = emp_id
        employee.address = address
        employee.department = department  # Assign the correct Departments instance
        employee.email = email
        employee.password = password  # It's better not to store the raw password here
        employee.role = role  # Assign the Role instance
        employee.salary = salary
        
        # Parse the joining date if provided
        try:
            if joining_date_str:
                employee.joining_date = datetime.strptime(joining_date_str, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Invalid date format for joining_date!", status=400)
        
        # Check if the company exists and update the company
        try:
            company = Company.objects.get(id=company_id)
            employee.company = company
        except Company.DoesNotExist:
            return HttpResponse("Company does not exist!", status=400)

        # Validate and save the updated employee
        try:
            employee.full_clean()  # Validate before saving
            employee.save()
        except ValidationError as e:
            return HttpResponse(f"Validation error: {e.message_dict}", status=400)
        except Exception as e:
            return HttpResponse(f"Error saving employee: {e}", status=400)

        # Redirect to a success page (e.g., employee list or detail page)
        return redirect('employee_list')
    
    # If GET request, render the employee edit form with existing data
    return render(request, 'update_employee.html', {
        'employee': employee,
        'company': cmpny,
        'departments': departments,  # Pass the departments queryset
        'roles': roles  # Pass the roles queryset
    })

   

def delete_employee(request, employee_id):
    # Get the employee object
    employee = get_object_or_404(Employee, id=employee_id)

    # Check if it's a POST request (to confirm deletion)
    if request.method == 'POST':
        employee.delete()  # Deletes the employee object
        return redirect('employee_list')  # Redirect to the employee list after deletion
    
    return render(request, 'employee_list.html', {'employee': employee})

def employee_list(request):
    user = request.user

    # Check if the user is an Admin, HR Manager, or Manager
    try:
        if user.is_admin:
            # For Admins, get the company directly (assuming Admin is linked to a company)
            company = Company.objects.get(user=user)
        elif hasattr(user, 'hr_manger'):
            # For HR Managers, get the company through their HR manager record
            hr_manager = Hr_manger.objects.get(user=user)
            company = hr_manager.company
        elif hasattr(user, 'manger'):
            # For Managers, get the company through their Manager record
            manager = Manger.objects.get(user=user)
            company = manager.company
        else:
            messages.error(request, 'You do not have permission to view this page.')
            # return redirect('home')  # Redirect to a home page or another page as appropriate

        # Filter employees that belong to the user's company
        employees = Employee.objects.filter(company=company)

        return render(request, 'employee_list.html', {'employees': employees})

    except Company.DoesNotExist:
        messages.error(request, 'Company not found for this user.')
        return redirect('home')  # Redirect to a home page or another page as appropriate
    except Hr_manger.DoesNotExist:
        messages.error(request, 'No HR Manager record found for this user.')
        return redirect('home')
    except Manger.DoesNotExist:
        messages.error(request, 'No Manager record found for this user.')
        return redirect('home')



def department(request):
    user = request.user
    company = None
    departments = None

    try:
        # Check the user's role and get the associated company
        if hasattr(user, 'hr_manger'):
            # HR Manager
            hr_manager = Hr_manger.objects.get(user=user)
            company = hr_manager.company
        elif user.is_admin:
            # Admin
            company = Company.objects.get(user=user)
        elif hasattr(user, 'manger'):
            # Manager
            manager = Manger.objects.get(user=user)
            company = manager.company
        else:
            return HttpResponseForbidden("You do not have permission to view this page.")
        
        # Fetch departments associated with the company
        departments = Departments.objects.filter(company=company)
    
    except Company.DoesNotExist:
        return HttpResponseForbidden("No company associated with this user.")
    except Hr_manger.DoesNotExist:
        return HttpResponseForbidden("No HR Manager found for this user.")
    except Manger.DoesNotExist:
        return HttpResponseForbidden("No Manager found for this user.")

    # Fetch all users associated with the company
    all_users = CustomerUser.objects.filter(company=company)
    admins = all_users.filter(is_admin=True)
    hr_managers = all_users.filter(is_hr_manager=True)
    managers = all_users.filter(is_manager=True)
    employees = all_users.filter(is_employee=True)
    
    context = {
        'company': company,
        'departments': departments,
        'admins': admins,
        'hr_managers': hr_managers,
        'managers': managers,
        'employees': employees,
    }

    return render(request, 'department.html', context)
   



def add_department(request):
    
    
    if request.method == 'POST':
        print('post')
        department_name = request.POST.get('department')  # Fetch department name
        company_id = request.POST.get('company')  # Fetch selected company ID
        
        # Get the selected company instance
        company = Company.objects.get(id=company_id)
        
        # Create and save the new department with the current user
        department = Departments(name=department_name, company=company, user=request.user)
        department.save()

        return redirect('department')  # Redirect after saving the department

    return render(request, 'department.html')


def roles(request):
    user = request.user  # Get the current logged-in user

    company = None

    try:
        # Determine the user's role and fetch the associated company
        if hasattr(user, 'hr_manger'):
            # HR Manager
            hr_manager = Hr_manger.objects.get(user=user)
            company = hr_manager.company
        elif user.is_admin:
            # Admin
            company = Company.objects.get(user=user)
        elif user.is_manager:  # Correct spelling for 'manger'
            # Manager
            print(f"User {user} is a manager.")  # Debugging output
            manager = Manger.objects.get(user=user)
            company = manager.company
            print(company)

        if company:
            departments = Departments.objects.filter(company=company)
            all_users = CustomerUser.objects.filter(company=company)
            admins = all_users.filter(is_admin=True)
            hr_managers = all_users.filter(is_hr_manager=True)
            managers = all_users.filter(is_manager=True)
            employees = all_users.filter(is_employee=True)
        else:
            messages.error(request, 'No company associated with this user.')
            return redirect('/')

    except (Company.DoesNotExist, Hr_manger.DoesNotExist, Manger.DoesNotExist) as e:
        messages.error(request, str(e))
        return redirect('/')

    context = {
        'company': company,
        'departments': departments,
        'admins': admins,
        'hr_managers': hr_managers,
        'managers': managers,
        'employees': employees,
    }

    return render(request, 'roles.html', context)


def add_roles(request):
    if request.method == 'POST':
        company_id = request.POST.get('company')
        department_id = request.POST.get('department')
        role_name = request.POST.get('role')
        
        print(f"Company ID: {company_id}, Department ID: {department_id}, Role: {role_name}")
        
        try:
            # Fetch the company and department from the database
            company = Company.objects.get(id=company_id)
            department = Departments.objects.get(id=department_id)

            # Debug prints
            print(f"Company: {company}, Department: {department}, Role Name: {role_name}")

            # Create and save the new role
            role = Role(name=role_name, company=company, department=department, user=request.user)
            role.save()
            
            messages.success(request, 'Role added successfully.')
            return redirect('roles')
        except Company.DoesNotExist:
            messages.error(request, 'Selected company does not exist.')
        except Departments.DoesNotExist:
            messages.error(request, 'Selected department does not exist.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'role.html')


def attendancepage(request):
    user = request.user

    print(f"Logged-in user: {user}")  # Debug output

    try:
        # Fetch the employee for the logged-in user
        employee = Employee.objects.get(user=user)  # Assuming one employee per user

        # Get the company from the employee instance
        company = employee.company
        print(f"Company for employee: {company}")  # Debug output

        # Fetch all employees in the same company
        employees = Employee.objects.filter(company=company)
        print(f"Employees in the company: {employees}")  # Debug output

    except Employee.DoesNotExist:
        # Handle the case when the employee or company does not exist
        return HttpResponse("Employee does not exist for the current user.", status=404)

    return render(request, 'attendance.html', {'employee': employees})
def track_attendance(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_name')
        clock_in = request.POST.get('clock_in')
        clock_out = request.POST.get('clock_out')
        date = request.POST.get('date')

        # Convert string to datetime if needed
        clock_in_datetime = parse_datetime(clock_in) if clock_in else None
        clock_out_datetime = parse_datetime(clock_out) if clock_out else None
        date_datetime = parse_datetime(date) if date else None
        user=request.user
        employee=Employee.objects.get(user=user)
        company = employee.company
        try:
            employee = Employee.objects.get(id=emp_id)
        except Employee.DoesNotExist:
            # Handle employee not found case
            return HttpResponse("Employee not found.", status=404)

        # Create and save the attendance record
        attendance = Attendance(
            employee=employee,
            clock_in=clock_in_datetime,
            clock_out=clock_out_datetime,
            date=date_datetime,
            company=company
        )
        attendance.save()

        return redirect('attendancepage')  # Redirect to a report page or success page

    else:
        # Provide the form with employee choices
        
        return render(request, 'attendance.html')
    

def attendance_list(request):
    

    attendance=Attendance.objects.all()
    return render(request, 'attendance_list.html',{'attendance':attendance})
@login_required
def Leave(request):
    user = request.user

    print(f"Logged-in user: {user}")  # Debug output

    try:
        # Fetch the employee for the logged-in user
        employee = Employee.objects.get(user=user)  # Assuming one employee per user

        # Get the company from the employee instance
        company = employee.company
        print(f"Company for employee: {company}")  # Debug output

        # Fetch all employees in the same company
        employees = Employee.objects.filter(company=company)
        print(f"Employees in the company: {employees}")  # Debug output

    except Employee.DoesNotExist:
        # Handle the case when the employee or company does not exist
        return HttpResponse("Employee does not exist for the current user.", status=404)

    return render(request, 'leave.html', {'employee': employees})


def leave_application(request):
    if request.method == 'POST':
        # Extract the data from the POST request
        employee_id = request.POST.get('emp_name')
        start_date = request.POST.get('Fromdate')
        end_date = request.POST.get('todate')
        reason = request.POST.get('reason')

        # Fetch the related employee instance
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            # Handle the case where the employee does not exist
            return render(request, 'leave_application.html', {
                'error': 'Invalid employee selected',
                'employees': Employee.objects.all()
            })

        # Assuming company is linked to employee, fetch the company from employee
        try:
            company = employee.company  # Assuming Company is related to Employee
        except Company.DoesNotExist:
            return render(request, 'leave_application.html', {
                'error': 'Company does not exist for the selected employee',
                'employees': Employee.objects.all()
            })

        # Create a new leave request object and save it
        leave_request = LeaveRequest(
            employee=employee,
            company=company,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status='Pending'  # Default status as pending
        )
        leave_request.save()

        # Redirect to a success page or some other relevant page
        return redirect('profile')  # Replace with your success URL

    # If the request is GET, render the form
    return render(request, 'leave.html', {
        'employees': Employee.objects.all()  # Replace with actual employee queryset
    })


def leavelist(request):
    user = request.user
    employee =Employee.objects.get(user=user)
    company=employee.company
    
    # Get all employees belonging to the company
    employees = Employee.objects.filter(company=company)
    
    # Get the list of employee IDs
    employee_ids = employees.values_list('id', flat=True)
    
    # Filter leave requests for employees in the company
    leave_requests = LeaveRequest.objects.filter(employee__in=employee_ids)
    
    return render(request, 'leavelist.html', {'leave': leave_requests,'employee':employee})


def leavelist_approval(request):
    user = request.user  # Get the current logged-in user
    leave_requests = None

    try:
        if hasattr(user, 'hr_manger'):
            # HR Manager: Can view all leave requests for their company
            hr_manager = Hr_manger.objects.get(user=user)
            company = hr_manager.company
            employees = Employee.objects.filter(company=company)
            leave_requests = LeaveRequest.objects.filter(employee__in=employees)
        
        elif user.is_admin:
            # Admin: Can view all leave requests for their company
            company = Company.objects.get(user=user)
            employees = Employee.objects.filter(company=company)
            leave_requests = LeaveRequest.objects.filter(employee__in=employees)
        
        elif hasattr(user, 'manger'):
            # Manager: Can only view leave requests of employees in their department
            manager = Manger.objects.get(user=user)
            company = manager.company
            employees = Employee.objects.filter(company=company)
            leave_requests = LeaveRequest.objects.filter(employee__in=employees)
        
        else:
            # If the user doesn't have any of the above roles, deny access
            return HttpResponseForbidden("You do not have permission to view this page.")

    except (Company.DoesNotExist, Hr_manger.DoesNotExist, Manger.DoesNotExist) as e:
        messages.error(request, str(e))
        return redirect('/')

    # Render the leave request page with the filtered leave requests
    return render(request, 'leavelist_approved.html', {'leave': leave_requests})

def update_leave_status(request, leave_id):
    if request.method == 'POST':
        # Get the leave request object
        leave_request = get_object_or_404(LeaveRequest, id=leave_id)
        
        # Get the new status from the form
        new_status = request.POST.get('status')
        if new_status in ['Approved', 'Rejected']:
            leave_request.status = new_status
            leave_request.save()
        
        # Redirect back to the leave list page after the update
        return redirect('leavelist_approval')  
    

def dashboard_view(request):
    # Key metrics
    total_employees = Employee.objects.count()
    total_leaves = LeaveRequest.objects.count()
    total_attendance = Attendance.objects.count()

    # Calculate attendance status (Present if clock_in and clock_out exist)
    present_count = Attendance.objects.filter(clock_in__isnull=False, clock_out__isnull=False).count()
    absent_count = total_attendance - present_count  # Assume absent if no clock_in/clock_out

    # Leave status breakdown (Approved, Pending, Rejected)
    leave_status_data = LeaveRequest.objects.values('status').annotate(total=Count('status'))

    context = {
        'total_employees': total_employees,
        'total_leaves': total_leaves,
        'total_attendance': total_attendance,
        'attendance_data': [{'status': 'Present', 'total': present_count}, {'status': 'Absent', 'total': absent_count}],
        'leave_status_data': list(leave_status_data),
    }

    return render(request, 'dashboard.html', context)



def profile(request):
    user = request.user
    try:
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        employee = None
    return render(request, 'profile.html', {'employee': employee})

def genicpage(request):
    return render(request, 'genicpage.html')
def logout_view(request):
    logout(request)  # This logs the user out
    return redirect('login_view') 

def employee_profile(request,pk):
    
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employeeprofile.html', {'employee': employee})
    # user = request.user

    # # Get the company associated with the logged-in user
    # try:
    #     company = Company.objects.get(user=user)
    # except Company.DoesNotExist:
    #     return render(request, 'employeeprofile.html', {'message': 'Company not found.'})

    # # Get the employee details based on the company and user
    # try:
    #     employee = Employee.objects.get(company=company, user=user, pk=pk)
    # except Employee.DoesNotExist:
    #     return render(request, 'employeeprofile.html', {'message': 'Employee not found.'})

    # # Pass employee details to the template
    # context = {
    #     'employee': employee,
    # }

    # return render(request, 'employeeprofile.html', context)




