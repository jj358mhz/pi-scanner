ScannerPi
=========

ScannerPi is a collection of scripts and configuration files that you can use to assist in setting up a RaspBerry Pi for streaming scanner audio to websites such as Broadcastify.com

## Step 1: RaspberryPi Pre-Configuration Steps

* These instructions assume you have installed Raspbian on your Pi

### Audio set-up

* With your USB sound stick installed, in a terminal on the RasPi run the command 

```bash
$ arecord –l
```
and note the output. You should see something like this:

```bash
**** List of CAPTURE Hardware Devices ****
card 1: Device [Generic USB Audio Device], device 0: USB Audio [USB Audio]
Subdevices: 1/1
Subdevice #0: subdevice #0
```
* This indicates that the capture (recording) device is card one. The numbering starts at zero and the on-board audio on the RasPi is card 0 (but it does not have a capture device). In ALSA configuration it is referred to by device and sub-device thusly: “hw:1,0”.

Next connect speakers to the audio jack on the RasPi (not the USB output) and a microphone or other audio input to the USB sound stick. A scanner tuned to NOAA weather with continuous output works well. Adjust the volume to mid level if using a scanner, etc. Then enter:

```bash
$ arecord -D plughw:1,0 temp.wav 
```
* In this case we use the plug-in called "plug" to handle format conversion. Otherwise you could use “arecord –D hw:1,0 somefile.wav but you would need to explicitly set the format to match your sound stick. Using “plughw:1,0” makes life easier.

If using a microphone, speak into it for about ten seconds. Then type “ctl-c” to stop recording. If you hear the audio when you enter the command,

```bash
$ aplay temp.wav
```
then the recording on the RasPi and USB device is working. If you don’t hear anything using “aplay temp.wav”, or if it is too soft or distorted, try using the command:

```bash
$ sudo alsamixer
```
(along with the volume control on the radio) to balance the recording level. After entering “alsamixer” press “F6” and select the sound card (maybe called generic USB device), then “F5” to display all controls for that device. 

Using one scanner I had to turn the scanner up quite loud, then using alsamixer turn on Auto Gain (arrow over to auto gain and press “**m**” until “**00**” is displayed). Using a different scanner I had to keep it rather low and turn auto gain off (mute) while keeping the capture level at + 9 dB - it’s fair to say “your mileage may vary.”

If despite all this you cannot get decent quality audio then you should suspect a problem with the attached audio hardware, audio cable, etc.

Once you have a feed running with good audio level you can save the alsamixer settings between reboots by issuing command:

```bash
$ sudo alsactl store
```

### Updates the Pi's Catalog, Kernel, & Firmware
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
Use the following text. The build will fail if the text contains SPACES instead of TABS.

You may want to copy fom this link: https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/debian_rules
```bash
#!/usr/bin/make -f

%:
	dh $@

.PHONY: override_dh_auto_configure
override_dh_auto_configure:
	ln -s /usr/share/misc/config.guess .
	ln -s /usr/share/misc/config.sub .
	dh_auto_configure -- --prefix=/usr --sysconfdir=/usr/share/doc/darkice/examples --with-vorbis-prefix=/usr/lib/arm-linux-gnueabihf/ --with-jack-prefix=/usr/lib/arm-linux-gnueabihf/ --with-alsa-prefix=/usr/lib/arm-linux-gnueabihf/ --with-faac-prefix=/usr/lib/arm-linux-gnueabihf/ --with-aacplus-prefix=/usr/lib/arm-linux-gnueabihf/ --with-samplerate-prefix=/usr/lib/arm-linux-gnueabihf/ --with-lame-prefix=/usr/lib/arm-linux-gnueabihf/ CFLAGS='-march=armv6 -mfpu=vfp -mfloat-abi=hard'
```

### Version to Reflect mp3 Support
Add the following "New build with mp3 support" text as shown below
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
### Folder Creation for Radioplay
```bash
$ sudo mkdir /etc/radioplay
$ sudo mkdir /var/lib/radioplay
```
### Create Scanneraudio & Sandbox Folders
Create this at the pi root (/home/pi)
```bash
$ mkdir scanneraduio
$ mkdir sandbox && cd sandbox
```
### Darkice Script
```bash
$ curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/darkice" -o darkice
```
### Darkice Configuration File
```bash
$ curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/darkice.cfg" -o darkice.cfg
```
### Radioplay Script
```bash
$ curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/radioplay" -o radioplay
```
### Radioplay Configuration File
```bash
$ curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/radioplay.conf" -o radioplay.conf
```
### Download them all at Once
```bash
$ curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/darkice" -o darkice && curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/darkice.cfg" -o darkice.cfg && curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/radioplay" -o radioplay && curl "https://raw.githubusercontent.com/jj358mhz/ScannerPi/master/radioplay.conf" -o radioplay.conf
```

* **Update the *darkice.cfg* and *radioplay.conf* configuration files using nano to conform it to your radiorefence.com settings**
* **You may also need to modify the *radioplay* script at the *trim* area to customize the feed mnemonic**

### Edit Permission & Ownership
```bash
$ sudo chown root:root darkice darkice.cfg radioplay radioplay.conf
$ sudo chmod 744 radioplay darkice
$ sudo chmod 644 radioplay.conf darkice.cfg
```
### Move Files to Destination Folders
```bash
$ sudo mv radioplay /usr/local/bin/radioplay
$ sudo mv radioplay.conf /etc/radioplay/radioplay.conf
$ sudo mv darkice /etc/init.d/darkice
$ sudo mv darkice.cfg /etc/darkice.cfg
```

## Step 4: Test and Final Cleanup
Test DarkIce without archiving
```bash
$ sudo /usr/bin/darkice
```
Listen to the feed and adjust the levels as needed. If all works as expected then “ctl-c” to stop darkice.  If you see this error when running darkice, “…lame lib opening underlying sink error…” then darkice was unable to connect to the server. Check “/etc/darkice.cfg” for the proper entries and make sure the RasPi can access the internet.

### Finalize the Installation
Update the root's crontab
```bash
$ sudo crontab -e
```
...and add the following lines
```bash
00 * * * *   [ -x /usr/local/bin/radioplay ] && /usr/local/bin/radioplay cron > /dev/null
@reboot [ -x /usr/bin/darkice ] && /usr/bin/darkice > /dev/null
```
Start DarkIce
```bash
$ sudo /etc/init.d/darkice start
```
Update the DarkIce startup script to run at boot
```bash
$ sudo update-rc.d darkice defaults
```
### Reboot!

There is a live working feed accessible here <http://www.jj358mhz.com>
