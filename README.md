# Konsultera Intern
A Django based inventory management system with multiple user roles and asynchronous cart management. This is an internship screening project for Konsultera.

## Setting up
1. Download / Git clone the project with `git clone https://github.com/tinshade/KonsulteraIntern.git`
2. Create a virtual environment with `python -m venv <name_of_environment>` and activate it.
3. Install the requirements with `pip install -r requirements.txt`.
4. Run the server with `python manage.py runserver` and visit http://127.0.0.1:8000/.

## Pre-existing Credentials
1. Super User > iyengar.abhi@gmail.com #Abhishek98
2. Administrator > newseller@gmail.com #Abhishek98
3. User > newpass@gmail.com #Abhishek98

## Things to note
1. The DB is already migrated.
2. Creating a virtual environment ensure smooth working of the project
3. Debugging is set to True, setting it to false will require collection of static files. Do that with `pythonmanage.py collectstatic` (NOT TESTED WITH DEBUG SET TO FALSE)


## Screenshots
![SS1](https://raw.githubusercontent.com/tinshade/KonsulteraIntern/main/SS/1.PNG "Login Page")
![SS2](https://raw.githubusercontent.com/tinshade/KonsulteraIntern/main/SS/2.PNG "Register Page")
![SS3](https://raw.githubusercontent.com/tinshade/KonsulteraIntern/main/SS/3.PNG "User Item Listing Page")
![SS4](https://raw.githubusercontent.com/tinshade/KonsulteraIntern/main/SS/4.PNG "Admin Item Listing Page")
![SS5](https://raw.githubusercontent.com/tinshade/KonsulteraIntern/main/SS/5.PNG "User Cart View Page")
![SS6](https://raw.githubusercontent.com/tinshade/KonsulteraIntern/main/SS/6.PNG "Admin Add/Edit Product Page")
![SS7](https://raw.githubusercontent.com/tinshade/KonsulteraIntern/main/SS/7.PNG "Logout Page")
![SS8](https://raw.githubusercontent.com/tinshade/KonsulteraIntern/main/SS/8.PNG "Common Jumbotron and Cart Components")