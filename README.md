# General USB 2.0 client
GUI application to communicate through any USB device. Made with Python 3.6 &amp; GTK 3.20

## WARNING !
**This program is still in development, the main goal of it is not working at all ! Do not try to lauch it without being sure of what you are doing, it could damage an USB device connected on your system**

## Require
To use this program correctly, **you must have python 3 installed on your system, as well as GTK 3.20 and PyUSB**. A GNU/Linux operating system is highly recommended ! Some functionnality wont work at this time of development. 

### Install PyUSB
To install PyUSB, refer to this link : 
https://github.com/walac/pyusb#installing-pyusb-on-gnulinux-systems

### Install GTK on Windows
To install GTK on Windows, refer to this link : 
https://www.gtk.org/download/windows.php

If something went wrong with the software, please make sure to report it. If you are a contributor and if you found a solution to an issue, please update the readme. Thanks.

Tested on :
	- Arch Linux with KDE
	- Arch Linux with XFCE

## Screenshot
![alt text](https://github.com/Lalks/General-USB-Client/blob/master/SCREENSHOTS/screenshot-01.png)

## Changelog
**0.03**
- replaced the terminal output (text) by a dynamic tree view
- the "extended" checkbox is removed thanks to the dynamic tree view which let the user choose the information
- temporary removed the menubar

**0.02**
- finished non-tested backend of the receive function
- finished non-tested backend of the send function
- finished non-tested backend of the connect function
- fixed bug on Return key shortcut on PID and VID entries
- updated title on Glade file
- changed font face of the textview 'terminalOutput'
- changed icon
- changed format Credits and Licence windows
- fix display of Credits window

**0.01**
- updated widgets' positions (progress bars, buttons, entries)
- replaced the lsusb command output by a function made in the program with pyusb (with Vendor and Product names resolver from IDs) 
- added 'extended' mode for the output about the devices that are connected to the computer
- changed font face of the textview 'terminalOutput'
- added Return key shortcut on PID and VID entries
- fixed child list to be able to Tab on VID -> PID -> Connect Button


## To do
	 [ ] Finish the USB functionnality (backend)
	 [ ] Clean up the code
	 [ ] Add better comments at the beginning of the source file
	 [ ] Translations (at least EN, FR)
	 [ ] Replace the TextView widget by a TreeView