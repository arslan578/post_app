# POST APP


### Features

1. **Local Authentication** using email and password with [allauth](https://pypi.org/project/django-allauth/)
2. **Rest API** using [django rest framework](http://www.django-rest-framework.org/)


# Development

Following are instructions on setting up your development environment.

## Local Setup 

1. [Python](https://www.python.org/downloads/release/python-365/)

### Installation

1. Install [pipenv](https://pypi.org/project/pipenv/)
2. Clone this repo and `cd post_app`
3. Run `pip3 install pipenv`
4. Run `pipenv install`

### Getting Started

1. Run `python manage.py makemigrations`
2. Run `python manage.py migrate`
3. Run `python manage.py runserver`
