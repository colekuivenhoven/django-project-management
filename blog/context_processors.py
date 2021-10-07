import pyodbc
from django.shortcuts import redirect

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

def SQL_get_all_employee_id():
    str = "SELECT * FROM Employee Where Emp_Status_ID != 2"
    conn = connection_init()
    cursor = connection_cursor_init(conn)
    query = connection_query(conn, cursor, str)
    close_connections(conn, cursor)
    return query
    
def empid_processor(request):
    context = {}
    emps = SQL_get_all_employee_id()
    if 'global_id' in request.session:
        global_id = request.session['global_id']
        context.update({
            'test': global_id,
            'emp_id': global_id,
            'emps': emps,
        })
    else:
        request.session['global_id'] = 1
        global_id = request.session['global_id']
        context.update({
            'test': global_id,
            'emp_id': global_id,
            'emps': emps,
        })
        
    if request.method == "POST":
        if 'global_id' in request.POST:
            global_id = request.POST.get('global_id')
            request.session['global_id'] = global_id
            context.update({
                'test': global_id,
                'emp_id': global_id,
                'emps': emps,
            })
            return context
            
    context.update({
            'emps': emps,
        })
    return context
    