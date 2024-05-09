# Diy Lovebox 
 Hey, this project is about a diy version of the known lovebox gadget for your loved ones! It runs on a docker container running a django framework to be as portable as possible and also an esp8266 with a tft display and a servo.
 <p align="center"> <img src="https://github.com/kdani3/diy-lovebox/blob/main/assets/diy-lovebox-logo.svg" width="30%" /> </p>

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
# Hardware Connections
The hardware that i mentioned above can be connected based on this schematic i have provided![Schematic For ESP, TFT, Servo](https://raw.githubusercontent.com/kdani3/django-lovebox/main/assets/Schematic.png)</br>
Furthermore, the zip file contains the schematic,pcb design and gerber files for ordering the pcb or for the files to be tailored  depending on your needs.
# 3D Models
You can find the heart to use with the servo from [clait's 3d model of the LoveBox](https://www.printables.com/en/model/156756-lovebox-clone-send-love-messages) 
# TO DO
There are many things I would like to implement and improve</br>
1. Implementing The Rest Api for improved security.</br>
2. Maybe a GIF player?? (I'm not gonna sleep).<br>
3. An auto update script for the esp boards that I'm not completely sure that is possible.</br>
4. A 3D printed case for the hardware.</br>
5. Many more that I'm going to think about down the road.

# Notes
I will upload files of the working configuration once I return from my holidays. I designed the pcb while on holidays so I will order it and see if it is functional.</br>
Please check out the amazing repos that gave me the inspiration at first hand [julissa99's Lovebox](https://github.com/julisa99/Lovebox) and [JulianBeaulieu's](https://github.com/JulianBeaulieu/DIY-LoveBox). Also, thanks to [clait](https://www.printables.com/@clait_237854) that I s̶t̶o̶l̶e̶ borrowed from their 3d model to use the heart with my servo. Last but not least, check out [Bodmer's TJpeg Decoder](https://github.com/Bodmer/TJpg_Decoder) that I used for fetching the jpeg to the Arduino esp8266
