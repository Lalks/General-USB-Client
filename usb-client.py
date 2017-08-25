#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""

This program is made to communicate with any USB device via the Universal Serial Bus.

The main functionnality doesn't work yet. The skeleton of the application
is made, but the USB communication part is still missing ; it is under
construction, using pyusb.

The goal of this application is to simply read data from the microcontroller
or to read some.




Copyright (C) 2017  Lalks

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


CHANGELOG
0.02 - finished non-tested backend of the receive function
	 - finished non-tested backend of the send function
	 - finished non-tested backend of the connect function
	 - fixed bug on Return key shortcut on PID and VID entries
	 - updated title on Glade file
	 - changed font face of the textview 'terminalOutput'
	 - changed icon
	 - changed format Credits and Licence windows
	 - fix display of Credits window

0.01 - updated widgets' positions (progress bars, buttons, entries)
	 - replaced the lsusb command output by a function made in the program with pyusb (with Vendor and Product names resolver from IDs) 
	 - added 'extended' mode for the output about the devices that are connected to the computer
	 - changed font face of the textview 'terminalOutput'
	 - added Return key shortcut on PID and VID entries
	 - fixed child list to be able to Tab on VID -> PID -> Connect Button


"""


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

import sys
import os

import usb.core # to use pyusb
import usb.util # to use pyusb


"""
SEE THE GIT PAGE TO USE PYUSB CORRECTLY

https://github.com/walac/pyusb/blob/master/docs/tutorial.rst
"""


class managegui:
	def __init__(self):
		self.gladefile = "fenetre-pilote.glade"
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladefile)
		self.builder.connect_signals(self)

		self.window = self.builder.get_object("window")
		self.windowLicence = self.builder.get_object("windowLicence")
		self.windowCredits = self.builder.get_object("windowCredits")

		self.Licence = self.builder.get_object("Licence")
		self.Credits = self.builder.get_object("Credits")
		

		self.boutonRecevoir = self.builder.get_object("boutonRecevoir")
		self.inputRecevoir = self.builder.get_object("inputRecevoir")
		self.boutonEnvoyer = self.builder.get_object("boutonEnvoyer")
		self.inputEnvoyer = self.builder.get_object("inputEnvoyer")


		self.detectGrid = self.builder.get_object("detectGrid")

		self.boutonConnect = self.builder.get_object("boutonConnect")

		self.terminalOutput = self.builder.get_object("terminalOutput")
		self.terminalBuffer = self.builder.get_object("terminalBuffer")
		self.terminalOutput.override_font( Pango.font_description_from_string('Monospace 9') )

		self.detectLabel = self.builder.get_object("detectLabel")

		self.verboseCheck = self.builder.get_object("verboseCheck")

		

		self.inputVID = self.builder.get_object("inputVID")
		self.inputPID = self.builder.get_object("inputPID")


		self.labelLastchange = self.builder.get_object("labelLastchange")


		self.detectGrid.set_focus_chain([self.inputVID, self.inputPID, self.boutonConnect])

		global VID
		VID = "0"
		global PID
		PID = "0"

		self.window.show_all()

	# Need the destroy function to quit when the window is destroy
	def on_window_destroy(self, object, data=None):
		Gtk.main_quit()
		sys.exit(0)

	# Receive button
	def on_boutonRecevoir_clicked(self, object, data=None):
		if VID != 0 and PID != 0:
			# Search the device
			device = usb.core.find(idVendor=VID, idProduct=PID)

			if device is None:
				errorstring = "Device not found: pid={} vid={}".format(VID, PID)
				self.labelLastchange.set_text(errorstring)
			else:
				self.labelLastchange.set_text("Device found")
				UsbDataRead = "Default Value"
				"""
				# GET THE SPEED OF THE DEVICE
				# To determine the maximum size of packet to read
				# 	
				# 	LOW = 1
				# 	FULL = 2
				# 	HIGH = 3
				# 	SUPER = 4
				# 	UNKNOWN = 0
				speed = device.speed
				if speed == 1:
					# The only size of packet is 8 bytes
					size = 8
				elif speed == 2 or speed == 3:
					# The maximum size of packet is 64 bytes
					size = 64
				elif speed == 4:
					# The maximum size of packet is 1024 bytes
					size = 1024
				else:
					size = 8 # Take no risk

				# GET THE CONFIGURATION OF THE DEVICE
				config = device.get_active_configuration()

				# GET THE INTERFACE (example: Human Interface Device)
				interface = config[(0,0)]

				# WE WANT TO WRITE SOMETHING. WE NEED AN ENDPOINT
				endpoint = usb.util.find_descriptor(
					interface,
					# Match the first OUT Endpoint 
					custom_match = \
					lambda e: \
						usb.util.endpoint_direction(e.bEndpointAddress) == \
						usb.util.ENDPOINT_IN)
			
				assert endpoint is not None
			
				# Read data
				UsbDataRead = endpoint.read(size, 3000) # Timeout 3000ms
				statusstring = "Sent: {} | Total of: {} byte.s".format(UsbDataRead, len(UsbDataWrite))
				self.labelLastchange.set_text(statusstring)
				"""
			self.inputRecevoir.set_text(UsbDataRead)
		else:
			self.labelLastchange.set_text("Not connected to any device")

	# Send button
	def on_boutonEnvoyer_clicked(self, object, data=None):
		if VID != 0 and PID != 0:
			UsbDataWrite = self.inputEnvoyer.get_text()

			if UsbDataWrite:
				# Search the device
				device = usb.core.find(idVendor=VID, idProduct=PID)
				print(device)

				if device is None:
					errorstring = "Device not found: pid={} vid={}".format(VID, PID)
					self.labelLastchange.set_text(errorstring)
				else:
					self.labelLastchange.set_text("Device found")
					"""
					# GET THE CONFIGURATION OF THE DEVICE
					config = device.get_active_configuration()

					# GET THE INTERFACE (example: Human Interface Device)
					interface = config[(0,0)]

					# WE WANT TO WRITE SOMETHING. WE NEED AN ENDPOINT
					endpoint = usb.util.find_descriptor(
						interface,
						# Match the first OUT Endpoint 
						custom_match = \
						lambda e: \
							usb.util.endpoint_direction(e.bEndpointAddress) == \
							usb.util.ENDPOINT_OUT)
				
					assert endpoint is not None
				
					# Write data
					size = endpoint.write(UsbDataWrite, 3000) # Timeout 3000ms
					statusstring = "Sent: {} | Total of: {} byte.s".format(UsbDataWrite, size)
					self.labelLastchange.set_text(statusstring)
					"""
			else:
				self.labelLastchange.set_text("No data entered")
		else:
			self.labelLastchange.set_text("Not connected to any device")

	# Refresh button
	""" The output of the 'lsusb' command is more precise than the function of usb.core """
	def on_boutonRefresh_clicked(self, object, data=None):
		verbose = self.verboseCheck.get_active()
		devices = usb.core.find(True)
		strings = ""
		output1 = ""

		for device in devices:
			# Get hexadecimal values (with leading zeros) as strings
			strvendid = str("%0.4X" % device.idVendor)
			strprodid = str("%0.4X" % device.idProduct)


			### GET THE VENDOR'S AND PRODUCT'S NAME FROM THE IDS
			vendor = "Unkown vendor"
			product = "Unkown product"
			vf = 0 # vendor found flag
			with open("usb.ids") as usbids_file:
				for line in usbids_file:
					if not vf:
						if not line[0] == '\t' and not line[0] == '#' and not line[0] == '\n':
							if int(strvendid, 16) == int(line[:4], 16):
								vendor = line[6:-1]
								vf = 1
					else:
						if line[0] == '\t' and not line[0] == '#' and not line[0] == '\n':
							if int(strprodid, 16) == int(line[1:5], 16):
								product = line[7:-1]
			usbids_file.close()

			if not verbose:
				output1 += "ID %s:%s %s %s\n" % (strvendid, strprodid, vendor, product)
			else:
				strings += "%s\n\n" % str(device)

		if verbose:
			output = usb.core._DescriptorInfo(strings)
			self.terminalBuffer.set_text(output)
		else:
			tip = "    VID:PID  VENDOR AND PRODUCT INFORMATIONS\n"
			self.terminalBuffer.set_text(tip+output1)
		self.labelLastchange.set_text("Liste des appareils rafraichie")
	
	def on_inputVID_key_press_event(self, object, event, data=None):
		if event.keyval == 65421: # Return key
			self.boutonConnect.activate()
	def on_inputPID_key_press_event(self, object, event, data=None):
		if event.keyval == 65421: # Return key
			self.boutonConnect.activate()

	# Connect button
	def on_boutonConnect_clicked(self, object, data=None):
		global VID # FOR SEND / RECEIVE FUNCTIONS TO BE ABLE TO GET THE IDs
		global PID # WHEN A BUTTON IS CLICKED. AVOIDS POTENTIAL PROBLEMS

		try:
			# Freeze the entry to variables to avoid problems
			localstrVID = self.inputVID.get_text()
			localstrPID = self.inputPID.get_text()

			# Convert them to int
			localintVID = int(localstrVID, 16)
			localintPID = int(localstrPID, 16)

			"""
			_WHAT IS DONE NEXT_ :
				>>> device = usb.core.find(idVendor=0x093A, idProduct=0x2510) # An USB Mouse
				>>> device
				<DEVICE ID 093a:2510 on Bus 001 Address 006>
				>>> config = device.get_active_configuration() # Config already set by distro drivers
				>>> config
				<CONFIGURATION 1: 100 mA>
				>>> interface = config[(0,0)]
				>>> interface
				<INTERFACE 0: Human Interface Device>
			"""

			# Search the device
			device = usb.core.find(idVendor=localintVID, idProduct=localintPID)

			if device is None:
				self.detectLabel.set_markup("<span foreground='#DD0000'>Non trouvé</span>")
				self.labelLastchange.set_text("Échec de connexion")
			else:
				VID = localintVID # The global vid & pid are modified
				PID = localintPID # because the device has been found


				# À PARTIR D'ICI, ON CONSIDÈRE QUE L'APPAREIL EST CONNECTÉ À L'ORDINATEUR (le kernel a géré le setup)
				
				"""
				DONC À PARTIR D'ICI, IL FAUT PROCÉDER À "SET CONFIGURATION", ÉTAPE 8 ENUMERATION

				pyusb nous permet de ne pas se compliquer la vie à vérifier le device descriptor
				pour mettre en place une configuration spécifique : tout se fait automatiquement
				"""

				""" I COMMENTED TO NOT DAMAGE THE DEVICE WHEN CLICKED THE BUTTON
					(TO UNCOMMENT WHEN SURE OF THE FUNCTION !)

				# SET THE CONFIGURATION
				# Sets the first configuration found
				# Important : if the device has more than one configuration possible
							  you have to add an argument, see the pyusb github repo
				device.set_configuration()

				
				
				self.detectLabel.set_markup("<span foreground='#00AA00'>Connecté !</span>")
				self.labelLastchange.set_text("Connexion établie")
				"""

				# THE TWO NEXT LINES HAVE TO BE DELETED WHEN THE FUNCTION WORKS AND IS UNCOMMENTED
				self.detectLabel.set_markup("<span foreground='#00BBFF'>Coming soon !</span>")
				self.labelLastchange.set_text("La fonction n'est pas encore prête")

		except ValueError:
			self.detectLabel.set_text("VID/PID incorrect")
			self.labelLastchange.set_text("Échec de connexion")
	
	def on_Licence_activate(self, object, data=None):
		self.windowLicence.show()
	def on_windowLicence_destroy(self, object, data=None):
		print("Destoyed") # Debug purpose
		self.windowLicence.hide() # HAVE TO CHECK AROUND HERE !! IT DOESN'T QUIT PROPERLY THE WINDOW
	def on_Credits_activate(self, object, data=None):
		self.windowCredits.show()
	def on_windowCredits_destroy(self, object, data=None):
		print("Destoyed") # Debug purpose
		self.windowCredits.hide() # HAVE TO CHECK AROUND HERE !! IT DOESN'T QUIT PROPERLY THE WINDOW

if __name__ == "__main__":
	main = managegui()
	Gtk.main()
