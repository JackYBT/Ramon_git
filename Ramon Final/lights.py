import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

class Lights():
	def __init__(self, ip="2.0.0.2", port=8010):
		    parser = argparse.ArgumentParser()
		    parser.add_argument("--ip", default=ip,
		                        help="The ip of the OSC server")
		    parser.add_argument("--port", type=int, default=port,
		                        help="The port the OSC server is listening on")
		    args = parser.parse_args()

		    self.client = client = udp_client.SimpleUDPClient(args.ip, args.port)

		    self.brightness = 0.5
		    self.speed = 1.0

		    self.client.send_message("/fixtures/Par54-Group-white/visible", "true")
		    self.client.send_message("/medias/Siren-white/Speed", self.speed)
		    self.client.send_message("/fixtures/Par54-Group-white/luminosity", self.brightness)


	def set_speed(self, speed):
		if speed < 0.1: speed = 0.1
		if speed > 3.0: speed = 3.0
		self.client.send_message("/medias/Siren-white/Speed", speed)
		self.speed = speed

	def set_brightness(self, brightness):
		if speed < 0.1: speed = 0.1
		if speed > 1.0: speed = 1.0
		self.client.send_message("/fixtures/Par54-Group-white/luminosity", brightness)
		self.brightness = brightness
