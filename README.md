ScannerPi
=========

ScannerPi is a collection of scripts and configuration files that you can use to assist in setting up a RaspBerry Pi for streaming scanner audio to websites such as Broadcastify.com

## Step 1: RaspberryPi Pre-Configuration Steps

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

## Step 2: Compile & Install Darkice
This installs the Darkice package and has you manually compile it to support mp3 encoding

### Add a deb-src repository to your sources list at /etc/apt/sources.list:
```bash
$ sudo sh -c "echo 'deb-src http://mirrordirector.raspbian.org/raspbian/ wheezy main contrib non-free rpi' >> /etc/apt/sources.list"
$ sudo apt-get update
```
### Fulfills Build Dependencies:
```bash
$ sudo apt-get --no-install-recommends install build-essential devscripts autotools-dev fakeroot dpkg-dev debhelper autotools-dev dh-make quilt ccache libsamplerate0-dev libpulse-dev libaudio-dev lame libjack-jackd2-dev libasound2-dev libtwolame-dev libfaad-dev libflac-dev libmp4v2-dev libshout3-dev libmp3lame-dev
```
### Create Working Directory:
```bash
$ mkdir src && cd src/
```
### Get the DarkIce Source Package
```bash
$ apt-get source darkice
```
### Change the Compile Configuration to Match the Raspbian Environment
```bash
$ cd darkice-1.0/
$ nano debian/rules
```
```bash
#!/usr/bin/make -f
```
Use the following text. The build will fail if the text contains SPACES instead of TABS
```bash
%:
	dh $@

.PHONY: override_dh_auto_configure
override_dh_auto_configure:
	ln -s /usr/share/misc/config.guess .
	ln -s /usr/share/misc/config.sub .
	dh_auto_configure -- --prefix=/usr --sysconfdir=/usr/share/doc/darkice/examples --with-vorbis-prefix=/usr/lib/arm-linux-gnueabihf/ --with-jack-prefix=/usr/lib/arm-linux-gnueabihf/ --with-alsa-prefix=/usr/lib/arm-linux-gnueabihf/ --with-faac-prefix=/usr/lib/arm-linux-gnueabihf/ --with-aacplus-prefix=/usr/lib/arm-linux-gnueabihf/ --with-samplerate-prefix=/usr/lib/arm-linux-gnueabihf/ --with-lame-prefix=/usr/lib/arm-linux-gnueabihf/ CFLAGS='-march=armv6 -mfpu=vfp -mfloat-abi=hard'
```

### Version to Reflect mp3 Support
```bash
$ debchange -v 1.0-999~mp3+1

darkice (1.0-999~mp3+1) UNRELEASED; urgency=low

  * New build with mp3 support

 --  <pi@raspberrypi>  Sat, 11 Aug 2012 13:35:06 +0000
 ```
 
 ### Build & Install the Darkice Package
 ```bash
$ dpkg-buildpackage -rfakeroot -uc -b
```
```bash
$ sudo dpkg -i ../darkice_1.0-999~mp3+1_armhf.deb

Preparing to replace darkice 1.0-999 (using .../darkice_1.0-999~mp3+1_armhf.deb) ...
Unpacking replacement darkice ...
Setting up darkice (1.0-999~mp3+1) ...
```
You have installed DarkIce with mp3 support

## Step 3: Configure & Install Support Scripts
This step will focus on installing and configuring DarkIce & Radioplay

### Install id3 Tag Package
```bash
$ sudo apt-get install id3v2
```
### Folder Creation
```bash
$ sudo mkdir /etc/radioplay
$ sudo mkdir /var/lib/radioplay
```
### Create Scanneraudio & Sandbox Folders
Create this at the pi root (/home/pi)
```bash
$ mkdir scanneraduio
$ mkdir sandbox
```
### Darkice Script
```bash
cd ~/sandbox
curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/darkice" -o darkice
```
### Darkice Configuration File
```bash
curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/darkice.cfg" -o darkice.cfg
```
### Radioplay Script
```bash
curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/radioplay" -o radioplay
```
### Radioplay Configuration File
```bash
curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/radioplay.conf" -o radioplay.conf
```
* **Update the *darkice.cfg* and *radioplay.conf* configuration files using nano to conform it to your radiorefence.com settings**
* **You may also need to modify the *radioplay* script at the *trim* area to customize the feed mnemonic**

A deeper dive detailing the complete installation and configuration can be found at glyman's site <https://sites.google.com/site/glyman3home/home>.

There is also instructions and a live working feed accessible here <http://www.jj358mhz.com>

