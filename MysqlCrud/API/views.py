# from django.shortcuts import render, redirect
# from dbconfig.student_model import get_db_connection

# def student_list(request):
#     con = get_db_connection()
#     cursor = con.cursor()
#     cursor.execute("SELECT id,name,email,age FROM student")
#     results = cursor.fetchall()
#     # con.close()
#     students = []
#     for row in results:
#         students.append({
#             'id': row[0],
#             'name': row[1],
#             'email': row[2],
#             'age': row[3]
#         })
#     return render(request, 'crudapp/student_list.html', {'students': students})

# def create_user(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         age = request.POST['age']
#         con = get_db_connection()
#         cursor = con.cursor()
#         cursor.execute("INSERT INTO student (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
#         con.commit()
#         con.close()
#         return redirect('student_list')
#     return render(request, 'crudapp/student_create.html')
        
# def student_edit(request, id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         age = request.POST['age']
#         cursor.execute("UPDATE student SET name=%s, email=%s, age=%s WHERE id=%s", (name, email, age, id))
#         conn.commit()
#         conn.close()
#         return redirect('student_list')
#     cursor.execute("SELECT * FROM student WHERE id=%s", (id,))
#     student = cursor.fetchone()
#     conn.close()
#     return render(request, 'crudapp/student_update.html', {'student': {'id': student[0],
#     'name': student[1],
#     'email': student[2],
#     'age': student[3]
# }})

# def student_delete(request, id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM student WHERE id=%s", (id,))
#     conn.commit()
#     conn.close()
#     return redirect('student_list')

#-----------------------------------------------------------------------------------------------------------------------
# Direct calling procesure  

from django.shortcuts import render, redirect
from dbconfig.student_model import get_db_connection

def student_list(request):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.callproc('GETALLSTUD')
    for result in cursor.stored_results():
        results = result.fetchall()
    students = [{'id': row[0], 'name': row[1], 'email': row[2], 'age': row[3]} for row in results]
    con.close()
    return render(request, 'crudapp/student_list.html', {'students': students})


def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        con = get_db_connection()
        cursor = con.cursor()
        cursor.callproc('InsertStudent', [name, email, age])
        con.commit()
        con.close()
        return redirect('student_list')
    return render(request, 'crudapp/student_create.html')


def student_edit(request, id):
    con = get_db_connection()
    cursor = con.cursor()

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        cursor.callproc('UpdateStudent', [id, name, email, age])
        con.commit()
        con.close()
        return redirect('student_list')

    cursor.callproc('GetStudentById', [id])
    for result in cursor.stored_results():
        student = result.fetchone()

    con.close()
    return render(request, 'crudapp/student_update.html', {
        'student': {'id': student[0], 'name': student[1], 'email': student[2], 'age': student[3]}
    })


def student_delete(request, id):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.callproc('DeleteStudent', [id])
    con.commit()
    con.close()
    return redirect('student_list')

#-----------------------------------------------------------------------------------------------------------------------
# Calling Via the Student Operation File 

# from django.views import View
# from django.shortcuts import render, redirect
# from API.Operations.student_ops import *


# class StudentListView(View):
#     def get(self, request):
#         try:
#             students = get_all_students()
#             return render(request, 'crudapp/student_list.html', {'students': students})
#         except Exception as e:
#             return render(request, 'crudapp/error.html', {'error': str(e)})


# class StudentCreateView(View):
#     def get(self, request):
#         try:
#             return render(request, 'crudapp/student_create.html')
#         except Exception as e:
#             return render(request, 'crudapp/error.html', {'error': str(e)})

#     def post(self, request):
#         try:
#             name = request.POST['name']
#             email = request.POST['email']
#             age = request.POST['age']
#             create_student(name, email, age)
#             return redirect('student_list')
#         except Exception as e:
#             return render(request, 'crudapp/error.html', {'error': str(e)})


# class StudentEditView(View):
#     def get(self, request, id):
#         try:
#             student = student_getby_id(id)
#             return render(request, 'crudapp/student_update.html', {'student': student})
#         except Exception as e:
#             return render(request, 'crudapp/error.html', {'error': str(e)})

#     def post(self, request, id):
#         try:
#             name = request.POST['name']
#             email = request.POST['email']
#             age = request.POST['age']
#             update_student(id, name, email, age)
#             return redirect('student_list')
#         except Exception as e:
#             return render(request, 'crudapp/error.html', {'error': str(e)})


# class StudentDeleteView(View):
#     def get(self, request, id):
#         try:
#             delete_student(id)
#             return redirect('student_list')
#         except Exception as e:
#             return render(request, 'crudapp/error.html', {'error': str(e)})
