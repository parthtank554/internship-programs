from .db_connection import get_db_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password, full_name):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    hashed_password = hash_password(password)
    
    try:
        cursor.callproc('RegisterUser', [username, email, hashed_password, full_name])
        for result in cursor.stored_results():
            user_id = result.fetchone()['user_id']
        con.commit()
        return user_id
    except Exception as e:
        con.rollback()
        raise e
    finally:
        con.close()

def get_user_by_username(username):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    
    try:
        cursor.callproc('GetUserByUsername', [username])
        for result in cursor.stored_results():
            user = result.fetchone()
        return user
    finally:
        con.close()

def get_user_by_email(email):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    
    try:
        cursor.callproc('GetUserByEmail', [email])
        for result in cursor.stored_results():
            user = result.fetchone()
        return user
    finally:
        con.close()

def get_user_by_id(user_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    
    try:
        cursor.callproc('GetUserById', [user_id])
        for result in cursor.stored_results():
            user = result.fetchone()
        return user
    finally:
        con.close()

def update_user_profile(user_id, full_name, profile_pic):
    con = get_db_connection()
    cursor = con.cursor()
    
    try:
        cursor.callproc('UpdateUserProfile', [user_id, full_name, profile_pic])
        con.commit()
    except Exception as e:
        con.rollback()
        raise e
    finally:
        con.close()

def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user and user['password'] == hash_password(password):
        return user
    return None

def follow_user(follower_id, username):
    con = get_db_connection()
    cursor = con.cursor()
    try:
        # Get the user_id of the user to be followed
        # cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        cursor.callproc('FollowUser', (follower_id, username))
        result = cursor.fetchone()
        if result:
            followed_id = result[0]
            # Insert into followers table (adjust table/column names as needed)
            # cursor.execute(
            #     "INSERT IGNORE INTO followers (follower_id, followed_id) VALUES (%s, %s)",
            #     (follower_id, followed_id)
            # )
            cursor.callproc('FollowUser', (follower_id, username))
            con.commit()
    finally:
        con.close()

def unfollow_user(follower_id, username):
    con = get_db_connection()
    cursor = con.cursor()
    try:
        cursor.callproc('UnfollowUser', (follower_id, username))
        result = cursor.fetchone()
        if result:
            followed_id = result[0]
            cursor.callproc('UnfollowUser', (follower_id, username))
            con.commit()
    finally:
        con.close()