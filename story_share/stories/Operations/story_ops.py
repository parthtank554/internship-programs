from django.shortcuts import redirect, render
from .db_connection import get_db_connection
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.urls import *


def create_story(user_id, media_url, media_type, duration):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    
    try:
        cursor.callproc('CreateStory', [user_id, media_url, media_type, duration])
        for result in cursor.stored_results():
            story_id = result.fetchone()['story_id']
        con.commit()
        return story_id
    except Exception as e:
        con.rollback()
        raise e
    finally:
        con.close()

def get_story(story_id):
    con = get_db_connection()
    cursor = con.cursor()
    query = """
        SELECT s.id, s.media_url, s.media_type, s.created_at,
               u.username, u.profile_pic
        FROM story s
        JOIN users u ON s.user_id = u.id
        WHERE s.id = %s
    """
    cursor.execute(query, (story_id,))
    row = cursor.fetchone()
    con.close()

    if row:
        return {
            'id': row[0],
            'media_url': row[1],
            'media_type': row[2],
            'created_at': row[3],
            'username': row[4],
            'profile_pic': row[5],
        }
    return None

def get_all_story_ids_ordered():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.callproc('GetActiveStories')

    story_ids = []
    for result in cursor.stored_results():
        for row in result.fetchall():
            story_ids.append(row[0])  # ID is column 0

    con.close()
    return story_ids

def get_active_stories():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    
    try:
        cursor.callproc('GetActiveStories')
        for result in cursor.stored_results():
            stories = result.fetchall()
        return stories
    finally:
        con.close()

def get_user_stories(user_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    
    try:
        cursor.callproc('GetUserStories', [user_id])
        for result in cursor.stored_results():
            stories = result.fetchall()
        return stories
    finally:
        con.close()

def get_story_details(story_id):
    con = get_db_connection()
    cursor = con.cursor()

    try:
        cursor.callproc('GET_SINGLE_STORY_BY_ID', [story_id])
        story = None

        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                story = {
                    'id': row[0],
                    'user_id': row[1],
                    'username': row[2],
                    'profile_pic': row[3],
                    'media_url': row[4],
                    'media_type': row[5],
                    'duration': row[6],
                    'created_at': row[7],
                }
        return story

    finally:
        con.close()
def story_details(request, story_id):
    if not request.session.get("user_id"):
        return redirect("login")

    story_data = get_story_details_by_id(story_id)

    if not story_data:
        return render(request, "story_not_found.html")

    return render(request, "story_details.html", {
        "story": story_data["story"],
        "views": story_data["views"],
        "likes": story_data["likes"],
        "replies": story_data["replies"]
    })

def get_story_details_by_id(story_id):
    con = get_db_connection()
    cursor = con.cursor()
    
    cursor.callproc("GetStoryDetails", [story_id])
    result_sets = []
    
    for result in cursor.stored_results():
        result_sets.append(result.fetchall())

    con.close()

    if not result_sets or not result_sets[0]:
        return None

    # First result is story info with user
    story_row = result_sets[0][0]
    story = {
        "id": story_row[0],
        "user_id": story_row[1],
        "media_url": story_row[2],
        "media_type": story_row[3],
        "duration": story_row[4],
        "created_at": story_row[5],
        "expires_at": story_row[6],
        "username": story_row[7],
        "profile_pic": story_row[8],
    }

    # Views (2nd result)
    views = [{
        "id": row[0],
        "story_id": row[1],
        "user_id": row[2],
        "viewed_at": row[3],
        "username": row[4],
        "profile_pic": row[5]
    } for row in result_sets[1]] if len(result_sets) > 1 else []

    # Likes (3rd result)
    likes = [{
        "id": row[0],
        "story_id": row[1],
        "user_id": row[2],
        "liked_at": row[3],
        "username": row[4],
        "profile_pic": row[5]
    } for row in result_sets[2]] if len(result_sets) > 2 else []

    # Replies (4th result)
    replies = [{
        "id": row[0],
        "story_id": row[1],
        "user_id": row[2],
        "message": row[3],
        "replied_at": row[4],
        "username": row[5],
        "profile_pic": row[6]
    } for row in result_sets[3]] if len(result_sets) > 3 else []

    return {
        "story": story,
        "views": views,
        "likes": likes,
        "replies": replies
    }
def get_all_story_ids():
    con = get_db_connection()
    cursor = con.cursor()

    try:
        cursor.callproc("GET_ALL_STORY_IDS")

        for result in cursor.stored_results():
            ids = result.fetchall()

        return [row[0] for row in ids]

    finally:
        con.close()

def check_user_liked_story(user_id, story_id):
    con = get_db_connection()
    cursor = con.cursor()

    try:
        cursor.callproc("CHECK_USER_LIKED", [user_id, story_id])
        for result in cursor.stored_results():
            data = result.fetchone()
        return bool(data and data[0] == 1)

    finally:
        con.close()

def add_story_view(user_id, story_id):
    con = get_db_connection()
    cursor = con.cursor()

    try:
        cursor.callproc("ADDSTORYVIEW", [user_id, story_id])
        con.commit()

    finally:
        con.close()

def add_story_like(user_id, story_id):
    con = get_db_connection()
    cursor = con.cursor()
    try:
        # Check if user already liked the story
        cursor.execute("SELECT COUNT(*) FROM story_likes WHERE user_id=%s AND story_id=%s", (user_id, story_id))
        result = cursor.fetchone()
        if result[0] == 0:  # User hasn't liked the story yet
            cursor.execute("INSERT INTO story_likes (user_id, story_id, created_at) VALUES (%s, %s, NOW())", 
                          (user_id, story_id))
            con.commit()
    finally:
        con.close()

def add_story_reply(user_id, story_id, reply_text):
    con = get_db_connection()
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO story_replies (user_id, story_id, reply_text, created_at) VALUES (%s, %s, %s, NOW())", 
                      (user_id, story_id, reply_text))
        con.commit()
    finally:
        con.close()

def get_likes(story_id):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.callproc('GetStoryDetails', [story_id])

    result_sets = []
    for result in cursor.stored_results():
        result_sets.append(result.fetchall())

    con.close()
    likes_data = result_sets[2] if len(result_sets) > 2 else []

    likes = [{
        'id': row[0],
        'story_id': row[1],
        'user_id': row[2],
        'liked_at': row[3],
        'username': row[4],
        'profile_pic': row[5]
    } for row in likes_data]

    return likes


def get_story_views(story_id):
    con = get_db_connection()
    cursor = con.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM story_views WHERE story_id = %s", (story_id,))
        result = cursor.fetchone()
        return result[0]
    finally:
        con.close()


def get_story_replies(story_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, reply_text, created_at FROM story_replies WHERE story_id = %s ORDER BY created_at DESC", (story_id,))
        replies = cursor.fetchall()
        return replies
    finally:
        con.close()
