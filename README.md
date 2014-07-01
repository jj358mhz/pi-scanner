ScannerPi
=========

ScannerPi is a collection of scripts and configuration files that you can use to assist in setting up a RaspBerry Pi for streaming scanner audio to websites such as Broadcastify.com

## RaspberryPi Pre-Configuration Steps

* These instructions assume you have installed Raspbian on your Pi

### Updates the Pi's Catalog, Kernal, & Firmware
Run these commands is sucessive order
```bash
$ sudo apt-get update
(wait)
```
```bash
$ sudo apt-get upgrade
(wait)
(reboot)
```
```bash
$ sudo rpi-update
(reboot)
```
### Add the SOX Package
This command installs the 'sox' package required for mp3 encoding
```bash
sudo apt-get install sox libsox-fmt-mp3
```

## Compile & Install Darkice
This installs the Darkice package and has you manually compile it to support mp3 encoding

### Add a deb-src repository to your sources list at /etc/apt/sources.list:
```bash
$ sudo sh -c "echo 'deb-src http://mirrordirector.raspbian.org/raspbian/ wheezy main contrib non-free rpi' >> /etc/apt/sources.list"

$$ sudo apt-get update
```
### Fulfills Build Dependencies
```bash
$ sudo apt-get --no-install-recommends install build-essential devscripts autotools-dev fakeroot dpkg-dev debhelper autotools-dev dh-make quilt ccache libsamplerate0-dev libpulse-dev libaudio-dev lame libjack-jackd2-dev libasound2-dev libtwolame-dev libfaad-dev libflac-dev libmp4v2-dev libshout3-dev libmp3lame-dev
```







A deeper dive detailing the complete installation and configuration can be found at glyman's site <https://sites.google.com/site/glyman3home/home>.

There is also instructions and a live working feed accessible here <http://www.jj358mhz.com>

