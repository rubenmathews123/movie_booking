superuser access: username: sthapa
                  password: 2215

# 🎬 Movie Theater Booking System

A Django-based web application for booking movie tickets, with a RESTful API.

## 📂 Project Structure
movie_theater_booking/
│── bookings/             # Django app (models, views, serializers)
│   ├── migrations/       # Database migrations
│   ├── templates/        # HTML templates
│   ├── static/           # CSS and static files
│   ├── tests.py          # Unit and API tests
│   ├── models.py         # Database models
│   ├── views.py          # Application logic
│   ├── serializers.py    # API serializers
│   ├── urls.py           # URL routing
│
│── movie_theater_booking/  # Django project settings
│   ├── settings.py        # Project settings
│   ├── urls.py            # Project-level URL routing
│
│── manage.py              # Django management script
│── db.sqlite3             # SQLite database (if used)
│── requirements.txt       # Dependencies file
│── README.md              # Documentation


# 🚀 How to Run the Project Locally

1️⃣ Install Dependencies
Make sure you have Python 3 and pip installed.
pip install -r requirements.txt

2️⃣ Apply Migrations
python manage.py migrate

3️⃣ Create a Superuser (for Admin Panel)
python manage.py createsuperuser

4️⃣ Run the Development Server
python manage.py runserver

Then visit http://127.0.0.1:8000/ in your browser.

--------------------------------------------------------

✅ How to Run Tests (13 tests are created)
To verify the functionality, 
run: python manage.py test bookings
