# Django Lovebox Docker 
Hey, this project is about a diy version of the known lovebox gadget for your loved ones! It runs on a docker container to be as portable as possible and also an esp8266 with a tft display and a servo.

1.To get started clone the repo and unzip it</br>

2.Inside the directory create a python venv 
```python -m venv venv```</br>
3.Activate the venv 
```source venv/bin/activate```</br>
4.Go into the django_docker dir and install the requirements.txt</br>
```cd django_docker && pip install -r requirements.txt```
5.run the following commands
```python manage.py makemigrations```
```python manage.py migrate```</br>
6. Create the admin user 
```python manage.py createsuperuser```</br>
7.Test that everything works and login
```python manage.py runserver```</br>
8.If everything works as expected deploy the django docker, the default port i chose in the docker deploy file is *3030* you can change it to whatever you wish.
# I'm going to continue with the instructions for the esp8266
