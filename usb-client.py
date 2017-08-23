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
0.01 - updated widgets' positions (progress bars, buttons, entries)
	 - replaced the lsusb command output by a function made in the program with pyusb
	 - added 'extended' mode for the output about the devices that are connected to the computer
	 - 



"""


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango

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

		self.Licence = self.builder.get_object("Licence")
		

		self.boutonRecevoir = self.builder.get_object("boutonRecevoir")
		self.inputRecevoir = self.builder.get_object("inputRecevoir")
		self.boutonEnvoyer = self.builder.get_object("boutonEnvoyer")
		self.inputEnvoyer = self.builder.get_object("inputEnvoyer")


		self.detectGrid = self.builder.get_object("detectGrid")

		self.boutonConnect = self.builder.get_object("boutonConnect")

		self.terminalOutput = self.builder.get_object("terminalOutput")
		self.terminalBuffer = self.builder.get_object("terminalBuffer")
		self.terminalOutput.override_font( Pango.font_description_from_string('Roboto Mono 9') )

		self.detectLabel = self.builder.get_object("detectLabel")

		self.verboseCheck = self.builder.get_object("verboseCheck")

		

		self.inputVID = self.builder.get_object("inputVID")
		self.inputPID = self.builder.get_object("inputPID")


		self.labelLastchange = self.builder.get_object("labelLastchange")


		self.detectGrid.set_focus_chain([self.inputVID, self.inputPID, self.boutonConnect])


		self.window.show_all()

	# Need the destroy function to quit when the window is destroy
	def on_window_destroy(self, object, data=None):
		Gtk.main_quit()
		sys.exit(0)

	# Receive button
	def on_boutonRecevoir_clicked(self, object, data=None):
		#usbPort = self.inputPort.get_text()
		""" ICI IL FAUT LIRE LES DONNEES DU BUS ET INSÉRER DANS LA VARIABLE UsbDataRead """
		UsbDataRead = "Default value"
		self.inputRecevoir.set_text(UsbDataRead)

	# Send button
	def on_boutonEnvoyer_clicked(self, object, data=None):
		usbPort = self.inputPort.get_text()
		""" ICI IL FAUT ÉCRIRE LES DONNEES VERS LE BUS """
		UsbDataWrite = self.inputEnvoyer.get_text()
		print(UsbDataWrite)

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
	
	def on_inputVID_key_press_event(self, object, ev, data=None):
		if ev.keyval == Gdk.KEY_Return:
			self.boutonConnect.activate()
	def on_inputPID_key_press_event(self, object, ev, data=None):
		if ev.keyval == Gdk.KEY_Return:
			self.boutonConnect.activate()

	# Connect button
	def on_boutonConnect_clicked(self, object, data=None):
		try:
			VID = int(self.inputVID.get_text(), 16)
			PID = int(self.inputPID.get_text(), 16)

			# Search the device
			device = usb.core.find(idVendor=VID, idProduct=PID)

			if device is None:
				self.detectLabel.set_markup("<span foreground='#DD0000'>Non trouvé</span>")
				self.labelLastchange.set_text("Échec de connexion")
			else:
				# À PARTIR D'ICI, ON CONSIDÈRE QUE LE MCU EST CONNECTÉ À L'ORDINATEUR
				# PRÈS À COMMUNIQUER DES DONNÉES
				# La première étape à partir d'ici est l'énumération 

				# Lalks' note : (CHECK PAGE 192 DOC PIC18F2455)
				
				"""
				DONC À PARTIR D'ICI, IL FAUT PROCÉDER À "SET CONFIGURATION", ÉTAPE 8 ENUMERATION

				pyusb nous permet de ne pas se compliquer la vie à vérifier le device descriptor
				pour mettre en place une configuration spécifique : tout se fait automatiquement
				"""

				""" I COMMENTED TO NOT DAMAGE DEVICE WHEN CLICKED THE BUTTON
					(TO UNCOMMENT WHEN SURE OF THE FUNCTION !)

				### SET THE CONFIGURATION
				# Sets the first configuration
				device.set_configuration()

				# Get an endpoint instance | NEED TO CLARIFY WHAT IS DONE HERE
				cfg = device.get_active_configuration()
				intf = cfg[(0,0)]

				# NEED TO CLARIFY WHAT IS DONE HERE
				ep = usb.util.find_descriptor(
					intf,
					# Match the first OUT Endpoint 
					custom_match = \
					lambda e: \
						usb.util.endpoint_direction(e.bEndpointAddress) == \
						usb.util.ENDPOINT_OUT)

				assert ep is not None

				# Write data
				ep.write(0xF0)
				
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

if __name__ == "__main__":
	main = managegui()
	Gtk.main()
