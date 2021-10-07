from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from datetime import date
import pyodbc

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

def SQL_get_all_states():
    str = "SELECT * FROM StateProvince"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query

def SQL_get_all_countries():
    str = "SELECT Country_ID,Country_Name FROM dbo.Country"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
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
    str = "SELECT Customer_ID,CompanyName FROM Customer"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query

# -------------------------------------------------------------
# SQL STATE
# -------------------------------------------------------------
def SQL_get_all_states():
    str = "SELECT * FROM StateProvince"
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
def SQL_get_all_jobs():
    str = "SELECT Job_ID FROM Job"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_jobcomplaints():
    str = "SELECT JobComplaint_ID FROM JobComplaint"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]

# -------------------------------------------------------------
# SQL EMPLOYEE
# -------------------------------------------------------------
def SQL_get_all_job_titles():
    str = "SELECT * FROM JobTitle"
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
    
def SQL_get_all_timesheets():
    str = "SELECT TimesheetEntry_Line_ID FROM TimesheetEntry_Line"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_announcements():
    str = "SELECT Announcement_ID FROM Announcement"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_products():
    str = "SELECT Product_ID FROM Product"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_orders_id():
    str = "SELECT Order_ID FROM Order_"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_orderlines_id():
    str = "SELECT OrderLine_ID FROM Order_Line"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_jobassignments_id():
    str = "SELECT EmployeeJobAssignment_ID FROM EmployeeJobAssignment"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_tasks():
    str = "SELECT Task_ID FROM Task"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_customers_id():
    str = "SELECT Customer_ID FROM Customer"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_employees_id():
    str = "SELECT Employee_ID FROM Employee"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    
    #--- Announcement Models ---#
    content = models.TextField(null=True)
    
    #--- Timesheet Models ---#
    content_projectNum = models.FloatField(default=1234.21)
    content_timeStart = models.TimeField(default='01:00')
    content_timeEnd = models.TimeField(default='01:00')
    content_totalHours = models.FloatField(default=0.15)
    
    #--- Task Models ---#
    #content_userID = models.CharField(max_length=100,choices=SQL_get_all_employees())
    content_userID = models.CharField(max_length=100)
    
    date_posted = models.DateTimeField(default=timezone.localtime)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts_likes')
    dislikes = models.ManyToManyField(User, related_name='blog_posts_dislikes')

    def total_likes(self):
        return self.likes.count()
        
    def total_dislikes(self):
        return self.dislikes.count()
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_total_hours(self):
        end_minutes = self.content_timeEnd.hour*60 + self.content_timeEnd.minute
        start_minutes = self.content_timeStart.hour*60 + self.content_timeStart.minute
        return round((end_minutes - start_minutes)/60, 2)

class AnnouncementModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True)
    status = models.CharField(default='1',max_length=100)
    priority = models.CharField(default='1',max_length=100)
    date_posted = models.DateTimeField(default=timezone.localtime)
    
    
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('announcement-detail-sql', kwargs={'pk': SQL_get_all_announcements()[-1]})

class ProductModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    status = models.CharField(max_length=100)
    category_id = models.CharField(default='1',max_length=100)
    date_posted = models.DateTimeField(default=timezone.localtime)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('product-detail-sql', kwargs={'pk': SQL_get_all_products()[-1]})
        
class TaskModel(models.Model):
    title = models.CharField(max_length=100)
    employee_id = models.CharField(default='1', max_length=100)
    job_id = models.CharField(default='1',max_length=100)
    startDate = models.DateTimeField(default=timezone.localtime)
    dueDate = models.DateTimeField(default=timezone.localtime)
    status = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    content = models.TextField(null=True)
    date_posted = models.DateTimeField(default=timezone.localtime)
    
    
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('task-detail-sql', kwargs={'pk': SQL_get_all_tasks()[-1]})

class TimesheetModel(models.Model):
    title = models.CharField(max_length=100)
    project_num = models.CharField(max_length=100)
    time_start = models.TimeField(default='01:00')
    time_end = models.TimeField(default='01:00')
    status = models.CharField(default='1', max_length=100)
    sheet_id = models.CharField(default='1', max_length=100)
    employee_id = models.CharField(default='1', max_length=100)
    #date_posted = models.DateTimeField(default=date.today())
    
    
    class Meta:
        verbose_name = 'Timesheet'
        verbose_name_plural = 'Timesheets'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('timesheet-detail-sql', kwargs={'pk': SQL_get_all_timesheets()[-1]})
        
    def get_total_hours(self):
        end_minutes = self.time_end.hour*60 + self.time_end.minute
        start_minutes = self.time_start.hour*60 + self.time_start.minute
        return round((end_minutes - start_minutes)/60, 2)
        
class CustomerModel(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.localtime)
    fName = models.CharField(max_length=100)
    lName = models.CharField(max_length=100)
    companyName = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=15, blank=True)
    priority = models.CharField(default='1', max_length=100)
    status = models.CharField(default='1', max_length=100)
    corpAddressLine1 = models.CharField(max_length=100)
    corpAddressLine2 = models.CharField(max_length=100)
    corpCity = models.CharField(max_length=100)
    corpState = models.IntegerField()
    corpZipcode = models.CharField(default='1', max_length=100)
    
    
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('customer-detail-sql', kwargs={'pk': SQL_get_all_customers_id()[-1]})
    
    def state_value_display(self):
        for c in SQL_get_all_states():
            if c[0] == self.corpState:
                return c[1]
    
    def country_value_display(self):
        for c in SQL_get_all_countries():
            if c[0] == self.corpCountry:
                return c[1]
    
    def phone_formatted(self):
        return ('({}) {}-{}'.format(self.phoneNumber[:3],self.phoneNumber[3:6],self.phoneNumber[6:]))

class EmployeeModel(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=15, blank=True)
    addressLine1 = models.CharField(max_length=100)
    addressLine2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.IntegerField()
    zipcode = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    pay_rate = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    
    def __str__(self):
        return ('{} {}'.format(self.firstName,self.lastName))
    
    def get_absolute_url(self):
        return reverse('employee-detail-sql', kwargs={'pk': SQL_get_all_employees_id()[-1]})
    
    def state_value_display(self):
        for c in SQL_get_all_states():
            if c[0] == self.state:
                return c[1]
    
    def country_value_display(self):
        for c in SQL_get_all_countries():
            if c[0] == self.country:
                return c[1]
    
    def phone_formatted(self):
        return ('({}) {}-{}'.format(self.phoneNumber[:3],self.phoneNumber[3:6],self.phoneNumber[6:]))

class OrderModel(models.Model):
    dueDate = models.DateField()
    job_id = models.CharField(default='1', max_length=100)
    priority = models.CharField(default='1', max_length=100)
    status = models.CharField(default='1', max_length=100)
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('order-detail-sql', kwargs={'pk': SQL_get_all_orders_id()[-1]})
        
class OrderlineModel(models.Model):
    order_id = models.CharField(default='1', max_length=100)
    product_id = models.CharField(default='1', max_length=100)
    quantity = models.CharField(default='1', max_length=100)
    price = models.CharField(default='1', max_length=100)
    priority = models.CharField(default='1', max_length=100)
    status = models.CharField(default='1', max_length=100)
    
    class Meta:
        verbose_name = 'Orderline'
        verbose_name_plural = 'Orderlines'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('orderline-detail-sql', kwargs={'pk': SQL_get_all_orderlines_id()[-1]})
        
class JobassignmentModel(models.Model):
    employee_id = models.CharField(default='1', max_length=100)
    job_id = models.CharField(default='1', max_length=100)
    date = models.DateField()
    status = models.CharField(default='1', max_length=100)
    
    class Meta:
        verbose_name = 'Job Assignment'
        verbose_name_plural = 'Job Assignments'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('jobass-detail-sql', kwargs={'pk': SQL_get_all_jobassignments_id()[-1]})

class JobModel(models.Model):
    title = models.CharField(max_length=100)
    budget = models.FloatField(default='')
    description = models.CharField(default='1', max_length=1024)
    date_posted = models.DateTimeField(default=timezone.localtime)
    jobCustomer = models.IntegerField()
    status = models.CharField(default='1', max_length=100)
    orders = models.ManyToManyField(OrderModel, related_name='job_orders')
    
    
    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('job-detail-sql', kwargs={'pk': SQL_get_all_jobs()[-1]})
        
    def total_orders(self):
        return self.orders.count()
        
    def customer_value_display(self):
        for c in SQL_get_all_customers():
            if c[0] == self.jobCustomer:
                return c[1]
                
class JobcomplaintModel(models.Model):
    job_id = models.CharField(default='1', max_length=100)
    detail = models.CharField(default='1', max_length=100)
    date = models.DateTimeField(default=timezone.localtime)
    status = models.CharField(default='1', max_length=100)
    
    class Meta:
        verbose_name = 'Job Complaint'
        verbose_name_plural = 'Job Complaints'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('jobcomplaint-detail-sql', kwargs={'pk': SQL_get_all_jobcomplaints()[-1]})
        
    def total_orders(self):
        return self.orders.count()