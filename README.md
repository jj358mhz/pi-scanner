# 📡 pi-scanner

**pi-scanner** is a collection of scripts and configuration files for setting up a Raspberry Pi to stream scanner audio
to [Broadcastify](https://www.broadcastify.com) and other Icecast-compatible services.

---

## 🗺️ Table of Contents

1. [Pre-Configuration](#-step-1-raspberrypi-pre-configuration)
2. [Install DarkIce](#-step-2-install-darkice--dependencies)
3. [Configure Scripts](#-step-3-configure--install-support-scripts)
4. [Test & Finalize](#-step-4-test--finalize)
5. [Optional: RClone](#-step-5-optional-cloud-sync-with-rclone)

---

## 🔧 Step 1: RaspberryPi Pre-Configuration

> These instructions assume you have installed **Raspbian Buster** on your Pi.

### 🎙️ Audio Setup

With your USB sound stick installed, run:

```bash
arecord -l
```

You should see output similar to:

```
**** List of CAPTURE Hardware Devices ****
card 1: Device [Generic USB Audio Device], device 0: USB Audio [USB Audio]
Subdevices: 1/1
Subdevice #0: subdevice #0
```

This means the capture device is **card 1** — referred to in ALSA as `hw:1,0`.

Connect speakers to the Pi's audio jack and your scanner (or other audio source) to the USB sound stick. Test the
recording:

```bash
arecord -D plughw:1,0 temp.wav
```

Speak into the mic (or let the scanner run) for ~10 seconds, then `Ctrl-C`. Play it back:

```bash
aplay temp.wav
```

If the audio is too soft or distorted, adjust levels with:

```bash
sudo alsamixer
```

Press **F6** to select the USB sound card, then **F5** to show all controls. Toggle Auto Gain with **m** (`00` =
enabled). Audio tuning varies by scanner model — your mileage may vary.

Once levels are dialed in, persist them across reboots:

```bash
sudo alsactl store
```

### 🔄 Update the Pi

```bash
sudo apt update && sudo apt upgrade -y
# reboot when complete
```

---

## 📦 Step 2: Install DarkIce & Dependencies

```bash
sudo apt install darkice -y
```

### Install SoX & id3v2

```bash
sudo apt install sox libsox-fmt-mp3 id3v2 -y
```

---

## ⚙️ Step 3: Configure & Install Support Scripts

### Create Required Folders

```bash
sudo mkdir /etc/radioplay
sudo mkdir /var/lib/radioplay
mkdir ~/scanneraudio
```

### Download Config Files

Clone the repo (recommended):

```bash
git clone https://github.com/jj358mhz/pi-scanner.git
```

> ✏️ **Edit `darkice.cfg` and `radioplay.conf`** to match your RadioReference/Broadcastify settings before copying files
> into place.
>
> You may also need to update the `radioplay` script's `trim` section to match your feed mnemonic.

### Set Permissions & Ownership

```bash
sudo chown root:root darkice.cfg radioplay radioplay.conf darkice.service darkice-watchdog.sh darkice-watchdog.service
sudo chmod 755 radioplay darkice.service darkice-watchdog.sh darkice-watchdog.service
sudo chmod 644 radioplay.conf darkice.cfg
```

### Copy Files to Destination

| Source                     | Destination                                      |
|----------------------------|--------------------------------------------------|
| `radioplay`                | `/usr/local/bin/radioplay`                       |
| `radioplay.conf`           | `/etc/radioplay/radioplay.conf`                  |
| `darkice.service`          | `/etc/systemd/system/darkice.service`            |
| `darkice.cfg`              | `/etc/darkice.cfg`                               |
| `darkice-watchdog.sh`      | `/usr/local/bin/darkice-watchdog.sh`             |
| `darkice-watchdog.service` | `/etc/systemd/system/darkice-watchdog.service`   |

```bash
sudo cp radioplay /usr/local/bin/radioplay
sudo cp radioplay.conf /etc/radioplay/radioplay.conf
sudo cp darkice.service /etc/systemd/system/darkice.service
sudo cp darkice.cfg /etc/darkice.cfg
sudo cp darkice-watchdog.sh /usr/local/bin/darkice-watchdog.sh
sudo cp darkice-watchdog.service /etc/systemd/system/darkice-watchdog.service
```

---

## ✅ Step 4: Test & Finalize

### Test DarkIce

Run DarkIce manually (without archiving) and listen to the feed:

```bash
sudo /usr/bin/darkice
```

Adjust levels as needed, then `Ctrl-C` to stop.

> ⚠️ If you see `lame lib opening underlying sink error`, DarkIce could not reach the server. Double-check
`/etc/darkice.cfg` and verify internet connectivity.

### Set Up Hourly Archiving (cron)

Create `/etc/cron.d/radioplay` and add:

```
00 * * * *   root [ -x /usr/local/bin/radioplay ] && /usr/local/bin/radioplay cron > /dev/null
```

### Enable & Start DarkIce

```bash
sudo systemctl enable darkice.service
sudo systemctl start darkice.service
```

### Enable & Start the WAN IP Watchdog

The watchdog monitors the public WAN IP every 10 seconds and automatically restarts DarkIce when the IP changes, preventing silent stream failures after ISP IP reassignments.

```bash
sudo systemctl enable darkice-watchdog.service
sudo systemctl start darkice-watchdog.service
```

### 🔁 Reboot!

```bash
sudo reboot
```

A live working feed is accessible at <http://www.jj358mhz.com>

---

## ☁️ Step 5: (Optional) Cloud Sync with RClone

[RClone](https://rclone.org/) syncs your local `/scanneraudio/` recordings to Dropbox (or 40+ other cloud storage
providers).

### Install

```bash
curl https://rclone.org/install.sh | sudo bash
```

### Configure for Dropbox

Follow the [RClone Dropbox guide](https://rclone.org/dropbox/).

### Add to Cron

Append to `/etc/cron.d/radioplay`:

```
05 * * * *   pi /usr/bin/rclone sync -P /home/pi/scanneraudio/ <YourDropboxAppName>:
```

---

## 📄 License

[MIT](LICENSE)
