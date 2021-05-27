# Facebull Application

The facebull application is an API for a social network.

# How to use

Follow the following steps :

- Create your virtual environment
- Git clone the project
- Install the requirements
- Launch the tests with python manage.py test

# Using Celery and Redis

If you want to test the application live, you can launch Redis with :
redis-server

Then, in another terminal, start celery with:
celery -A tradecore worker -l info