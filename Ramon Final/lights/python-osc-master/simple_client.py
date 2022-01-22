"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="2.0.0.2",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8010,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    brightness = 1.0 #0-1
    brightness_change = 0.1
    speed = 2.0 #0.1-4
    speed_change = 0.2

    sign = 0

    #White Color
    client.send_message("/fixtures/Par54-Group-white/visible", "true")

    while True:
        sign = int(input("Are you sad or happy?"))
        if sign == 1:
            print("You're happy")
        elif sign == 0:
            print("You're sad")
        else:
            break

        print("brightness: ", brightness, " speed: ", speed)
        if sign == 0:
        	if brightness >= 0.1:
        		brightness-= brightness_change
        		speed -= speed_change
        elif sign == 1:
        	if brightness <=0.9:
        		brightness += brightness_change
        		speed += speed_change

        client.send_message("/fixtures/Par54-Group-white/luminosity", brightness)
        client.send_message("/medias/Siren-white/Speed", speed)

        time.sleep(1) #Waiting for the EMOTIV to send new signal
    client.send_message("/fixtures/Par54-Group-white/visible", "false")




    blue = 1.0
    red = 0.2
    color_fade_speed = 0.1
    initial_speed = 2.0
    rotate_speed_change = 0.2 #0-4, best if within 1
    
    client.send_message("/fixtures/Par54-Group/visible", "true")
    client.send_message("/fixtures/Par54-Group/children/sliders/1", 26.0)
    while True:
        client.send_message("/medias/Siren/Color/Front_Color/blue", blue)
        client.send_message("/medias/Siren/Color/Front_Color/red", red)
        client.send_message("/medias/Siren/Speed", initial_speed)
        time.sleep(0.1)
    
        print("red: ",red," blue: ", blue, " speed: ", initial_speed)
    
        if blue >= 0.3:
            blue -= color_fade_speed
            initial_speed -= rotate_speed_change
        elif red < 1:
            red += color_fade_speed
            initial_speed += rotate_speed_change
    
        if red > 1:
            client.send_message("/medias/Siren/Speed", 0)
            break
        time.sleep(1)


    # for x in range(10):
    #     #for step in range(10):
    #         #client.send_message("/fixtures/Par54-Group/children/sliders/6", 100)
    #
    #     print("Breakpoint1")
    #     time.sleep(1)
