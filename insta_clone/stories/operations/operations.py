import MySQLdb
from django.conf import settings

def get_connection():
    return MySQLdb.connect(
        host = 'localhost',
        user = 'root',
        password = 'admin',
        database = 'insta_story',
    )

def create_story(user_id, media_url, media_type, duration):
    con = get_connection()
    cursor = con.cursor()
    try:
        cursor.callproc('Create_Story', [user_id, media_url, media_type, duration])
        con.commit()
    except Exception as e:
        raise e
    finally:
        con.close()

def get_active_stories():
    con = get_connection()
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('GET_ACTIVE_STORIES')
    for result in cursor.stored_results():
        stories = result.fetchall()
    con.close()
    return stories

def add_story_view(user_id, story_id):
    con = get_connection()
    cursor = con.cursor()
    cursor.callproc('ADD_STORY_VIEW', [user_id, story_id])
    con.commit()
    con.close()

def add_story_like(user_id, story_id):
    con = get_connection()
    cursor = con.cursor()
    cursor.callproc('ADD_STORY_LIKE', [user_id, story_id])
    con.commit()
    con.close()

def add_story_reply(user_id, story_id, message):
    con = get_connection()
    cursor = con.cursor()
    cursor.callproc('ADD_STORY_REPLY', [user_id, story_id, message])
    con.commit()
    con.close()

def get_story_details(story_id):
    con = get_connection()
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('GET_STORY_DETAILS', [story_id])
    results = [r.fetchall() for r in cursor.stored_results()]
    con.close()
    return {
        "story": results[0][0],
        "views": results[1],
        "likes": results[2],
        "replies": results[3],
    }
