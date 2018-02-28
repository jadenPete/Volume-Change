#!/usr/bin/env python3

import socket

from gi.repository import Notify
from subprocess    import getoutput

def volume_decrease():
	# Decrease the volume and get the percentage
	percent = int(getoutput('amixer -D pulse sset Master 2%- | grep -oP "(?<=\[)[0-9]{1,2}(?=%\])" | sort -nr | head -n 1'))

	# Mute if the volume is 0
	if percent == 0:
		getoutput('amixer -D pulse set Master mute');

	# Determine the logo from the percent
	logo = 'audio-volume-'

	if percent == 0:
		logo += 'muted'
	elif percent < 30:
		logo += 'low'
	elif percent < 70:
		logo += 'medium'
	else:
		logo += 'high'

	logo += '-symbolic'

	# Create and show the notification
	notification.update(" ", icon = logo)
	notification.set_hint_int32("value", percent)

def volume_increase():
	# Increase the volume and get the percentage
	percent = int(getoutput('amixer -D pulse sset Master 2%+ > /dev/null; amixer -D pulse sset Master unmute | grep -oP "(?<=\[)[0-9]{1,2}(?=%\])" | sort -nr | head -n 1'))

	# Determine the logo from the percent
	logo = 'audio-volume-'

	if percent < 30:
		logo += 'low'
	elif percent < 70:
		logo += 'medium'
	else:
		logo += 'high'

	logo += '-symbolic'

	# Create and show the notification
	notification.update(" ", icon = logo)
	notification.set_hint_int32("value", percent)

def volume_toggle():
	# Mute the volume and get the percentage
	percent = int(getoutput('amixer -D pulse sget Master | grep -oP "(?<=\[)[0-9]{1,2}(?=%\])" | sort -nr | head -n 1'))

	# Determine the logo from the percent
	logo = 'audio-volume-'

	# Mute if the volume is not 0
	if percent != 0:
		getoutput('amixer -D pulse sset Master toggle')

		if percent < 30:
			logo += 'low'
		elif percent < 70:
			logo += 'medium'
		else:
			logo += 'high'
	else:
		logo += 'muted'

	logo += '-symbolic'

	# Create and show the notification
	notification.update(" ", icon = logo)
	notification.set_hint_int32("value", percent)

# Initialize the socket connection
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 2357))
serversocket.listen(1)

# Initialise the D-Bus connection
Notify.init("volume-change")

# Initialize the Notification
notification = Notify.Notification.new("")

while True:
	connection, address = serversocket.accept()
	buf = connection.recv(1)

	if len(buf) > 0:
		if buf == b"0":
			volume_decrease()
		elif buf == b"1":
			volume_increase()
		elif buf == b"2":
			volume_toggle()
		else:
			continue

		notification.close()
		notification.show()
