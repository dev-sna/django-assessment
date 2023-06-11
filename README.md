# django-assessment

This project is based on Django 3>
Built on Docker to avoid setup issues related to dependencies

Initial Setup

Run: make upnew

After that, run: make shell
In the shell type: ./manage.py migrate
This will create postgresql tables

Later Run: make up

In order to create a super user do following steps:

1. Start the server: make up
2. Open another terminal in the same directory and run: make shell
3. Now in the shell type: ./manage.py createsuperuer
4. Follow the prompts
