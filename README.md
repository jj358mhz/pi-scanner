pi-scanner
=========

pi-scanner is a collection of scripts and configuration files that you can use to assist in setting up a RaspBerry Pi for streaming scanner audio to websites such as Broadcastify.com

# Step 1: RaspberryPi Pre-Configuration Steps

* These instructions assume you have installed Raspbian Buster on your Pi

## Audio set-up

* With your USB sound stick installed, in a terminal on the RasPi run the command

```bash
arecord –l
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
arecord -D plughw:1,0 temp.wav
```
* In this case we use the plug-in called "plug" to handle format conversion. Otherwise you could use “arecord –D hw:1,0 somefile.wav but you would need to explicitly set the format to match your sound stick. Using “plughw:1,0” makes life easier.

If using a microphone, speak into it for about ten seconds. Then type “ctl-c” to stop recording. If you hear the audio when you enter the command,

```bash
aplay temp.wav
```
then the recording on the RasPi and USB device is working. If you don’t hear anything using “aplay temp.wav”, or if it is too soft or distorted, try using the command:

```bash
sudo alsamixer
```
(along with the volume control on the radio) to balance the recording level. After entering “alsamixer” press “F6” and select the sound card (maybe called generic USB device), then “F5” to display all controls for that device.

Using one scanner I had to turn the scanner up quite loud, then using alsamixer turn on Auto Gain (arrow over to auto gain and press “**m**” until “**00**” is displayed). Using a different scanner I had to keep it rather low and turn auto gain off (mute) while keeping the capture level at + 9 dB - it’s fair to say “your mileage may vary.”

If despite all this you cannot get decent quality audio then you should suspect a problem with the attached audio hardware, audio cable, etc.

Once you have a feed running with good audio level you can save the alsamixer settings between reboots by issuing command:

```bash
sudo alsactl store
```

## Update the Pi's Catalog, Kernel, & Firmware
Run these commands is successive order
```bash
sudo apt update
(wait)
```
```bash
sudo apt upgrade
(wait)
(reboot)
```
# Step 2: Install Darkice & its Dependencies
This installs the Darkice package and its dependencies for file trimming and processing
```bash
sudo apt install darkice -y
```

## Install the SoX (Sound Exchange) & id3v2 Tag Packages
This command installs the *sox* package required for mp3 encoding
```bash
sudo apt install sox libsox-fmt-mp3 id3v2 -y
```

# Step 3: Configure & Install Support Scripts
This step will focus on installing and configuring DarkIce & Radioplay

## Folder Creation for Radioplay
```bash
sudo mkdir /etc/radioplay
sudo mkdir /var/lib/radioplay
sudo mkdir scanneraudio
```

## Download all Configurations Files
```bash
curl "https://raw.githubusercontent.com/jj358mhz/pi-scanner/master/darkice.service" -o darkice.service && curl "https://raw.githubusercontent.com/jj358mhz/pi-scanner/master/darkice.cfg" -o darkice.cfg && curl "https://raw.githubusercontent.com/jj358mhz/pi-scanner/master/radioplay" -o radioplay && curl "https://raw.githubusercontent.com/jj358mhz/pi-scanner/master/radioplay.conf" -o radioplay.conf

OR clone the repo

git clone https://github.com/jj358mhz/pi-scanner.git
```
* **Update the *darkice.cfg* and *radioplay.conf* configuration files using vi or nano to conform it to your radioreference.com settings**
* **You may also need to modify the *radioplay* script at the *trim* area to customize the feed mnemonic**

## Edit Permission & Ownership
```bash
sudo chown root:root darkice darkice.cfg radioplay radioplay.conf
sudo chmod 755 radioplay darkice.service
sudo chmod 644 radioplay.conf darkice.cfg
```

## Copy Files to Destination Folders
```bash
sudo cp radioplay /usr/local/bin/radioplay
sudo cp radioplay.conf /etc/radioplay/radioplay.conf
sudo cp darkice.service /etc/systemd/system/darkice.service
sudo cp darkice.cfg /etc/darkice.cfg
```

# Step 4: Test and Final Cleanup
Test DarkIce without archiving
```bash
sudo /usr/bin/darkice
```
Listen to the feed and adjust the levels as needed. If all works as expected then “ctl-c” to stop DarkIce. If you see this error when running DarkIce, “…lame lib opening underlying sink error…” then DarkIce was unable to connect to the server. Check “/etc/darkice.cfg” for the proper entries and make sure the RasPi can access the internet.

## Finalize the Installation
Create the cron.d file
```bash
cd /etc/cron.d
sudo nano radioplay
```
...and add the following lines
```bash
00 * * * *   root [ -x /usr/local/bin/radioplay ] && /usr/local/bin/radioplay cron > /dev/null
```
Enable the DarkIce startup service to run at boot & start DarkIce
```bash
sudo systemctl enable darkice.service
sudo systemctl start darkice.service
```

## Reboot!

There is a live working feed accessible here <http://www.jj358mhz.com>

# Step 5: (OPTIONAL)

## RClone (third-party download)
<https://rclone.org/>

We will leverage it for syncronizing our local /scanneraudio/<files> to Dropbox. NOTE: You can also configure it to integrate into other cloud storage of your choosing.

### Rclone
Rclone is a command line program to manage files on cloud storage. It is a feature rich alternative to cloud vendors' web storage interfaces. Over 40 cloud storage products support rclone including S3 object stores, business & consumer file storage services

#### Install Rclone
To install rclone on Linux/macOS/BSD systems, run:
```bash
curl https://rclone.org/install.sh | sudo bash
```

#### Configure for Dropbox
See the configuration documentation for Dropbox here:
<https://rclone.org/dropbox/>

#### Finalize the Installation
Create the cron.d file
```bash
cd /etc/cron.d
sudo nano radioplay
```
...and add the following lines
```bash
05 * * * * pi /usr/bin/rclone sync -P /home/pi/scanneraudio/ <YourDropboxAppName>:
```
