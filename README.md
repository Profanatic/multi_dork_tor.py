
# MULTI_DORK_TOR 

An OSINT tool enabling anonymous dork searches over Tor with Startpage or Yandex support.

> 🛡️ Designed for cybersecurity researchers and osint analysts focused on privacy-preserving reconnaissance.

---

## ⚙️ Requirements

- Python 3.8 or newer
- Tor running on port 9050 (e.g., `sudo systemctl start tor`)
- Linux/WSL/macOS (recommended)

---

## 🚀 Installation

### 1. Clone the repository

git clone https://github.com/Profanatic/multi_dork_tor.py

cd multi_dork_tor.py

python3 -m venv venv

source venv/bin/activate

pip3 install --break-system-packages -r requirements.txt

Usage

1. Create a dork file:

echo 'site:example.com intitle:"admin login"' > dorks.txt

python3 multi_dork_tor.py -d dorks.txt --engine yandex -o results.txt

Or

python3 multi_dork_tor.py -d dorks.txt --engine startpage -o results.txt

🛡️ Notes

This script routes traffic through the Tor network.

Startpage and Yandex are less aggressive with CAPTCHA and block detection.

Respect each search engine's terms of service.

