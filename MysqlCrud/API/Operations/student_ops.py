from dbconfig.student_model import get_db_connection

def get_all_students():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.callproc('GETALLSTUD')
    result = []
    for res in cursor.stored_results():
        for row in res.fetchall():
            result.append({
                'id' : row[0],
                'name' : row[1],
                'email' : row[2],
                'age' : row[3]
            })
    con.close()
    return result

def student_getby_id(student_id):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.callproc('GetStudentById', [student_id])
    student = {}
    for res in cursor.stored_results():
        row = res.fetchone()
        if row:
            student = {
                'id' : row[0],
                'name' : row[1],
                'email' : row[2],
                'age' : row[3]
            }
    con.close()
    return student

def create_student(name, email, age):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.colalproc('InsertStudent', [name, email, age])
    con.commit()
    con.close()


def update_student(student_id, name, email, age):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.callproc('UpdateStudent', [student_id, name, email, age])
    con.commit()
    con.close()

def delete_student(student_id):
    con = get_db_connection()
    cursor = con. cursor()
    cursor.callproc('DeleteStudent', student_id)
    con.commit()
    con.close()



