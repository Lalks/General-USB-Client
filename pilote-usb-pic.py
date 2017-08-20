#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""

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

"""


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import subprocess # for lsusb command output

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

		self.Licence = self.builder.get_object("Licence")

		self.boutonRecevoir = self.builder.get_object("boutonRecevoir")
		self.inputRecevoir = self.builder.get_object("inputRecevoir")
		self.boutonEnvoyer = self.builder.get_object("boutonEnvoyer")
		self.inputEnvoyer = self.builder.get_object("inputEnvoyer")
		self.inputPort = self.builder.get_object("inputPort")
		self.terminalOutput = self.builder.get_object("terminalOutput")
		self.terminalBuffer = self.builder.get_object("terminalBuffer")
		self.detectLabel = self.builder.get_object("detectLabel")

		self.inputVID = self.builder.get_object("inputVID")
		self.inputPID = self.builder.get_object("inputPID")

		self.labelLastchange = self.builder.get_object("labelLastchange")

		self.window.show_all()

	# Need the destroy function to quit when the window is destroy
	def on_window_destroy(self, object, data=None):
		Gtk.main_quit()

	# "Recevoir" button
	def on_boutonRecevoir_clicked(self, object, data=None):
		#usbPort = self.inputPort.get_text()
		""" ICI IL FAUT LIRE LES DONNEES DU BUS ET INSÉRER DANS LA VARIABLE UsbDataRead """
		UsbDataRead = "Default value"
		self.inputRecevoir.set_text(UsbDataRead)

	# "Envoyer" button
	def on_boutonEnvoyer_clicked(self, object, data=None):
		usbPort = self.inputPort.get_text()
		""" ICI IL FAUT ÉCRIRE LES DONNEES VERS LE BUS """
		UsbDataWrite = self.inputEnvoyer.get_text()
		print(UsbDataWrite)

	# Refresh button
	def on_boutonRefresh_clicked(self, object, data=None):
		command = "lsusb"
		process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()
		if error == None:
			self.terminalBuffer.set_text(output.decode("utf-8"))
			self.labelLastchange.set_text("Liste des appareils rafraichie")
		else:
			self.terminalBuffer.set_text(error.decode("utf-8"))
			self.labelLastchange.set_text("Échec de rafraichissement de la liste des appareils")


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
				""" ICI IL FAUT LANCER L'INITIALISATION ENTRE HOST ET DEVICE """

				""" FOLLOWED TUTORIAL OF WALAC ! """
				"""
				device.set_configuration()
				cfg = device.get_active_configuration()
				intf = cfg[(0,0)]

				ep = usb.util.find_descriptor(intf, custom_match = lambda e: \
						usb.util.endpoint_direction(e.bEndpointAddress) == \
						usb.util.ENDPOINT_OUT)

				assert ep is not None

				ep.write(0xF0)
				"""
				self.detectLabel.set_markup("<span foreground='#00AA00'>Connecté !</span>")
				self.labelLastchange.set_text("Connexion établie")
		except ValueError:
			self.detectLabel.set_text("VID/PID incorrect")
			self.labelLastchange.set_text("Échec de connexion")
		

if __name__ == "__main__":
	main = managegui()
	Gtk.main()
