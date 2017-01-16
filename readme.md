# Tool to display a tray app - which will monitor the number of running vagrant VM's

Developing with vagrant is awesome. There are many reasons to use it.

However, one issue (risk) when working on a number of projects throughout the day is having many vagrant VM's running.
Having a simple monitor of this - to show how many are running means that a developer can keep an eye on it, and know if it's a 
likely suspect if a machine is starting to get a bit slow.

It requires pyside, Python 2.7 and has been tested on Windows.

# Usage

## Windows 

Clone this, ensure you have pyside installed (`pip install pyside` works on most systems).
Then run `python vagrant_monitor.py`

## Linux Fedora/Redhat

To install Pyside: `sudo dnf install python-pyside`

Then git clone, and run `python vagrant_monitor.py`

## Mac/OSX

To be confirmed.

# TODO

* Testing on Mac
* Packaging and clean up (it's a bit messy right now)
  * Bundling into a windows exe as a release path.
  * Bundling into mac pkg.
  * Bundling into linux deb/rpm for desktop distributions.
* Offering a tooltip with a list of the named VM's.
* Offering context menu stuff to interact
  * pop up a terminal in the directory a VM is running in.
  * Stop (halt/suspend/destroy)
  * Resume
  * Suspend all
  * Halt all
* An about box.

# Why python 2.7

This is simply down to the PySide binaries being available for Windows here. I should probably ensure it would work if the dependancies are installed correctly.
