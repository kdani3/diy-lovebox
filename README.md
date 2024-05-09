# Django Lovebox Docker 
Hey, this project is about a diy version of the known lovebox gadget for your loved ones! It runs on a docker container to be as portable as possible and also an esp8266 with a tft display and a servo.

1.To get started clone the repo and unzip it</br>

2.Inside the directory create a python venv 
```python -m venv venv```</br>
3.Activate the venv 
```source venv/bin/activate```</br>
4.Go into the django_docker dir and install the requirements.txt
```cd django_docker && pip install -r requirements.txt```</br>
5.run the following commands
```python manage.py makemigrations```
```python manage.py migrate```</br>
6. Create the admin user 
```python manage.py createsuperuser```</br>
7.Test that everything works and login
```python manage.py runserver```</br>
8.If everything works as expected deploy the django docker, the default port I chose in the docker deploy file is *3030* you can change it to whatever you wish.
I used a [cloudflare tunnel](https://www.cloudflare.com/products/tunnel/) on my Rock64 to make the django container accessible to the esp boards outside of my LAN. If you wish you could also use the local IP of your docker container to communicate with an esp in your LAN, but i haven't tested that yet.  
# Hardware
The TFT LCD screen I used is the 1.8-inch 128x160 with the ST7735 board that can be found [here](https://www.amazon.com/M%C3%B3dulo-pantalla-pulgadas-ST7735-128x160/dp/B07BFV69DZ?language=en_US&currency=USD)</br>
The ESP8266 board can be bought [here](https://store.arduino.cc/products/nodemcu-esp8266)</br>
Finally,the servo I used is the SG90 Micro Servo and can be found [here](https://www.amazon.com/Miuzei-Helicopter-Airplane-Remote-Control/dp/B07NSVKZP7/ref=sr_1_1?sr=8-1)</br>
You will also need a way to power the arduino so plan accordingly</br>

