# QuizApp

A Django web application for creating and taking quizzes with user authentication.

## Features

- User registration and login
- Random quiz questions (5 per quiz)
- Score tracking and results
- Admin panel for managing questions



## Usage
Register at /

Login at /login/

Take quiz at /quiz/index-page

View results at /quiz/show-results

Admin panel at /admin/

## Project Structure

```text
quizapp/
├── authentication/     # User auth
├── quiz/              # Quiz functionality
├── templates/         # HTML templates
├── quizapp/          # Main settings
└── requirements.txt   # Dependencies

```
## Dependencies
Django 5.0.4

validate_email 1.3

whitenoise 6.6.0

python-decouple 3.8

## License
MIT License

Copyright (c) [2025] [Mazlum Unay]