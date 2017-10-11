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
0.03 - replaced the terminal output (text) by a dynamic tree view
	 - the "extended" checkbox is removed thanks to the dynamic tree view which let the user choose the information
	 - temporary removed the menubar

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
from gi.repository import Gtk, Pango, GObject

import sys
import os

sys.path.append("./pyusb/")

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

		self.treeOutput = self.builder.get_object("treeOutput")
		self.treestore1 = self.builder.get_object("treestore1")
		self.VID_tree = self.builder.get_object("VID_tree")
		self.PID_tree = self.builder.get_object("PID_tree")
		self.INFO_tree = self.builder.get_object("INFO_tree")

		self.treeviewcolumn1 = self.builder.get_object("treeviewcolumn1")


		self.detectLabel = self.builder.get_object("detectLabel")
		

		self.inputVID = self.builder.get_object("inputVID")
		self.inputPID = self.builder.get_object("inputPID")


		self.labelLastchange = self.builder.get_object("labelLastchange")




		self.detectGrid.set_focus_chain([self.inputVID, self.inputPID, self.boutonConnect])

		global VID
		VID = "0"
		global PID
		PID = "0"


		### BLOCK TO AUTO GENERATE COLUMNS
		tree_columns = ["Name", "Value", "Detail"]

		for i, tree_column in enumerate(tree_columns):
			cell = Gtk.CellRendererText()
			col = Gtk.TreeViewColumn(tree_column, cell, text=i)
			col.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
			col.set_resizable(True)
			self.treeOutput.append_column(col)



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

	# "Send data" button
	def on_boutonEnvoyer_clicked(self, object, data=None):
		if VID != "0" and PID != "0":
			UsbDataWrite = self.inputEnvoyer.get_text()

			if UsbDataWrite:
				# Search for the device
				device = usb.core.find(idVendor=VID, idProduct=PID)

				if device is None:
					errorstring = "No device with these ID {}:{}".format(VID, PID)
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
	def on_boutonRefresh_clicked(self, object, data=None):
		devices = usb.core.find(True)
		strings = ""
		output1 = ""
		
		# We need to clear the store first
		self.treestore1.clear()

		for device in devices:

			# Get hexadecimal values (with leading zeros) as strings
			strvendid = str("%0.4X" % device.idVendor)
			strprodid = str("%0.4X" % device.idProduct)

			### GET THE VENDOR'S AND PRODUCT'S NAME FROM THE IDS
			vendor = "Unknown vendor" # Default informations
			product = "Unknown product"
			vf = 0 # vendor found flag

			# Thanks to a file containing USB IDs that we parse here, we retrieve the different informations
			"""
			This search process could be better by using the number of tabulations before the IDs. In this algorithm for now, each row containing information are compared
			with ours. The problem is that if we are searching for a VID, even if the line contains a PID it will be compared with. Maybe this could be optimized by checking
			the number of tabulations before the ID (to determine if it is a VID, a PID or sub ID)... Just an idea
			"""
			with open("usb.ids") as usbids_file: # Open the file first
				for line in usbids_file: # Then we read it line by line
					if not vf: # We first search for the vendor ID, see the file to understand why (PID depending from VID : optimizing the search process)
						if not line[0] == '\t' and not line[0] == '#' and not line[0] == '\n': # Skip all blank lines and comments
							if int(strvendid, 16) == int(line[:4], 16):
								vendor = line[6:-1]
								vf = 1
					else:
						if line[0] == '\t' and not line[0] == '#' and not line[0] == '\n':
							if int(strprodid, 16) == int(line[1:5], 16):
								product = line[7:-1]
			usbids_file.close()


			venduct = vendor + " " + product # Make the fusion between the vendor name and the product info



			### DESCRIPTOR
			# Inspired from the source of pyusb core

			# CONFIGURATION
			active_configuration = device.get_active_configuration()
			first_interface = active_configuration.interfaces()[0] # Get the first interface /!\ Could make confusion if it is not the wished one
			endpoint = first_interface.endpoints()[0]

			if active_configuration.bmAttributes & (1<<6):
				powered = "Self powered"
			else:
				powered = "Bus powered"

			if active_configuration.bmAttributes & (1<<5):
				remote_wakeup = ", Remote Wakeup"
			else:
				remote_wakeup = ""

			powering = powered + remote_wakeup
			max_current = usb.core._lu.MAX_POWER_UNITS_USB2p0 * active_configuration.bMaxPower


				
			if device.bcdUSB & 0xf:
				low_bcd_usb = str(device.bcdUSB & 0xf)
			else:
				low_bcd_usb = ""
			bcdUSBtreated = [(device.bcdUSB & 0xff00)>>8, (device.bcdUSB & 0xf0) >> 4, low_bcd_usb]
			

			if device.bcdDevice & 0xf:
				low_bcd_device = str(device.bcdDevice & 0xf)
			else:
				low_bcd_device = ""
			bcdDevicetreated = [(device.bcdDevice & 0xff00)>>8, (device.bcdDevice & 0xf0) >> 4, low_bcd_device]

			if usb.core.util.endpoint_direction(endpoint.bEndpointAddress) == usb.core.util.ENDPOINT_IN:
				direction = "IN"
			else:
				direction = "OUT"


			pyusb_commands_device= [["Vendor ID", device.idVendor, vendor],
									["Product ID", device.idProduct, product],
									["Descriptor Type", device.bDescriptorType, str(usb.core._try_lookup(usb.core._lu.descriptors, device.bDescriptorType))],
									["Device Class", device.bDeviceClass, str(usb.core._try_lookup(usb.core._lu.device_classes, device.bDeviceClass)) ],
									["Device Version", device.bcdDevice, "Device %s.%s%s" % (bcdDevicetreated[0], bcdDevicetreated[1], low_bcd_usb)],
									["USB Version", device.bcdUSB, "USB %s.%s%s" % (bcdUSBtreated[0], bcdUSBtreated[1], low_bcd_usb)],
									["Device Protocol", device.bDeviceProtocol, None],
									["Device Sub Class", device.bDeviceSubClass, None] ]

			""" For active config only ! I (Lalks) don't have any device that has more than one configuration
				so I can't test a tree where there would have multiple configurations listed. """
			pyusb_commands_config= [["Powering", active_configuration.bmAttributes, powering],
									["Max current", active_configuration.bMaxPower, "%s mA" % max_current]]

			pyusb_commands_intrfc= [["Interface Class", first_interface.bInterfaceClass, str(usb.core._try_lookup(usb.core._lu.interface_classes, first_interface.bInterfaceClass))]]
			
			pyusb_commands_endpnt= [["Address", endpoint.bEndpointAddress, direction],
									["Length", endpoint.bLength, "%s bytes" % str(endpoint.bLength)],
									["Type", endpoint.bmAttributes, str(usb.core._lu.ep_attributes[(endpoint.bmAttributes & 0x3)]) ],
									["Max packet size", endpoint.wMaxPacketSize, "%s bytes" % str(endpoint.wMaxPacketSize)],
									["Interval", endpoint.bInterval, str(endpoint.bInterval)] ]

			### CONSTRUCT THE TREE
			# Adding parent
			iter0 = self.treestore1.append(None, [strvendid, strprodid, venduct])

			# Adding childs
			for result in pyusb_commands_device:
				self.treestore1.append( iter0, [ result[0], hex(result[1]), result[2]] )

			iter1 = self.treestore1.append(iter0, ["Active configuration", None, None])
			for result in pyusb_commands_config:
				self.treestore1.append( iter1, [ result[0], hex(result[1]), result[2]] )

			iter2 = self.treestore1.append(iter1, ["Interface", None, None])
			for result in pyusb_commands_intrfc:
				self.treestore1.append( iter2, [ result[0], hex(result[1]), result[2]] )

			iter3 = self.treestore1.append(iter2, ["Endpoint", None, None])
			for result in pyusb_commands_endpnt:
				self.treestore1.append( iter3, [ result[0], hex(result[1]), result[2]] )
				

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
				>>> config = device.get_active_configuration() # Config already set by the OS's drivers
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

				# SET THE CONFIGURATION (NOTE: Need to be root)
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
	
	def on_treeOutput_row_activated(self, object, selection, data):
		# 	   data : TreeViewColumn
		# selection : TreePath

		# k_list : gtkliststore
		k_list = object.get_model()

		# m_ids : list where the row's data are going to be stored
		m_ids = list()

		# m_item = the row kind of place, index
		m_item = k_list.get_iter(selection)

		m_ids.append(k_list.get_value(m_item, 0)) # VID
		m_ids.append(k_list.get_value(m_item, 1)) # PID
		m_ids.append(k_list.get_value(m_item, 2)) # Info

		# Now m_ids is at this format : ['VID', 'PID', 'Information about the device']

		self.inputVID.set_text(m_ids[0])
		self.inputPID.set_text(m_ids[1])


		device = usb.core.find(idVendor=int(m_ids[0], 16), idProduct=int(m_ids[1], 16))

		# Get hexadecimal values (with leading zeros) as strings
		strvendid = str("%0.4X" % device.idVendor)
		strprodid = str("%0.4X" % device.idProduct)


		### GET THE VENDOR'S AND PRODUCT'S NAME FROM THE IDS
		vendor = "Unknown vendor"
		product = "Unknown product"
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
