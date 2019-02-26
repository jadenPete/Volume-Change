#!/usr/bin/env python

import socket
import subprocess
import os

import gi
gi.require_version("Notify", "0.7")
from gi.repository import Notify, GLib

def get_volume(command):
	output = subprocess.getoutput(command)

	start = output.find('[') + 1
	end = output.find('%]', start + 1)

	return int(output[start:end]), output[end:end + 6] == "%] [on"

def get_icon(volume, enabled):
	icon = "audio-volume-"

	if not enabled or volume == 0:
		icon += "muted"
	elif volume < 34:
		icon += "low"
	elif volume < 67:
		icon += "medium"
	else:
		icon += "high"

	return icon

def set_volume(volume):
	volume, enabled = get_volume("amixer set Master " + volume)

	notification.update(" ", icon = get_icon(volume, enabled))
	notification.set_hint("value", GLib.Variant("i", volume))

server_address = "/tmp/vc-server"

try:
	os.unlink(server_address)
except OSError:
	if os.path.exists(server_address):
		raise

# Initialize the socket connection
server_socket = socket.socket(socket.AF_UNIX)
server_socket.bind(server_address)
server_socket.listen(1)

# Initialise the D-Bus connection
Notify.init("volume-change")

# Initialize the notification
notification = Notify.Notification.new("")

while True:
	buffer = server_socket.accept()[0].recv(1)

	if len(buffer) > 0:
		if buffer == b"0":
			set_volume("2%-")
		elif buffer == b"1":
			set_volume("2%+")
		elif buffer == b"2":
			set_volume("toggle")
		else:
			continue

		# Prevent duplicate notifications
		notification.show()
