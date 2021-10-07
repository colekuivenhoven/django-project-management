import pyodbc

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
    
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA #
#                            END                                #
# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV #


# ------------------------------------------------------------- #
# 'GET ALL' METHODS
# ------------------------------------------------------------- #

# Timesheet Entry ----------------------------------------------------------------------------->
def SQL_get_all_timesheet_entries():
    str = '''
          SELECT
          TimesheetEntry_Line.TimesheetEntry_Line_ID AS 'EntryID',
          TimesheetEntry_LineStatus.TimesheetEntryLineStatus AS 'Status',
          EmployeeJobAssignment.EmployeeJobAssignment_ID AS 'EmployeeJobAssignmentID',
          Employee.Employee_ID AS 'EmployeeID',
          Employee.Emp_FirstName + ' ' + Employee.Emp_LastName AS 'FullName',
          Job.Job_ID AS 'JobID',
          Timesheet.TimesheetDate AS 'Date'
          
          FROM TimesheetEntry_Line 
          JOIN TimesheetEntry_LineStatus ON TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = TimesheetEntry_Line.TimesheetEntry_LineStatus_ID
          JOIN EmployeeJobAssignment ON EmployeeJobAssignment.EmployeeJobAssignment_ID = TimesheetEntry_Line.EmployeeJobAssignment_ID
          JOIN Employee ON Employee.Employee_ID = EmployeeJobAssignment.Employee_ID
          JOIN Job ON Job.Job_ID = EmployeeJobAssignment.Job_ID
          JOIN Timesheet ON Timesheet.Timesheet_ID = TimesheetEntry_Line.Timesheet_ID
          
          WHERE TimesheetEntry_Line.TimesheetEntry_LineStatus_ID != 2
          
          ORDER BY TimesheetEntry_Line.TimesheetEntry_Line_ID DESC
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query
    
def SQL_get_all_timesheet_entries2():
    str = "SELECT TimesheetEntry_Line_ID FROM TimesheetEntry_Line"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]

def SQL_get_all_employee_jobs(id):
    str = '''
          SELECT
          EmployeeJobAssignment.Job_ID,
          EmployeeJobAssignment.Employee_ID,
          EmployeeJobAssignment.EmployeeJobAssignment_Date,
          EmployeeJobAssignment.EmployeeJobAssignment_Status,
          Job.Job_ID AS 'JobID',
          Job.JobDescription AS 'JobDescription',
          Job.Customer_ID AS 'CustomerID',
          Job.JobBudget AS 'Budget',
          JobStatus.JobStatus AS 'Status',
          Customer.CompanyName AS 'CustomerName'
          
          FROM EmployeeJobAssignment 
          JOIN Job ON Job.Job_ID = EmployeeJobAssignment.Job_ID
          JOIN JobStatus ON JobStatus.JobStatus_ID = Job.JobStatus_ID
          JOIN Customer ON Customer.Customer_ID = Job.Customer_ID 
          
          WHERE Employee_ID = {} AND EmployeeJobAssignment_Status != 2 AND Job.JobStatus_ID != 2
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return [x[0] for x in query]
    
def SQL_get_all_employee_jobs2(id):
    str = '''
          SELECT
          EmployeeJobAssignment.Job_ID,
          EmployeeJobAssignment.Employee_ID,
          EmployeeJobAssignment.EmployeeJobAssignment_Date,
          EmployeeJobAssignment.EmployeeJobAssignment_Status,
          Job.Job_ID AS 'JobID',
          Job.JobDescription AS 'JobDescription',
          Job.Customer_ID AS 'CustomerID',
          Job.JobBudget AS 'Budget',
          JobStatus.JobStatus AS 'Status',
          Customer.CompanyName AS 'CustomerName'
          
          FROM EmployeeJobAssignment 
          JOIN Job ON Job.Job_ID = EmployeeJobAssignment.Job_ID
          JOIN JobStatus ON JobStatus.JobStatus_ID = Job.JobStatus_ID
          JOIN Customer ON Customer.Customer_ID = Job.Customer_ID
          
          WHERE Employee_ID = {} AND EmployeeJobAssignment_Status != 2 
          
          ORDER BY Job.Job_ID DESC
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def SQL_get_all_emp_jobs_assigned(sheetid):
    str = '''
          SELECT 
          EmployeeJobAssignment.EmployeeJobAssignment_ID AS 'EmployeeJobAssignmentID',
          EmployeeJobAssignment.Job_ID AS 'JobID',
          EmployeeJobAssignment.Employee_ID AS 'EmployeeID',
          TimesheetEntry_Line.TimesheetEntry_Line_ID AS 'TimesheetEntry_LineID'
          
          FROM EmployeeJobAssignment 
          JOIN TimesheetEntry_Line ON TimesheetEntry_Line.EmployeeJobAssignment_ID = EmployeeJobAssignment.EmployeeJobAssignment_ID
          WHERE TimesheetEntry_Line.TimesheetEntry_Line_ID = {};
          '''.format(sheetid)
          
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]

# Announcment -----------------------------------------------------------------------------> 
def SQL_get_all_announcements():
    str =   '''
            SELECT Announcement.Announcement_ID,
            Announcement.Announcement_Name,
            Announcement.AnnouncementContent,
            AnnouncementStatus.AnnouncementStatus AS 'Status' 
            
            FROM Announcement 
            JOIN AnnouncementStatus ON AnnouncementStatus.AnnouncementStatus_ID = Announcement.AnnouncementStatus_ID
            
            WHERE Announcement.AnnouncementStatus_ID != 2
            
            ORDER BY Announcement.Announcement_ID DESC
            '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query
    
# Task ----------------------------------------------------------------------------->
def SQL_get_all_tasks():
    str = '''
          SELECT
          Task.Task_ID AS 'TaskID',
          Task.Job_ID AS 'JobID',
          Task.TaskStartDate AS 'StartDate',
          Task.TaskDueDate AS 'DueDate',
          Employee.Employee_ID AS 'EmployeeID',
          Employee.Emp_FirstName AS 'eFirstName',
          Employee.Emp_LastName AS 'eLastName',
          TaskAssignment.TaskAssignment_ID AS 'TaskAssID'
          
          FROM Task
          JOIN TaskAssignment ON TaskAssignment.Task_ID = Task.Task_ID
          JOIN Employee ON Employee.Employee_ID = TaskAssignment.Employee_ID
          
          WHERE Task.TaskStatus_ID != 2
          
          ORDER BY Task.Task_ID DESC
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query
    
def SQL_get_tasks_employee_id(id):
    str = '''
          SELECT
          Task.Task_ID AS 'TaskID',
          Task.Job_ID AS 'JobID',
          Task.TaskStartDate AS 'StartDate',
          Task.TaskDueDate AS 'DueDate',
          Employee.Employee_ID AS 'EmployeeID',
          Employee.Emp_FirstName AS 'eFirstName',
          Employee.Emp_LastName AS 'eLastName',
          TaskAssignment.TaskAssignment_ID AS 'TaskAssID'
          
          FROM Task
          JOIN TaskAssignment ON TaskAssignment.Task_ID = Task.Task_ID
          JOIN Employee ON Employee.Employee_ID = TaskAssignment.Employee_ID
          
          WHERE Task.TaskStatus_ID != 2 AND Employee.Employee_ID = {}
          
          
          ORDER BY Task.Task_ID DESC
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query

# Timesheet ----------------------------------------------------------------------------->
def SQL_get_all_timesheets():
    str = "SELECT * FROM Timesheet ORDER BY Timesheet.Timesheet_ID DESC"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query

# Product ----------------------------------------------------------------------------->
def SQL_get_all_products():
    str = '''
          SELECT
          Product.Product_ID,
          Product.ProductCategory_ID,
          Product.ProductName,
          Product.ProductDescription,
          Product.ProductStatus_ID,
          ProductStatus.Product_Status AS 'Status',
          ProductCategory.ProductCategory_Name AS 'CategoryName'
          
          FROM Product
          JOIN ProductStatus ON ProductStatus.ProductStatus_ID = Product.ProductStatus_ID
          JOIN ProductCategory ON ProductCategory.ProductCategory_ID = Product.ProductCategory_ID
          
          WHERE Product.ProductStatus_ID != 2
          
          ORDER BY Product.Product_ID DESC
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query

# Order ----------------------------------------------------------------------------->
def SQL_get_all_orders():
    str = '''
          SELECT
          Order_.Order_ID,
          Order_.OrderDueDate,
          Order_.Job_ID,
          OrderPriority.Order_Priority AS 'Priority',
          OrderStatus.Order_Status AS 'Status'
          
          FROM Order_ 
          JOIN OrderStatus ON OrderStatus.OrderStatus_ID = Order_.OrderStatus_ID
          JOIN OrderPriority ON OrderPriority.OrderPriority_ID = Order_.OrderPriority_ID
          
          WHERE Order_.OrderStatus_ID != 2
          
          ORDER BY Order_.Order_ID DESC
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query

# OrderLine ----------------------------------------------------------------------------->
def SQL_get_all_orderlines(id):
    str = '''
          SELECT
          Order_Line.OrderLine_ID,
          Order_Line.Order_ID,
          Order_Line.Product_ID,
          Order_Line.Product_Quantity,
          Order_Line.Product_Price,
          Order_Line.OrderLine_Status_ID,
          Order_Line.OrderLine_Priority_ID,
          Order_Line.OrderLine_Total,
          OrderLine_Priority.OrderLine_Priority AS 'Priority',
          OrderLine_Status.OrderLineStatus AS 'Status'
          
          FROM Order_Line 
          JOIN OrderLine_Priority ON OrderLine_Priority.OrderLine_Priority_ID = Order_Line.OrderLine_Priority_ID
          JOIN OrderLine_Status ON OrderLine_Status.OrderLine_Status_ID = Order_Line.OrderLine_Status_ID
          
          WHERE Order_Line.Order_ID = {} AND Order_Line.OrderLine_Status_ID != 2
          
          ORDER BY Order_Line.OrderLine_ID DESC
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query

# Customer ----------------------------------------------------------------------------->
def SQL_get_all_customers():
    str = '''
          SELECT
          Customer.Customer_ID,
          Customer.CustomerFirstName,
          Customer.CustomerLastName,
          Customer.CompanyName,
          Customer.CustomerPhone,
          Customer.CustomerPriority_ID,
          Customer.CustomerStatus_ID,
          Customer.CorpAddress_Line1,
          Customer.CorpAddress_Line2,
          Customer.CorpLocation_City,
          Customer.CorpLocation_ZipCode,
          Customer.CorpLocation_State,
          CustomerStatus.Customer_Status AS 'Status',
          CustomerPriority.Customer_Priority AS 'Priority',
          StateProvince.State_ID AS 'StateID',
          StateProvince.State_Name AS 'StateName',
          Country.Country_ID AS 'CountryID',
          Country.Country_Name AS 'CountryName'
          
          FROM Customer 
          JOIN CustomerStatus ON CustomerStatus.CustomerStatus_ID = Customer.CustomerStatus_ID
          JOIN CustomerPriority ON CustomerPriority.CustomerPriority_ID = Customer.CustomerPriority_ID
          JOIN StateProvince ON StateProvince.State_ID = Customer.CorpLocation_State
          JOIN Country ON Country.Country_ID = StateProvince.Country_ID
          
          WHERE Customer.CustomerStatus_ID != 2
          
          ORDER BY Customer.Customer_ID DESC
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query   
    
def SQL_get_all_customer_jobs(id):
    str = '''
          SELECT
          Job.Job_ID AS 'JobID',
          Job.JobDescription AS 'JobDescription',
          Job.Customer_ID AS 'CustomerID',
          Job.JobBudget AS 'Budget',
          JobStatus.JobStatus AS 'Status',
          Customer.CompanyName AS 'CustomerName'
          
          FROM Job
          JOIN JobStatus ON JobStatus.JobStatus_ID = Job.JobStatus_ID
          JOIN Customer ON Customer.Customer_ID = Job.Customer_ID
          
          WHERE Customer.Customer_ID = {0} AND Job.JobStatus_ID != 2
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query
    
# Employee ----------------------------------------------------------------------------->
def SQL_get_all_employees():
    str = '''
          SELECT
          Employee.Employee_ID,
          Employee.Emp_FirstName,
          Employee.Emp_LastName,
          Employee.Emp_FirstName,
          Employee.Emp_Phone,
          Employee.Emp_Email,
          Employee.Emp_JobTitle,
          Employee.Emp_PayRate_ID,
          Employee.Emp_Status_ID,
          Employee.Emp_Address_Address1,
          Employee.Emp_Address_Address2,
          Employee.Emp_Location_City,
          Employee.Emp_Location_State,
          Employee.Emp_ZipCode,
          Employee.Emp_Type,
          JobTitle.EmployeeTitle AS 'JobTitle',
          EmployeeDepartment.Emp_Department_ID AS 'DepartmentID',
          EmployeeDepartment.DepartmentName AS 'DepartmentName',
          EmployeePayRate.Emp_PayRate AS 'PayRate',
          EmployeeStatus.Emp_Status AS 'Status',
          StateProvince.State_ID AS 'StateID',
          StateProvince.State_Name AS 'StateName',
          Country.Country_ID AS 'CountryID',
          Country.Country_Name AS 'CountryName',
          EmployeeType.Emp_Type AS 'Type'
          
          FROM Employee
          JOIN JobTitle ON JobTitle.JobTitle_ID = Employee.Emp_JobTitle
          JOIN EmployeeDepartment ON EmployeeDepartment.Emp_Department_ID = JobTitle.Department_ID
          JOIN EmployeePayRate ON EmployeePayRate.EmployeePayRate_ID = Employee.Emp_PayRate_ID
          JOIN EmployeeStatus ON EmployeeStatus.EmployeeStatus_ID = Employee.Emp_Status_ID
          JOIN StateProvince ON StateProvince.State_ID = Employee.Emp_Location_State
          JOIN Country ON Country.Country_ID = StateProvince.Country_ID
          JOIN EmployeeType ON EmployeeType.Emp_Type_ID = Employee.Emp_Type
          
          WHERE Employee.Emp_Status_ID != 2
          
          ORDER BY Employee.Employee_ID DESC
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query 

# Job ----------------------------------------------------------------------------->
def SQL_get_all_jobs():
    str = '''
          SELECT
          Job.Job_ID AS 'JobID',
          Job.JobDescription AS 'JobDescription',
          Job.Customer_ID AS 'CustomerID',
          Job.JobBudget AS 'Budget',
          JobStatus.JobStatus AS 'Status',
          Customer.CompanyName AS 'CustomerName'
          
          FROM Job
          JOIN JobStatus ON JobStatus.JobStatus_ID = Job.JobStatus_ID
          JOIN Customer ON Customer.Customer_ID = Job.Customer_ID
          
          WHERE Job.JobStatus_ID != 2
          
          ORDER BY Job.Job_ID DESC
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query
    
def SQL_get_all_job_orders(id):
    str = "SELECT * FROM Order_ WHERE Order_.Job_ID = {} AND Order_.OrderStatus_ID != 2 ORDER BY Order_.Order_ID DESC".format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query
    
def SQL_get_all_jobass():
    str = '''
          SELECT
          EmployeeJobAssignment.EmployeeJobAssignment_ID,
          EmployeeJobAssignment.Employee_ID,
          EmployeeJobAssignment.Job_ID,
          EmployeeJobAssignment.EmployeeJobAssignment_Date,
          Employee.Emp_FirstName AS 'first',
          Employee.Emp_LastName AS 'last',
          EmployeeJobAssignment_Status.EmployeeJobAssignment_Status AS 'Status'
          
          FROM EmployeeJobAssignment 
          JOIN Employee ON Employee.Employee_ID = EmployeeJobAssignment.Employee_ID
          JOIN EmployeeJobAssignment_Status ON EmployeeJobAssignment_Status.EmployeeJobAssignment_Status_ID = EmployeeJobAssignment.EmployeeJobAssignment_Status
          
          WHERE EmployeeJobAssignment.EmployeeJobAssignment_Status != 2
    
          ORDER BY EmployeeJobAssignment.EmployeeJobAssignment_ID DESC
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query
    
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA #
#                            END                                #
# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV #


# ------------------------------------------------------------- #
# 'GET INDIVIDUAL' METHODS
# ------------------------------------------------------------- #
    
# Timesheet Entry
def SQL_get_timesheet_entry_by_id(id):
    str = "SELECT * FROM TimesheetEntry_Line WHERE TimesheetEntry_Line_ID = {0}".format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]

def SQL_get_timesheet_entry_info(id):
    str = '''
          SELECT
          TimesheetEntry_Line.TimesheetEntry_Line_ID AS 'EntryID',
          TimesheetEntry_LineStatus.TimesheetEntryLineStatus AS 'Status',
          EmployeeJobAssignment.EmployeeJobAssignment_ID AS 'EmployeeJobAssignmentID',
          EmployeeJobAssignment.EmployeeJobAssignment_Date AS 'EmployeeJobAssignmentDate',
          Employee.Employee_ID AS 'EmployeeID',
          Employee.Emp_FirstName + ' ' + Employee.Emp_LastName AS 'FullName',
          Job.Job_ID AS 'JobID',
          Timesheet.TimesheetDate AS 'TimesheetDate',
          Timesheet.Timesheet_ID AS 'Timesheet_ID'
          
          FROM TimesheetEntry_Line 
          JOIN TimesheetEntry_LineStatus ON TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = TimesheetEntry_Line.TimesheetEntry_LineStatus_ID
          JOIN EmployeeJobAssignment ON EmployeeJobAssignment.EmployeeJobAssignment_ID = TimesheetEntry_Line.EmployeeJobAssignment_ID
          JOIN Employee ON Employee.Employee_ID = EmployeeJobAssignment.Employee_ID
          JOIN Job ON Job.Job_ID = EmployeeJobAssignment.Job_ID
          JOIN Timesheet ON Timesheet.Timesheet_ID = TimesheetEntry_Line.Timesheet_ID
          
          WHERE TimesheetEntry_Line_ID = {0}
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]
    
def SQL_get_timesheet_entry_employee_id(id):
    str = '''
          SELECT
          TimesheetEntry_Line.TimesheetEntry_Line_ID AS 'EntryID',
          TimesheetEntry_LineStatus.TimesheetEntryLineStatus AS 'Status',
          EmployeeJobAssignment.EmployeeJobAssignment_ID AS 'EmployeeJobAssignmentID',
          Employee.Employee_ID AS 'EmployeeID',
          Job.Job_ID AS 'JobID',
          TimesheetEntry_Line.ClockInTime AS 'ClockInTime',
          TimesheetEntry_Line.ClockOutTime AS 'ClockOutTime',
          Timesheet.TimesheetDate AS 'Date'
          
          FROM TimesheetEntry_Line 
          JOIN TimesheetEntry_LineStatus ON TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = TimesheetEntry_Line.TimesheetEntry_LineStatus_ID
          JOIN EmployeeJobAssignment ON EmployeeJobAssignment.EmployeeJobAssignment_ID = TimesheetEntry_Line.EmployeeJobAssignment_ID
          JOIN Employee ON Employee.Employee_ID = EmployeeJobAssignment.Employee_ID
          JOIN Job ON Job.Job_ID = EmployeeJobAssignment.Job_ID
          JOIN Timesheet ON Timesheet.Timesheet_ID = TimesheetEntry_Line.Timesheet_ID
          
          WHERE Employee.Employee_ID = {0}
          ORDER BY TimesheetEntry_Line.TimesheetEntry_Line_ID DESC
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query
    
def SQL_get_jobassid_main(empid, jobid, status):
    str = '''
          SELECT EmployeeJobAssignment_ID AS 'JobAssignmentID'
          FROM EmployeeJobAssignment 
          WHERE Employee_ID = {} AND Job_ID = {} AND EmployeeJobAssignment_Status = {};
          '''.format(empid, jobid, status)
          
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]
    
def SQL_get_jobassid(empid, jobid):
    str = '''
          SELECT EmployeeJobAssignment_ID AS 'JobAssignmentID'
          FROM EmployeeJobAssignment 
          WHERE Employee_ID = {} AND Job_ID = {};
          '''.format(empid, jobid)
          
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]
    
def SQL_get_jobass(id):
    str = '''
          SELECT
          EmployeeJobAssignment.EmployeeJobAssignment_ID,
          EmployeeJobAssignment.Employee_ID,
          EmployeeJobAssignment.Job_ID,
          EmployeeJobAssignment.EmployeeJobAssignment_Date,
          EmployeeJobAssignment.EmployeeJobAssignment_Status,
          Employee.Emp_FirstName AS 'first',
          Employee.Emp_LastName AS 'last',
          EmployeeJobAssignment_Status.EmployeeJobAssignment_Status AS 'Status'
          
          FROM EmployeeJobAssignment 
          JOIN Employee ON Employee.Employee_ID = EmployeeJobAssignment.Employee_ID
          JOIN EmployeeJobAssignment_Status ON EmployeeJobAssignment_Status.EmployeeJobAssignment_Status_ID = EmployeeJobAssignment.EmployeeJobAssignment_Status
          WHERE EmployeeJobAssignment_ID = {};
          '''.format(id)
          
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]

# Announcment   
def SQL_get_announcement_by_id(id):
    str = '''
          SELECT
          Announcement.Announcement_ID,
          Announcement.Announcement_Name,
          Announcement.AnnouncementContent,
          Announcement.AnnouncementStatus_ID,
          Announcement.AnnouncementPriority_ID,
          AnnouncementPriority.AnnouncementPriority AS 'Priority',
          AnnouncementStatus.AnnouncementStatus AS 'Status'
          
          FROM Announcement
          JOIN AnnouncementStatus ON AnnouncementStatus.AnnouncementStatus_ID = Announcement.AnnouncementStatus_ID
          JOIN AnnouncementPriority ON AnnouncementPriority.AnnouncementPriority_ID = Announcement.AnnouncementPriority_ID
          
          WHERE Announcement.Announcement_ID = {0}
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query[0]
    
# Task  
def SQL_get_task_by_id(id):
    str = '''
          SELECT
          Task.Task_ID,
          Task.Job_ID,
          Task.TaskStartDate,
          Task.TaskDueDate,
          Task.TaskDetails,
          Task.TaskPriority_ID,
          Task.TaskStatus_ID,
          TaskPriority.TaskPriority AS 'Priority',
          TaskStatus.TaskStatus AS 'Status',
          TaskAssignment.TaskAssignment_Date AS 'AssignDate',
          Employee.Employee_ID AS 'EmployeeID'
          
          FROM Task 
          JOIN TaskStatus ON TaskStatus.TaskStatus_ID = Task.TaskStatus_ID
          JOIN TaskPriority ON TaskPriority.TaskPriority_ID = Task.TaskPriority_ID
          JOIN TaskAssignment ON TaskAssignment.Task_ID = Task.Task_ID
          JOIN Employee ON Employee.Employee_ID = TaskAssignment.Employee_ID
          
          WHERE Task.Task_ID = {0}
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]

# Timesheet 
def SQL_get_timesheet_by_date(date, empid):
    str = '''
          SELECT Timesheet_ID FROM Timesheet WHERE Timesheet.TimesheetDate = '{}' AND Timesheet.Employee_ID = {}
          '''.format(date, empid)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]

# Product
def SQL_get_product_by_id(id):
    str = '''
          SELECT
          Product.Product_ID,
          Product.ProductCategory_ID,
          Product.ProductName,
          Product.ProductDescription,
          Product.ProductStatus_ID,
          ProductStatus.Product_Status AS 'Status',
          ProductCategory.ProductCategory_Name AS 'CategoryName'
          
          FROM Product
          JOIN ProductStatus ON ProductStatus.ProductStatus_ID = Product.ProductStatus_ID
          JOIN ProductCategory ON ProductCategory.ProductCategory_ID = Product.ProductCategory_ID
          
          WHERE Product_ID = {}
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]

# Order
def SQL_get_order_by_id(id):
    str = '''
          SELECT
          Order_.Order_ID,
          Order_.OrderDueDate,
          Order_.Job_ID,
          Order_.OrderPriority_ID,
          Order_.OrderStatus_ID,
          OrderPriority.Order_Priority AS 'Priority',
          OrderStatus.Order_Status AS 'Status'
          
          FROM Order_ 
          JOIN OrderStatus ON OrderStatus.OrderStatus_ID = Order_.OrderStatus_ID
          JOIN OrderPriority ON OrderPriority.OrderPriority_ID = Order_.OrderPriority_ID 
          
          WHERE Order_ID = {}
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]

# Orderline
def SQL_get_orderline_by_id(id):
    str = '''
          SELECT
          Order_Line.OrderLine_ID,
          Order_Line.Order_ID,
          Order_Line.Product_ID,
          Order_Line.Product_Quantity,
          Order_Line.Product_Price,
          Order_Line.OrderLine_Status_ID,
          Order_Line.OrderLine_Priority_ID,
          Order_Line.OrderLine_Total,
          OrderLine_Priority.OrderLine_Priority AS 'Priority',
          OrderLine_Status.OrderLineStatus AS 'Status',
          Product.ProductName AS 'Product'
          
          FROM Order_Line 
          JOIN OrderLine_Priority ON OrderLine_Priority.OrderLine_Priority_ID = Order_Line.OrderLine_Priority_ID
          JOIN OrderLine_Status ON OrderLine_Status.OrderLine_Status_ID = Order_Line.OrderLine_Status_ID
          JOIN Product ON Product.Product_ID = Order_Line.Product_ID
          
          WHERE Order_Line.OrderLine_ID = {} 
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]

# Customer  
def SQL_get_customer_by_id(id):
    str = '''
          SELECT
          Customer.Customer_ID,
          Customer.CustomerFirstName,
          Customer.CustomerLastName,
          Customer.CompanyName,
          Customer.CustomerPhone,
          Customer.CustomerPriority_ID,
          Customer.CustomerStatus_ID,
          Customer.CorpAddress_Line1,
          Customer.CorpAddress_Line2,
          Customer.CorpLocation_City,
          Customer.CorpLocation_ZipCode,
          Customer.CorpLocation_State,
          CustomerStatus.Customer_Status AS 'Status',
          CustomerPriority.Customer_Priority AS 'Priority',
          StateProvince.State_ID AS 'StateID',
          StateProvince.State_Name AS 'StateName',
          Country.Country_ID AS 'CountryID',
          Country.Country_Name AS 'CountryName'
          
          FROM Customer 
          JOIN CustomerStatus ON CustomerStatus.CustomerStatus_ID = Customer.CustomerStatus_ID
          JOIN CustomerPriority ON CustomerPriority.CustomerPriority_ID = Customer.CustomerPriority_ID
          JOIN StateProvince ON StateProvince.State_ID = Customer.CorpLocation_State
          JOIN Country ON Country.Country_ID = StateProvince.Country_ID
          
          WHERE Customer.Customer_ID = {}
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0] 
    
# Employee
def SQL_get_employee_by_id(id):
    str = '''
          SELECT
          Employee.Employee_ID,
          Employee.Emp_FirstName,
          Employee.Emp_LastName,
          Employee.Emp_Phone,
          Employee.Emp_Email,
          Employee.Emp_JobTitle,
          Employee.Emp_PayRate_ID,
          Employee.Emp_Status_ID,
          Employee.Emp_Address_Address1,
          Employee.Emp_Address_Address2,
          Employee.Emp_Location_City,
          Employee.Emp_Location_State,
          Employee.Emp_ZipCode,
          Employee.Emp_Type,
          JobTitle.EmployeeTitle AS 'JobTitle',
          EmployeeDepartment.Emp_Department_ID AS 'DepartmentID',
          EmployeeDepartment.DepartmentName AS 'DepartmentName',
          EmployeePayRate.Emp_PayRate AS 'PayRate',
          EmployeeStatus.Emp_Status AS 'Status',
          StateProvince.State_ID AS 'StateID',
          StateProvince.State_Name AS 'StateName',
          Country.Country_ID AS 'CountryID',
          Country.Country_Name AS 'CountryName',
          EmployeeType.Emp_Type AS 'Type'
          
          FROM Employee
          JOIN JobTitle ON JobTitle.JobTitle_ID = Employee.Emp_JobTitle
          JOIN EmployeeDepartment ON EmployeeDepartment.Emp_Department_ID = JobTitle.Department_ID
          JOIN EmployeePayRate ON EmployeePayRate.EmployeePayRate_ID = Employee.Emp_PayRate_ID
          JOIN EmployeeStatus ON EmployeeStatus.EmployeeStatus_ID = Employee.Emp_Status_ID
          JOIN StateProvince ON StateProvince.State_ID = Employee.Emp_Location_State
          JOIN Country ON Country.Country_ID = StateProvince.Country_ID
          JOIN EmployeeType ON EmployeeType.Emp_Type_ID = Employee.Emp_Type
          
          WHERE Employee.Employee_ID = {0}
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0] 

# Job
def SQL_get_job_by_id(id):
    str = '''
          SELECT
          Job.Job_ID,
          Job.JobDescription,
          Job.Customer_ID,
          Job.JobStatus_ID,
          Job.JobBudget,
          JobStatus.JobStatus AS 'Status',
          Customer.CompanyName AS 'CustomerName'
          
          FROM Job
          JOIN JobStatus ON JobStatus.JobStatus_ID = Job.JobStatus_ID
          JOIN Customer ON Customer.Customer_ID = Job.Customer_ID
          
          WHERE Job.Job_ID = {0}
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]
    
def SQL_get_all_job_complaints(id):
    str = "SELECT * FROM JobComplaint WHERE JobComplaint.Job_ID = {} AND JobComplaint.JobComplaintStatus_ID != 2 ORDER BY JobComplaint.JobComplaint_ID DESC".format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query
    
# JobComplaint
def SQL_get_job_complaint_by_id(id):
    str = '''
          SELECT
          JobComplaint.JobComplaint_ID,
          JobComplaint.Job_ID,
          JobComplaint.JobComplaint_ComplaintDetail,
          JobComplaint.JobComplaint_Date,
          JobComplaint.JobComplaintStatus_ID,
          JobComplaintStatus.JobComplaint_Status AS 'Status'
          
          FROM JobComplaint
          JOIN JobComplaintStatus ON JobComplaintStatus.JobComplaintStatus_ID = JobComplaint.JobComplaintStatus_ID
          
          WHERE JobComplaint.JobComplaint_ID = {0}
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return query[0]
    
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA #
#                            END                                #
# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV #


# ------------------------------------------------------------- #
# 'INSERT/UPDATE' METHODS
# ------------------------------------------------------------- #

# Timesheet Entry
def SQL_insert_timesheet(sheetid, jobassid, statusid, time1, time2):
    str = '''
          INSERT INTO TimesheetEntry_Line 
          (Timesheet_ID, EmployeeJobAssignment_ID, TimesheetEntry_LineStatus_ID, ClockInTime, ClockOutTime) 
          VALUES ({},{},{},'{}','{}')
              
          '''.format(sheetid, jobassid, statusid, time1, time2)
          
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor) 
    
def SQL_update_timesheet(sheetid, jobass, statusid, time1, time2, id):
    str = '''
          UPDATE TimesheetEntry_Line 
          SET Timesheet_ID = {}, 
          EmployeeJobAssignment_ID = {},
          TimesheetEntry_LineStatus_ID = {},
          ClockInTime = '{}', 
          ClockOutTime = '{}'
          
          WHERE TimesheetEntry_Line_ID = {};
          '''.format(sheetid,jobass,statusid,time1,time2,id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor) 

# Announcement   
def SQL_insert_announcement(name, content, statusid, priorityid):
    str = "INSERT INTO Announcement (Announcement_Name, AnnouncementContent, AnnouncementStatus_ID, AnnouncementPriority_ID) VALUES ('{}',(?),{},{});".format(name, statusid, priorityid)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str, content)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_insert_jobcomplaint(jobid, detail, date, status):
    str = "INSERT INTO JobComplaint (Job_ID, JobComplaint_ComplaintDetail, JobComplaint_Date, JobComplaintStatus_ID) VALUES ({},(?),'{}',{});".format(jobid, date, status)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str, detail)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_update_announcement(name,content,status,priority,id):
    str = '''
          UPDATE Announcement
          SET Announcement_Name = '{}', 
          AnnouncementContent = (?),
          AnnouncementStatus_ID = {},
          AnnouncementPriority_ID = {}
          
          WHERE Announcement_ID = {};
          '''.format(name,status,priority,id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str, content)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_update_jobcomplaint(jobid,detail,date,status,id):
    str = '''
          UPDATE JobComplaint
          SET Job_ID = {}, 
          JobComplaint_ComplaintDetail = (?),
          JobComplaint_Date = '{}',
          JobComplaintStatus_ID = {}
          
          WHERE JobComplaint_ID = {};
          '''.format(jobid,date,status,id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str, detail)
    conn.commit()
    close_connections(conn, cursor)
    

    
# Task  
def SQL_insert_task(jobid, startdate, duedate, details, priorityid, statusid):
    str = "INSERT INTO Task (Job_ID, TaskStartDate, TaskDueDate, TaskDetails, TaskPriority_ID, TaskStatus_ID) VALUES ({},'{}','{}',(?),{},{});".format(jobid, startdate, duedate, priorityid, statusid)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str, details)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_insert_taskassignment(empid,taskid,date):
    str = "INSERT INTO TaskAssignment (Employee_ID, Task_ID, TaskAssignment_Date) VALUES ({},{},'{}');".format(empid,taskid,date)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_get_last_taskid():
    str = "SELECT TOP 1 Task_ID FROM Task ORDER BY Task_ID DESC"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)  
    return [x[0] for x in query]
    
def SQL_update_task(jobid, startdate, duedate, details, priorityid, statusid, id):
    str = '''
          UPDATE Task 
          SET Job_ID = {}, 
          TaskStartDate = '{}',
          TaskDueDate = '{}',
          TaskDetails = (?), 
          TaskPriority_ID = {},
          TaskStatus_ID = '{}'
          
          WHERE Task_ID = {};
          '''.format(jobid, startdate, duedate, priorityid, statusid, id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str, details)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_update_taskassignment(empid,date,taskid):
    str = '''
          UPDATE TaskAssignment 
          SET Employee_ID = {}, 
          TaskAssignment_Date = '{}'
          
          WHERE Task_ID = {};
          '''.format(empid,date,taskid)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor)

# Timesheet 
def SQL_insert_timesheet_main(date,empid):
    str = "INSERT INTO Timesheet (TimesheetDate,Employee_ID) VALUES ('{}',{});".format(date,empid)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor)

# Product
def SQL_insert_product(catgoryid, name, description, statusid):
    str = "INSERT INTO Product (ProductCategory_ID, ProductName, ProductDescription, ProductStatus_ID) VALUES ({},(?),(?),{});".format(catgoryid, statusid)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str, name, description)
    conn.commit()
    close_connections(conn, cursor)

def SQL_update_product(name, description, catgoryid, statusid, id):
    str = '''
          UPDATE Product 
          SET ProductName = (?), 
          ProductDescription = (?),
          ProductCategory_ID = {},
          ProductStatus_ID = {}
          
          WHERE Product_ID = {};
          '''.format(catgoryid,statusid,id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str, name, description)
    conn.commit()
    close_connections(conn, cursor) 

# Order
def SQL_insert_order(jobid, duedate, statusid, priorityid):
    str = "INSERT INTO Order_ (Job_ID, OrderDueDate, OrderStatus_ID, OrderPriority_ID) VALUES ({},'{}',{},{});".format(jobid, duedate, statusid, priorityid)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_update_order(jobid, duedate, statusid, priorityid, id):
    str = '''
          UPDATE Order_ 
          SET Job_ID = {}, 
          OrderDueDate = '{}',
          OrderStatus_ID = {},
          OrderPriority_ID = {}
          
          WHERE Order_ID = {};
          '''.format(jobid, duedate, statusid, priorityid, id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor)
    
# Orderline
def SQL_insert_orderline(orderid, productid, quantity, price, status, priority):
    str = '''
          INSERT INTO Order_Line 
          (Order_ID, Product_ID, Product_Quantity, Product_Price, OrderLine_Status_ID, OrderLine_Priority_ID)
          VALUES ({},{},'{}','{}',{},{});
          '''.format(orderid, productid, quantity, price, status, priority)
          
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor) 
    
def SQL_update_orderline(orderid, productid, quantity, price, status, priority, id):
    str = '''
          UPDATE Order_Line 
          SET Order_ID = {}, 
          Product_ID = {},
          Product_Quantity = {},
          Product_Price = {},
          OrderLine_Status_ID = {},
          OrderLine_Priority_ID = {}
          
          WHERE OrderLine_ID = {};
          '''.format(orderid, productid, quantity, price, status, priority, id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor)

# Customer  
def SQL_insert_customer(fname,lname,companyname,phone,priority,status,address1,address2,city,zip,state):
    str = "INSERT INTO Customer (CustomerFirstName,CustomerLastName,CompanyName,CustomerPhone,CustomerPriority_ID,CustomerStatus_ID,CorpAddress_Line1,CorpAddress_Line2,CorpLocation_City,CorpLocation_ZipCode,CorpLocation_State) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(fname,lname,companyname,phone,priority,status,address1,address2,city,zip,state)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_update_customer(fname,lname,companyname,phone,priority,status,address1,address2,city,zip,state,id):
    str = '''
          UPDATE Customer 
          SET CustomerFirstName = (?),
          CustomerLastName = (?),
          CompanyName = (?),
          CustomerPhone = (?),
          CustomerPriority_ID = (?),
          CustomerStatus_ID = (?),
          CorpAddress_Line1 = (?),
          CorpAddress_Line2 = (?),
          CorpLocation_City = (?),
          CorpLocation_ZipCode = (?),
          CorpLocation_State = (?)

          WHERE Customer_ID = {};
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str,fname,lname,companyname,phone,priority,status,address1,address2,city,zip,state)
    conn.commit()
    close_connections(conn, cursor)
    
# Employee
def SQL_insert_employee(fname,lname,phone,email,title,payrate,status,address1,address2,city,state,zip,type):
    str = "INSERT INTO Employee (Emp_FirstName, Emp_LastName, Emp_Phone, Emp_Email, Emp_JobTitle, Emp_PayRate_ID, Emp_Status_ID, Emp_Address_Address1, Emp_Address_Address2, Emp_Location_City, Emp_Location_State, Emp_ZipCode, Emp_Type) VALUES ((?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?));"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str,fname,lname,phone,email,title,payrate,status,address1,address2,city,state,zip,type)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_update_employee(fname,lname,phone,email,title,payrate,status,address1,address2,city,state,zip,type,id):
    str = '''
          UPDATE Employee 
          SET Emp_FirstName = (?),
          Emp_LastName = (?),
          Emp_Phone = (?),
          Emp_Email = (?),
          Emp_JobTitle = (?),
          Emp_PayRate_ID = (?),
          Emp_Status_ID = (?),
          Emp_Address_Address1 = (?),
          Emp_Address_Address2 = (?),
          Emp_Location_City = (?),
          Emp_Location_State = (?),
          Emp_ZipCode = (?),
          Emp_Type = (?)
          
          WHERE Employee_ID = {};
          '''.format(id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str,fname,lname,phone,email,title,payrate,status,address1,address2,city,state,zip,type)
    conn.commit()
    close_connections(conn, cursor)

# Job
def SQL_insert_job(description, customerid, statusid, budget):
    str = "INSERT INTO Job (JobDescription, Customer_ID, JobStatus_ID, JobBudget) VALUES ((?),{},{},{});".format(customerid, statusid, budget)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str, description)
    conn.commit()
    close_connections(conn, cursor) 
    
def SQL_insert_jobass(employeeid, jobid, date, status):
    str = "INSERT INTO EmployeeJobAssignment (Employee_ID, Job_ID, EmployeeJobAssignment_Date, EmployeeJobAssignment_Status) VALUES ({},{},'{}',{});".format(employeeid, jobid, date, status)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor) 
    
def SQL_update_jobass(employeeid, jobid, date, status, id):
    str = '''
          UPDATE EmployeeJobAssignment 
          SET Employee_ID = {}, 
          Job_ID = {},
          EmployeeJobAssignment_Date = '{}',
          EmployeeJobAssignment_Status = {}
          
          WHERE EmployeeJobAssignment_ID = {};
          '''.format(employeeid, jobid, date, status, id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_update_job(description, customerid, statusid, budget, id):
    str = '''
          UPDATE Job 
          SET JobDescription = (?), 
          Customer_ID = {},
          JobStatus_ID = {},
          JobBudget = {}
          
          WHERE Job_ID = {};
          '''.format(customerid, statusid, budget, id)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str, description)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_delete_job_orders(jobid):
    str = '''
          UPDATE Order_
          SET OrderStatus_ID = 2
          
          WHERE Job_ID = {};
          '''.format(jobid)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor)
    
def SQL_delete_order_orderlines(orderid):
    str = '''
          UPDATE Order_Line
          SET OrderLine_Status_ID = 2
          
          WHERE Order_ID = {};
          '''.format(orderid)
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    cursor.execute(str)
    conn.commit()
    close_connections(conn, cursor)
    
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA #
#                            END                                #
# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV #


# ------------------------------------------------------------- #
# 'Report' QUERIES
# ------------------------------------------------------------- #

# AnnouncementsAfterDate
def SQL_announcements_after_date():
    str = '''
        DECLARE
@dept varchar(25)

SELECT @dept = 'Administration'
SELECT
Announcement.Announcement_ID,
Announcement_Name,
AnnouncementStatus.AnnouncementStatus AS 'Status',
AnnouncementPriority.AnnouncementPriority AS 'Priority',
FORMAT(DepartmentAnnouncement.DepartmentAnnouncement_Date,'MMMM dd, yyyy') AS 'Date',
EmployeeDepartment.DepartmentName AS 'Department',
DATEDIFF(day,DepartmentAnnouncement.DepartmentAnnouncement_Date,GETDATE()) AS 'Days Old'

FROM Announcement 
JOIN AnnouncementStatus ON AnnouncementStatus.AnnouncementStatus_ID = Announcement.AnnouncementStatus_ID
JOIN AnnouncementPriority ON AnnouncementPriority.AnnouncementPriority_ID = Announcement.AnnouncementPriority_ID
JOIN DepartmentAnnouncement ON DepartmentAnnouncement.Announcement_ID = Announcement.Announcement_ID
JOIN EmployeeDepartment ON EmployeeDepartment.Emp_Department_ID = DepartmentAnnouncement.Department_ID

WHERE EmployeeDepartment.DepartmentName = @dept 
AND AnnouncementStatus.AnnouncementStatus = 'Active' 
AND AnnouncementPriority.AnnouncementPriority = 'High'
AND DATEDIFF(day,DepartmentAnnouncement.DepartmentAnnouncement_Date,GETDATE()) > 90
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# EmployeeJobs
def SQL_employee_jobs():
    str = '''
DECLARE
@jobtitle varchar(10)

SELECT @jobtitle = 'Accountant'
SELECT
Employee.Employee_ID AS 'Employee ID',
(Employee.Emp_FirstName+' '+Employee.Emp_LastName) AS 'Employee Name',
JobTitle.EmployeeTitle AS 'Job Title',
Job.Job_ID AS 'Job ID',
FORMAT(EmployeeJobAssignment.EmployeeJobAssignment_Date,'MMMM dd, yyyy') AS 'Date Assigned To Job',
JobStatus.JobStatus AS 'Job Status'

FROM Employee
JOIN JobTitle ON JobTitle.JobTitle_ID = Employee.Emp_JobTitle
JOIN EmployeeType ON EmployeeType.Emp_Type_ID = Employee.Emp_Type
JOIN EmployeeStatus ON EmployeeStatus.EmployeeStatus_ID = Employee.Emp_Status_ID
JOIN EmployeeJobAssignment ON EmployeeJobAssignment.Employee_ID = Employee.Employee_ID
JOIN Job ON Job.Job_ID = EmployeeJobAssignment.Job_ID
JOIN JobStatus ON JobStatus.JobStatus_ID = Job.JobStatus_ID

WHERE JobTitle.EmployeeTitle = @jobtitle
AND EmployeeJobAssignment.EmployeeJobAssignment_Status != 2
AND Employee.Emp_Status_ID != 2
AND Job.JobStatus_ID != 2

ORDER BY 'Job Status' ASC;
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# EmployeesTimesheets
def SQL_employee_timesheets():
    str = '''
SELECT
TimesheetEntry_Line.TimesheetEntry_Line_ID AS 'Timesheet Entry ID',
TimesheetEntry_LineStatus.TimesheetEntryLineStatus AS 'Timesheet Entry Status',
(Employee.Emp_FirstName+' '+Employee.Emp_LastName) AS 'Employee Name',
Job.Job_ID AS 'Job',
FORMAT(TimesheetEntry_Line.ClockInTime, '') AS 'Clock-In Time',
FORMAT(TimesheetEntry_Line.ClockOutTime, '') AS 'Clock-Out Time',
FORMAT(TimesheetEntry_Line.TotalHours, 'N2') AS 'Total Hours',
FORMAT(Timesheet.TimesheetDate,'MMMM dd, yyyy') AS 'Date Logged',
DATEDIFF(day,Timesheet.TimesheetDate,GETDATE()) AS 'Days Old'
          
FROM TimesheetEntry_Line 
JOIN TimesheetEntry_LineStatus ON TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = TimesheetEntry_Line.TimesheetEntry_LineStatus_ID
JOIN EmployeeJobAssignment ON EmployeeJobAssignment.EmployeeJobAssignment_ID = TimesheetEntry_Line.EmployeeJobAssignment_ID
JOIN Employee ON Employee.Employee_ID = EmployeeJobAssignment.Employee_ID
JOIN Job ON Job.Job_ID = EmployeeJobAssignment.Job_ID
JOIN Timesheet ON Timesheet.Timesheet_ID = TimesheetEntry_Line.Timesheet_ID
          
WHERE Employee.Emp_Status_ID != 2
AND Job.JobStatus_ID != 2
AND TimesheetEntry_Line.TimesheetEntry_LineStatus_ID = 3
AND DATEDIFF(day,Timesheet.TimesheetDate,GETDATE()) < 60

ORDER BY TimesheetEntry_Line.TimesheetEntry_Line_ID DESC
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# EmployeesWithIncompleteTasks
def SQL_employees_with_incomplete_tasks():
    str = '''
        DECLARE
@status varchar(15)

SELECT @status = 'Incomplete'
SELECT
Employee.Employee_ID AS 'Employee ID',
(Employee.Emp_FirstName+' '+Employee.Emp_LastName) AS 'Employee Name',
Task.Task_ID AS 'Task ID',
FORMAT(TaskAssignment.TaskAssignment_Date,'MMMM, dd yyyy') AS 'Task Assignment Date',
FORMAT(Task.TaskDueDate,'MMMM dd, yyyy') AS 'Task Due Date',
TaskStatus.TaskStatus AS 'Task Status',
TaskPriority.TaskPriority AS 'Task Priority',
DATEDIFF(day,Task.TaskDueDate,GETDATE()) AS 'Days Overdue'

FROM Employee
JOIN TaskAssignment ON TaskAssignment.Employee_ID = Employee.Employee_ID
JOIN Task ON Task.Task_ID = TaskAssignment.Task_ID
JOIN TaskStatus ON TaskStatus.TaskStatus_ID = Task.TaskStatus_ID
JOIN TaskPriority ON TaskPriority.TaskPriority_ID = Task.TaskPriority_ID

WHERE TaskStatus.TaskStatus = @status
AND DATEDIFF(day,Task.TaskDueDate,GETDATE()) > 30

ORDER BY Task.TaskDueDate DESC;
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# JobsWithNotCompleteOrder
def SQL_jobs_with_not_complete_order():
    str = '''
SELECT 
Job.Job_ID AS 'Job ID',
Job.JobDescription AS 'Job Description',
JobStatus.JobStatus AS 'Job Status',
Order_.Order_ID AS 'Order ID',
Order_.OrderDueDate AS 'Order Due Date',
OrderStatus.Order_Status AS 'Order Status',
OrderNote.OrderNote_ID AS 'Order Note ID',
OrderNote.OrderNote_Detail AS 'Order Note Detail'

FROM Job
JOIN JobStatus ON JobStatus.JobStatus_ID = Job.JobStatus_ID
JOIN Order_ ON Order_.Job_ID = Job.Job_ID
JOIN OrderStatus ON OrderStatus.OrderStatus_ID = Order_.OrderStatus_ID
JOIN OrderNote ON OrderNote.Order_ID = Order_.Order_ID

WHERE 
OrderStatus.Order_Status = 'Not Complete' 
ORDER BY Order_.OrderDueDate 

          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# JobsByHighestCustomerPriority
def SQL_jobs_by_highest_customer_priority():
    str = '''
SELECT 
CustomerPriority.CustomerPriority_ID AS 'Customer Priority ID',
CustomerPriority.Customer_Priority AS 'Customer Priority',
CustomerStatus.Customer_Status AS 'Customer Status',
Customer.Customer_ID AS 'Customer ID',
Customer.CompanyName AS 'Company Name',
Job.Job_ID AS 'Job ID',
JobStatus.JobStatus AS 'Job Status'

FROM Customer
JOIN CustomerPriority ON CustomerPriority.CustomerPriority_ID = Customer.CustomerPriority_ID
JOIN CustomerStatus ON CustomerStatus.CustomerStatus_ID = Customer.CustomerStatus_ID
JOIN Job ON Job.Customer_ID = Customer.Customer_ID
JOIN JobStatus ON JobStatus.JobStatus_ID = Job.JobStatus_ID

WHERE CustomerStatus.Customer_Status != 'Inactive' AND JobStatus.JobStatus != 'Inactive'

ORDER BY [Customer Priority ID] DESC

          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# ActiveJobswithUnresolvedComplaints
def SQL_active_jobs_with_unresolved_complaints():
    str = '''
SELECT
JobStatus.JobStatus AS 'Job Status',
Job.Job_ID AS 'Job ID',
Job.JobDescription AS 'Job Description',
JobComplaintStatus.JobComplaint_Status AS 'Job Complaint Status',
JobComplaint.JobComplaint_ComplaintDetail AS 'Complaint Details'

FROM Job
JOIN JobStatus ON JobStatus.JobStatus_ID = Job.JobStatus_ID
JOIN JobComplaint ON JobComplaint.Job_ID = Job.Job_ID
JOIN JobComplaintStatus ON JobComplaintStatus.JobComplaintStatus_ID = JobComplaint.JobComplaintStatus_ID

WHERE 
JobStatus = 'In progress' AND JobComplaintStatus.JobComplaint_Status = 'Unresolved'

          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# ActiveJobswithUnresolvedComplaints
def SQL_incomplete_high_priority_jobs():
    str = '''
SELECT 
Order_.Job_ID AS 'Order ID',
JobStatus.JobStatus AS 'Job Status',
OrderStatus.Order_Status AS 'Order Status',
OrderPriority.Order_Priority As 'Order Priority',
Order_.OrderDueDate As 'Due Date'

FROM Order_
JOIN Job ON Job.Job_ID = Order_.Job_ID
JOIN OrderStatus ON Order_.OrderStatus_ID = OrderStatus.OrderStatus_ID
JOIN OrderPriority ON Order_.OrderPriority_ID = OrderPriority.OrderPriority_ID
JOIN JobStatus ON JobStatus.JobStatus_ID = Job.JobStatus_ID

WHERE
OrderPriority.Order_Priority = 'High'  AND OrderStatus.Order_Status = 'Not Complete' AND JobStatus.JobStatus = 'In progress'

ORDER BY Order_.OrderDueDate Desc;
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# TimesheetEntriesReport
def SQL_Timesheet_Entries_Report():
    str = '''
SELECT
Timesheet.TimesheetDate AS 'Date',
Employee.Employee_ID AS 'Emp ID',
Employee.Emp_FirstName AS 'First Name',
Employee.Emp_LastName AS 'Last Name',
EmployeeJobAssignment.Job_ID AS 'Job ID',
Job.JobDescription AS 'Job Description',
FORMAT(TimesheetEntry_Line.ClockInTime, 't') AS 'In Time',
FORMAT(TimesheetEntry_Line.ClockOutTime, 't') AS 'Out Time',
CONVERT(DECIMAL(6,2),TimesheetEntry_Line.TotalHours) AS 'Hours',
TimesheetEntry_LineStatus.TimesheetEntryLineStatus AS 'Status'

FROM TimesheetEntry_Line
JOIN Timesheet ON Timesheet.Timesheet_ID = TimesheetEntry_Line.Timesheet_ID
JOIN EmployeeJobAssignment ON EmployeeJobAssignment.EmployeeJobAssignment_ID = TimesheetEntry_Line.EmployeeJobAssignment_ID
JOIN Employee ON Employee.Employee_ID = EmployeeJobAssignment.Employee_ID
JOIN TimesheetEntry_LineStatus ON TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = TimesheetEntry_Line.TimesheetEntry_LineStatus_ID
JOIN Job ON Job.Job_ID = EmployeeJobAssignment.Job_ID

WHERE
TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = 3 AND
EmployeeJobAssignment.EmployeeJobAssignment_Status != 2 AND
Job.JobStatus_ID != 2

ORDER BY Timesheet.TimesheetDate DESC;
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)
    return query
    
# TimesheetDailyTotalReport
def SQL_Timesheet_Daily_Total_Report():
    str = '''
SELECT
Timesheet.TimesheetDate AS 'Date',
Employee.Employee_ID AS 'Emp ID',
Employee.Emp_FirstName AS 'First Name',
Employee.Emp_LastName AS 'Last Name',
EmployeeJobAssignment.Job_ID AS 'Job ID',
Job.JobDescription AS 'Job Description',
CONVERT(DECIMAL(6,2),SUM(TimesheetEntry_Line.TotalHours)) AS 'Total Hours'

FROM TimesheetEntry_Line
JOIN Timesheet ON Timesheet.Timesheet_ID = TimesheetEntry_Line.Timesheet_ID
JOIN EmployeeJobAssignment ON EmployeeJobAssignment.EmployeeJobAssignment_ID = TimesheetEntry_Line.EmployeeJobAssignment_ID
JOIN Employee ON Employee.Employee_ID = EmployeeJobAssignment.Employee_ID
JOIN TimesheetEntry_LineStatus ON TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = TimesheetEntry_Line.TimesheetEntry_LineStatus_ID
JOIN Job ON Job.Job_ID = EmployeeJobAssignment.Job_ID


WHERE
EmployeeJobAssignment.EmployeeJobAssignment_Status != 2 AND --Only consider active job assignments--
TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = 3 AND --Only consider approved timesheet entries--
Job.JobStatus_ID !=2 --No logical deletes-

GROUP BY
Employee.Employee_ID,
Timesheet.TimesheetDate,
Employee.Emp_FirstName,
Employee.Emp_LastName,
EmployeeJobAssignment.Job_ID,
Job.JobDescription

ORDER BY Timesheet.TimesheetDate DESC;
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)
    return query
    
# JobCostandBudgetReport
def SQL_Job_Cost_and_Budget_Report():
    str = '''
SELECT
EmployeeJobAssignment.Job_ID AS 'Job ID',
Job.JobDescription AS 'Job Description',
CONVERT(DECIMAL(6,2),SUM(TimesheetEntry_Line.TotalHours)) AS 'Total Hours',
FORMAT(Job.JobBudget,'C') AS 'Budget',
FORMAT(SUM(EmployeePayRate.Emp_PayRate * TimesheetEntry_Line.TotalHours), 'C')  AS 'Total Cost',
FORMAT((Job.JobBudget - (SUM(EmployeePayRate.Emp_PayRate * TimesheetEntry_Line.TotalHours))), 'C') AS 'Budget Variance'

FROM TimesheetEntry_Line
JOIN Timesheet ON Timesheet.Timesheet_ID = TimesheetEntry_Line.Timesheet_ID
JOIN EmployeeJobAssignment ON EmployeeJobAssignment.EmployeeJobAssignment_ID = TimesheetEntry_Line.EmployeeJobAssignment_ID
JOIN Employee ON Employee.Employee_ID = EmployeeJobAssignment.Employee_ID
JOIN JobTitle ON JobTitle.JobTitle_ID = Employee.Emp_JobTitle
JOIN EmployeeDepartment ON EmployeeDepartment.Emp_Department_ID = JobTitle.Department_ID
JOIN EmployeePayRate ON EmployeePayRate.EmployeePayRate_ID = Employee.Emp_PayRate_ID
JOIN TimesheetEntry_LineStatus ON TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = TimesheetEntry_Line.TimesheetEntry_LineStatus_ID
JOIN Job ON Job.Job_ID = EmployeeJobAssignment.Job_ID

WHERE
EmployeeJobAssignment.EmployeeJobAssignment_Status != 2 AND
TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = 3 AND
Job.JobStatus_ID !=2

GROUP BY
Job.Job_ID,
EmployeeJobAssignment.Job_ID,
Job.JobDescription,
Job.JobBudget

ORDER BY Job.Job_ID DESC;
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)
    return query
    
# DepartmentTotalHoursandLaborReport
def SQL_Department_Total_Hours_and_Labor_Report():
    str = '''
SELECT
Timesheet.TimesheetDate AS 'Date',
EmployeeDepartment.DepartmentName AS 'Department',
EmployeeJobAssignment.Job_ID AS 'Job ID',
Job.JobDescription AS 'Job Description',
CONVERT(DECIMAL(6,2),SUM(TimesheetEntry_Line.TotalHours)) AS 'Department Hours',
FORMAT(SUM(EmployeePayRate.Emp_PayRate * TimesheetEntry_Line.TotalHours), 'C') AS 'Department Cost'


FROM TimesheetEntry_Line
JOIN Timesheet ON Timesheet.Timesheet_ID = TimesheetEntry_Line.Timesheet_ID
JOIN EmployeeJobAssignment ON EmployeeJobAssignment.EmployeeJobAssignment_ID = TimesheetEntry_Line.EmployeeJobAssignment_ID
JOIN Employee ON Employee.Employee_ID = EmployeeJobAssignment.Employee_ID
JOIN JobTitle ON JobTitle.JobTitle_ID = Employee.Emp_JobTitle
JOIN EmployeeDepartment ON EmployeeDepartment.Emp_Department_ID = JobTitle.Department_ID
JOIN EmployeePayRate ON EmployeePayRate.EmployeePayRate_ID = Employee.Emp_PayRate_ID
JOIN TimesheetEntry_LineStatus ON TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = TimesheetEntry_Line.TimesheetEntry_LineStatus_ID
JOIN Job ON Job.Job_ID = EmployeeJobAssignment.Job_ID

WHERE
EmployeeJobAssignment.EmployeeJobAssignment_Status != 2 AND --Only consider active job assignments--
TimesheetEntry_LineStatus.TimesheetEntry_LineStatus_ID = 3 AND --Only consider approved timesheet entries--
Job.JobStatus_ID !=2 --No logical deletes-


GROUP BY
Timesheet.TimesheetDate,
EmployeeDepartment.DepartmentName,
EmployeeJobAssignment.Job_ID,
Job.JobDescription

ORDER BY Timesheet.TimesheetDate DESC;
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)
    return query
    
# OverdueTasks
def SQL_overdue_tasks():
    str = '''
Select 
Task.Task_ID as 'Task ID', 
Task.TaskDetails as 'Task Details', 
FORMAT(TaskAssignment.TaskAssignment_Date,'MMMM dd, yyyy') as 'Task Assignment Date',
FORMAT(Task.TaskDueDate,'MMMM dd, yyyy') as 'Task Due Date',
TaskPriority.TaskPriority as 'Task Priority', 
TaskStatus.TaskStatus as 'Task Status',
Employee.Emp_FirstName as 'Employee First Name',
Employee.Emp_LastName as 'Employee Last Name'
From Task
JOIN TaskAssignment ON TaskAssignment.Task_ID = Task.Task_ID
JOIN TaskPriority ON TaskPriority.TaskPriority_ID = Task.TaskPriority_ID
JOIN TaskStatus ON TaskStatus.TaskStatus_ID = Task.TaskStatus_ID
JOIN Employee ON Employee.Employee_ID = TaskAssignment.Employee_ID
Where Task.TaskStatus_ID = 1 AND Task.TaskDueDate < GETDATE()
ORDER BY Task.TaskDueDate asc , Task.TaskPriority_ID desc
          '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)
    return query
    
# ProductOrdersByOrderLinePriority
def SQL_Product_Orders_By_OrderLine_Priority():
    str = '''

DECLARE @quantity INT, @priority INT

SELECT 
@quantity = 5,
@priority = 1

SELECT 
Order_Line.Order_ID AS 'Order ID',
Order_Line.OrderLine_ID AS 'OrderLine ID',
Order_Line.Product_Quantity 'Order Quantity',
Product.ProductName AS 'Product Name',
OrderLine_Priority.OrderLine_Priority AS 'Order Line Priority',
OrderLine_Status.OrderLineStatus AS 'Order Status',
ProductStatus.Product_Status AS 'Product Status'

FROM Order_Line
JOIN Product ON Product.Product_ID = Order_Line.Product_ID
JOIN OrderLine_Priority ON OrderLine_Priority.OrderLine_Priority_ID = Order_Line.OrderLine_Priority_ID 
JOIN OrderLine_Status ON OrderLine_Status.OrderLine_Status_ID = Order_Line.OrderLine_Status_ID
JOIN ProductStatus ON ProductStatus.ProductStatus_ID = Product.ProductStatus_ID

WHERE OrderLine_Status.OrderLineStatus = 'Not Complete' 
AND Order_Line.Product_Quantity >= @quantity 
AND Order_Line.OrderLine_Priority_ID >= @priority
AND ProductStatus.Product_Status = 'Active'

ORDER BY OrderLine_Priority.OrderLine_Priority_ID DESC, [Order Quantity] DESC
        '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query

# OverdueTasksInPipeline
def SQL_Overdue_Tasks_In_Pipeline():
    str = '''

DECLARE @priority INT, @daysOverdue INT

SELECT 
@priority = 3,
@daysOverdue = 300

SELECT DISTINCT

Task.Task_ID AS 'Task ID',
Task.TaskDetails AS 'Task Details',
TaskAssignment.TaskAssignment_Date AS 'Task Assignment Date',
Task.TaskDueDate 'Task Due Date',

[Days In Pipeline] = DATEDIFF(day, TaskAssignment.TaskAssignment_Date, GETDATE()),
CASE WHEN TaskStatus_ID = 1
	 THEN DATEDIFF(day, TaskDueDate, GETDATE()) ELSE 0 END AS 'Days Overdue',

Employee.Employee_ID AS 'Employee ID',

CASE WHEN TaskStatus_ID = 1 THEN 'Incomplete' 
	 WHEN TaskStatus_ID = 2 THEN 'Inactive' 
	 ELSE 'Finished' 
	 END AS 'Task Status',

CASE WHEN TaskPriority.TaskPriority_ID = 1 THEN 'Low' 
	 WHEN TaskPriority.TaskPriority_ID = 2 THEN 'Medium' 
	 WHEN TaskPriority.TaskPriority_ID = 3 AND DATEDIFF(day, TaskDueDate, GETDATE()) <= @daysOverdue THEN 'High' 
	 ELSE 'Urgent'
	 END AS 'Task Priority'

FROM EmployeeJobAssignment
JOIN Employee ON Employee.Employee_ID = EmployeeJobAssignment.Employee_ID
JOIN TaskAssignment ON TaskAssignment.Employee_ID = Employee.Employee_ID
JOIN Task ON Task.Task_ID = TaskAssignment.Task_ID
JOIN TaskPriority ON TaskPriority.TaskPriority_ID = Task.TaskPriority_ID

WHERE TaskStatus_ID = 1 AND TaskPriority.TaskPriority_ID >= @priority
ORDER BY [Task Priority] DESC, [Days Overdue] DESC, [Days In Pipeline] DESC
        '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# NetRevenueAndProfitPerHour
def SQL_Net_Revenue_And_Profit_Per_Hour():
    str = '''

SELECT DISTINCT

Order_.Order_ID AS 'Order ID',
Product.ProductName AS 'Product Name',
Order_Line.Product_Price AS 'Product Price',
Order_Line.Product_Quantity AS 'Product Quantity',
CAST(DATEDIFF(day, Task.TaskStartDate, Task.TaskDueDate) AS DECIMAL) AS 'Production Time (days)',
Job.JobBudget AS 'Job Budget',
Product_Price * Product_Quantity AS 'Net Revenue',

    CASE WHEN
    (DATEDIFF(hour, Task.TaskStartDate, Task.TaskDueDate)) = 0
    THEN ROUND(((Product_Price * Product_Quantity - Job.JobBudget) / 8),2)
    ELSE ROUND((Product_Price * Product_Quantity - Job.JobBudget) / (8 * (1 + (DATEDIFF(day, Task.TaskStartDate, Task.TaskDueDate)))),2) END AS 'Net Profit Per Hour'

FROM Order_
JOIN Order_Line ON Order_Line.Order_ID = Order_.Order_ID
JOIN Product ON Product.Product_ID = Order_Line.Product_ID
JOIN Job ON Job.Job_ID = Order_.Job_ID
JOIN Task ON Task.Job_ID = Job.Job_ID 
JOIN TaskStatus ON TaskStatus.TaskStatus_ID = Task.TaskStatus_ID

WHERE TaskStatus.TaskStatus_ID = 3

GROUP BY Order_.Order_ID, Product.ProductName, Order_Line.Product_Quantity, Order_Line.Product_Price, Job.JobBudget, Task.TaskStartDate, Task.TaskDueDate
ORDER BY [Net Profit Per Hour] DESC
        '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# MonthlySalesComparison
def SQL_Monthly_Sales_Comparison():
    str = '''

SELECT 

DATENAME (MONTH, DATEADD(MONTH, MONTH(Order_.OrderDueDate) - 1, '1900-01-01')) Month,
YEAR(Order_.OrderDueDate) AS 'Year',
COUNT(DISTINCT Customer.Customer_ID) AS '# of Customers',
SUM(Order_Line.Product_Quantity) AS '# of Products Sold',
SUM(Order_Line.OrderLine_Total) AS 'Total Sold (in USD)',

ROUND(
		LAG(SUM(Order_Line.OrderLine_Total), 1) OVER(ORDER BY YEAR(Order_.OrderDueDate)), 
		1) AS 'Previous Month Total Sold',

		FORMAT(((SUM(Order_Line.OrderLine_Total)) - (ROUND(
		LAG(SUM(Order_Line.OrderLine_Total), 1) OVER(ORDER BY YEAR(Order_.OrderDueDate)), 
		1)))  / (ROUND(
		LAG(SUM(Order_Line.OrderLine_Total), 1) OVER(ORDER BY YEAR(Order_.OrderDueDate)), 
		1)), 'P') 'vs. Previous Month'

FROM Order_Line
JOIN Product ON Product.Product_ID= Order_Line.Product_ID
JOIN Order_ ON Order_.Order_ID = Order_Line.Order_ID
JOIN Job ON Job.Job_ID = Order_.Job_ID
JOIN Customer ON Customer.Customer_ID = Job.Customer_ID

GROUP BY YEAR(Order_.OrderDueDate), Month(Order_.OrderDueDate)
ORDER BY YEAR(Order_.OrderDueDate), Month(Order_.OrderDueDate)
        '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query

# CompleteHighPriorityOrderLine
def SQL_complete_high_priority_order_line():
    str = '''
Select
Order_Line.Order_ID As 'Order ID',
Order_Line.Product_ID As ' Product ID',
OrderLine_Status.OrderLineStatus As 'Order Line Status',
OrderLine_Priority.OrderLine_Priority As 'Order Line Priority',
Product_Quantity as 'Product Quantity',
OrderLine_Total as 'Order Line Total'

from Order_
Join Order_Line on Order_.Order_ID =  Order_Line.Order_ID
Join OrderLine_Status on Order_.OrderStatus_ID = Order_Line.OrderLine_Status_ID
Join OrderLine_Priority on Order_.OrderPriority_ID = Order_Line.OrderLine_Priority_ID
Join Product on Product.Product_ID = Order_Line.Product_ID

Where OrderLine_Status.OrderLineStatus = 'Complete' and OrderLine_Priority.OrderLine_Priority = 'High'

Order by [Product Quantity] Asc;

   '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# IncompleteHighPriorityOrders
def SQL_incomplete_high_priority_orders():
    str = '''
SELECT 
Order_.Job_ID AS 'Order ID',
JobStatus.JobStatus AS 'Job Status',
OrderStatus.Order_Status AS 'Order Status ',
OrderPriority.Order_Priority As 'Order Priority ',
OrderDueDate As 'Due Date'

from Order_
JOIN Job ON Job.Job_ID = Order_.Job_ID
JOIN OrderStatus ON Order_.OrderStatus_ID = OrderStatus.OrderStatus_ID
JOIN OrderPriority ON Order_.OrderPriority_ID = OrderPriority.OrderPriority_ID
JOIN JobStatus ON JobStatus.JobStatus_ID = Job.JobStatus_ID

where
OrderPriority.Order_Priority = 'High'  and 
OrderStatus.Order_Status = 'Not Complete' 
and JobStatus.JobStatus = 'In progress'

Order by  OrderDueDate Desc;


   '''
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    columns = [column[0] for column in cursor.description]
    query.insert(0, columns)
    close_connections(conn, cursor)  
    return query
    
# Query List
def all_queries():
    object_list = [
                   (1, 'Active Admin Announcements More Than 90 Days Old', 'Announcement', SQL_announcements_after_date()),
                   
                   (2, 'Jobs By Low Customer Priority', 'Customer', SQL_jobs_by_highest_customer_priority()),
                   
                   (3, 'Department Total Hours and Labor Report', 'Employee', SQL_Department_Total_Hours_and_Labor_Report()),
                   (4, 'Employees with Tasks Overdue by Over 30 Days', 'Employee', SQL_employees_with_incomplete_tasks()),
                   
                   (5, 'Jobs With Not Complete Order', 'Job', SQL_jobs_with_not_complete_order()),
                   (6, 'Active Jobs with Unresolved Complaints', 'Job', SQL_active_jobs_with_unresolved_complaints()),
                   (7, 'Incomplete High Priority Jobs', 'Job', SQL_incomplete_high_priority_jobs()),
                   (8, 'Job Costs and Budget Report', 'Job', SQL_Job_Cost_and_Budget_Report()),
                   
                   (9, 'Complete High Priority Order Line', 'Order', SQL_complete_high_priority_order_line()),
                   (10, 'Incomplete High Priority Orders', 'Order', SQL_incomplete_high_priority_orders),
                   
                   (11, 'Product Orders Arranged by OrderLine Priority', 'Product', SQL_Product_Orders_By_OrderLine_Priority()),
                   (12, 'Monthly Sales Comparison', 'Product', SQL_Monthly_Sales_Comparison()),
                   (13, 'Net Revenue and Profit Per Hour', 'Product', SQL_Net_Revenue_And_Profit_Per_Hour()),
                   
                   (14, 'Overdue Tasks In Pipeline', 'Task', SQL_Overdue_Tasks_In_Pipeline()),
                   
                   (15, 'Timesheet Entries Report', 'Timesheet', SQL_Timesheet_Entries_Report()),
                   (16, 'Approved Timesheet Entries Made in the Last 60 Days', 'Timesheet', SQL_employee_timesheets()),
                   (17, 'Timesheet Daily Total Report', 'Timesheet', SQL_Timesheet_Daily_Total_Report()),
                   
                   #(13, 'Overdue Tasks', 'Task', SQL_overdue_tasks()),
                   #(2, 'Accountants Who Are Actively Assigned to Jobs', 'Employee', SQL_employee_jobs()),
                  ]

    return object_list