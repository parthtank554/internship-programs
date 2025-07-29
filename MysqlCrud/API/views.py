from django.shortcuts import render, redirect
from dbconfig.student_model import get_db_connection

def student_list(request):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT id,name,email,age FROM student")
    results = cursor.fetchall()
    # con.close()
    students = []
    for row in results:
        students.append({
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'age': row[3]
        })
    return render(request, 'crudapp/student_list.html', {'students': students})

def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO student (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
        con.commit()
        con.close()
        return redirect('student_list')
    return render(request, 'crudapp/student_create.html')
        
def student_edit(request, id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        cursor.execute("UPDATE student SET name=%s, email=%s, age=%s WHERE id=%s", (name, email, age, id))
        conn.commit()
        conn.close()
        return redirect('student_list')
    cursor.execute("SELECT * FROM student WHERE id=%s", (id,))
    student = cursor.fetchone()
    conn.close()
    return render(request, 'crudapp/student_update.html', {'student': {'id': student[0],
    'name': student[1],
    'email': student[2],
    'age': student[3]
}})

def student_delete(request, id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('student_list')
    