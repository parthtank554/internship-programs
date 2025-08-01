# 🐍 Django CRUD API 🚀

A simple and clean **CRUD API** built using the **Django Framework** and **SQLite Database**. This project allows you to **Create**, **Read**, **Update**, and **Delete** student records with ease using RESTful principles.

---

## 📁 Project Structure

dgapi/
├── manage.py
├── db.sqlite3  
├── dgapi/
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
├── API/
│ ├── migrations/
│ ├── models.py 📦
│ ├── views.py 👁️
│ ├── urls.py 🌐
│ ├── serializers.py 🧰
---

## 🧩 Features

- 🔁 **Full CRUD Operations**
- 🛡️ Built with Django REST Framework
- 🗃️ Connected with MySQL Database
- 💡 JSON API endpoints with proper response structure
- ✅ Easily testable with **Thunder Client** / **Postman**

---

## ⚙️ Setup Instructions

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-username/django-crud-api.git
cd django-crud-api

# 2️⃣ Create virtual environment and activate
python -m venv venv
# For macOS/Linux:
source venv/bin/activate
# For Windows:
venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Update database settings in dgapi/settings.py 🛠️
# Open the file and replace the DATABASES section:
# (Skip this if you're using SQLite)
# 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'your_db_name',
#         'USER': 'your_username',
#         'PASSWORD': 'your_password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# 5️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

# 6️⃣ Run the development server
python manage.py runserver

# 7️⃣ Open browser or API client (Thunder Client/Postman)
# Go to: http://127.0.0.1:8000/students/
```

🔗 API Endpoints
Method	Endpoint	Description
GET	/students/	Get all students
POST	/students/	Add a new student
GET	/students/{id}	Get a student by ID
PUT	/students/{id}	Update student by ID
DELETE	/students/{id}	Delete student by ID

📍 You can test these endpoints using Thunder Client or Postman.

🧪 Sample JSON Body (for POST/PUT)
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 21
}

###✨ Tech Stack
🐍 Python 3.x

🦄 Django 4.x

🔧 Django REST Framework

🐬 SQLITE3

💻 Thunder Client / Postman (for testing)

🙌 Author
Made with ❤️ by Parth Tank
