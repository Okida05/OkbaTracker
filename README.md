# OkbaTracker

![Version](https://img.shields.io/badge/version-1.0-brightgreen)
![Python](https://img.shields.io/badge/python-3.x-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

**OkbaTracker** is a multi-purpose OSINT and information gathering tool. It provides IP geolocation, phone number lookup, username search across social media, URL expansion, VPN/proxy detection, and reverse DNS lookups — all from an interactive terminal menu.

---

## Features

### 🌐 IP Tracker
Geolocate any IP address using the ipwho.is API. Displays country, region, city, coordinates, ISP, ASN, timezone, and a Google Maps link.

### ℹ️ My IP
Quickly fetch your own public IP address.

### 📱 Phone Lookup
Parse and validate phone numbers using the `phonenumbers` library. Shows international format, carrier, location, timezone, line type (mobile/fixed), and validity.

### 👤 Username Scan
Check the availability of a username across 19 social media platforms:
Facebook, Twitter/X, Instagram, LinkedIn, GitHub, TikTok, YouTube, Twitch, Snapchat, Telegram, Pinterest, Tumblr, Behance, Medium, Quora, Flickr, Dribbble, SoundCloud, Product Hunt.

### 🔗 URL Expander
Unshorten URLs by following HTTP redirect chains, meta-refresh redirects, and JavaScript-based redirects. Supports batch input (space, comma, or newline separated).

### 🛡️ VPN/Proxy Check
Detect if an IP is behind a VPN, proxy, Tor exit node, or hosting provider using ip-api.com and the official Tor exit node list.

### 📡 Reverse DNS
Perform reverse DNS (PTR) lookups on IP addresses and display A records and hostname aliases.

---

## Installation

### Linux (Debian-based)
```bash
sudo apt-get install git python3 python3-pip
git clone https://github.com/Okida05/OkbaTracker.git
cd OkbaTracker
pip3 install -r requirements.txt
python3 OkbaTrack.py
```

### Termux
```bash
pkg install git python3
git clone https://github.com/Okida05/OkbaTracker.git
cd OkbaTracker
pip3 install -r requirements.txt
python3 OkbaTrack.py
```

### Windows
```cmd
git clone https://github.com/Okida05/OkbaTracker.git
cd OkbaTracker
pip install -r requirements.txt
python OkbaTrack.py
```
Or double-click `run.bat`.

---

## Requirements

- Python 3.x
- `requests` — HTTP requests
- `phonenumbers` — phone number parsing/validation

These are installed automatically on first run if missing, or manually via:
```bash
pip3 install -r requirements.txt
```

---

## Usage

Run the script:
```bash
python3 OkbaTrack.py
```

You'll be greeted with an ASCII banner and a numbered menu. Enter the number of the feature you want to use and follow the prompts.

### Example
```
   ⚡ Select option → 1
   🎯 Enter IP target → 8.8.8.8
```

---

## Disclaimer

This tool is intended for **educational purposes and authorized security research only**. Do not use it against targets without their explicit consent. The author is not responsible for any misuse.

---

## Author

- **Okba** — [@Okida05](https://github.com/Okida05)

---

## License

MIT
