from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
import pyodbc
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import Job, Customer, Order, Timesheet, Announcement, Task, Product, Employee, Orderline, Jobassignment, Jobcomplaint
from .models import Post, JobModel, CustomerModel, OrderModel, OrderlineModel, TimesheetModel, AnnouncementModel, TaskModel, ProductModel, EmployeeModel, JobassignmentModel, JobcomplaintModel
from django.db.models.functions import Concat
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext 
from django.shortcuts import render
from .sql_methods import *
import csv
from datetime import datetime
from django.contrib import messages
import datetime


# ------------------------------------------------------------- #
#                     CONNECTION METHODS                        #
# ------------------------------------------------------------- #
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

# ------------------------------------------------------------- #
#                      HAIL MARY METHODS                        #
# ------------------------------------------------------------- #     
def SQL_get_timesheet_by_id(id):
    str = "SELECT * FROM Timesheet WHERE Timesheet_ID = {0}".format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]
    
def SQL_get_all_timesheet_byID(id):
    str = "SELECT * FROM TimesheetEntry_Line WHERE Employee_ID = {}".format(id)
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
    
# ------------------------------------------------------------- #
#                             END                               #
# ------------------------------------------------------------- #

def SQL_get_all_timesheet_entry_ids():
    str = "SELECT TimesheetEntry_Line_ID FROM TimesheetEntry_Line"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query  

#@login_required(login_url='login')
def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    
    return render(request, 'blog/home.html', context)
    
def portal_view(request):
    context = {
        
    }
    
    return render(request, 'blog/portalSelect.html', context)
    
def home_employee_view(request):
    if 'global_id' in request.session:
        my_id = request.session['global_id']
    else:
        my_id = 1
    object_list = SQL_get_timesheet_entry_employee_id(my_id)
    page = request.GET.get('page', 1)
    employee = SQL_get_employee_by_id(my_id)
    
    paginator = Paginator(object_list, 12)
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/home_employee.html', { 'entries': entries, 'current_title': 'Timesheet Entries: ', 'employee': employee, 'my_id': my_id})
    
def home_admin_view(request):
    if 'global_id' in request.session:
        my_id = request.session['global_id']
    else:
        my_id = 1
    object_list = SQL_get_timesheet_entry_employee_id(my_id)
    page = request.GET.get('page', 1)
    employee = SQL_get_employee_by_id(my_id)

    paginator = Paginator(object_list, 12)
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/home.html', { 'entries': entries, 'current_title': 'Timesheet Entries: ', 'employee': employee, 'my_id': my_id})

class all_jobs(ListView):
    model = Post
    template_name = 'blog/all_jobs.html'
    context_object_name = 'jobs'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_jobs, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Jobs'
        return context
    
    def get_queryset(self):
        return JobModel.objects.filter().order_by('-date_posted')

class all_orders(ListView):
    model = Post
    template_name = 'blog/all_orders.html'
    context_object_name = 'orders'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_orders, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Orders'
        return context
    
    def get_queryset(self):
        return OrderModel.objects.filter().order_by('-date_posted')

class all_customers(ListView):
    model = Post
    template_name = 'blog/all_customers.html'
    context_object_name = 'customers'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_customers, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Customers'
        #context['customers'] = SQL_get_all_customers()
        return context
    
    def get_queryset(self):
        return CustomerModel.objects.filter().order_by('-date_posted')

class all_jobs_sql(ListView):
    model = Post
    template_name = 'blog/all_jobs_sql.html'
    context_object_name = 'jobs'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_jobs_sql, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Jobs SQL'
        context['jobs'] = SQL_get_all_jobs()
        return context
    
    def get_queryset(self):
        return JobModel.objects.filter().order_by('-date_posted')
        
class all_timesheets_sql(ListView):
    model = Post
    template_name = 'blog/all_timesheets_sql.html'
    context_object_name = 'timesheets'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_timesheets_sql, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Timesheets SQL'
        context['timesheets'] = SQL_get_all_timesheet_entries()
        return context
    
    def get_queryset(self):
        return TimesheetModel.objects.filter().order_by('-date_posted')
        
class all_tasks_sql(ListView):
    model = Post
    template_name = 'blog/all_tasks_sql.html'
    context_object_name = 'tasks'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_tasks_sql, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Tasks SQL'
        context['tasks'] = SQL_get_all_tasks()
        return context
    
    def get_queryset(self):
        return TaskModel.objects.filter().order_by('-date_posted')
        
class all_announcements_sql(ListView):
    model = Post
    template_name = 'blog/all_announcements_sql.html'
    context_object_name = 'announcements'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_announcements_sql, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Announcements SQL'
        context['announcements'] = SQL_get_all_announcements()
        context['status'] = SQL_get_all_announcement_status()
        return context
    
    def get_queryset(self):
        return AnnouncementModel.objects.filter().order_by('-date_posted')
        
class all_products_sql(ListView):
    model = Post
    template_name = 'blog/all_products_sql.html'
    context_object_name = 'products'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_products_sql, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Products SQL'
        context['products'] = SQL_get_all_products()
        return context
    
    def get_queryset(self):
        return JobModel.objects.filter().order_by('-date_posted')
 
class all_customers_sql(ListView):
    model = Post
    template_name = 'blog/all_customers_sql.html'
    context_object_name = 'customers'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_customers_sql, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Customers SQL'
        context['customers'] = SQL_get_all_customers()
        return context
    
    def get_queryset(self):
        return CustomerModel.objects.filter().order_by('-date_posted')
        
class all_employees_sql(ListView):
    model = Post
    template_name = 'blog/all_employees_sql.html'
    context_object_name = 'employees'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_employees_sql, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Employees SQL'
        context['employees'] = SQL_get_all_employees()
        return context
    
    def get_queryset(self):
        return EmployeeModel.objects.filter().order_by('-date_posted')
        
class all_employees(ListView):
    model = Post
    template_name = 'blog/all_employees.html'
    context_object_name = 'employees'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_employees, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Employees'
        return context
    
    def get_queryset(self):
        return EmployeeModel.objects.filter().order_by('-start_date')

class all_timesheets(ListView):
    model = Post
    template_name = 'blog/all_timesheets.html'
    context_object_name = 'timesheets'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_timesheets, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Timesheets'
        return context
    
    def get_queryset(self):
        return TimesheetModel.objects.filter().order_by('-date_posted')
        
class all_announcements(ListView):
    model = Post
    template_name = 'blog/all_announcements.html'
    context_object_name = 'announcements'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_announcements, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Announcements'
        return context
    
    def get_queryset(self):
        return AnnouncementModel.objects.filter().order_by('-date_posted')

class all_tasks(ListView):
    model = Post
    template_name = 'blog/all_tasks.html'
    context_object_name = 'tasks'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_tasks, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Tasks'
        return context
    
    def get_queryset(self):
        return TaskModel.objects.filter().order_by('-date_posted')

class all_products(ListView):
    model = Post
    template_name = 'blog/all_products.html'
    context_object_name = 'products'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(all_products, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Products'
        return context
    
    def get_queryset(self):
        return ProductModel.objects.filter().order_by('-date_posted')

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    #context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'My Entries'
        return context
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date_posted')
        
def PostListView_sql(request):
    context = {
        'current_title': 'My Entries'
        
    }
    
    return render(request, 'blog/home.html', context)

class AllUserEntriesView(ListView):
    template_name = 'blog/home.html'
    context_object_name = 'entries'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(AllUserEntriesView, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'My Entries'
        return context
    
    def get_queryset(self):
        my_timesheets = TimesheetModel.objects.filter(author=self.request.user).all()
        my_announcements = AnnouncementModel.objects.filter(author=self.request.user).all()
        my_products = ProductModel.objects.filter(author=self.request.user).all()
        my_tasks = TaskModel.objects.filter(author=self.request.user).all()
        
        meta_query = list(my_timesheets) + list(my_announcements) + list(my_products) + list(my_tasks)
        return meta_query

class AllPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(AllPostListView, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Data Entries'
        return context
    
    def get_queryset(self):
        group =  Group.objects.get(name='Administration')
        if (group in self.request.user.groups.all()):
            return Post.objects.filter().order_by('-date_posted')
        else:
            return Post.objects.filter(author=self.request.user).order_by('-date_posted') | Post.objects.filter(title='Announcement').order_by('-date_posted')

class LatestPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date_posted') | Post.objects.filter(title='Announcement').order_by('-date_posted')


class AnnouncementPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(AnnouncementPostListView, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'Announcements'
        return context
    
    def get_queryset(self):
        return Post.objects.filter(title='Announcement').filter(author=self.request.user).order_by('-date_posted') | Post.objects.filter(title='Announcement').order_by('-date_posted')


class TimesheetPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(TimesheetPostListView, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'My Timesheets'
        return context
    
    def get_queryset(self):
        return Post.objects.filter(title='Timesheet').filter(author=self.request.user).order_by('-date_posted')


class AllTimesheetPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(AllTimesheetPostListView, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Timesheets'
        return context
    
    def get_queryset(self):
        group =  Group.objects.get(name='Administration')
        if (group in self.request.user.groups.all()):
            return Post.objects.filter(title='Timesheet').order_by('-date_posted')
        else:
            return Post.objects.filter(title='Timesheet').filter(author=self.request.user).order_by('-date_posted')


class TaskAssignmentPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(TaskAssignmentPostListView, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'My Task Assignments'
        return context
    
    def get_queryset(self):
        return Post.objects.filter(title='Task Assignment').filter(author=self.request.user).order_by('-date_posted')


class AllTaskAssignmentPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(AllTaskAssignmentPostListView, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'All Task Assignments'
        return context
    
    def get_queryset(self):
        group =  Group.objects.get(name='Administration')
        if (group in self.request.user.groups.all()):
            return Post.objects.filter(title='Task Assignment').order_by('-date_posted')
        else:
            return Post.objects.filter(title='Task Assignment').filter(author=self.request.user).order_by('-date_posted')

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        
        return context


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        
        return super().form_valid(form)


class PostCreateAnnouncementView(CreateView):
    model = Post
    fields = ['title', 'content']
    
    def __init__(self, *args, **kwargs):
        kwargs.update(initial={
            'title': 'Announcement',
            'content': ''
        })

        super(PostCreateAnnouncementView, self).__init__(*args, **kwargs)
    
    def form_valid(self, form):
        
        return super().form_valid(form)


class PostCreateTimesheetView(CreateView):
    template_name = "blog/post_form_timesheet.html"
    model = Post
    fields = ['title', 'content_projectNum', 'content_timeStart', 'content_timeEnd']
    
    def __init__(self, *args, **kwargs):
        kwargs.update(initial={
            'title': 'Timesheet',
            #'content_projectNum': '',
            #'content_timeStart': '',
            #'content_timeEnd': ''
            
        })

        super(PostCreateTimesheetView, self).__init__(*args, **kwargs)
    
    def form_valid(self, form):
        
        return super().form_valid(form)


class PostCreateNewClientView(CreateView):
    model = Post
    fields = ['title', 'content']
    
    def __init__(self, *args, **kwargs):
        kwargs.update(initial={
            'title': 'New Client',
            'content': ''
        })

        super(PostCreateNewClientView, self).__init__(*args, **kwargs)
    
    def form_valid(self, form):
        
        return super().form_valid(form)


class PostCreateTaskAssignmentView(CreateView):
    template_name = "blog/post_form_task.html"
    model = Post
    fields = ['title', 'content_userID', 'content_projectNum', 'content']
    
    def __init__(self, *args, **kwargs):
        kwargs.update(initial={
            'title': 'Task Assignment',
            'content': '',
        })

        super(PostCreateTaskAssignmentView, self).__init__(*args, **kwargs)
    
    def form_valid(self, form):
        
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

@login_required(login_url='login')
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

@login_required(login_url='login')
def DislikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.remove(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

@login_required(login_url='login')
def SQLView(request):
    model = Post
    context = {
        'sql_users': SQL_get_all_users(),
        'sql_posts': SQL_get_all_posts(),
    }
    
    def __init__(self, *args, **kwargs):
        kwargs.update(initial={
            'title': 'Task Assignment',
            'content': ''
        })
    
    return render(request, 'blog/about.html', context)
    
# ------------------------------------------------------------- #
#                        JOBASS VIEWS                           #
# ------------------------------------------------------------- # 
class create_jobass(CreateView):
    model = JobassignmentModel
    form_class = Jobassignment
    
    def get_context_data(self, *args, **kwargs):
        context = super(create_jobass, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Job Assignment Entry'
        return context

    def form_valid(self, form):
        try:
            exist_test = SQL_get_jobassid_main(form.instance.employee_id, form.instance.job_id, 1)
            if exist_test.JobAssignmentID > 0:
                messages.warning(self.request, 'That employee is already assigned to the specified job!')
                return HttpResponseRedirect(reverse('all-jobass-sql'))
        except IndexError:
            SQL_insert_jobass(form.instance.employee_id,
                           form.instance.job_id, 
                           form.instance.date,
                           form.instance.status)
            return super().form_valid(form)

class update_jobass(CreateView):
    model = JobassignmentModel
    form_class = Jobassignment
    template_name = 'blog/jobass_form_update.html'
    
    def get_initial(self):
        object = SQL_get_jobass(self.kwargs.get('pk'))
        
        return {
            'employee_id': object.Employee_ID,
            'job_id': object.Job_ID,
            'date': object.EmployeeJobAssignment_Date,
            'status': object.EmployeeJobAssignment_Status,
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(update_jobass, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Update Job Assignment Entry'
        return context

    def form_valid(self, form):
        SQL_update_jobass(form.instance.employee_id,
                       form.instance.job_id, 
                       form.instance.date, 
                       form.instance.status,
                       self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('jobass-detail-sql', args = (self.kwargs.get('pk'),))
        
class delete_jobass(CreateView):
    model = JobassignmentModel
    form_class = Jobassignment
    template_name = 'blog/jobass_form_delete.html'
    
    def get_initial(self):
        object = SQL_get_jobass(self.kwargs.get('pk'))
        
        return {
            'employee_id': object.Employee_ID,
            'job_id': object.Job_ID,
            'date': object.EmployeeJobAssignment_Date,
            'status': object.EmployeeJobAssignment_Status,
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(delete_jobass, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Are you sure you want to delete this job assignment entry?'
        return context

    def form_valid(self, form):
        SQL_update_jobass(form.instance.employee_id,
                       form.instance.job_id, 
                       form.instance.date, 
                       2,
                       self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('jobass-detail-sql', args = (self.kwargs.get('pk'),))

def jobass_detail_sql(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_jobass(pk)
        
    }
    return render(request, 'blog/jobass_detail_sql.html', context)

def all_jobass_sql(request):
    object_list = SQL_get_all_jobass()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_jobass_SQL.html', { 'objects': objects, 'current_title': 'All Job Assignments' })
# ------------------------------------------------------------- #
#                         JOB VIEWS                             #
# ------------------------------------------------------------- # 
class create_job(CreateView):
    model = JobModel
    form_class = Job
    
    def get_context_data(self, *args, **kwargs):
        context = super(create_job, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Job Entry'
        return context

    def form_valid(self, form):
        SQL_insert_job(form.instance.description,
                       form.instance.jobCustomer, 
                       form.instance.status, 
                       form.instance.budget)
        return super().form_valid(form)

class update_job(CreateView):
    model = JobModel
    form_class = Job
    template_name = 'blog/jobmodel_form_update.html'
    
    def get_initial(self):
        object = SQL_get_job_by_id(self.kwargs.get('pk'))
        
        return {
            'jobCustomer': object.Customer_ID,
            'status': object.JobStatus_ID,
            'description': object.JobDescription,
            'budget': object.JobBudget,
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(update_job, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Update Job Entry'
        return context

    def form_valid(self, form):
        SQL_update_job(form.instance.description,
                       form.instance.jobCustomer, 
                       form.instance.status, 
                       form.instance.budget,
                       self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('job-detail-sql', args = (self.kwargs.get('pk'),))

class delete_job(CreateView):
    model = JobModel
    form_class = Job
    template_name = 'blog/jobmodel_form_delete.html'
    
    def get_initial(self):
        object = SQL_get_job_by_id(self.kwargs.get('pk'))
        
        return {
            'jobCustomer': object.Customer_ID,
            'status': object.JobStatus_ID,
            'description': object.JobDescription,
            'budget': object.JobBudget,
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(delete_job, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Are you sure you want to delete this job entry?'
        return context

    def form_valid(self, form):
        joborders = SQL_get_all_job_orders(self.kwargs.get('pk'))
        SQL_update_job(form.instance.description,
                       form.instance.jobCustomer, 
                       2, 
                       form.instance.budget,
                       self.kwargs.get('pk'))
        SQL_delete_job_orders(self.kwargs.get('pk'))
        for order in joborders:
            SQL_delete_order_orderlines(order.Order_ID)
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('job-detail-sql', args = (self.kwargs.get('pk'),))

class job_detail(DetailView):
    model = JobModel
    
    def get_context_data(self, *args, **kwargs):
        context = super(job_detail, self).get_context_data(*args, **kwargs)
        context['orders'] = OrderModel.objects.filter(job_id=self.kwargs.get('pk')).order_by('-date_posted')
        return context
        
def job_detail_sql(request, pk):
    order_list = SQL_get_all_job_orders(pk)
    page = request.GET.get('page', 1)
    
    paginator = Paginator(order_list, 10)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
        
    context = {
        'id': pk,
        'object': SQL_get_job_by_id(pk),
        'orders' : orders,
        'complaints': SQL_get_all_job_complaints(pk)
        
    }
    return render(request, 'blog/jobmodel_detail_sql.html', context)

def job_detail_sql_employee(request, pk):
    order_list = SQL_get_all_job_orders(pk)
    page = request.GET.get('page', 1)
    
    paginator = Paginator(order_list, 10)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
        
    context = {
        'id': pk,
        'object': SQL_get_job_by_id(pk),
        'orders' : orders,
        'complaints': SQL_get_all_job_complaints(pk)
        
    }
    return render(request, 'blog/jobmodel_detail_sql_employee.html', context)     

def all_jobs_sql(request):
    object_list = SQL_get_all_jobs()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_jobs_sql.html', { 'objects': objects, 'current_title': 'All Jobs' })

def all_jobs_sql_employee(request):
    object_list = SQL_get_all_employee_jobs2(request.session['global_id'])
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_jobs_sql_employee.html', { 'objects': objects, 'current_title': 'My Jobs' })        

# ------------------------------------------------------------- #
#                       Job Complaint VIEWS                     #
# ------------------------------------------------------------- #
class create_jobcomplaint(CreateView):
    model = JobcomplaintModel
    form_class = Jobcomplaint

    def get_context_data(self, *args, **kwargs):
        context = super(create_jobcomplaint, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Job Complaint Entry'
        return context
        
    def get(self, request, *args, **kwargs):
        def_pk = self.kwargs.get('pk')
        form = Jobcomplaint(initial=dict(
                    job_id=self.kwargs.get('pk')))
        form.fields['job_id'].choices = [(1,self.kwargs.get('pk'))]
        context = dict(form=form)
        context['entry_title'] = "Job Complaint Entry for Job #"+str(self.kwargs.get('pk'))
        template_name = 'blog/jobcomplaintmodel_form.html'
        return render(request, template_name, context)

    def form_valid(self, form):
        SQL_insert_jobcomplaint(self.kwargs.get('pk'), form.instance.detail, form.instance.date, form.instance.status)
        return super().form_valid(form)

class update_jobcomplaint(CreateView):
    model = JobcomplaintModel
    form_class = Jobcomplaint
    template_name = 'blog/jobcomplaintmodel_form_update.html'
    
    def get_initial(self):
        object = SQL_get_job_complaint_by_id(self.kwargs.get('pk'))
        
        return {
            'job_id': object.Job_ID,
            'detail': object.JobComplaint_ComplaintDetail,
            'date': object.JobComplaint_Date,
            'status': object.JobComplaintStatus_ID
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(update_jobcomplaint, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Update Job Complaint Entry'
        return context

    def form_valid(self, form):
        SQL_update_jobcomplaint(form.instance.job_id,form.instance.detail,form.instance.date,form.instance.status,self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('jobcomplaint-detail-sql', args = (self.kwargs.get('pk'),))

class delete_jobcomplaint(CreateView):
    model = JobcomplaintModel
    form_class = Jobcomplaint
    template_name = 'blog/jobcomplaintmodel_form_delete.html'
    
    def get_initial(self):
        object = SQL_get_job_complaint_by_id(self.kwargs.get('pk'))
        
        return {
            'job_id': object.Job_ID,
            'detail': object.JobComplaint_ComplaintDetail,
            'date': object.JobComplaint_Date,
            'status': object.JobComplaintStatus_ID
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(delete_jobcomplaint, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Are you sure you want to delete this job complaint entry?'
        return context

    def form_valid(self, form):
        SQL_update_jobcomplaint(form.instance.job_id,form.instance.detail,form.instance.date,2,self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('jobcomplaint-detail-sql', args = (self.kwargs.get('pk'),))
        
def jobcomplaint_detail_sql(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_job_complaint_by_id(pk),
        
    }
    return render(request, 'blog/jobcomplaintmodel_detail_sql.html', context) 
    
def jobcomplaint_detail_sql_employee(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_job_complaint_by_id(pk),
        
    }
    return render(request, 'blog/jobcomplaintmodel_detail_sql_employee.html', context) 
# ------------------------------------------------------------- #
#                       TIMESHEET VIEWS                         #
# ------------------------------------------------------------- #
class create_timesheet_test(CreateView):
    model = TimesheetModel
    form_class = Timesheet
    
    def get_context_data(self, *args, **kwargs):
        context = super(create_timesheet_test, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Timesheet Entry'
        return context
        
    def get(self, request, *args, **kwargs):
        def_pk = self.kwargs.get('pk')
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        if len(SQL_get_all_employee_jobs(request.session['global_id'])) > 0:
            try:
                test_timesheet = SQL_get_timesheet_by_date(current_date,request.session['global_id'])
                if test_timesheet.Timesheet_ID > 0:
                    form = Timesheet(initial=dict(
                            employee_id=request.session['global_id'],
                            sheet_id = SQL_get_timesheet_by_date(current_date,request.session['global_id']).Timesheet_ID))
                    form.fields['project_num'].choices = tuple(zip(SQL_get_all_employee_jobs(request.session['global_id']),
                                                                   SQL_get_all_employee_jobs(request.session['global_id'])))
                    context = dict(form=form)
                    context['entry_title'] = 'Timesheet Entry'
                    context['date'] = current_date
                    template_name = 'blog/timesheetmodel_form.html'
                    return render(request, template_name, context)
            except IndexError:
                SQL_insert_timesheet_main(current_date,request.session['global_id'])
                form = Timesheet(initial=dict(
                            employee_id=request.session['global_id'],
                            sheet_id = SQL_get_timesheet_by_date(current_date,request.session['global_id']).Timesheet_ID))
                form.fields['project_num'].choices = tuple(zip(SQL_get_all_employee_jobs(request.session['global_id']),
                                                               SQL_get_all_employee_jobs(request.session['global_id'])))
                context = dict(form=form)
                context['entry_title'] = 'Timesheet Entry'
                context['date'] = current_date
                template_name = 'blog/timesheetmodel_form.html'
                return render(request, template_name, context)
        else:
            messages.warning(self.request, 'You do not have any jobs assigned to you yet!')
            return HttpResponseRedirect(reverse('admin-home'))
            
    def form_valid(self, form):
        jobassid = SQL_get_jobassid(form.instance.employee_id,form.instance.project_num)
        SQL_insert_timesheet(form.instance.sheet_id,
                            jobassid.JobAssignmentID,
                            form.instance.status,
                            form.instance.time_start,
                            form.instance.time_end)
        return super().form_valid(form)
        
class create_timesheet_test_employee(CreateView):
    model = TimesheetModel
    form_class = Timesheet
    template_name = 'blog/timesheetmodel_form_employee.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(create_timesheet_test_employee, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Timesheet Entry'
        return context
        
    def get(self, request, *args, **kwargs):
        def_pk = self.kwargs.get('pk')
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        if len(SQL_get_all_employee_jobs(request.session['global_id'])) > 0:
            try:
                test_timesheet = SQL_get_timesheet_by_date(current_date,request.session['global_id'])
                if test_timesheet.Timesheet_ID > 0:
                    form = Timesheet(initial=dict(
                            employee_id=request.session['global_id'],
                            sheet_id = SQL_get_timesheet_by_date(current_date,request.session['global_id']).Timesheet_ID))
                    form.fields['project_num'].choices = tuple(zip(SQL_get_all_employee_jobs(request.session['global_id']),
                                                                   SQL_get_all_employee_jobs(request.session['global_id'])))
                    context = dict(form=form)
                    context['entry_title'] = 'Timesheet Entry'
                    context['date'] = current_date
                    template_name = 'blog/timesheetmodel_form_employee.html'
                    return render(request, template_name, context)
            except IndexError:
                SQL_insert_timesheet_main(current_date,request.session['global_id'])
                form = Timesheet(initial=dict(
                            employee_id=request.session['global_id'],
                            sheet_id = SQL_get_timesheet_by_date(current_date,request.session['global_id']).Timesheet_ID))
                form.fields['project_num'].choices = tuple(zip(SQL_get_all_employee_jobs(request.session['global_id']),
                                                               SQL_get_all_employee_jobs(request.session['global_id'])))
                context = dict(form=form)
                context['entry_title'] = 'Timesheet Entry'
                context['date'] = current_date
                template_name = 'blog/timesheetmodel_form_employee.html'
                return render(request, template_name, context)
        else:
            messages.warning(self.request, 'You do not have any jobs assigned to you yet!')
            return HttpResponseRedirect(reverse('employee-home'))
            
    def form_valid(self, form):
        jobassid = SQL_get_jobassid(form.instance.employee_id,form.instance.project_num)
        SQL_insert_timesheet(form.instance.sheet_id,
                            jobassid.JobAssignmentID,
                            form.instance.status,
                            form.instance.time_start,
                            form.instance.time_end)
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('timesheet-detail-sql-employee', args = (SQL_get_all_timesheet_entries2()[-1],))
            

class update_timesheet(CreateView):
    model = TimesheetModel
    form_class = Timesheet
    template_name = 'blog/timesheetmodel_form_update.html'

    def get_initial(self):
        object = SQL_get_timesheet_entry_by_id(self.kwargs.get('pk'))
        info = SQL_get_timesheet_entry_info(self.kwargs.get('pk'))
        jobs_assigned = SQL_get_all_emp_jobs_assigned(self.kwargs.get('pk'))
        
        return {
            'project_num': info.JobID,
            'sheet_id': info.Timesheet_ID,
            'status': object.TimesheetEntry_LineStatus_ID,
            'time_start': object.ClockInTime,
            'time_end': object.ClockOutTime,
            'employee_id': info.EmployeeID
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(update_timesheet, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Timesheet Entry Update'
        context['jobid'] = SQL_get_all_emp_jobs_assigned(self.kwargs.get('pk')).JobID
        return context

    def form_valid(self, form):
        jobassid = SQL_get_jobassid(form.instance.employee_id,form.instance.project_num)
        SQL_update_timesheet(form.instance.sheet_id, 
                             jobassid.JobAssignmentID,
                             form.instance.status, 
                             form.instance.time_start, 
                             form.instance.time_end,
                             self.kwargs.get('pk'))
                             
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('timesheet-detail-sql', args = (self.kwargs.get('pk'),))

class delete_timesheet(CreateView):
    model = TimesheetModel
    form_class = Timesheet
    template_name = 'blog/timesheetmodel_form_delete.html'
    
    def get_initial(self):
        object = SQL_get_timesheet_entry_by_id(self.kwargs.get('pk'))
        info = SQL_get_timesheet_entry_info(self.kwargs.get('pk'))
        
        return {
            'project_num': info.JobID,
            'sheet_id': info.Timesheet_ID,
            'status': object.TimesheetEntry_LineStatus_ID,
            'time_start': object.ClockInTime,
            'time_end': object.ClockOutTime,
            'employee_id': info.EmployeeID
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(delete_timesheet, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Are you sure you want to delete this timesheet entry?'
        return context

    def form_valid(self, form):
        jobassid = SQL_get_jobassid(form.instance.employee_id,form.instance.project_num)
        SQL_update_timesheet(form.instance.sheet_id, 
                             jobassid.JobAssignmentID, 
                             2, 
                             form.instance.time_start, 
                             form.instance.time_end,
                             self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('timesheet-detail-sql', args = (self.kwargs.get('pk'),))       

class timesheet_detail(DetailView):
    model = TimesheetModel
    
    def get_context_data(self, *args, **kwargs):
        context = super(timesheet_detail, self).get_context_data(*args, **kwargs)
        return context

def timesheet_detail_sql(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_timesheet_entry_by_id(pk),
        'info': SQL_get_timesheet_entry_info(pk)
        
    }
    return render(request, 'blog/timesheetmodel_detail_sql.html', context)
    
def timesheet_detail_sql_employee(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_timesheet_entry_by_id(pk),
        'info': SQL_get_timesheet_entry_info(pk)
        
    }
    return render(request, 'blog/timesheetmodel_detail_sql_employee.html', context)
    

def all_timesheets_sql(request):
    object_list = SQL_get_all_timesheet_entries()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_timesheets_sql.html', { 'objects': objects, 'current_title': 'All Timesheet Entries' }) 
    
def all_timesheets_sql_employee(request):
    object_list = SQL_get_timesheet_entry_employee_id(request.session['global_id'])
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_timesheets_sql_employee.html', { 'objects': objects, 'current_title': 'My Timesheet Entries' }) 
        
class UserTimesheetsView(ListView):
    model = TimesheetModel
    template_name = 'blog/home.html'
    context_object_name = 'timesheets'
    ordering = ['-date_posted']
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(AllUserEntriesView, self).get_context_data(*args, **kwargs)
        context['current_title'] = 'My Timesheets'
        return context
    
    def get_queryset(self):
        return TimesheetModel.objects.filter(author=self.request.user).order_by('-date_posted')
        

# ------------------------------------------------------------- #
#                       ANNOUNCEMENT VIEWS                      #
# ------------------------------------------------------------- #

class create_announcement(CreateView):
    model = AnnouncementModel
    form_class = Announcement
    
    def get_context_data(self, *args, **kwargs):
        context = super(create_announcement, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Announcement Entry'
        return context

    def form_valid(self, form):
        SQL_insert_announcement(form.instance.title, form.instance.content, form.instance.status, form.instance.priority)
        return super().form_valid(form)

class update_announcement(CreateView):
    model = AnnouncementModel
    form_class = Announcement
    template_name = 'blog/announcementmodel_form_update.html'
    
    def get_initial(self):
        object = SQL_get_announcement_by_id(self.kwargs.get('pk'))
        
        return {
            'title': object.Announcement_Name,
            'content': object.AnnouncementContent,
            'status': object.AnnouncementStatus_ID,
            'priority': object.AnnouncementPriority_ID
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(update_announcement, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Update Announcement Entry'
        return context

    def form_valid(self, form):
        SQL_update_announcement(form.instance.title, form.instance.content, form.instance.status, form.instance.priority, self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('announcement-detail-sql', args = (self.kwargs.get('pk'),))

class delete_announcement(CreateView):
    model = AnnouncementModel
    form_class = Announcement
    template_name = 'blog/announcementmodel_form_delete.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(delete_announcement, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Are you sure you want to delete this announcement entry?'
        return context
    
    def get_initial(self):
        object = SQL_get_announcement_by_id(self.kwargs.get('pk'))
        
        return {
            'title': object.Announcement_Name,
            'content': object.AnnouncementContent,
            'status': object.AnnouncementStatus_ID,
            'priority': object.AnnouncementPriority_ID
        }
        
    def form_valid(self, form):
        SQL_update_announcement(form.instance.title, form.instance.content, 2, form.instance.priority, self.kwargs.get('pk'))
        return super().form_valid(form) 
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('announcement-detail-sql', args = (self.kwargs.get('pk'),))

class announcement_detail(DetailView):
    model = AnnouncementModel
    
    def get_context_data(self, *args, **kwargs):
        context = super(announcement_detail, self).get_context_data(*args, **kwargs)
        return context
        
def announcement_detail_sql(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_announcement_by_id(pk),
        
    }
    return render(request, 'blog/announcementmodel_detail_sql.html', context) 
    
def announcement_detail_sql_employee(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_announcement_by_id(pk),
        
    }
    return render(request, 'blog/announcementmodel_detail_sql_employee.html', context) 

def all_announcements_sql(request):
    object_list = SQL_get_all_announcements()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_announcements_sql.html', { 'objects': objects, 'current_title': 'All Announcements' })
    
def all_announcements_sql_employee(request):
    object_list = SQL_get_all_announcements()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_announcements_sql_employee.html', { 'objects': objects, 'current_title': 'All Announcements' })
       

# ------------------------------------------------------------- #
#                         PRODUCT VIEWS                         #
# ------------------------------------------------------------- #

class create_product(CreateView):
    model = ProductModel
    form_class = Product
    
    def get_context_data(self, *args, **kwargs):
        context = super(create_product, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Product Entry'
        return context

    def form_valid(self, form):
        SQL_insert_product(form.instance.category_id, form.instance.name, form.instance.description, form.instance.status)
        return super().form_valid(form)

class update_product(CreateView):
    model = ProductModel
    form_class = Product
    template_name = 'blog/productmodel_form_update.html'
    
    def get_initial(self):
        object = SQL_get_product_by_id(self.kwargs.get('pk'))
        
        return {
            'name': object.ProductName,
            'description': object.ProductDescription,
            'category_id': object.ProductCategory_ID,
            'status': object.ProductStatus_ID
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(update_product, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Update Product Entry'
        return context

    def form_valid(self, form):
        SQL_update_product(form.instance.name, 
                           form.instance.description, 
                           form.instance.category_id, 
                           form.instance.status, 
                           self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('product-detail-sql', args = (self.kwargs.get('pk'),))

class delete_product(CreateView):
    model = ProductModel
    form_class = Product
    template_name = 'blog/productmodel_form_delete.html'
    
    def get_initial(self):
        object = SQL_get_product_by_id(self.kwargs.get('pk'))
        
        return {
            'name': object.ProductName,
            'description': object.ProductDescription,
            'category_id': object.ProductCategory_ID,
            'status': object.ProductStatus_ID
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(delete_product, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Are you sure you want to delete this product entry?'
        return context

    def form_valid(self, form):
        SQL_update_product(form.instance.name, 
                           form.instance.description, 
                           form.instance.category_id, 
                           2, 
                           self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('product-detail-sql', args = (self.kwargs.get('pk'),))

class product_detail(DetailView):
    model = ProductModel
    
    def get_context_data(self, *args, **kwargs):
        context = super(product_detail, self).get_context_data(*args, **kwargs)
        return context
        
def product_detail_sql(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_product_by_id(pk)
        
    }
    return render(request, 'blog/productmodel_detail_sql.html', context)
    
def all_products_sql(request):
    object_list = SQL_get_all_products()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_products_sql.html', { 'objects': objects, 'current_title': 'All Products' })
    
# ------------------------------------------------------------- #
#                          TASK VIEWS                           #
# ------------------------------------------------------------- #
class create_task(CreateView):
    model = TaskModel
    form_class = Task

    def get_context_data(self, *args, **kwargs):
        context = super(create_task, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Task Entry'
        return context
    
    def form_valid(self, form):
        try:
            exist_test = SQL_get_jobassid(form.instance.employee_id, form.instance.job_id)
            if exist_test.JobAssignmentID > 0:
                SQL_insert_task(form.instance.job_id, 
                                 form.instance.startDate, 
                                 form.instance.dueDate, 
                                 form.instance.content, 
                                 form.instance.priority, 
                                 form.instance.status)
                                 
                last_id_created = SQL_get_last_taskid()[0]
                SQL_insert_taskassignment(form.instance.employee_id, 
                                     last_id_created, 
                                     form.instance.startDate)
                return super().form_valid(form)
        except:
            messages.warning(self.request, 'You can not assign a task to an employee with a job they are not assigned to!')
            return HttpResponseRedirect(reverse('all-tasks-sql'))
        
class update_task(CreateView):
    model = TaskModel
    form_class = Task
    template_name = 'blog/taskmodel_form_update.html'
        
    def get_initial(self):
        object = SQL_get_task_by_id(self.kwargs.get('pk'))
        
        return {
            'job_id': object.Job_ID,
            'startDate': object.TaskStartDate,
            'dueDate': object.TaskDueDate,
            'content': object.TaskDetails,
            'priority': object.TaskPriority_ID,
            'status': object.TaskStatus_ID,
            'employee_id': object.EmployeeID,
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(update_task, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Task Entry Update'
        return context

    def form_valid(self, form):
        try:
            exist_test = SQL_get_jobassid(form.instance.employee_id, form.instance.job_id)
            if exist_test.JobAssignmentID > 0:
                SQL_update_task(form.instance.job_id, 
                                     form.instance.startDate, 
                                     form.instance.dueDate, 
                                     form.instance.content, 
                                     form.instance.priority, 
                                     form.instance.status,
                                     self.kwargs.get('pk'))
                SQL_update_taskassignment(form.instance.employee_id, 
                                     form.instance.startDate,
                                     self.kwargs.get('pk'))
                return super().form_valid(form)
        except:
            messages.warning(self.request, 'You can not assign a task to an employee with a job they are not assigned to!')
            return HttpResponseRedirect(reverse('all-tasks-sql'))
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('task-detail-sql', args = (self.kwargs.get('pk'),))
        
class delete_task(CreateView):
    model = TaskModel
    form_class = Task
    template_name = 'blog/taskmodel_form_delete.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(delete_task, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Are you sure you want to delete this task entry?'
        return context
        
    def get_initial(self):
        object = SQL_get_task_by_id(self.kwargs.get('pk'))
        
        return {
            'job_id': object.Job_ID,
            'startDate': object.TaskStartDate,
            'dueDate': object.TaskDueDate,
            'content': object.TaskDetails,
            'priority': object.TaskPriority_ID,
            'status': object.TaskStatus_ID,
            'employee_id': object.EmployeeID,
        }

    def form_valid(self, form):
        SQL_update_task(form.instance.job_id, 
                             form.instance.startDate, 
                             form.instance.dueDate, 
                             form.instance.content, 
                             form.instance.priority, 
                             2,
                             self.kwargs.get('pk'))
        SQL_update_taskassignment(form.instance.employee_id, 
                             form.instance.startDate,
                             self.kwargs.get('pk'))
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('task-detail-sql', args = (self.kwargs.get('pk'),))

class task_detail(DetailView):
    model = TaskModel
    
    def get_context_data(self, *args, **kwargs):
        context = super(task_detail, self).get_context_data(*args, **kwargs)
        return context
        
def task_detail_sql(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_task_by_id(pk),
    }
    return render(request, 'blog/taskmodel_detail_sql.html', context) 

def task_detail_sql_employee(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_task_by_id(pk),
    }
    return render(request, 'blog/taskmodel_detail_sql_employee.html', context)

def all_tasks_sql(request):
    object_list = SQL_get_all_tasks()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_tasks_sql.html', { 'objects': objects, 'current_title': 'All Tasks' })
    
def all_tasks_sql_employee(request):
    object_list = SQL_get_tasks_employee_id(request.session['global_id'])
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_tasks_sql_employee.html', { 'objects': objects, 'current_title': 'My Tasks' })
        

# ------------------------------------------------------------- #
#                        ORDER VIEWS                            #
# ------------------------------------------------------------- #

class create_order(CreateView):
    model = OrderModel
    form_class = Order
    
    def get_context_data(self, *args, **kwargs):
        context = super(create_order, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Order Entry'
        return context
        
    def get(self, request, *args, **kwargs):
        def_pk = self.kwargs.get('pk')
        form = Order(initial=dict(
                    job_id=self.kwargs.get('pk')))
        form.fields['job_id'].choices = [(1,self.kwargs.get('pk'))]
        context = dict(form=form)
        context['entry_title'] = "Order Entry for Job #"+str(self.kwargs.get('pk'))
        template_name = 'blog/ordermodel_form.html'
        return render(request, template_name, context)
            
    def form_valid(self, form):
        SQL_insert_order(self.kwargs.get('pk'), 
                             form.instance.dueDate, 
                             form.instance.status, 
                             form.instance.priority)
        return super().form_valid(form)   

class update_order(CreateView):
    model = OrderModel
    form_class = Order
    template_name = 'blog/ordermodel_form_update.html'
    
    def get_initial(self):
        object = SQL_get_order_by_id(self.kwargs.get('pk'))
        
        return {
            'job_id': object.Job_ID,
            'dueDate': object.OrderDueDate,
            'priority': object.OrderPriority_ID,
            'status': object.OrderStatus_ID,
        }
    
    def form_valid(self, form):
        SQL_update_order(form.instance.job_id, 
                        form.instance.dueDate, 
                        form.instance.status, 
                        form.instance.priority, 
                        self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_context_data(self, *args, **kwargs):
        context = super(update_order, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Update Order Entry'
        return context
            
    def get_success_url(self, **kwargs):
        return reverse_lazy('order-detail-sql', args = (self.kwargs.get('pk'),))

class delete_order(CreateView):
    model = OrderModel
    form_class = Order
    template_name = 'blog/ordermodel_form_delete.html'
    
    def get_initial(self):
        object = SQL_get_order_by_id(self.kwargs.get('pk'))
        
        return {
            'job_id': object.Job_ID,
            'dueDate': object.OrderDueDate,
            'priority': object.OrderPriority_ID,
            'status': object.OrderStatus_ID,
        }
    
    def form_valid(self, form):
        SQL_update_order(form.instance.job_id, 
                        form.instance.dueDate, 
                        2, 
                        form.instance.priority, 
                        self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_context_data(self, *args, **kwargs):
        context = super(delete_order, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Are you sure you want to delete this order entry?'
        return context
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('order-detail-sql', args = (self.kwargs.get('pk'),))

class create_order_sql(CreateView):
    model = OrderModel
    form_class = Order
    
    def get_context_data(self, *args, **kwargs):
        context = super(create_order_sql, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Order Entry'
        return context

    def form_valid(self, form):
        SQL_insert_order(form.instance.job_id, 
                             form.instance.dueDate, 
                             form.instance.status, 
                             form.instance.priority)
        return super().form_valid(form)           
        
def order_detail_sql(request, pk):
    orderline_list = SQL_get_all_orderlines(pk)
    page = request.GET.get('page', 1)
    
    paginator = Paginator(orderline_list, 10)
    try:
        orderlines = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
        
    context = {
        'id': pk,
        'object': SQL_get_order_by_id(pk),
        'orderlines': orderlines
        
    }
    return render(request, 'blog/ordermodel_detail_sql.html', context)
    
def order_detail_sql_employee(request, pk):
    orderline_list = SQL_get_all_orderlines(pk)
    page = request.GET.get('page', 1)
    
    paginator = Paginator(orderline_list, 10)
    try:
        orderlines = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
        
    context = {
        'id': pk,
        'object': SQL_get_order_by_id(pk),
        'orderlines': orderlines
        
    }
    return render(request, 'blog/ordermodel_detail_sql_employee.html', context)
    
def all_orders_sql(request):
    object_list = SQL_get_all_orders()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_orders_sql.html', { 'objects': objects, 'current_title': 'All Orders' })

# ------------------------------------------------------------- #
#                       CUSTOMER VIEWS                          #
# ------------------------------------------------------------- #

class create_customer(CreateView):
    model = CustomerModel
    form_class = Customer
    
    def get_context_data(self, *args, **kwargs):
        context = super(create_customer, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Customer Entry'
        return context
    
    def form_valid(self, form):
        form.instance.title = str(form.instance.companyName)
        SQL_insert_customer(form.instance.fName, 
                             form.instance.lName, 
                             form.instance.companyName, 
                             form.instance.phoneNumber, 
                             form.instance.priority, 
                             form.instance.status,
                             form.instance.corpAddressLine1,
                             form.instance.corpAddressLine2,
                             form.instance.corpCity,
                             form.instance.corpZipcode,
                             form.instance.corpState)
        return super().form_valid(form)
        
class update_customer(CreateView):
    model = CustomerModel
    form_class = Customer
    template_name = 'blog/customermodel_form_update.html'
    
    def get_initial(self):
        object = SQL_get_customer_by_id(self.kwargs.get('pk'))
        
        return {
            'fName': object.CustomerFirstName,
            'lName': object.CustomerLastName,
            'companyName': object.CompanyName,
            'phoneNumber': object.CustomerPhone,
            'corpAddressLine1': object.CorpAddress_Line1,
            'corpAddressLine2': object.CorpAddress_Line2,
            'corpCity': object.CorpLocation_City,
            'corpState': object.CorpLocation_State,
            'status': object.CustomerStatus_ID,
            'priority': object.CustomerPriority_ID,
            'corpZipcode': object.CorpLocation_ZipCode,
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(update_customer, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Update Customer Entry'
        return context
    
    def form_valid(self, form):
        form.instance.title = str(form.instance.companyName)
        SQL_update_customer(form.instance.fName, 
                             form.instance.lName, 
                             form.instance.companyName, 
                             form.instance.phoneNumber, 
                             form.instance.priority, 
                             form.instance.status,
                             form.instance.corpAddressLine1,
                             form.instance.corpAddressLine2,
                             form.instance.corpCity,
                             form.instance.corpZipcode,
                             form.instance.corpState,
                             self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('customer-detail-sql', args = (self.kwargs.get('pk'),))
        
class delete_customer(CreateView):
    model = CustomerModel
    form_class = Customer
    template_name = 'blog/customermodel_form_delete.html'
    
    def get_initial(self):
        object = SQL_get_customer_by_id(self.kwargs.get('pk'))
        
        return {
            'fName': object.CustomerFirstName,
            'lName': object.CustomerLastName,
            'companyName': object.CompanyName,
            'phoneNumber': object.CustomerPhone,
            'corpAddressLine1': object.CorpAddress_Line1,
            'corpAddressLine2': object.CorpAddress_Line2,
            'corpCity': object.CorpLocation_City,
            'corpState': object.CorpLocation_State,
            'status': object.CustomerStatus_ID,
            'priority': object.CustomerPriority_ID,
            'corpZipcode': object.CorpLocation_ZipCode,
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(delete_customer, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Are you sure you want to delete this customer entry?'
        return context
    
    def form_valid(self, form):
        form.instance.title = str(form.instance.companyName)
        SQL_update_customer(form.instance.fName, 
                             form.instance.lName, 
                             form.instance.companyName, 
                             form.instance.phoneNumber, 
                             form.instance.priority, 
                             2,
                             form.instance.corpAddressLine1,
                             form.instance.corpAddressLine2,
                             form.instance.corpCity,
                             form.instance.corpZipcode,
                             form.instance.corpState,
                             self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('customer-detail-sql', args = (self.kwargs.get('pk'),))
        
class customer_detail(DetailView):
    model = CustomerModel
    template_name = 'blog/customermodel_detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(customer_detail, self).get_context_data(*args, **kwargs)
        context['jobs'] = JobModel.objects.filter(jobCustomer=self.object.companyName).order_by('-date_posted')
        return context

def customer_detail_sql(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_customer_by_id(pk),
        'jobs': SQL_get_all_customer_jobs(pk)
        
    }
    return render(request, 'blog/customermodel_detail_sql.html', context) 
    
def all_customers_sql(request):
    object_list = SQL_get_all_customers()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_customers_sql.html', { 'objects': objects, 'current_title': 'All Customers' })
    
# ------------------------------------------------------------- #
#                       EMPLOYEE VIEWS                          #
# ------------------------------------------------------------- #
class create_employee(CreateView):
    model = EmployeeModel
    form_class = Employee
    
    def get_context_data(self, *args, **kwargs):
        context = super(create_employee, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Employee Entry'
        return context
    
    def form_valid(self, form):
        SQL_insert_employee(form.instance.firstName, 
                         form.instance.lastName, 
                         form.instance.phoneNumber, 
                         form.instance.email, 
                         form.instance.job_title,
                         form.instance.pay_rate, 
                         form.instance.status, 
                         form.instance.addressLine1,
                         form.instance.addressLine2,
                         form.instance.city,
                         form.instance.state,
                         form.instance.zipcode,
                         form.instance.type)
        return super().form_valid(form)
        
class update_employee(CreateView):
    model = EmployeeModel
    form_class = Employee
    template_name = 'blog/employeemodel_form_update.html'
    
    def get_initial(self):
        object = SQL_get_employee_by_id(self.kwargs.get('pk'))
        
        return {
            'firstName': object.Emp_FirstName,
            'lastName': object.Emp_LastName,
            'phoneNumber': object.Emp_Phone,
            'email': object.Emp_Email,
            'job_title': object.Emp_JobTitle,
            'pay_rate': object.Emp_PayRate_ID,
            'status': object.Emp_Status_ID,
            'addressLine1': object.Emp_Address_Address1,
            'addressLine2': object.Emp_Address_Address2,
            'city': object.Emp_Location_City,
            'state': object.Emp_Location_State,
            'zipcode': object.Emp_ZipCode,
            'type': object.Emp_Type,
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(update_employee, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Update Employee Entry'
        return context
    
    def form_valid(self, form):
        SQL_update_employee(form.instance.firstName, 
                         form.instance.lastName, 
                         form.instance.phoneNumber, 
                         form.instance.email, 
                         form.instance.job_title,
                         form.instance.pay_rate, 
                         form.instance.status, 
                         form.instance.addressLine1,
                         form.instance.addressLine2,
                         form.instance.city,
                         form.instance.state,
                         form.instance.zipcode,
                         form.instance.type,
                         self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('employee-detail-sql', args = (self.kwargs.get('pk'),))
        
class delete_employee(CreateView):
    model = EmployeeModel
    form_class = Employee
    template_name = 'blog/employeemodel_form_delete.html'
    
    def get_initial(self):
        object = SQL_get_employee_by_id(self.kwargs.get('pk'))
        
        return {
            'firstName': object.Emp_FirstName,
            'lastName': object.Emp_LastName,
            'phoneNumber': object.Emp_Phone,
            'email': object.Emp_Email,
            'job_title': object.Emp_JobTitle,
            'pay_rate': object.Emp_PayRate_ID,
            'status': object.Emp_Status_ID,
            'addressLine1': object.Emp_Address_Address1,
            'addressLine2': object.Emp_Address_Address2,
            'city': object.Emp_Location_City,
            'state': object.Emp_Location_State,
            'zipcode': object.Emp_ZipCode,
            'type': object.Emp_Type,
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(delete_employee, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Are you sure you want to delete this employee entry?'
        return context
    
    def form_valid(self, form):
        SQL_update_employee(form.instance.firstName, 
                         form.instance.lastName, 
                         form.instance.phoneNumber, 
                         form.instance.email, 
                         form.instance.job_title,
                         form.instance.pay_rate, 
                         2, 
                         form.instance.addressLine1,
                         form.instance.addressLine2,
                         form.instance.city,
                         form.instance.state,
                         form.instance.zipcode,
                         form.instance.type,
                         self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('employee-detail-sql', args = (self.kwargs.get('pk'),))

class employee_detail(DetailView):
    model = EmployeeModel
    
    def get_context_data(self, *args, **kwargs):
        context = super(employee_detail, self).get_context_data(*args, **kwargs)
        return context
   
def employee_detail_sql(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_employee_by_id(pk),
        
    }
    return render(request, 'blog/employeemodel_detail_sql.html', context) 
    
def employee_detail_sql_employee(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_employee_by_id(pk),
        
    }
    return render(request, 'blog/employeemodel_detail_sql_employee.html', context) 


def all_employees_sql(request):
    object_list = SQL_get_all_employees()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_employees_sql.html', { 'objects': objects, 'current_title': 'All Employees' })
    
# ------------------------------------------------------------- #
#                       ORDERLINE VIEWS                         #
# ------------------------------------------------------------- #
def orderline_detail_sql(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_orderline_by_id(pk),
        
    }
    return render(request, 'blog/orderlinemodel_detail_sql.html', context) 
    
def orderline_detail_sql_employee(request, pk):
    context = {
        'id': pk,
        'object': SQL_get_orderline_by_id(pk),
        
    }
    return render(request, 'blog/orderlinemodel_detail_sql_employee.html', context)
    
class create_orderline(CreateView):
    model = OrderlineModel
    form_class = Orderline
    
    def get_context_data(self, *args, **kwargs):
        context = super(create_orderline, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Orderline Entry'
        return context
    
    def get(self, request, *args, **kwargs):
        def_pk = self.kwargs.get('pk')
        form = Orderline(initial=dict(
                    order_id=self.kwargs.get('pk')))
        context = dict(form=form)
        context['entry_title'] = 'Orderline Entry'
        template_name = 'blog/orderlinemodel_form.html'
        return render(request, template_name, context)
    
    def form_valid(self, form):
        SQL_insert_orderline(form.instance.order_id,
                             form.instance.product_id,
                             form.instance.quantity,
                             form.instance.price,
                             form.instance.status,
                             form.instance.priority
                             )
        return super().form_valid(form)   
        
class update_orderline(CreateView):
    model = OrderlineModel
    form_class = Orderline
    template_name = 'blog/orderlinemodel_form_update.html'
    
    def get_initial(self):
        object = SQL_get_orderline_by_id(self.kwargs.get('pk'))
        
        return {
            'order_id': object.Order_ID,
            'product_id': object.Product_ID,
            'quantity': object.Product_Quantity,
            'price': object.Product_Price,
            'status': object.OrderLine_Status_ID,
            'priority': object.OrderLine_Priority_ID,
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(update_orderline, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Update Orderline Entry'
        return context
    
    def form_valid(self, form):
        SQL_update_orderline(form.instance.order_id, 
                             form.instance.product_id,
                             form.instance.quantity,
                             form.instance.price,
                             form.instance.status,
                             form.instance.priority,
                             self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('orderline-detail-sql', args = (self.kwargs.get('pk'),))
        
class delete_orderline(CreateView):
    model = OrderlineModel
    form_class = Orderline
    template_name = 'blog/orderlinemodel_form_delete.html'
    
    def get_initial(self):
        object = SQL_get_orderline_by_id(self.kwargs.get('pk'))
        
        return {
            'order_id': object.Order_ID,
            'product_id': object.Product_ID,
            'quantity': object.Product_Quantity,
            'price': object.Product_Price,
            'status': object.OrderLine_Status_ID,
            'priority': object.OrderLine_Priority_ID,
        }
    
    def get_context_data(self, *args, **kwargs):
        context = super(delete_orderline, self).get_context_data(*args, **kwargs)
        context['entry_title'] = 'Are you sure you want to delete this orderline entry?'
        return context
    
    def form_valid(self, form):
        SQL_update_orderline(form.instance.order_id, 
                             form.instance.product_id,
                             form.instance.quantity,
                             form.instance.price,
                             2,
                             form.instance.priority,
                             self.kwargs.get('pk'))
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('orderline-detail-sql', args = (self.kwargs.get('pk'),))
  
# ------------------------------------------------------------- #
#                         QUERY VIEWS                           #
# ------------------------------------------------------------- #    
def all_queries_sql(request):
    object_list = all_queries()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'blog/all_queries_sql.html', { 'objects': objects, 'current_title': 'All Reports' })
    
def query_detail_sql(request, pk):
    context = {
        'id': pk,
        'objects': all_queries()[pk-1][3],
        'current_title': all_queries()[pk-1][1],
        
    }
    return render(request, 'blog/query_detail_sql.html', context) 
    
def export_csv(request, pk):
   response = HttpResponse(content_type='text/csv')
   filename = str(all_queries()[pk-1][1])+"_"+datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")+".csv"
   response['Content-Disposition'] = u'attachment; filename="{0}"'.format(filename)
   writer = csv.writer(
      response,
      quoting=csv.QUOTE_ALL
   )

   writer.writerows(all_queries()[pk-1][3])

   return response