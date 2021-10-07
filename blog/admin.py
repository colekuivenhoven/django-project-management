from django.contrib import admin
from .models import Post, JobModel, CustomerModel, OrderModel, TimesheetModel, AnnouncementModel, TaskModel, ProductModel, EmployeeModel

admin.site.register(Post)
admin.site.register(JobModel)
admin.site.register(CustomerModel)
admin.site.register(OrderModel)
admin.site.register(TimesheetModel)
admin.site.register(AnnouncementModel)
admin.site.register(TaskModel)
admin.site.register(ProductModel)
admin.site.register(EmployeeModel)