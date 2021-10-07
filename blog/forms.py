from django import forms
from django.forms import ModelForm, CharField, TextInput
from .models import Post, JobModel, CustomerModel, OrderModel, TimesheetModel, AnnouncementModel, TaskModel, ProductModel, EmployeeModel, OrderlineModel, JobassignmentModel, JobcomplaintModel
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from django.core.validators import RegexValidator, MaxLengthValidator
import pyodbc

# -------------------------------------------------------------
# SQL CONNECTION
# -------------------------------------------------------------
def connection_init():
    #connection = pyodbc.connect(driver='ODBC Driver 17 for SQL Server', server='COLEPC-RTX', database='development_database', trusted_connection='yes', uid='test', password='testPass!@123')
    connection = pyodbc.connect(driver='ODBC Driver 17 for SQL Server', server='172.26.54.36', database='CyltexDB', trusted_connection='no', uid='test', password='testPass!@123')
    return connection
    
def connection_cursor_init(connection):
    cursor = connection.cursor()
    return cursor

def connection_query(connection, cursor, str):
    iterator = cursor.execute(str)
    result = iterator.fetchall()
    return result

def close_connections(connection, cursor):
    cursor.close()
    connection.rollback()

# -------------------------------------------------------------
# SQL EMPLOYEE
# -------------------------------------------------------------
def SQL_get_all_employees():
    str = "SELECT Employee_ID FROM Employee"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
# -------------------------------------------------------------
# SQL CUSTOMER
# -------------------------------------------------------------
def SQL_get_all_customers():
    str = "SELECT Customer_ID, CompanyName FROM Customer"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query

# -------------------------------------------------------------
# SQL STATE
# -------------------------------------------------------------
def SQL_get_all_states():
    str = "SELECT State_ID, State_Name FROM StateProvince"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query

# -------------------------------------------------------------
# SQL COUNTRY
# -------------------------------------------------------------
def SQL_get_all_countries():
    str = "SELECT Country_ID,Country_Name FROM dbo.Country"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query

# -------------------------------------------------------------
# SQL TASK
# -------------------------------------------------------------
def SQL_get_all_task_status():
    str = "SELECT * FROM TaskStatus"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_jobcomplaint_status():
    str = "SELECT * FROM JobComplaintStatus"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query

def SQL_get_all_task_priority():
    str = "SELECT * FROM TaskPriority"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query

# -------------------------------------------------------------
# SQL PRODUCT
# -------------------------------------------------------------
def SQL_get_all_product_status():
    str = "SELECT * FROM ProductStatus"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query

def SQL_get_all_product_priority():
    str = "SELECT * FROM ProductPriority"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
# -------------------------------------------------------------
# SQL JOB
# -------------------------------------------------------------
def SQL_get_all_employee_jobs(id):
    str = "SELECT Job_ID FROM EmployeeJobAssignment WHERE Employee_ID = {}".format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_jobs():
    str = "SELECT Job_ID FROM Job"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_jobs_active():
    str = "SELECT Job_ID FROM Job WHERE Job.JobStatus_ID != 2"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]

def SQL_get_all_job_complaints():
    str = "SELECT JobComplaint_ID FROM JobComplaint"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_job_status():
    str = "SELECT * FROM JobStatus"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_jobass_status():
    str = "SELECT * FROM EmployeeJobAssignment_Status"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_orders():
    str = "SELECT Order_ID FROM Order_"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_products():
    str = "SELECT Product_ID, ProductName FROM Product"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
# -------------------------------------------------------------
# SQL EMPLOYEE
# -------------------------------------------------------------
def SQL_get_all_job_titles():
    str = "SELECT JobTitle_ID,EmployeeTitle FROM JobTitle"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_departments():
    str = "SELECT * FROM EmployeeDepartment"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_pay_rates():
    str = "SELECT * FROM EmployeePayRate"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_employee_types():
    str = "SELECT * FROM EmployeeType"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_employee_status():
    str = "SELECT * FROM EmployeeStatus"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query

def SQL_get_all_employee_id():
    str = "SELECT Employee_ID FROM Employee"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
# -------------------------------------------------------------
# SQL TIMESHEET ENTRY
# -------------------------------------------------------------
def SQL_get_all_timesheet_entry_status():
    str = "SELECT * FROM TimesheetEntry_LineStatus"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_announcement_status():
    str = "SELECT * FROM AnnouncementStatus"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_announcement_priority():
    str = "SELECT * FROM AnnouncementPriority"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_product_category():
    str = "SELECT ProductCategory_ID, ProductCategory_Name FROM ProductCategory"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_customer_status():
    str = "SELECT * FROM CustomerStatus"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_customer_priority():
    str = "SELECT * FROM CustomerPriority"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_order_status():
    str = "SELECT * FROM OrderStatus"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_order_priority():
    str = "SELECT * FROM OrderPriority"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_orderline_status():
    str = "SELECT * FROM OrderLine_Status"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_orderline_priority():
    str = "SELECT * FROM OrderLine_Priority"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query


#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO#
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO#
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO#


# -------------------------------------------------------------
# FORM TIMESHEET
# -------------------------------------------------------------
class Timesheet(forms.ModelForm):
    title = forms.CharField()
    project_num = forms.ChoiceField(choices=tuple(zip(SQL_get_all_jobs(),SQL_get_all_jobs())), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    #project_num = forms.ChoiceField(widget=forms.Select(choices=[], attrs={'style': 'width:120px; height:30px'}))
    time_start = forms.TimeField()
    time_end = forms.TimeField()
    status = forms.ChoiceField(choices=(SQL_get_all_timesheet_entry_status()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}), initial=1)
    sheet_id = forms.CharField(widget=forms.NumberInput(attrs={'style': 'width:120px; height:30px;'}))
    employee_id = forms.CharField(widget=forms.NumberInput(attrs={'style': 'width:120px; height:30px;'}))
    
    class Meta:
        model = TimesheetModel
        fields = ('title', 'project_num', 'time_start', 'time_end', 'status', 'sheet_id', 'employee_id')
    
    def __init__(self,*args,**kwargs):
        super(Timesheet, self).__init__(*args, **kwargs)
        self.fields['title'].disabled = True
        self.fields['title'].initial = 'Timesheet'
        self.fields['sheet_id'].disabled = False
        self.fields['employee_id'].disabled = False
        self.fields['project_num'].required = True

class Announcement(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    status = forms.ChoiceField(choices=(SQL_get_all_announcement_status()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    priority = forms.ChoiceField(choices=(SQL_get_all_announcement_priority()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    
    class Meta:
        model = AnnouncementModel
        fields = ('title', 'content', 'status', 'priority')
    
    def __init__(self, *args, **kwargs):
        super(Announcement, self).__init__(*args, **kwargs)
        #self.fields['title'].disabled = True
        self.fields['title'].initial = 'Announcement'

class Product(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    category_id = forms.ChoiceField(choices=(SQL_get_all_product_category()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    status = forms.ChoiceField(choices=(SQL_get_all_product_status()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    
    class Meta:
        model = ProductModel
        fields = ('name', 'description', 'status', 'category_id')
    
    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)

class Task(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    employee_id = forms.ChoiceField(choices=tuple(zip(SQL_get_all_employees(),SQL_get_all_employees())), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    job_id = forms.ChoiceField(choices=tuple(zip(SQL_get_all_jobs(),SQL_get_all_jobs())), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    startDate = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'style':  'height:31px'}))
    dueDate = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'style':  'height:31px'}))
    status = forms.ChoiceField(choices=(SQL_get_all_task_status()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    priority = forms.ChoiceField(choices=(SQL_get_all_task_priority()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    
    class Meta:
        model = TaskModel
        fields = ('title', 'dueDate', 'content', 'status', 'priority', 'job_id', 'startDate', 'employee_id')
    
    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.fields['title'].disabled = True
        self.fields['title'].initial = 'Task Assignment'

class Jobcomplaint(forms.ModelForm):
    job_id = forms.ChoiceField(choices=tuple(zip(SQL_get_all_jobs_active(),SQL_get_all_jobs_active())), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    detail = forms.CharField(widget=forms.Textarea)
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'style':  'height:31px'}))
    status = forms.ChoiceField(choices=(SQL_get_all_jobcomplaint_status()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    
    class Meta:
        model = JobcomplaintModel
        fields = ('job_id', 'detail', 'date', 'status')
    
    def __init__(self, *args, **kwargs):
        super(Jobcomplaint, self).__init__(*args, **kwargs)

class Job(forms.ModelForm):
    budget = forms.FloatField()
    jobCustomer = forms.ChoiceField(choices=(SQL_get_all_customers()), widget=forms.Select(attrs={'style': 'width:220px; height:30px'}))
    #description = forms.CharField(widget=forms.Textarea)
    description = forms.CharField(widget=forms.Textarea)
    status = forms.ChoiceField(choices=(SQL_get_all_job_status()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    budget.widget.attrs.update({'type': 'number', 'step' : '0.01', 'pattern' : '[0-9]{4}'})
    
    class Meta:
        model = JobModel
        fields = ('title', 'budget', 'jobCustomer', 'description', 'status')
    
    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.fields['title'].disabled = True
        self.fields['title'].initial = 'New Job'

class Customer(forms.ModelForm):
    fName = forms.CharField()
    lName = forms.CharField()
    companyName = forms.CharField()
    phoneNumber = forms.CharField()
    corpAddressLine1 = forms.CharField()
    corpAddressLine2 = forms.CharField(required=False)
    corpCity = forms.CharField()
    corpState = forms.ChoiceField(choices=(SQL_get_all_states()))
    status = forms.ChoiceField(choices=(SQL_get_all_customer_status()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    priority = forms.ChoiceField(choices=(SQL_get_all_customer_priority()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    corpZipcode = forms.CharField()
    
    class Meta:
        model = CustomerModel
        fields = ('title', 'fName', 'lName', 'companyName', 'phoneNumber', 'corpAddressLine1', 'corpAddressLine2', 'corpCity', 'corpState', 'status', 'priority', 'corpZipcode')
    
    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)
        self.fields['title'].disabled = True
        self.fields['title'].initial = 'New Customer'

class Employee(forms.ModelForm):
    firstName = forms.CharField()
    lastName = forms.CharField()
    email = forms.CharField()
    phoneNumber = forms.CharField()
    addressLine1 = forms.CharField()
    addressLine2 = forms.CharField(required=False)
    city = forms.CharField()
    state = forms.ChoiceField(choices=(SQL_get_all_states()), widget=forms.Select(attrs={'style': 'width:180px; height:30px'}))
    zipcode = forms.CharField()
    job_title = forms.ChoiceField(choices=(SQL_get_all_job_titles()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    pay_rate = forms.ChoiceField(choices=(SQL_get_all_pay_rates()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    status = forms.ChoiceField(choices=(SQL_get_all_employee_status()), widget=forms.Select(attrs={'style': 'width:108px; height:30px'}))
    type = forms.ChoiceField(choices=(SQL_get_all_employee_types()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    
    class Meta:
        model = EmployeeModel
        fields = ('firstName', 'lastName', 'email', 'phoneNumber', 'addressLine1', 'addressLine2', 'city', 'state', 'zipcode', 'pay_rate', 'status', 'type', 'job_title')
    
    def __init__(self, *args, **kwargs):
        super(Employee, self).__init__(*args, **kwargs)

class DateInput(forms.DateInput):
    input_type = 'date'
    
class Order(forms.ModelForm):
    dueDate = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    job_id = forms.ChoiceField(choices=tuple(zip(SQL_get_all_jobs(),SQL_get_all_jobs())), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    status = forms.ChoiceField(choices=(SQL_get_all_order_status()), widget=forms.Select(attrs={'style': 'width:160px; height:30px'}))
    priority = forms.ChoiceField(choices=(SQL_get_all_order_priority()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    
    class Meta:
        model = OrderModel
        fields = ('dueDate', 'job_id', 'status', 'priority')
    
    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        
class Orderline(forms.ModelForm):
    order_id = forms.CharField(widget=forms.NumberInput(attrs={'style': 'width:80px; height:30px;'}))
    product_id = forms.ChoiceField(choices=(SQL_get_all_products()), widget=forms.Select(attrs={'style': 'width:220px; height:30px'}))
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'style': 'width:120px; height:30px;'}))
    price = forms.CharField(widget=forms.NumberInput(attrs={'style': 'width:120px; height:30px;'}))
    status = forms.ChoiceField(choices=(SQL_get_all_orderline_status()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    priority = forms.ChoiceField(choices=(SQL_get_all_orderline_priority()), widget=forms.Select(attrs={'style': 'width:120px; height:30px'}))
    
    class Meta:
        model = OrderlineModel
        fields = ('order_id', 'product_id', 'quantity', 'price', 'priority', 'status')
    
    def __init__(self, *args, **kwargs):
        super(Orderline, self).__init__(*args, **kwargs)
        
class Jobassignment(forms.ModelForm):
    employee_id = forms.ChoiceField(choices=tuple(zip(SQL_get_all_employees(),SQL_get_all_employees())), widget=forms.Select(attrs={'style': 'width:80px; height:30px;'}))
    job_id = forms.ChoiceField(choices=tuple(zip(SQL_get_all_jobs(),SQL_get_all_jobs())), widget=forms.Select(attrs={'style': 'width:80px; height:30px;'}))
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'style':  'height:31px'}))
    status = forms.ChoiceField(choices=(SQL_get_all_jobass_status()), widget=forms.Select(attrs={'style': 'width:108px; height:30px'}))
    
    class Meta:
        model = JobassignmentModel
        fields = ('employee_id', 'job_id', 'date', 'status')
    
    def __init__(self, *args, **kwargs):
        super(Jobassignment, self).__init__(*args, **kwargs)